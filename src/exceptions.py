"""
Custom exception classes for the autonomous AI system.

Provides domain-specific exceptions with clear error context and recovery suggestions.
This enables precise error handling throughout the system.
"""
from typing import Optional, Dict, Any


class AutonomousAIException(Exception):
    """Base exception for all autonomous AI system errors"""
    
    def __init__(self, message: str, error_code: str = "ERROR", context: Optional[Dict[str, Any]] = None):
        """
        Initialize exception with message, code, and context.
        
        Args:
            message: Human-readable error description
            error_code: Machine-readable error identifier (e.g., 'KB_OVERFLOW')
            context: Additional contextual information about the error
        """
        self.message = message
        self.error_code = error_code
        self.context = context or {}
        super().__init__(f"[{error_code}] {message}")


class KnowledgeBaseException(AutonomousAIException):
    """Raised when knowledge base operations fail"""
    pass


class MemoryException(AutonomousAIException):
    """Raised when memory operations fail"""
    pass


class CrawlerException(AutonomousAIException):
    """Raised when web crawling fails"""
    pass


class ReasoningException(AutonomousAIException):
    """Raised when reasoning operations fail"""
    pass


class LearningException(AutonomousAIException):
    """Raised when learning operations fail"""
    pass


class ValidationException(AutonomousAIException):
    """Raised when input validation fails"""
    pass


class ResourceExhaustionException(AutonomousAIException):
    """Raised when system resources are exhausted (memory, network, etc.)"""
    pass


class ConfigurationException(AutonomousAIException):
    """Raised when configuration is invalid or missing"""
    pass


class TimeoutException(AutonomousAIException):
    """Raised when an operation exceeds timeout"""
    pass


class PersistenceException(AutonomousAIException):
    """Raised when persistence operations fail"""
    pass


class CircuitBreakerOpenException(AutonomousAIException):
    """Raised when circuit breaker is open (preventing cascading failures)"""
    pass
