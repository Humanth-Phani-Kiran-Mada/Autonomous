"""
Unit tests for exceptions module

Validates custom exception hierarchy, error codes, and context handling.
"""

import pytest
from src.exceptions import (
    AutonomousAIException,
    KnowledgeBaseException,
    MemoryException,
    CrawlerException,
    ReasoningException,
    ValidationException,
    CircuitBreakerOpenException,
    ResourceExhaustedException,
)


class TestAutonomousAIException:
    """Tests for base exception class"""
    
    def test_create_base_exception(self):
        """Base exception stores message and error code"""
        exc = AutonomousAIException("Test error", error_code="TEST_001")
        assert exc.message == "Test error"
        assert exc.error_code == "TEST_001"
    
    def test_exception_string_representation(self):
        """Exception has human-readable string"""
        exc = AutonomousAIException("Test error", error_code="TEST_001")
        exc_str = str(exc)
        assert "TEST_001" in exc_str
        assert "Test error" in exc_str
    
    def test_exception_context(self):
        """Exception can store additional context"""
        exc = AutonomousAIException(
            "Test error", 
            error_code="TEST_001",
            context={"module": "test", "operation": "fetch"}
        )
        assert exc.context["module"] == "test"


class TestKnowledgeBaseException:
    """Tests for KnowledgeBase-specific exception"""
    
    def test_kb_exception_creation(self):
        """KnowledgeBaseException inherits from base"""
        exc = KnowledgeBaseException("KB error", error_code="KB_001")
        assert isinstance(exc, AutonomousAIException)
        assert exc.message == "KB error"


class TestMemoryException:
    """Tests for Memory-specific exception"""
    
    def test_memory_exception_creation(self):
        """MemoryException inherits from base"""
        exc = MemoryException("Memory error", error_code="MEM_001")
        assert isinstance(exc, AutonomousAIException)
        assert exc.error_code == "MEM_001"


class TestCrawlerException:
    """Tests for Crawler-specific exception"""
    
    def test_crawler_exception_creation(self):
        """CrawlerException inherits from base"""
        exc = CrawlerException("Crawl error", error_code="CRAWL_001")
        assert isinstance(exc, AutonomousAIException)
        assert exc.message == "Crawl error"


class TestValidationException:
    """Tests for Validation-specific exception"""
    
    def test_validation_exception_creation(self):
        """ValidationException inherits from base"""
        exc = ValidationException("Invalid input", error_code="VAL_001")
        assert isinstance(exc, AutonomousAIException)


class TestCircuitBreakerException:
    """Tests for CircuitBreaker-specific exception"""
    
    def test_circuit_breaker_exception(self):
        """CircuitBreakerOpenException inherits from base"""
        exc = CircuitBreakerOpenException(
            "Circuit open",
            error_code="CB_001",
            recovery_time=60
        )
        assert isinstance(exc, AutonomousAIException)
        assert exc.recovery_time == 60


class TestResourceExhaustedException:
    """Tests for Resource exhaustion exception"""
    
    def test_resource_exception(self):
        """ResourceExhaustedException stores resource info"""
        exc = ResourceExhaustedException(
            "Out of memory",
            error_code="RES_001",
            resource_type="memory",
            limit_value=1024
        )
        assert isinstance(exc, AutonomousAIException)
        assert exc.resource_type == "memory"
        assert exc.limit_value == 1024


class TestExceptionHierarchy:
    """Tests for exception inheritance chain"""
    
    def test_all_custom_exceptions_inherit_from_base(self):
        """All custom exceptions should inherit from AutonomousAIException"""
        exceptions = [
            KnowledgeBaseException,
            MemoryException,
            CrawlerException,
            ReasoningException,
            ValidationException,
            CircuitBreakerOpenException,
            ResourceExhaustedException,
        ]
        
        for exc_class in exceptions:
            exc = exc_class("test")
            assert isinstance(exc, AutonomousAIException)
    
    def test_exception_catching_by_base_type(self):
        """Can catch derived exceptions using base type"""
        try:
            raise KnowledgeBaseException("Test")
        except AutonomousAIException as e:
            assert isinstance(e, KnowledgeBaseException)


class TestErrorCodes:
    """Tests for error code usage"""
    
    def test_error_code_format(self):
        """Error codes follow expected format"""
        exc = ValidationException("test", error_code="VAL_001")
        # Error code should be uppercase with numbers
        assert exc.error_code == "VAL_001"
        assert exc.error_code.isupper() or exc.error_code[0].isupper()
    
    def test_different_error_codes(self):
        """Different exceptions can have different codes"""
        kb_exc = KnowledgeBaseException("error1", error_code="KB_001")
        val_exc = ValidationException("error2", error_code="VAL_001")
        
        assert kb_exc.error_code != val_exc.error_code


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
