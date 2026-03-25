"""
Type Definitions and Interfaces for the Autonomous AI System

This module provides comprehensive type hints and interfaces used throughout
the system to ensure type safety and better IDE support.
"""

from typing import Any, Callable, Dict, List, Optional, Tuple, Union, Protocol
from enum import Enum
from dataclasses import dataclass
from datetime import datetime

# ============================================================================
# Enumerations
# ============================================================================

class TaskType(str, Enum):
    """Enumeration of supported task types."""
    LEARNING = "learning"
    REASONING = "reasoning"
    IMPROVEMENT = "improvement"
    CRAWLING = "crawling"
    INTEGRATION = "integration"
    MAINTENANCE = "maintenance"


class MemoryType(str, Enum):
    """Enumeration of memory tier types."""
    SHORT_TERM = "short_term"
    LONG_TERM = "long_term"
    EPISODIC = "episodic"
    PROCEDURAL = "procedural"


class GoalStatus(str, Enum):
    """Enumeration of goal statuses."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    ABANDONED = "abandoned"


class ReasoningStrategy(str, Enum):
    """Enumeration of reasoning strategies."""
    DEDUCTIVE = "deductive"
    INDUCTIVE = "inductive"
    ABDUCTIVE = "abductive"
    BAYESIAN = "bayesian"
    EVOLUTIONARY = "evolutionary"


# ============================================================================
# Data Classes
# ============================================================================

@dataclass
class KnowledgeEntry:
    """Represents a single knowledge entry in the knowledge base."""
    content: str
    source: str
    timestamp: datetime
    embedding: Optional[List[float]] = None
    metadata: Dict[str, Any] = None
    relevance_score: float = 1.0
    access_count: int = 0
    
    def __post_init__(self):
        """Validate and initialize metadata."""
        if self.metadata is None:
            self.metadata = {}


@dataclass
class Goal:
    """Represents an autonomous goal."""
    goal_id: str
    goal_name: str
    description: str
    priority: float
    status: GoalStatus = GoalStatus.PENDING
    created_at: datetime = None
    completed_at: Optional[datetime] = None
    progress: float = 0.0
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        """Initialize defaults."""
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.metadata is None:
            self.metadata = {}


@dataclass
class TaskResult:
    """Result of a task execution."""
    task_id: str
    task_type: TaskType
    success: bool
    result: Any = None
    error: Optional[str] = None
    execution_time: float = 0.0
    timestamp: datetime = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        """Initialize defaults."""
        if self.timestamp is None:
            self.timestamp = datetime.now()
        if self.metadata is None:
            self.metadata = {}


@dataclass
class AgentState:
    """Complete state of the autonomous agent."""
    agent_id: str
    total_cycles: int
    total_tasks: int
    successful_tasks: int
    failed_tasks: int
    knowledge_size: int
    memory_size: int
    current_goals: List[Goal]
    last_update: datetime
    metadata: Dict[str, Any] = None
    
    @property
    def success_rate(self) -> float:
        """Calculate success rate as percentage."""
        if self.total_tasks == 0:
            return 0.0
        return (self.successful_tasks / self.total_tasks) * 100


@dataclass
class SearchResult:
    """Result from knowledge base search."""
    content: str
    source: str
    score: float
    distance: float
    metadata: Dict[str, Any]


# ============================================================================
# Protocol Interfaces (for structural typing)
# ============================================================================

class CrawlableSource(Protocol):
    """Protocol for crawlable sources."""
    
    def fetch_content(self, url: str) -> str:
        """Fetch content from the source."""
        ...
    
    def validate_url(self, url: str) -> bool:
        """Validate if URL is crawlable."""
        ...


class Learnable(Protocol):
    """Protocol for learnable components."""
    
    def learn(self, content: str, source: str) -> bool:
        """Learn from content."""
        ...
    
    def improve(self) -> float:
        """Improve and return improvement score."""
        ...


class Reasoner(Protocol):
    """Protocol for reasoning components."""
    
    def reason(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Perform reasoning and return result."""
        ...
    
    def explain(self) -> str:
        """Provide explanation of reasoning."""
        ...


class Executable(Protocol):
    """Protocol for executable tasks."""
    
    async def execute(self, args: Dict[str, Any]) -> TaskResult:
        """Execute task with arguments."""
        ...
    
    def is_cancellable(self) -> bool:
        """Check if task can be cancelled."""
        ...


# ============================================================================
# Type Aliases
# ============================================================================

# Knowledge and Learning
KnowledgeData = Dict[str, Any]
EmbeddingVector = List[float]
ConceptMap = Dict[str, List[str]]

