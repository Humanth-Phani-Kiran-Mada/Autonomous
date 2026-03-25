"""
Advanced Caching System: Multi-level intelligent caching

Provides:
- L1 in-memory cache with LRU eviction
- TTL-based expiration
- Automatic cache warming
- Cache invalidation strategies
- Cache statistics and diagnostics
"""
from typing import Any, Dict, Optional, Callable, List, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from collections import OrderedDict
import hashlib
import json

import config
from logger import logger


@dataclass
class CacheEntry:
    """Single cache entry"""
    key: str
    value: Any
    created_at: datetime
    accessed_at: datetime
    ttl_seconds: Optional[int]
    hit_count: int = 0
    
    @property
    def is_expired(self) -> bool:
        """Check if entry has expired"""
        if self.ttl_seconds is None:
            return False
        
        age = (datetime.now() - self.created_at).total_seconds()
        return age > self.ttl_seconds
    
    def update_access(self) -> None:
        """Update last access time"""
        self.accessed_at = datetime.now()
        self.hit_count += 1


class AdvancedCache:
    """
    Multi-level intelligent cache system.
    
    Features:
    - LRU eviction policy
    - TTL-based expiration
    - Cache statistics
    - Key namespace support
    - Cache warming
    """
    
    def __init__(
        self,
        max_size: int = 1000,
        default_ttl_seconds: Optional[int] = 3600,
        eviction_policy: str = "lru"
    ):
        """
        Initialize cache
        
        Args:
            max_size: Maximum cache entries
            default_ttl_seconds: Default time-to-live
            eviction_policy: "lru" (least recently used) or "lfu" (least frequently used)
        """
        self.max_size = max_size
        self.default_ttl_seconds = default_ttl_seconds
        self.eviction_policy = eviction_policy
        
        self.store: Dict[str, CacheEntry] = {}
        self.access_order: OrderedDict = OrderedDict()  # For LRU tracking
        
        self.stats = {
            "hits": 0,
            "misses": 0,
            "evictions": 0,
            "expirations": 0,
            "updates": 0
        }
        
        logger.info(f"✓ Advanced Cache initialized (size: {max_size})")
    
    def get(self, key: str, namespace: str = "default") -> Optional[Any]:
        """
        Get value from cache
        
        Args:
            key: Cache key
            namespace: Cache namespace
        
        Returns:
            Cached value or None
        """
        full_key = self._make_key(key, namespace)
        
        entry = self.store.get(full_key)
        
        if entry is None:
            self.stats["misses"] += 1
            return None
        
        if entry.is_expired:
            self.stats["expirations"] += 1
            del self.store[full_key]
            return None
        
        # Update access time
        entry.update_access()
        self.access_order.move_to_end(full_key)
        self.stats["hits"] += 1
        
        return entry.value
    
    def set(
        self,
        key: str,
        value: Any,
        ttl_seconds: Optional[int] = None,
        namespace: str = "default"
    ) -> None:
        """
        Set value in cache
        
        Args:
            key: Cache key
            value: Cache value
            ttl_seconds: Time-to-live (uses default if None)
            namespace: Cache namespace
        """
        full_key = self._make_key(key, namespace)
        ttl = ttl_seconds if ttl_seconds is not None else self.default_ttl_seconds
        
        now = datetime.now()
        entry = CacheEntry(
            key=full_key,
            value=value,
            created_at=now,
            accessed_at=now,
            ttl_seconds=ttl
        )
        
        # Check if new entry would exceed capacity
        if full_key not in self.store and len(self.store) >= self.max_size:
            self._evict()
        
        self.store[full_key] = entry
        self.access_order[full_key] = entry
        self.stats["updates"] += 1
        
        logger.debug(f"Cached: {full_key} (ttl: {ttl}s)")
    
    def delete(self, key: str, namespace: str = "default") -> None:
        """Delete cache entry"""
        full_key = self._make_key(key, namespace)
        
        if full_key in self.store:
            del self.store[full_key]
            del self.access_order[full_key]
    
    def clear(self, namespace: str = "") -> int:
        """
        Clear cache entries
        
        Args:
            namespace: Clear only this namespace (empty for all)
        
        Returns:
            Number of entries cleared
        """
        if not namespace:
            initial_count = len(self.store)
            self.store.clear()
            self.access_order.clear()
            return initial_count
        
        prefix = f"{namespace}:"
        keys_to_delete = [k for k in self.store if k.startswith(prefix)]
        
        for key in keys_to_delete:
            del self.store[key]
            del self.access_order[key]
        
        return len(keys_to_delete)
    
    def _evict(self) -> None:
        """Evict entry based on policy"""
        if not self.store:
            return
        
        if self.eviction_policy == "lru":
            # Evict least recently used
            evict_key = next(iter(self.access_order))
        else:
            # Evict least frequently used
            evict_key = min(
                self.store.keys(),
                key=lambda k: self.store[k].hit_count
            )
        
        del self.store[evict_key]
        del self.access_order[evict_key]
        self.stats["evictions"] += 1
        logger.debug(f"Evicted cache entry: {evict_key}")
    
    def _make_key(self, key: str, namespace: str) -> str:
        """Create full cache key with namespace"""
        return f"{namespace}:{key}"
    
    def warm_cache(
        self,
        data: Dict[str, Any],
        namespace: str = "default",
        ttl_seconds: Optional[int] = None
    ) -> None:
        """
        Warm cache with initial data
        
        Args:
            data: Dictionary of key-value pairs
            namespace: Cache namespace
            ttl_seconds: TTL for all entries
        """
        for key, value in data.items():
            self.set(key, value, ttl_seconds, namespace)
        
        logger.info(f"Cache warmed with {len(data)} entries ({namespace})")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        total_requests = self.stats["hits"] + self.stats["misses"]
        hit_rate = (
            (self.stats["hits"] / total_requests * 100)
            if total_requests > 0
            else 0
        )
        
        return {
            "size": len(self.store),
            "max_size": self.max_size,
            "utilization_percent": int((len(self.store) / self.max_size * 100)),
            "hits": self.stats["hits"],
            "misses": self.stats["misses"],
            "hit_rate_percent": hit_rate,
            "evictions": self.stats["evictions"],
            "expirations": self.stats["expirations"],
            "updates": self.stats["updates"]
        }
    
    def get_entry_info(self, key: str, namespace: str = "default") -> Optional[Dict[str, Any]]:
        """Get detailed info about a cache entry"""
        full_key = self._make_key(key, namespace)
        entry = self.store.get(full_key)
        
        if not entry:
            return None
        
        age = (datetime.now() - entry.created_at).total_seconds()
        
        return {
            "key": key,
            "namespace": namespace,
            "age_seconds": age,
            "ttl_seconds": entry.ttl_seconds,
            "is_expired": entry.is_expired,
            "hit_count": entry.hit_count,
            "created_at": entry.created_at.isoformat(),
            "accessed_at": entry.accessed_at.isoformat()
        }
    
    def cleanup_expired(self) -> int:
        """Remove all expired entries"""
        expired_keys = [
            key for key, entry in self.store.items()
            if entry.is_expired
        ]
        
        for key in expired_keys:
            del self.store[key]
            del self.access_order[key]
            self.stats["expirations"] += 1
        
        if expired_keys:
            logger.debug(f"Cleaned up {len(expired_keys)} expired cache entries")
        
        return len(expired_keys)


