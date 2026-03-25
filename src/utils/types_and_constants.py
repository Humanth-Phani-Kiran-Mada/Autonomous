"""
Type definitions and constants for the autonomous AI system.

Provides:
- Custom type aliases for better code clarity
- Enum definitions for state management
- Constant configuration values
- Data structure definitions
"""
from enum import Enum
from typing import TypedDict, Dict, Any, List, Optional
from datetime import datetime


# ============================================================================
# ENUMS for State Management
# ============================================================================

class MemoryType(str, Enum):
    """Types of memory in the system"""
    SHORT_TERM = "short_term"
    LONG_TERM = "long_term"
    EPISODIC = "episodic"
    WORKING = "working"


class CrawlerState(str, Enum):
    """States of the web crawler"""
    IDLE = "idle"
    CRAWLING = "crawling"
    PROCESSING = "processing"
    ERROR = "error"
    PAUSED = "paused"


class LearningPhase(str, Enum):
    """Phases of the learning cycle"""
    CRAWLING = "crawling"
    LEARNING = "learning"
    REASONING = "reasoning"
    IMPROVEMENT = "improvement"
    MAINTENANCE = "maintenance"


class GoalStatus(str, Enum):
    """Status of goals"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"


class KnowledgeType(str, Enum):
    """Types of knowledge entries"""
    ARTICLE = "article"
    LINK = "link"
    HEADER = "header"
    CONCEPT = "concept"
    PATTERN = "pattern"
    SKILL = "skill"
    THEORY = "theory"


class CircuitBreakerState(str, Enum):
    """States of circuit breaker"""
    CLOSED = "closed"  # Normal operation
    OPEN = "open"      # Failing, rejecting requests
    HALF_OPEN = "half_open"  # Attempting recovery


# ============================================================================
# TypedDict Definitions for Data Structures
# ============================================================================

class KnowledgeEntry(TypedDict, total=False):
    """Structure of a knowledge base entry"""
    id: str
    content: str
    source: str
    type: str
    created_at: str
    accessed_count: int
    relevance_score: float
    metadata: Dict[str, Any]


class MemoryEntry(TypedDict, total=False):
    """Structure of a memory entry"""
    key: str
    value: Any
    stored_at: str
    importance: float
    last_accessed: str


class EpisodeMemory(TypedDict, total=False):
    """Structure of an episodic memory"""
    id: str
    description: str
    actions: List[str]
    outcomes: List[str]
    timestamp: str
    importance: float


class Goal(TypedDict, total=False):
    """Structure of a goal"""
    id: int
    name: str
    description: str
    priority: float
    deadline: Optional[str]
    created_at: str
    status: str
    progress: float
    sub_goals: List[str]


class Skill(TypedDict, total=False):
    """Structure of a skill entry"""
    name: str
    level: float  # 0.0 to 1.0
    domain: str
    last_practiced: str
    practice_count: int
    improvement_rate: float


class LearningMetric(TypedDict, total=False):
    """Structure of learning metrics"""
    timestamp: str
    knowledge_id: str
    categories: List[str]
    key_concepts: List[str]
    applicability: float
    improvement_potential: float


class CrawlResult(TypedDict, total=False):
    """Structure of web crawl results"""
    url: str
    status_code: int
    content_length: int
    timestamp: str
    extracted_knowledge: List[KnowledgeEntry]
    error: Optional[str]


class ReasoningDecision(TypedDict, total=False):
    """Structure of a reasoning decision"""
    decision_id: str
    timestamp: str
    goal_id: int
    options: List[Dict[str, Any]]
    selected_option: str
    confidence: float
    rationale: str


# ============================================================================
# Type Aliases for Better Code Clarity
# ============================================================================

# URL and path types
URL = str
FilePath = str

# Numeric types
ProbabilityScore = float  # 0.0 to 1.0
ConfidenceScore = float  # 0.0 to 1.0
RelevanceScore = float   # 0.0 to 1.0
SkillLevel = float       # 0.0 to 1.0

# Collection types
Knowledge = Dict[str, Any]
Memory = Dict[str, Any]
Metrics = Dict[str, Any]

# Time types
Timestamp = str  # ISO format string
Duration = float  # seconds


# ============================================================================
# System Constants
# ============================================================================

class SystemConstants:
    """System-wide constants"""
    
    # Skill levels
    MIN_SKILL_LEVEL = 0.0
    MAX_SKILL_LEVEL = 1.0
    EXPERT_THRESHOLD = 0.9
    PROFICIENT_THRESHOLD = 0.7
    NOVICE_THRESHOLD = 0.3
    
    # Learning rates
    DEFAULT_LEARNING_RATE = 0.01
    MIN_LEARNING_RATE = 0.001
    MAX_LEARNING_RATE = 0.1
    
    # Memory thresholds
    DEFAULT_MEMORY_TTL_SECONDS = 3600
    LONG_TERM_MEMORY_TTL_DAYS = 90
    MAX_MEMORY_ENTRIES = 100000
    MEMORY_COMPRESSION_RATIO = 0.8
    
    # Knowledge base
    MAX_KNOWLEDGE_ENTRIES = 100000
    KNOWLEDGE_EMBEDDING_DIMENSION = 384
    KNOWLEDGE_RELEVANCE_THRESHOLD = 0.3
    
    # Web crawling
    DEFAULT_CRAWLER_TIMEOUT = 30
    DEFAULT_MAX_WORKERS = 5
    DEFAULT_BATCH_SIZE = 10
    MAX_RETRIES = 3
    
    # Goal management
    DEFAULT_GOAL_PRIORITY = 0.5
    HIGH_PRIORITY_THRESHOLD = 0.7
    CRITICAL_PRIORITY_THRESHOLD = 0.9
    
    # Reasoning
    DECISION_CONFIDENCE_THRESHOLD = 0.6
    MIN_OPTIONS_FOR_DECISION = 2
    MAX_DEPTH_FOR_DECOMPOSITION = 10
    
    # Improvement
    IMPROVEMENT_THRESHOLD = 0.05  # 5% improvement needed
    MIN_SUCCESS_RATE_FOR_LEARNING = 0.3
    
    # Resource limits
    MAX_MEMORY_MB = 4096
    MAX_CPU_PERCENT = 80.0
    RATE_LIMIT_PER_SECOND = 10
    
    # Timeouts
    TASK_TIMEOUT_SECONDS = 300
    CRAWL_TIMEOUT_SECONDS = 30
    LEARNING_TIMEOUT_SECONDS = 60


class ErrorCodes:
    """Standardized error codes"""
    
    # Validation errors
    INVALID_PARAM_TYPE = "INVALID_PARAM_TYPE"
    PARAM_TOO_SHORT = "PARAM_TOO_SHORT"
    PARAM_TOO_LONG = "PARAM_TOO_LONG"
    INVALID_VALUE_RANGE = "INVALID_VALUE_RANGE"
    
    # Resource errors
    MEMORY_EXHAUSTED = "MEMORY_EXHAUSTED"
    RESOURCE_LIMIT_EXCEEDED = "RESOURCE_LIMIT_EXCEEDED"
    TIMEOUT = "TIMEOUT"
    
    # Network errors
    NETWORK_ERROR = "NETWORK_ERROR"
    CONNECTION_TIMEOUT = "CONNECTION_TIMEOUT"
    CONNECTION_REFUSED = "CONNECTION_REFUSED"
    
    # Persistence errors
    PERSISTENCE_FAILED = "PERSISTENCE_FAILED"
    LOAD_FAILED = "LOAD_FAILED"
    FILE_NOT_FOUND = "FILE_NOT_FOUND"
    
    # Circuit breaker
    CIRCUIT_BREAKER_OPEN = "CIRCUIT_BREAKER_OPEN"
    
    # Configuration
    CONFIG_INVALID = "CONFIG_INVALID"
    CONFIG_MISSING = "CONFIG_MISSING"
    
    # Operation errors
    OPERATION_FAILED = "OPERATION_FAILED"
    OPERATION_UNSUPPORTED = "OPERATION_UNSUPPORTED"


class LogMessages:
    """Standardized log messages"""
    
    # Initialization
    INIT_COMPONENT = "Initializing {component}..."
    INIT_COMPLETE = "{component} initialized successfully"
    INIT_FAILED = "Failed to initialize {component}: {error}"
    
    # State management
    STATE_LOADED = "State loaded for {component}: {count} entries"
    STATE_SAVED = "State saved for {component}"
    STATE_SAVE_FAILED = "Failed to save state for {component}: {error}"
    
    # Operations
    OPERATION_START = "Starting {operation}..."
    OPERATION_COMPLETE = "{operation} completed successfully in {duration}s"
    OPERATION_FAILED = "{operation} failed: {error}"
    OPERATION_RETRY = "Retrying {operation} (attempt {attempt}/{max_attempts})"
    
    # Performance
    PERFORMANCE_DEGRADED = "Performance warning: {message}"
    RESOURCE_ALERT = "Resource alert: {resource} at {usage}%"
    
    # Learning
    LEARNING_START = "Learning from: {source}"
    LEARNING_RESULT = "Learning result: {result}"
    SKILL_IMPROVEMENT = "Skill improvement: {skill} {old_level}% → {new_level}%"