# Goals and Planning  
GoalHierarchy = Dict[str, List[Goal]]
PlanStep = Tuple[str, Dict[str, Any]]
ExecutionPlan = List[PlanStep]

# Reasoning and Decisions
DecisionContext = Dict[str, Any]
ReasoningResult = Dict[str, Union[str, float, bool, List[Any]]]
ConfidenceScore = float  # 0.0 to 1.0

# Memory and Persistence
MemorySnapshot = Dict[str, Any]
PersistenceMap = Dict[str, bytes]

# Monitoring and Metrics
MetricPoint = Tuple[datetime, float]
MetricsSeries = Dict[str, List[MetricPoint]]

# Event System
EventCallback = Callable[[str, Dict[str, Any]], None]
EventHandler = Callable[[str, Dict[str, Any]], Any]

# Async Execution
AsyncTaskResult = Tuple[bool, Any, Optional[str]]
AsyncCallback = Callable[..., Any]


# ============================================================================
# Result Types
# ============================================================================

class Success(dict):
    """Represents a successful operation result."""
    def __init__(self, data: Any = None, message: str = "Success"):
        super().__init__(
            success=True,
            data=data,
            message=message,
            timestamp=datetime.now().isoformat()
        )


class Failure(dict):
    """Represents a failed operation result."""
    def __init__(self, error: str, code: int = 1, data: Any = None):
        super().__init__(
            success=False,
            error=error,
            code=code,
            data=data,
            timestamp=datetime.now().isoformat()
        )


# ============================================================================
# System Constants
# ============================================================================

class SystemConstants:
    """System-wide constants and configuration values."""
    
    # Limits
    MAX_CONCURRENT_TASKS = 10
    MAX_MEMORY_ENTRIES = 100000
    MAX_KNOWLEDGE_SIZE = 1_000_000
    MAX_LEARNING_RATE = 1.0
    MIN_LEARNING_RATE = 0.001
    
    # Timeouts (seconds)
    DEFAULT_TASK_TIMEOUT = 300
    CRAWLER_TIMEOUT = 30
    MEMORY_PERSISTENCE_INTERVAL = 300
    
    # Thresholds
    IMPROVEMENT_THRESHOLD = 0.05
    CONFIDENCE_THRESHOLD = 0.7
    SIMILARITY_THRESHOLD = 0.5
    
    # Cache
    CACHE_TTL_SECONDS = 3600
    CACHE_MAX_SIZE = 10000
    
    # Batch Processing
    BATCH_SIZE_KNOWLEDGE = 100
    BATCH_SIZE_CRAWLER = 10
    BATCH_SIZE_LEARNING = 50
    
    # Memory Tiers
    SHORT_TERM_CAPACITY = 10000
    LONG_TERM_CAPACITY = MAX_KNOWLEDGE_SIZE
    EPISODIC_CAPACITY = 50000
    
    # Learning Parameters
    DEFAULT_LEARNING_RATE = 0.01
    DEFAULT_EXPLORATION_RATE = 0.2
    DEFAULT_DISCOUNT_FACTOR = 0.99


# ============================================================================
# Optional Validation Helper
# ============================================================================

def validate_goal(goal: Goal) -> bool:
    """Validate goal object for correctness."""
    if not goal.goal_id or not goal.goal_name:
        return False
    if not (0.0 <= goal.priority <= 1.0):
        return False
    if not (0.0 <= goal.progress <= 1.0):
        return False
    return True


def validate_knowledge_entry(entry: KnowledgeEntry) -> bool:
    """Validate knowledge entry for correctness."""
    if not entry.content or not entry.source:
        return False
    if not (0.0 <= entry.relevance_score <= 1.0):
        return False
    if entry.access_count < 0:
        return False
    return True


__all__ = [
    # Enumerations
    "TaskType",
    "MemoryType",
    "GoalStatus",
    "ReasoningStrategy",
    # Data Classes
    "KnowledgeEntry",
    "Goal",
    "TaskResult",
    "AgentState",
    "SearchResult",
    # Protocols
    "CrawlableSource",
    "Learnable",
    "Reasoner",
    "Executable",
    # Type Aliases
    "KnowledgeData",
    "EmbeddingVector",
    "ConceptMap",
    "GoalHierarchy",
    "PlanStep",
    "ExecutionPlan",
    "DecisionContext",
    "ReasoningResult",
    "ConfidenceScore",
    "MemorySnapshot",
    "PersistenceMap",
    "MetricPoint",
    "MetricsSeries",
    "EventCallback",
    "EventHandler",
    "AsyncTaskResult",
    "AsyncCallback",
    # Result Types
    "Success",
    "Failure",
    # Constants
    "SystemConstants",
    # Validators
    "validate_goal",
    "validate_knowledge_entry",
]
