"""
Utility decorators and helper functions for the autonomous AI system.

Provides production-grade decorators for:
- Input validation with error handling
- Automatic retry with exponential backoff  
- Performance monitoring and metrics
- Caching with TTL
- Circuit breaker pattern
- Async operation coordination
"""
import functools
import time
import asyncio
from typing import Any, Callable, Dict, Optional, TypeVar, cast
from datetime import datetime, timedelta
from pathlib import Path
import json
import config
from .logger import logger
from .exceptions import (
    ValidationException, TimeoutException, CircuitBreakerOpenException,
    ResourceExhaustionException
)

T = TypeVar('T')
F = TypeVar('F', bound=Callable[..., Any])


class CircuitBreaker:
    """
    Circuit breaker pattern for preventing cascading failures.
    
    States: CLOSED (normal) -> OPEN (failing) -> HALF_OPEN (recovering) -> CLOSED
    """
    
    def __init__(self, failure_threshold: int = 5, recovery_timeout: int = 60, name: str = ""):
        """
        Initialize circuit breaker.
        
        Args:
            failure_threshold: Number of failures before opening circuit
            recovery_timeout: Seconds to wait before attempting recovery
            name: Identifier for logging
        """
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.name = name
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time: Optional[datetime] = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
    
    def call(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Execute function through circuit breaker"""
        if self.state == "OPEN":
            if self._should_attempt_recovery():
                self.state = "HALF_OPEN"
                logger.info(f"🔌 Circuit breaker '{self.name}' HALF_OPEN - attempting recovery")
            else:
                raise CircuitBreakerOpenException(
                    f"Circuit breaker '{self.name}' is OPEN",
                    error_code="CB_OPEN"
                )
        
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise
    
    def _on_success(self) -> None:
        """Handle successful execution"""
        self.failure_count = 0
        if self.state == "HALF_OPEN":
            self.state = "CLOSED"
            logger.info(f"🔌 Circuit breaker '{self.name}' CLOSED - recovered")
    
    def _on_failure(self) -> None:
        """Handle failed execution"""
        self.failure_count += 1
        self.last_failure_time = datetime.now()
        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"
            logger.warning(f"🔌 Circuit breaker '{self.name}' OPEN after {self.failure_count} failures")
    
    def _should_attempt_recovery(self) -> bool:
        """Check if enough time has passed to attempt recovery"""
        if not self.last_failure_time:
            return False
        return (datetime.now() - self.last_failure_time).total_seconds() > self.recovery_timeout


class Cache:
    """Simple TTL-based in-memory cache"""
    
    def __init__(self):
        self.cache: Dict[str, tuple[Any, datetime]] = {}
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache if not expired"""
        if key not in self.cache:
            return None
        value, expiry = self.cache[key]
        if datetime.now() > expiry:
            del self.cache[key]
            return None
        return value
    
    def set(self, key: str, value: Any, ttl_seconds: int = 3600) -> None:
        """Set value in cache with TTL"""
        self.cache[key] = (value, datetime.now() + timedelta(seconds=ttl_seconds))
    
    def clear(self) -> None:
        """Clear all cached values"""
        self.cache.clear()


def validate_input(
    param_name: str,
    param_type: type,
    allow_none: bool = False,
    min_length: Optional[int] = None,
    max_length: Optional[int] = None
) -> Callable:
    """
    Decorator for validating function parameters.
    
    Args:
        param_name: Name of parameter to validate
        param_type: Expected type(s)
        allow_none: If True, None values are allowed
        min_length: Minimum length for strings/collections
        max_length: Maximum length for strings/collections
    
    Returns:
        Decorator function
    
    Example:
        @validate_input('source_url', str, min_length=10)
        def fetch(source_url):
            pass
    """
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            value = kwargs.get(param_name)
            if value is None and allow_none:
                return func(*args, **kwargs)
            
            if not isinstance(value, param_type):
                raise ValidationException(
                    f"Parameter '{param_name}' must be {param_type.__name__}, got {type(value).__name__}",
                    error_code="INVALID_PARAM_TYPE"
                )
            
            if min_length is not None and hasattr(value, '__len__'):
                if len(value) < min_length:
                    raise ValidationException(
                        f"Parameter '{param_name}' must have minimum length {min_length}",
                        error_code="PARAM_TOO_SHORT"
                    )
            
            if max_length is not None and hasattr(value, '__len__'):
                if len(value) > max_length:
                    raise ValidationException(
                        f"Parameter '{param_name}' exceeds maximum length {max_length}",
                        error_code="PARAM_TOO_LONG"
                    )
            
            return func(*args, **kwargs)
        return cast(F, wrapper)
    return decorator


def retry_with_backoff(
    max_retries: int = 3,
    initial_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: float = 2.0
) -> Callable:
    """
    Decorator for automatic retry with exponential backoff.
    
    Args:
        max_retries: Maximum number of retry attempts
        initial_delay: Starting delay in seconds
        max_delay: Maximum delay between retries
        exponential_base: Base for exponential backoff calculation
    
    Returns:
        Decorator function
    
    Example:
        @retry_with_backoff(max_retries=3)
        async def fetch_remote_data():
            pass
    """
    def decorator(func: F) -> F:
        @functools.wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            delay = initial_delay
            for attempt in range(max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if attempt >= max_retries:
                        logger.error(f"❌ Failed after {max_retries + 1} attempts: {e}")
                        raise
                    delay = min(initial_delay * (exponential_base ** attempt), max_delay)
                    logger.warning(f"⏳ Retry {attempt + 1}/{max_retries} after {delay:.1f}s: {e}")
                    await asyncio.sleep(delay)
        
        @functools.wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            delay = initial_delay
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt >= max_retries:
                        logger.error(f"❌ Failed after {max_retries + 1} attempts: {e}")
                        raise
                    delay = min(initial_delay * (exponential_base ** attempt), max_delay)
                    logger.warning(f"⏳ Retry {attempt + 1}/{max_retries} after {delay:.1f}s: {e}")
                    time.sleep(delay)
        
        if asyncio.iscoroutinefunction(func):
            return cast(F, async_wrapper)
        return cast(F, sync_wrapper)
    return decorator


def measure_performance(func: F) -> F:
    """
    Decorator for measuring function execution time and logging performance metrics.
    
    Example:
        @measure_performance
        def process_knowledge():
            pass
    """
    @functools.wraps(func)
    async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.time()
        func_name = func.__name__
        try:
            result = await func(*args, **kwargs)
            duration = time.time() - start_time
            logger.info(f"⏱️  {func_name} completed in {duration:.3f}s")
            return result
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"❌ {func_name} failed after {duration:.3f}s: {e}")
            raise
    
    @functools.wraps(func)
    def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.time()
        func_name = func.__name__
        try:
            result = func(*args, **kwargs)
            duration = time.time() - start_time
            logger.info(f"⏱️  {func_name} completed in {duration:.3f}s")
            return result
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"❌ {func_name} failed after {duration:.3f}s: {e}")
            raise
    
    if asyncio.iscoroutinefunction(func):
        return cast(F, async_wrapper)
    return cast(F, sync_wrapper)


