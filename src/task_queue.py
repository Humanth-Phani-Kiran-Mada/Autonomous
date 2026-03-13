"""
Priority-Based Task Queue: Job scheduling and execution system

Provides:
- Priority-based task queuing
- Async and sync execution
- Task lifecycle management
- Execution history and statistics
- Task batching and scheduling
"""
from typing import Any, Callable, Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
from collections import deque
import asyncio
import threading
import uuid
import time

import config
from logger import logger
from exceptions import AutonomousAIException


class TaskPriority(int, Enum):
    """Task priority levels (lower number = higher priority)"""
    CRITICAL = 0
    HIGH = 1
    NORMAL = 2
    LOW = 3
    BACKGROUND = 4


class TaskState(str, Enum):
    """Task execution states"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    RETRYING = "retrying"


@dataclass
class Task:
    """Represents a task in the queue"""
    task_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    fn: Optional[Callable] = None
    args: Tuple = field(default_factory=tuple)
    kwargs: Dict = field(default_factory=dict)
    priority: TaskPriority = TaskPriority.NORMAL
    state: TaskState = TaskState.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Any = None
    error: Optional[str] = None
    retry_count: int = 0
    max_retries: int = 3
    timeout_seconds: Optional[int] = None
    depends_on: Optional[List[str]] = None  # Task IDs to wait for
    tags: Dict[str, str] = field(default_factory=dict)
    
    def __lt__(self, other: 'Task') -> bool:
        """For priority queue ordering (lower priority value first)"""
        if self.priority.value != other.priority.value:
            return self.priority.value < other.priority.value
        return self.created_at < other.created_at
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "task_id": self.task_id,
            "name": self.name,
            "priority": self.priority.name,
            "state": self.state.value,
            "created_at": self.created_at.isoformat(),
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "error": self.error,
            "retry_count": self.retry_count,
            "duration_seconds": self._calculate_duration()
        }
    
    def _calculate_duration(self) -> Optional[float]:
        """Calculate task duration"""
        if not self.started_at:
            return None
        
        end = self.completed_at or datetime.now()
        return (end - self.started_at).total_seconds()


class TaskQueue:
    """
    Priority-based task queue with async support.
    
    Features:
    - Priority-based scheduling
    - Async and sync execution
    - Task dependencies
    - Retry logic
    - Execution history
    """
    
    def __init__(self, max_workers: int = 4):
        """
        Initialize task queue
        
        Args:
            max_workers: Maximum concurrent task workers
        """
        self.max_workers = max_workers
        self.queue: deque = deque()
        self.completed_tasks: Dict[str, Task] = {}
        self.pending_tasks: Dict[str, Task] = {}
        self.running_tasks: Dict[str, Task] = {}
        self.task_lock = threading.Lock()
        self.workers_active = 0
        self.stats = {
            "total_tasks": 0,
            "completed": 0,
            "failed": 0,
            "retried": 0
        }
        
        logger.info(f"✓ Task Queue initialized (workers: {max_workers})")
    
    def enqueue(
        self,
        fn: Callable,
        name: str = "",
        priority: TaskPriority = TaskPriority.NORMAL,
        *args,
        timeout_seconds: Optional[int] = None,
        max_retries: int = 3,
        depends_on: Optional[List[str]] = None,
        tags: Optional[Dict[str, str]] = None,
        **kwargs
    ) -> str:
        """
        Enqueue a task
        
        Args:
            fn: Function to execute
            name: Task name
            priority: Task priority
            *args: Function arguments
            timeout_seconds: Execution timeout
            max_retries: Maximum retry attempts
            depends_on: Task IDs this task depends on
            tags: Task tags for filtering
            **kwargs: Function keyword arguments
        
        Returns:
            Task ID
        """
        task = Task(
            name=name or fn.__name__,
            fn=fn,
            args=args,
            kwargs=kwargs,
            priority=priority,
            timeout_seconds=timeout_seconds,
            max_retries=max_retries,
            depends_on=depends_on or [],
            tags=tags or {}
        )
        
        with self.task_lock:
            self.queue.append(task)
            self.pending_tasks[task.task_id] = task
            self.stats["total_tasks"] += 1
        
        logger.debug(f"Enqueued task: {task.name} (priority: {priority.name})")
        return task.task_id
    
    def get_task_status(self, task_id: str) -> Optional[Task]:
        """Get task status"""
        with self.task_lock:
            if task_id in self.completed_tasks:
                return self.completed_tasks[task_id]
            if task_id in self.pending_tasks:
                return self.pending_tasks[task_id]
            if task_id in self.running_tasks:
                return self.running_tasks[task_id]
        
        return None
    
    def get_queue_stats(self) -> Dict[str, Any]:
        """Get queue statistics"""
        with self.task_lock:
            return {
                "pending": len(self.pending_tasks),
                "running": len(self.running_tasks),
                "completed": len(self.completed_tasks),
                "total": self.stats["total_tasks"],
                "stats": self.stats.copy(),
                "workers_active": self.workers_active,
                "max_workers": self.max_workers
            }
    
    def process_queue(self, async_mode: bool = False) -> None:
        """
        Process queue tasks
        
        Args:
            async_mode: Use async execution
        """
        if async_mode:
            asyncio.run(self._process_queue_async())
        else:
            self._process_queue_sync()
    
    def _process_queue_sync(self) -> None:
        """Synchronous queue processing"""
        while True:
            if self.workers_active >= self.max_workers:
                time.sleep(0.1)
                continue
            
            task = self._get_next_task()
            if not task:
                break
            
            self.workers_active += 1
            try:
                self._execute_task(task)
            finally:
                self.workers_active -= 1
    
    async def _process_queue_async(self) -> None:
        """Asynchronous queue processing"""
        while True:
            if self.workers_active >= self.max_workers:
                await asyncio.sleep(0.1)
                continue
            
            task = self._get_next_task()
            if not task:
                break
            
            self.workers_active += 1
            asyncio.create_task(self._execute_task_async(task))
    
    def _get_next_task(self) -> Optional[Task]:
        """Get next highest priority task ready to execute"""
        with self.task_lock:
            # Sort queue by priority
            sorted_tasks = sorted(list(self.queue))
            
            for task in sorted_tasks:
                # Check dependencies
                if task.depends_on:
                    all_deps_met = all(
                        dep_id in self.completed_tasks
                        for dep_id in task.depends_on
                    )
                    if not all_deps_met:
                        continue
                
                # Task is ready
                self.queue.remove(task)
                task.state = TaskState.RUNNING
                task.started_at = datetime.now()
                self.running_tasks[task.task_id] = task
                del self.pending_tasks[task.task_id]
                
                return task
        
        return None
    
    def _execute_task(self, task: Task) -> None:
        """Execute a task synchronously"""
        try:
            if task.timeout_seconds:
                # TODO: Implement timeout mechanism
                result = task.fn(*task.args, **task.kwargs)
            else:
                result = task.fn(*task.args, **task.kwargs)
            
            self._complete_task(task, result=result)
        
        except Exception as e:
            if task.retry_count < task.max_retries:
                logger.warning(
                    f"Task {task.name} failed (attempt {task.retry_count + 1}/"
                    f"{task.max_retries}): {e}"
                )
                task.retry_count += 1
                task.state = TaskState.RETRYING
                self.stats["retried"] += 1
                
                with self.task_lock:
                    self.queue.append(task)
                    self.pending_tasks[task.task_id] = task
                    del self.running_tasks[task.task_id]
            else:
                self._fail_task(task, str(e))
    
    async def _execute_task_async(self, task: Task) -> None:
        """Execute a task asynchronously"""
        try:
            if task.timeout_seconds:
                try:
                    result = await asyncio.wait_for(
                        task.fn(*task.args, **task.kwargs),
                        timeout=task.timeout_seconds
                    )
                except asyncio.TimeoutError:
                    raise AutonomousAIException(
                        f"Task {task.name} timed out",
                        error_code="TASK_TIMEOUT"
                    )
            else:
                result = await task.fn(*task.args, **task.kwargs)
            
            self._complete_task(task, result=result)
        
        except Exception as e:
            if task.retry_count < task.max_retries:
                logger.warning(f"Async task {task.name} failed: {e}")
                task.retry_count += 1
                task.state = TaskState.RETRYING
                
                with self.task_lock:
                    self.queue.append(task)
                    self.pending_tasks[task.task_id] = task
                    del self.running_tasks[task.task_id]
            else:
                self._fail_task(task, str(e))
    
    def _complete_task(self, task: Task, result: Any = None) -> None:
        """Mark task as completed"""
        task.state = TaskState.COMPLETED
        task.completed_at = datetime.now()
        task.result = result
        
        with self.task_lock:
            del self.running_tasks[task.task_id]
            self.completed_tasks[task.task_id] = task
            self.stats["completed"] += 1
        
        logger.info(f"✓ Task completed: {task.name}")
    
    def _fail_task(self, task: Task, error: str) -> None:
        """Mark task as failed"""
        task.state = TaskState.FAILED
        task.completed_at = datetime.now()
        task.error = error
        
        with self.task_lock:
            del self.running_tasks[task.task_id]
            self.completed_tasks[task.task_id] = task
            self.stats["failed"] += 1
        
        logger.error(f"Task failed: {task.name} - {error}")
    
    def clear_completed_tasks(self, keep_hours: int = 24) -> int:
        """Remove old completed tasks"""
        cutoff = datetime.now() - timedelta(hours=keep_hours)
        initial_count = len(self.completed_tasks)
        
        tasks_to_remove = [
            task_id for task_id, task in self.completed_tasks.items()
            if task.completed_at and task.completed_at < cutoff
        ]
        
        for task_id in tasks_to_remove:
            del self.completed_tasks[task_id]
        
        removed_count = initial_count - len(self.completed_tasks)
        if removed_count > 0:
            logger.debug(f"Cleaned up {removed_count} completed tasks")
        
        return removed_count


# Global task queue instance
_task_queue: Optional[TaskQueue] = None


def get_task_queue(max_workers: int = 4) -> TaskQueue:
    """Get or create global task queue"""
    global _task_queue
    if _task_queue is None:
        _task_queue = TaskQueue(max_workers)
    return _task_queue
