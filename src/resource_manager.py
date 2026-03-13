"""
Resource Manager: Unified resource allocation and management

Provides:
- Memory pooling and allocation
- CPU quota management
- Connection pooling
- Resource cleanup and garbage collection
- Resource usage monitoring
"""
from typing import Dict, Optional, Any, List, Set
from dataclasses import dataclass
from datetime import datetime
import gc
import psutil
import threading
from collections import defaultdict

import config
from logger import logger
from exceptions import AutonomousAIException


@dataclass
class ResourceQuota:
    """Resource quota for a component"""
    component_name: str
    max_memory_mb: float
    max_cpu_percent: float = 80.0
    max_connections: int = 10
    current_memory_mb: float = 0.0
    current_cpu_percent: float = 0.0
    current_connections: int = 0


@dataclass
class ResourcePool:
    """Managed resource pool"""
    resource_type: str  # memory, connection, etc.
    capacity: int
    allocated: int = 0
    available: int = 0
    
    def acquire(self, amount: int = 1) -> bool:
        """Try to acquire resources"""
        if self.available >= amount:
            self.allocated += amount
            self.available -= amount
            return True
        return False
    
    def release(self, amount: int = 1) -> None:
        """Release resources back to pool"""
        self.allocated = max(0, self.allocated - amount)
        self.available = self.capacity - self.allocated