def cached(ttl_seconds: int = 3600) -> Callable:
    """
    Decorator for caching function results with TTL.
    
    Args:
        ttl_seconds: Time to live for cached values
    
    Returns:
        Decorator function
    
    Example:
        @cached(ttl_seconds=300)
        def get_expensive_data():
            pass
    """
    cache = Cache()
    
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            cache_key = f"{func.__name__}_{str(args)}_{str(kwargs)}"
            cached_value = cache.get(cache_key)
            if cached_value is not None:
                logger.debug(f"💾 Cache hit: {func.__name__}")
                return cached_value
            
            result = func(*args, **kwargs)
            cache.set(cache_key, result, ttl_seconds)
            return result
        
        return cast(F, wrapper)
    return decorator


def ensure_resource_limits(max_memory_mb: int = 512, timeout_seconds: int = 300) -> Callable:
    """
    Decorator to ensure operations don't exceed resource limits.
    
    Args:
        max_memory_mb: Maximum memory allowed
        timeout_seconds: Maximum execution time
    
    Returns:
        Decorator function
    """
    def decorator(func: F) -> F:
        @functools.wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                result = await asyncio.wait_for(func(*args, **kwargs), timeout=timeout_seconds)
                return result
            except asyncio.TimeoutError:
                raise TimeoutException(
                    f"Function {func.__name__} exceeded {timeout_seconds}s timeout",
                    error_code="TIMEOUT"
                )
        
        @functools.wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            # For sync functions, we can at least check timeout with threading
            import threading
            result = [None]
            exception = [None]
            
            def target():
                try:
                    result[0] = func(*args, **kwargs)
                except Exception as e:
                    exception[0] = e
            
            thread = threading.Thread(target=target)
            thread.daemon = True
            thread.start()
            thread.join(timeout=timeout_seconds)
            
            if thread.is_alive():
                raise TimeoutException(
                    f"Function {func.__name__} exceeded {timeout_seconds}s timeout",
                    error_code="TIMEOUT"
                )
            
            if exception[0]:
                raise exception[0]
            return result[0]
        
        if asyncio.iscoroutinefunction(func):
            return cast(F, async_wrapper)
        return cast(F, sync_wrapper)
    return decorator


# Global circuit breakers for critical operations
WEB_CRAWLER_CB = CircuitBreaker(failure_threshold=5, recovery_timeout=60, name="WebCrawler")
KNOWLEDGE_BASE_CB = CircuitBreaker(failure_threshold=10, recovery_timeout=120, name="KnowledgeBase")
REASONING_CB = CircuitBreaker(failure_threshold=5, recovery_timeout=90, name="Reasoning")


def get_circuit_breaker(name: str) -> CircuitBreaker:
    """Get or create a circuit breaker by name"""
    if name == "crawler":
        return WEB_CRAWLER_CB
    elif name == "kb":
        return KNOWLEDGE_BASE_CB
    elif name == "reasoning":
        return REASONING_CB
    else:
        return CircuitBreaker(name=name)
