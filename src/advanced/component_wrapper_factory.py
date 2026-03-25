"""
Phase 2: Component Wrapper Factory

Wraps components with automatic monitoring, tracing, caching, and performance optimization.
Provides transparent enhancement of Phase 1 components with middleware capabilities.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Any, Callable, Dict, List, Optional, TypeVar, Generic
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from functools import wraps
import asyncio
import time
import uuid

from src.logger import logger
from src.monitoring_engine import monitoring_engine
from src.integration_layer import integration_layer

T = TypeVar('T')


@dataclass
class ComponentMetrics:
    """Metrics for a wrapped component"""
    component_id: str
    call_count: int = 0
    error_count: int = 0
    total_latency: float = 0.0
    min_latency: float = float('inf')
    max_latency: float = 0.0
    cache_hits: int = 0
    cache_misses: int = 0
    last_error: Optional[str] = None
    last_success: Optional[datetime] = None
    last_error_time: Optional[datetime] = None
    avg_latency: float = 0.0
    success_rate: float = 1.0
    
    def update_call(self, latency: float, success: bool = True, cache_hit: bool = False):
        """Update metrics after a call"""
        self.call_count += 1
        
        if success:
            self.total_latency += latency
            self.avg_latency = self.total_latency / self.call_count
            self.min_latency = min(self.min_latency, latency)
            self.max_latency = max(self.max_latency, latency)
            self.last_success = datetime.now()
        else:
            self.error_count += 1
        
        if cache_hit:
            self.cache_hits += 1
        else:
            self.cache_misses += 1
        
        self.success_rate = (self.call_count - self.error_count) / self.call_count if self.call_count > 0 else 1.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "component_id": self.component_id,
            "call_count": self.call_count,
            "error_count": self.error_count,
            "avg_latency": self.avg_latency,
            "min_latency": self.min_latency if self.min_latency != float('inf') else 0,
            "max_latency": self.max_latency,
            "cache_hits": self.cache_hits,
            "cache_misses": self.cache_misses,
            "success_rate": self.success_rate,
            "last_error": self.last_error,
            "last_success": self.last_success.isoformat() if self.last_success else None,
        }


@dataclass
class CallContext:
    """Context for a wrapped component call"""
    call_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    component_id: str = ""
    method_name: str = ""
    start_time: float = field(default_factory=time.time)
    end_time: Optional[float] = None
    latency: float = 0.0
    success: bool = True
    error: Optional[str] = None
    cache_hit: bool = False
    parent_call_id: Optional[str] = None
    depth: int = 0
    
    def complete(self):
        """Mark call as complete"""
        self.end_time = time.time()
        self.latency = (self.end_time - self.start_time) * 1000
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "call_id": self.call_id,
            "component_id": self.component_id,
            "method_name": self.method_name,
            "latency_ms": self.latency,
            "success": self.success,
            "error": self.error,
            "cache_hit": self.cache_hit,
            "depth": self.depth,
        }


class ComponentWrapper(Generic[T]):
    """Wraps a component with monitoring, caching, and tracing"""
    
    def __init__(self, 
                 component: T,
                 component_id: str,
                 enable_caching: bool = True,
                 cache_ttl_seconds: int = 300,
                 enable_tracing: bool = True,
                 enable_monitoring: bool = True):
        
        self.component = component
        self.component_id = component_id
        self.enable_caching = enable_caching
        self.cache_ttl_seconds = cache_ttl_seconds
        self.enable_tracing = enable_tracing
        self.enable_monitoring = enable_monitoring
        
        self._cache: Dict[str, tuple] = {}  # (value, expiry_time)
        self._metrics = ComponentMetrics(component_id=component_id)
        self._call_stack: List[CallContext] = []
        self._current_context: Optional[CallContext] = None
        
        logger.info(f"✓ Wrapped component: {component_id}")
    
    def _cache_key(self, method_name: str, args: tuple, kwargs: dict) -> str:
        """Generate cache key"""
        # Simple cache key generation
        args_str = str(args) if args else ""
        kwargs_str = str(kwargs) if kwargs else ""
        return f"{self.component_id}:{method_name}:{args_str}:{kwargs_str}"
    
    def _get_cached(self, key: str) -> Optional[Any]:
        """Get value from cache if not expired"""
        if key in self._cache:
            value, expiry = self._cache[key]
            if time.time() < expiry:
                self._metrics.update_call(0, success=True, cache_hit=True)
                return value
            else:
                del self._cache[key]
        
        return None
    
    def _set_cached(self, key: str, value: Any):
        """Set value in cache with TTL"""
        expiry = time.time() + self.cache_ttl_seconds
        self._cache[key] = (value, expiry)
    
    def _start_tracing(self, method_name: str) -> CallContext:
        """Start tracing a call"""
        depth = len(self._call_stack)
        
        context = CallContext(
            component_id=self.component_id,
            method_name=method_name,
            parent_call_id=self._current_context.call_id if self._current_context else None,
            depth=depth
        )
        
        self._call_stack.append(context)
        old_context = self._current_context
        self._current_context = context
        
        if self.enable_tracing:
            logger.debug(f"[TRACE] {'  ' * depth}→ {self.component_id}.{method_name}")
        
        return context
    
    def _end_tracing(self, context: CallContext, success: bool = True, error: str = None):
        """End tracing a call"""
        context.complete()
        context.success = success
        context.error = error
        
        if self.enable_tracing:
            status = "✓" if success else "✗"
            logger.debug(f"[TRACE] {'  ' * context.depth}← {self.component_id}.{context.method_name} {status} {context.latency:.2f}ms")
        
        if self.enable_monitoring:
            self._metrics.update_call(context.latency, success=success, cache_hit=context.cache_hit)
            monitoring_engine.record_metric(
                f"components.{self.component_id}.{context.method_name}_latency",
                context.latency
            )
        
        self._call_stack.pop()
        if self._call_stack:
            self._current_context = self._call_stack[-1]
        else:
            self._current_context = None
    
    def wrap_method(self, method_name: str):
        """Decorator to wrap a method"""
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                context = self._start_tracing(method_name)
                
                try:
                    # Try cache first
                    if self.enable_caching and func.__name__ not in ['create', 'update', 'delete']:
                        cache_key = self._cache_key(method_name, args, kwargs)
                        cached = self._get_cached(cache_key)
                        if cached is not None:
                            context.cache_hit = True
                            self._end_tracing(context, success=True)
                            return cached
                    
                    # Call wrapped function
                    result = func(*args, **kwargs)
                    
                    # Cache result
                    if self.enable_caching and func.__name__ not in ['create', 'update', 'delete']:
                        cache_key = self._cache_key(method_name, args, kwargs)
                        self._set_cached(cache_key, result)
                    
                    self._end_tracing(context, success=True)
                    return result
                
                except Exception as e:
                    self._metrics.last_error = str(e)
                    self._metrics.last_error_time = datetime.now()
                    self._end_tracing(context, success=False, error=str(e))
                    raise
            
            return wrapper
        
        return decorator
    
    async def wrap_async_method(self, method_name: str):
        """Decorator to wrap async methods"""
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            async def wrapper(*args, **kwargs):
                context = self._start_tracing(method_name)
                
                try:
                    # Try cache first
                    if self.enable_caching and func.__name__ not in ['create', 'update', 'delete']:
                        cache_key = self._cache_key(method_name, args, kwargs)
                        cached = self._get_cached(cache_key)
                        if cached is not None:
                            context.cache_hit = True
                            self._end_tracing(context, success=True)
                            return cached
                    
                    # Call wrapped function
                    result = await func(*args, **kwargs)
                    
                    # Cache result
                    if self.enable_caching and func.__name__ not in ['create', 'update', 'delete']:
                        cache_key = self._cache_key(method_name, args, kwargs)
                        self._set_cached(cache_key, result)
                    
                    self._end_tracing(context, success=True)
                    return result
                
                except Exception as e:
                    self._metrics.last_error = str(e)
                    self._metrics.last_error_time = datetime.now()
                    self._end_tracing(context, success=False, error=str(e))
                    raise
            
            return wrapper
        
        return decorator
    
    def __getattr__(self, name: str) -> Any:
        """Proxy attribute access to wrapped component"""
        attr = getattr(self.component, name)
        
        # If it's a callable, wrap it with tracing
        if callable(attr):
            @wraps(attr)
            def method_wrapper(*args, **kwargs):
                context = self._start_tracing(name)
                
                try:
                    result = attr(*args, **kwargs)
                    self._end_tracing(context, success=True)
                    return result
                except Exception as e:
                    self._metrics.last_error = str(e)
                    self._metrics.last_error_time = datetime.now()
                    self._end_tracing(context, success=False, error=str(e))
                    raise
            
            return method_wrapper
        
        return attr
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get component metrics"""
        return self._metrics.to_dict()
    
    def clear_cache(self):
        """Clear component cache"""
        self._cache.clear()
        logger.debug(f"Cache cleared for {self.component_id}")
    
    def get_call_stack(self) -> List[Dict[str, Any]]:
        """Get current call stack"""
        return [ctx.to_dict() for ctx in self._call_stack]