class ResourceManager:
    """
    Manages system resources across components.
    
    Features:
    - Per-component resource quotas
    - Resource pooling (memory, connections)
    - Usage monitoring
    - Automatic cleanup
    - Resource exhaustion prevention
    """
    
    def __init__(self, check_interval: int = 30):
        """
        Initialize resource manager
        
        Args:
            check_interval: Resource check interval (seconds)
        """
        self.quotas: Dict[str, ResourceQuota] = {}
        self.pools: Dict[str, ResourcePool] = {}
        self.check_interval = check_interval
        self.running = False
        self.check_thread: Optional[threading.Thread] = None
        self.violations: List[Dict[str, Any]] = []
        
        # Default pools
        self.pools["memory"] = ResourcePool("memory", 4000)  # MB
        self.pools["connections"] = ResourcePool("connections", 100)
        
        # Process for monitoring
        self.process = psutil.Process()
        
        logger.info("✓ Resource Manager initialized")
    
    def register_component(
        self,
        component_name: str,
        max_memory_mb: float = 500.0,
        max_cpu_percent: float = 80.0,
        max_connections: int = 10
    ) -> None:
        """
        Register component resource quotas
        
        Args:
            component_name: Component name
            max_memory_mb: Maximum memory in MB
            max_cpu_percent: Maximum CPU percentage
            max_connections: Maximum concurrent connections
        """
        quota = ResourceQuota(
            component_name=component_name,
            max_memory_mb=max_memory_mb,
            max_cpu_percent=max_cpu_percent,
            max_connections=max_connections
        )
        self.quotas[component_name] = quota
        logger.info(f"✓ Registered component resource quota: {component_name}")
    
    def allocate_memory(self, component_name: str, size_mb: float) -> bool:
        """
        Allocate memory for a component
        
        Args:
            component_name: Component name
            size_mb: Size in MB
        
        Returns:
            True if allocated successfully
        """
        quota = self.quotas.get(component_name)
        
        if not quota:
            raise AutonomousAIException(
                f"Component {component_name} not registered",
                error_code="COMPONENT_NOT_REGISTERED"
            )
        
        # Check quota
        if quota.current_memory_mb + size_mb > quota.max_memory_mb:
            logger.warning(
                f"Memory quota exceeded for {component_name}: "
                f"{quota.current_memory_mb + size_mb} > {quota.max_memory_mb}"
            )
            return False
        
        # Check pool
        pool = self.pools["memory"]
        if not pool.acquire(int(size_mb)):
            logger.warning(f"Memory pool exhausted")
            return False
        
        quota.current_memory_mb += size_mb
        logger.debug(f"Allocated {size_mb}MB to {component_name}")
        return True
    
    def release_memory(self, component_name: str, size_mb: float) -> None:
        """Release allocated memory"""
        quota = self.quotas.get(component_name)
        if quota:
            quota.current_memory_mb = max(0, quota.current_memory_mb - size_mb)
            pool = self.pools["memory"]
            pool.release(int(size_mb))
    
    def allocate_connection(self, component_name: str) -> bool:
        """Allocate a connection slot"""
        quota = self.quotas.get(component_name)
        
        if not quota:
            return False
        
        if quota.current_connections >= quota.max_connections:
            logger.warning(
                f"Connection quota exceeded for {component_name}: "
                f"{quota.current_connections} >= {quota.max_connections}"
            )
            return False
        
        pool = self.pools["connections"]
        if not pool.acquire(1):
            logger.warning("Connection pool exhausted")
            return False
        
        quota.current_connections += 1
        return True
    
    def release_connection(self, component_name: str) -> None:
        """Release a connection slot"""
        quota = self.quotas.get(component_name)
        if quota:
            quota.current_connections = max(0, quota.current_connections - 1)
            pool = self.pools["connections"]
            pool.release(1)
    
    def check_quotas(self) -> Dict[str, List[str]]:
        """
        Check resource quotas for all components
        
        Returns:
            Dictionary of violations per component
        """
        violations = defaultdict(list)
        
        for component, quota in self.quotas.items():
            # Check memory
            if quota.current_memory_mb > quota.max_memory_mb * 0.9:
                violations[component].append(
                    f"Memory near limit: {quota.current_memory_mb:.1f}/"
                    f"{quota.max_memory_mb:.1f} MB"
                )
            
            # Check connections
            if quota.current_connections > quota.max_connections * 0.8:
                violations[component].append(
                    f"Connections near limit: {quota.current_connections}/"
                    f"{quota.max_connections}"
                )
        
        return violations
    
    def get_system_resources(self) -> Dict[str, Any]:
        """Get current system resource usage"""
        try:
            memory_info = self.process.memory_info()
            cpu_percent = self.process.cpu_percent(interval=0.1)
            
            return {
                "process_rss_mb": memory_info.rss / (1024 * 1024),
                "process_vms_mb": memory_info.vms / (1024 * 1024),
                "process_cpu_percent": cpu_percent,
                "system_memory_available_mb": psutil.virtual_memory().available / (1024 * 1024),
                "system_cpu_percent": psutil.cpu_percent(interval=0.1)
            }
        except Exception as e:
            logger.error(f"Failed to get resource usage: {e}")
            return {}
    
    def get_pool_status(self) -> Dict[str, Dict[str, int]]:
        """Get status of all resource pools"""
        status = {}
        for pool_name, pool in self.pools.items():
            status[pool_name] = {
                "total": pool.capacity,
                "allocated": pool.allocated,
                "available": pool.available,
                "utilization_percent": int((pool.allocated / pool.capacity * 100))
            }
        return status
    
    def get_quota_status(self) -> Dict[str, Dict[str, Any]]:
        """Get quota status for all components"""
        status = {}
        for component, quota in self.quotas.items():
            status[component] = {
                "memory_mb": {
                    "used": quota.current_memory_mb,
                    "max": quota.max_memory_mb,
                    "utilization_percent": int(
                        (quota.current_memory_mb / quota.max_memory_mb * 100)
                    )
                },
                "connections": {
                    "used": quota.current_connections,
                    "max": quota.max_connections,
                    "utilization_percent": int(
                        (quota.current_connections / quota.max_connections * 100)
                    )
                }
            }
        return status
    
    def cleanup(self) -> None:
        """Perform garbage collection and cleanup"""
        gc.collect()
        logger.debug("Resource cleanup performed")
    
    def start_monitoring(self) -> None:
        """Start background resource monitoring"""
        if self.running:
            logger.warning("Resource monitoring already running")
            return
        
        self.running = True
        self.check_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.check_thread.start()
        logger.info("✓ Resource monitoring started")
    
    def stop_monitoring(self) -> None:
        """Stop background resource monitoring"""
        self.running = False
        if self.check_thread:
            self.check_thread.join(timeout=5)
        logger.info("Resource monitoring stopped")
    
    def _monitor_loop(self) -> None:
        """Background monitoring loop"""
        import time
        while self.running:
            try:
                violations = self.check_quotas()
                for component, violation_list in violations.items():
                    for violation in violation_list:
                        logger.warning(f"⚠️ Resource warning: {component} - {violation}")
                
                time.sleep(self.check_interval)
            except Exception as e:
                logger.error(f"Error in resource monitoring: {e}")
                time.sleep(1)


# Global resource manager instance
_resource_manager: Optional[ResourceManager] = None


def get_resource_manager() -> ResourceManager:
    """Get or create global resource manager"""
    global _resource_manager
    if _resource_manager is None:
        _resource_manager = ResourceManager()
    return _resource_manager
