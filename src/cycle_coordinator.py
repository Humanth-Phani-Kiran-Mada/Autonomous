"""
Cycle Coordinator - Orchestration of the 8 Autonomous Cycles

Manages the execution, timing, dependency resolution, and coordination
of the 8 main cycles with proper error handling and cross-cycle communication.
"""

from typing import Dict, List, Callable, Any, Optional
from datetime import datetime
from enum import Enum
import asyncio
import time
from .logger import logger
from .integration_layer import integration_layer, IntegrationLayer
from .monitoring_engine import monitoring_engine


class CycleStatus(Enum):
    """Status of a cycle execution"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class CycleExecution:
    """Record of a single cycle execution"""
    
    def __init__(self, cycle_name: str, cycle_index: int, iteration: int):
        self.cycle_name = cycle_name
        self.cycle_index = cycle_index
        self.iteration = iteration
        self.status = CycleStatus.PENDING
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
        self.result: Dict[str, Any] = {}
        self.error: Optional[str] = None
        self.dependencies_met = False
        self.retry_count = 0
        self.max_retries = 3
    
    def start(self):
        """Mark cycle as started"""
        self.status = CycleStatus.RUNNING
        self.start_time = datetime.now()
        logger.debug(f"▶️ Cycle '{self.cycle_name}' starting...")
    
    def complete(self, result: Dict[str, Any]):
        """Mark cycle as completed"""
        self.end_time = datetime.now()
        self.result = result
        self.status = CycleStatus.COMPLETED
    
    def fail(self, error: str):
        """Mark cycle as failed"""
        self.end_time = datetime.now()
        self.error = error
        self.status = CycleStatus.FAILED
    
    def get_duration(self) -> float:
        """Get execution duration in seconds"""
        if not self.start_time:
            return 0.0
        end = self.end_time or datetime.now()
        return (end - self.start_time).total_seconds()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "cycle": self.cycle_name,
            "iteration": self.iteration,
            "status": self.status.value,
            "duration": self.get_duration(),
            "result": self.result,
            "error": self.error,
            "retries": self.retry_count
        }


class CycleCoordinator:
    """Coordinates execution of the 8 autonomous cycles"""
    
    # Define the 8 cycles in order
    CYCLE_ORDER = [
        "crawl",                    # Acquire new knowledge from web
        "learn",                    # Process and learn from knowledge
        "consolidate_memory",       # Prevent catastrophic forgetting
        "introspect",               # Self-analysis and awareness
        "generate_goals",           # Create autonomous goals
        "reason",                   # Reasoning and planning
        "improve",                  # Self-improvement via meta-learning
        "maintain"                  # Save state and optimize
    ]
    
    # Dependencies: cycle -> list of cycles it depends on
    CYCLE_DEPENDENCIES = {
        "learn": ["crawl"],
        "consolidate_memory": ["learn"],
        "introspect": ["learn", "consolidate_memory"],
        "generate_goals": ["introspect"],
        "reason": ["generate_goals", "introspect"],
        "improve": ["reason", "generate_goals"],
        "maintain": ["improve"]
    }
    
    def __init__(self, max_retries: int = 3):
        self.cycle_handlers: Dict[str, Callable] = {}
        self.max_retries = max_retries
        self.execution_history: List[CycleExecution] = []
        self.current_iteration = 0
        self.completed_cycles = 0
        self.failed_cycles = 0
        self.skipped_cycles = 0
        self.total_time = 0.0
        self.performance_metrics: Dict[str, List[float]] = {
            cycle: [] for cycle in self.CYCLE_ORDER
        }
    
    def register_cycle(self, cycle_name: str, handler: Callable):
        """Register a handler for a cycle"""
        if cycle_name not in self.CYCLE_ORDER:
            logger.warning(f"⚠️ Registering unknown cycle: {cycle_name}")
        
        self.cycle_handlers[cycle_name] = handler
        logger.debug(f"✅ Registered cycle handler: {cycle_name}")
    
    def register_cycles(self, handlers: Dict[str, Callable]):
        """Register multiple cycle handlers at once"""
        for cycle_name, handler in handlers.items():
            self.register_cycle(cycle_name, handler)
    
    def check_dependencies(self, cycle_name: str,
                          completed: Dict[str, CycleExecution]) -> bool:
        """Check if all dependencies for a cycle are satisfied"""
        dependencies = self.CYCLE_DEPENDENCIES.get(cycle_name, [])
        
        for dep in dependencies:
            if dep not in completed:
                logger.warning(f"⚠️ Dependency not found: {dep}")
                return False
            
            if completed[dep].status != CycleStatus.COMPLETED:
                logger.warning(f"⚠️ Dependency not completed: {dep}")
                return False
        
        return True
    
    def _should_skip_cycle(self, cycle_name: str,
                          previous_result: Dict[str, Any]) -> bool:
        """Determine if a cycle should be skipped"""
        # Skip crawl if recent crawl was successful and found little new info
        if cycle_name == "crawl" and previous_result:
            if previous_result.get("items_processed", 0) < 3:
                return False  # Always run crawl
        
        # Never skip critical cycles like maintain
        if cycle_name in ["maintain", "introspect"]:
            return False
        
        return False
    
    async def execute_cycle_async(self, execution: CycleExecution) -> Dict[str, Any]:
        """Execute an async cycle"""
        handler = self.cycle_handlers.get(execution.cycle_name)
        if not handler:
            raise ValueError(f"No handler for cycle: {execution.cycle_name}")
        
        execution.start()
        
        try:
            if asyncio.iscoroutinefunction(handler):
                result = await handler()
            else:
                result = handler()
            
            execution.complete(result)
            logger.info(f"✅ {execution.cycle_name} completed in {execution.get_duration():.2f}s")
            return result
        
        except Exception as e:
            execution.fail(str(e))
            logger.error(f"❌ {execution.cycle_name} failed: {e}")
            raise
    
    def execute_cycle_sync(self, execution: CycleExecution) -> Dict[str, Any]:
        """Execute a synchronous cycle"""
        handler = self.cycle_handlers.get(execution.cycle_name)
        if not handler:
            raise ValueError(f"No handler for cycle: {execution.cycle_name}")
        
        execution.start()
        
        try:
            result = handler()
            execution.complete(result)
            logger.info(f"✅ {execution.cycle_name} completed in {execution.get_duration():.2f}s")
            return result
        
        except Exception as e:
            execution.fail(str(e))
            logger.error(f"❌ {execution.cycle_name} failed: {e}")
            raise
    
    async def execute_cycle_with_retry(self, execution: CycleExecution,
                                      is_async: bool = False) -> Dict[str, Any]:
        """Execute a cycle with automatic retry on failure"""
        for attempt in range(self.max_retries):
            try:
                execution.retry_count = attempt
                
                if is_async:
                    result = await self.execute_cycle_async(execution)
                else:
                    result = self.execute_cycle_sync(execution)
                
                # Record performance
                self.performance_metrics[execution.cycle_name].append(
                    execution.get_duration()
                )
                
                # Update monitoring
                monitoring_engine.record_metric(
                    f"cycles.{execution.cycle_name}_duration",
                    execution.get_duration()
                )
                
                return result
            
            except Exception as e:
                if attempt < self.max_retries - 1:
                    wait_time = 2 ** attempt  # Exponential backoff
                    logger.warning(f"⏳ Retrying {execution.cycle_name} after {wait_time}s...")
                    await asyncio.sleep(wait_time)
                else:
                    raise
    
    async def execute_iteration(self, iteration: int) -> Dict[str, CycleExecution]:
        """Execute one complete iteration of all cycles"""
        logger.info(f"\n{'🔄' * 30}")
        logger.info(f"ITERATION {iteration}: Starting cycle sequence")
        logger.info(f"{'🔄' * 30}")
        
        self.current_iteration = iteration
        iteration_start = time.time()
        completed_executions: Dict[str, CycleExecution] = {}
        
        # Report iteration started
        integration_layer.event_bus.publish_event(
            "iteration.started",
            "coordinator",
            {"iteration": iteration},
            priority=6
        )
        
        for cycle_index, cycle_name in enumerate(self.CYCLE_ORDER):
            # Create execution record
            execution = CycleExecution(cycle_name, cycle_index, iteration)
            
            # Check dependencies
            if not self.check_dependencies(cycle_name, completed_executions):
                execution.status = CycleStatus.SKIPPED
                self.skipped_cycles += 1
                logger.warning(f"⏭️ Skipping {cycle_name} - dependencies not met")
                completed_executions[cycle_name] = execution
                continue
            
            # Report cycle starting
            integration_layer.report_cycle_start(
                cycle_name,
                {"iteration": iteration, "cycle_index": cycle_index}
            )
            
            try:
                # Determine if sync or async
                is_async = cycle_name in ["crawl", "learn"]
                
                # Execute with retry
                result = await self.execute_cycle_with_retry(
                    execution,
                    is_async=is_async
                )
                
                self.completed_cycles += 1
                
                # Report cycle completion
                integration_layer.report_cycle_complete(
                    cycle_name,
                    result,
                    execution.get_duration()
                )
                
            except Exception as e:
                self.failed_cycles += 1
                logger.error(f"❌ {cycle_name} failed after {self.max_retries} retries: {e}")
                
                # Report cycle failure
                integration_layer.report_cycle_error(
                    cycle_name,
                    e,
                    {"iteration": iteration}
                )
                
                # Update monitoring
                monitoring_engine.update_component_health(cycle_name, "failed")
                
                # Don't stop iteration on error - continue with other cycles
            
            completed_executions[cycle_name] = execution
        
        # Calculate iteration stats
        iteration_duration = time.time() - iteration_start
        self.total_time += iteration_duration
        
        successful = sum(1 for e in completed_executions.values()
                        if e.status == CycleStatus.COMPLETED)
        
        logger.info(f"\n{'✅' * 20}")
        logger.info(f"ITERATION {iteration} COMPLETE")
        logger.info(f"  Cycles: {successful}/{len(self.CYCLE_ORDER)} successful")
        logger.info(f"  Duration: {iteration_duration:.2f}s")
        logger.info(f"{'✅' * 20}\n")
        
        # Update global metrics
        monitoring_engine.record_metric("cycles.total_completed", self.completed_cycles)
        monitoring_engine.record_metric("cycles.success_rate",
                                       successful / len(self.CYCLE_ORDER))
        monitoring_engine.record_metric("cycles.avg_duration",
                                       iteration_duration)
        
        # Record execution history
        self.execution_history.extend(completed_executions.values())
        
        return completed_executions
    
    def get_execution_summary(self) -> Dict[str, Any]:
        """Get summary of all executions"""
        return {
            "total_iterations": self.current_iteration,
            "completed_cycles": self.completed_cycles,
            "failed_cycles": self.failed_cycles,
            "skipped_cycles": self.skipped_cycles,
            "total_time": self.total_time,
            "avg_iteration_time": self.total_time / max(1, self.current_iteration),
            "performance_metrics": {
                cycle: {
                    "avg": sum(times) / len(times) if times else 0,
                    "min": min(times) if times else 0,
                    "max": max(times) if times else 0,
                    "count": len(times)
                }
                for cycle, times in self.performance_metrics.items()
            }
        }
    
    def get_cycle_health(self) -> Dict[str, Dict[str, Any]]:
        """Get health status for each cycle"""
        health = {}
        
        for cycle in self.CYCLE_ORDER:
            times = self.performance_metrics[cycle]
            success_count = sum(1 for e in self.execution_history
                              if e.cycle_name == cycle and 
                              e.status == CycleStatus.COMPLETED)
            total_count = sum(1 for e in self.execution_history
                            if e.cycle_name == cycle)
            
            success_rate = (success_count / total_count) if total_count > 0 else 0
            
            health[cycle] = {
                "success_rate": success_rate,
                "avg_duration": sum(times) / len(times) if times else 0,
                "executions": total_count,
                "status": "healthy" if success_rate >= 0.8 else "degraded"
            }
        
        return health
    
    def print_iteration_summary(self, executions: Dict[str, CycleExecution]):
        """Print summary of an iteration"""
        logger.info(f"\n📊 ITERATION SUMMARY")
        logger.info("-" * 60)
        
        for cycle_name in self.CYCLE_ORDER:
            if cycle_name in executions:
                exec_data = executions[cycle_name]
                
                if exec_data.status == CycleStatus.COMPLETED:
                    status_icon = "✅"
                elif exec_data.status == CycleStatus.FAILED:
                    status_icon = "❌"
                elif exec_data.status == CycleStatus.SKIPPED:
                    status_icon = "⏭️"
                else:
                    status_icon = "❓"
                
                logger.info(f"{status_icon} {exec_data.cycle_name:20} "
                           f"{exec_data.status.value:10} "
                           f"{exec_data.get_duration():7.2f}s")


# Global cycle coordinator instance
cycle_coordinator = CycleCoordinator()
