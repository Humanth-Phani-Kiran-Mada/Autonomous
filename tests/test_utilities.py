"""
Unit tests for utilities module

Tests coverage for decorators and utility functions:
- Retry with exponential backoff
- Performance monitoring
- Caching with TTL
- Resource limits
- Circuit breaker pattern
"""

import pytest
import time
import asyncio
from unittest.mock import patch, MagicMock
from src.utilities import (
    retry_with_backoff,
    measure_performance,
    cached,
    ensure_resource_limits,
    CircuitBreaker,
)
from src.exceptions import CircuitBreakerOpenException


class TestRetryDecorator:
    """Tests for retry_with_backoff decorator"""
    
    def test_successful_call_no_retry(self):
        """Successful call shouldn't retry"""
        call_count = 0
        
        @retry_with_backoff(max_retries=3)
        def succeed():
            nonlocal call_count
            call_count += 1
            return "success"
        
        result = succeed()
        assert result == "success"
        assert call_count == 1
    
    def test_retry_on_failure(self):
        """Failed calls should retry"""
        call_count = 0
        
        @retry_with_backoff(max_retries=3, initial_delay=0.01)
        def fail_twice():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ValueError("Temporary failure")
            return "success"
        
        result = fail_twice()
        assert result == "success"
        assert call_count == 3
    
    def test_max_retries_exceeded(self):
        """Should raise after max retries"""
        call_count = 0
        
        @retry_with_backoff(max_retries=2, initial_delay=0.01)
        def always_fail():
            nonlocal call_count
            call_count += 1
            raise ValueError("Always fails")
        
        with pytest.raises(ValueError):
            always_fail()
        
        assert call_count == 3  # initial + 2 retries


class TestMeasurePerformanceDecorator:
    """Tests for measure_performance decorator"""
    
    def test_logs_execution_time(self, capsys):
        """Should log function execution time"""
        @measure_performance
        def timed_function():
            time.sleep(0.01)  # Sleep for 10ms
            return "done"
        
        result = timed_function()
        assert result == "done"
        # Should have logged timing information
    
    def test_returns_correct_value(self):
        """Decorator should return function result unchanged"""
        @measure_performance
        def return_value():
            return 42
        
        result = return_value()
        assert result == 42
    
    def test_works_with_arguments(self):
        """Decorator should work with function arguments"""
        @measure_performance
        def add(a, b):
            return a + b
        
        result = add(5, 3)
        assert result == 8


class TestCacheDecorator:
    """Tests for cached decorator"""
    
    def test_caches_results(self):
        """Results should be cached"""
        call_count = 0
        
        @cached(ttl_seconds=10)
        def expensive_operation():
            nonlocal call_count
            call_count += 1
            return "result"
        
        result1 = expensive_operation()
        result2 = expensive_operation()
        
        assert result1 == result2
        assert call_count == 1  # Called once, second was cached
    
    def test_cache_expiration(self):
        """Cache should expire after TTL"""
        call_count = 0
        
        @cached(ttl_seconds=0.05)  # 50ms TTL
        def operation():
            nonlocal call_count
            call_count += 1
            return f"result_{call_count}"
        
        result1 = operation()
        time.sleep(0.1)  # Wait for cache to expire
        result2 = operation()
        
        assert result1 == "result_1"
        assert result2 == "result_2"  # New cache entry
        assert call_count == 2
    
    def test_different_arguments_different_cache(self):
        """Different arguments should use different cache entries"""
        call_count = 0
        
        @cached(ttl_seconds=10)
        def operation(value):
            nonlocal call_count
            call_count += 1
            return f"result_{value}"
        
        result1 = operation("a")
        result2 = operation("b")
        result3 = operation("a")  # Should hit cache
        
        assert result1 == "result_a"
        assert result2 == "result_b"
        assert result3 == "result_a"
        assert call_count == 2  # Only called twice


class TestResourceLimitsDecorator:
    """Tests for ensure_resource_limits decorator"""
    
    def test_function_completes_within_limits(self):
        """Function within limits should complete successfully"""
        @ensure_resource_limits(max_memory_mb=512, timeout_seconds=5)
        def quick_operation():
            return "success"
        
        result = quick_operation()
        assert result == "success"
    
    def test_timeout_exceeded(self):
        """Should raise on timeout"""
        @ensure_resource_limits(timeout_seconds=0.01)
        def slow_operation():
            time.sleep(1)
            return "done"
        
        with pytest.raises(TimeoutError):
            slow_operation()


class TestCircuitBreaker:
    """Tests for CircuitBreaker pattern"""
    
    def test_normal_operation(self):
        """Circuit should be closed during normal operation"""
        cb = CircuitBreaker(failure_threshold=3, recovery_timeout=10)
        
        def operation():
            return "success"
        
        result = cb.call(operation)
        assert result == "success"
    
    def test_opens_on_failures(self):
        """Circuit should open after threshold failures"""
        cb = CircuitBreaker(failure_threshold=2, recovery_timeout=10)
        call_count = 0
        
        def failing_operation():
            nonlocal call_count
            call_count += 1
            raise ValueError("Operation failed")
        
        # First two calls fail
        for _ in range(2):
            with pytest.raises(ValueError):
                cb.call(failing_operation)
        
        # Circuit should now be open
        with pytest.raises(CircuitBreakerOpenException):
            cb.call(failing_operation)
        
        # Verify operation wasn't called for 3rd attempt
        assert call_count == 2
    
    def test_recovery_timeout(self):
        """Circuit should attempt recovery after timeout"""
        cb = CircuitBreaker(failure_threshold=1, recovery_timeout=0.05)
        
        def failing_op():
            raise ValueError("Failed")
        
        # Fail once to open circuit
        with pytest.raises(ValueError):
            cb.call(failing_op)
        
        # Circuit is open
        with pytest.raises(CircuitBreakerOpenException):
            cb.call(failing_op)
        
        # Wait for recovery timeout
        time.sleep(0.1)
        
        # Should attempt half-open
        def recovering_op():
            return "recovered"
        
        result = cb.call(recovering_op)
        assert result == "recovered"
    
    def test_circuit_state_transitions(self):
        """Circuit should transition through states correctly"""
        cb = CircuitBreaker(failure_threshold=2, recovery_timeout=10)
        
        # Initial state: CLOSED
        assert cb.state == "CLOSED"
        
        # Fail twice to open
        for _ in range(2):
            try:
                cb.call(lambda: 1/0)
            except:
                pass
        
        assert cb.state == "OPEN"
        
        # Verify circuit is open
        with pytest.raises(CircuitBreakerOpenException):
            cb.call(lambda: "success")


class TestCheckDecorators:
    """Integration tests for multiple decorators"""
    
    def test_retry_and_cache_together(self):
        """Both decorators should work together"""
        call_count = 0
        
        @cached(ttl_seconds=10)
        @retry_with_backoff(max_retries=2, initial_delay=0.01)
        def operation():
            nonlocal call_count
            call_count += 1
            return "result"
        
        result1 = operation()
        result2 = operation()  # From cache
        
        assert result1 == result2
        assert call_count == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