class ComponentWrapperFactory:
    """Factory for creating wrapped components"""
    
    def __init__(self):
        self.wrapped_components: Dict[str, ComponentWrapper] = {}
        self.wrapper_stats: Dict[str, ComponentMetrics] = {}
        
        logger.info("✓ Component Wrapper Factory initialized")
    
    def wrap_component(self,
                      component: Any,
                      component_id: str,
                      enable_caching: bool = True,
                      cache_ttl: int = 300,
                      enable_tracing: bool = True) -> ComponentWrapper:
        """Wrap a component with monitoring and tracing"""
        
        wrapper = ComponentWrapper(
            component=component,
            component_id=component_id,
            enable_caching=enable_caching,
            cache_ttl_seconds=cache_ttl,
            enable_tracing=enable_tracing
        )
        
        self.wrapped_components[component_id] = wrapper
        self.wrapper_stats[component_id] = wrapper._metrics
        
        logger.info(f"✓ Component {component_id} wrapped")
        
        return wrapper
    
    def wrap_batch(self, components: Dict[str, Any]) -> Dict[str, ComponentWrapper]:
        """Wrap multiple components at once"""
        wrapped = {}
        
        for component_id, component in components.items():
            wrapped[component_id] = self.wrap_component(component, component_id)
        
        logger.info(f"✓ Wrapped {len(wrapped)} components")
        
        return wrapped
    
    def get_component_metrics(self, component_id: str) -> Optional[Dict[str, Any]]:
        """Get metrics for a wrapped component"""
        if component_id in self.wrapped_components:
            return self.wrapped_components[component_id].get_metrics()
        
        return None
    
    def get_all_metrics(self) -> Dict[str, Dict[str, Any]]:
        """Get metrics for all wrapped components"""
        return {
            comp_id: wrapper.get_metrics()
            for comp_id, wrapper in self.wrapped_components.items()
        }
    
    def clear_all_caches(self):
        """Clear caches for all components"""
        for wrapper in self.wrapped_components.values():
            wrapper.clear_cache()
        
        logger.info("All component caches cleared")
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get health status of all wrapped components"""
        health = {}
        
        for comp_id, wrapper in self.wrapped_components.items():
            metrics = wrapper.get_metrics()
            
            # Determine health based on success rate and latency
            status = "healthy"
            if metrics['success_rate'] < 0.9:
                status = "degraded"
            elif metrics['success_rate'] < 0.7:
                status = "unhealthy"
            
            if metrics['avg_latency'] > 5000:  # 5 seconds
                status = "slow"
            
            health[comp_id] = {
                "status": status,
                "success_rate": metrics['success_rate'],
                "avg_latency": metrics['avg_latency'],
                "error_count": metrics['error_count'],
                "last_error": metrics['last_error']
            }
        
        return health
    
    def print_summary(self):
        """Print summary of wrapped components"""
        logger.info("\n" + "="*80)
        logger.info("COMPONENT WRAPPER FACTORY SUMMARY")
        logger.info("="*80)
        
        all_metrics = self.get_all_metrics()
        
        for comp_id, metrics in all_metrics.items():
            logger.info(f"\n{comp_id}:")
            logger.info(f"  Calls: {metrics['call_count']}")
            logger.info(f"  Avg Latency: {metrics['avg_latency']:.2f}ms")
            logger.info(f"  Success Rate: {metrics['success_rate']:.1%}")
            logger.info(f"  Cache Hits: {metrics['cache_hits']}")


# Global factory instance
component_wrapper_factory = ComponentWrapperFactory()


def get_component_wrapper_factory() -> ComponentWrapperFactory:
    """Get the global component wrapper factory"""
    return component_wrapper_factory