class ConfigValidator:
    """Validates system configuration"""
    
    @staticmethod
    def validate_component_config(config_dict: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Validate component configuration
        
        Args:
            config_dict: Configuration dictionary
        
        Returns:
            (is_valid, list_of_errors)
        """
        errors = []
        
        # Check required fields
        required_fields = ["name", "type"]
        for field in required_fields:
            if field not in config_dict:
                errors.append(f"Missing required field: {field}")
        
        # Validate resource limits
        if "resource_limits" in config_dict:
            limits = config_dict["resource_limits"]
            if "memory_mb" in limits and limits["memory_mb"] <= 0:
                errors.append("memory_mb must be positive")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_system_config(config_dict: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Validate full system configuration
        
        Args:
            config_dict: Configuration dictionary
        
        Returns:
            (is_valid, list_of_errors)
        """
        errors = []
        
        # Check for minimum required components
        required_components = [
            "knowledge_base", "memory_manager", "learning_engine"
        ]
        
        components = config_dict.get("components", [])
        component_names = [c.get("name") for c in components]
        
        for required in required_components:
            if required not in component_names:
                errors.append(f"Missing required component: {required}")
        
        return len(errors) == 0, errors


# Global cache instance
_cache: Optional[AdvancedCache] = None


def get_cache(max_size: int = 1000) -> AdvancedCache:
    """Get or create global cache"""
    global _cache
    if _cache is None:
        _cache = AdvancedCache(max_size)
    return _cache
