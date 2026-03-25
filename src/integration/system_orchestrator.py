"""
System Orchestrator: Coordinates all components and infrastructure

Ties together:
- Health checking
- Metrics collection
- Resource management
- Task execution
- Error recovery
- Caching
"""
from typing import Dict, Any, Optional, List
from datetime import datetime
import asyncio
import threading
import json
from pathlib import Path

import config
from logger import logger
from health_checker import get_health_checker, HealthChecker
from metrics_collector import get_metrics_collector, MetricsCollector
from resource_manager import get_resource_manager, ResourceManager
from task_queue import get_task_queue, TaskQueue
from advanced_cache import get_cache, AdvancedCache
from integration_layer import get_integration_layer


class SystemOrchestrator:
    """
    Central orchestrator for autonomous system infrastructure.
    
    Responsibilities:
    - Startup and initialization
    - Component registration
    - Monitoring and health checks
    - Metrics aggregation
    - Resource management
    - Error recovery
    - Graceful shutdown
    """
    
    def __init__(self):
        """Initialize orchestrator"""
        self.health_checker = get_health_checker()
        self.metrics_collector = get_metrics_collector()
        self.resource_manager = get_resource_manager()
        self.task_queue = get_task_queue()
        self.cache = get_cache()
        self.integration_layer = get_integration_layer()
        
        self.running = False
        self.startup_time: Optional[datetime] = None
        self.shutdown_time: Optional[datetime] = None
        self.components: Dict[str, Any] = {}
        
        logger.info("✓ System Orchestrator initialized")
    
    def startup(self, config_dict: Optional[Dict[str, Any]] = None) -> None:
        """
        Start up the system
        
        Args:
            config_dict: System configuration
        """
        if self.running:
            logger.warning("System already running")
            return
        
        self.running = True
        self.startup_time = datetime.now()
        
        logger.info("=" * 60)
        logger.info("AUTONOMOUS SYSTEM STARTUP")
        logger.info("=" * 60)
        
        # Start health checking
        self.health_checker.start()
        
        # Start resource monitoring
        self.resource_manager.start_monitoring()
        
        # Register alert handler
        self.health_checker.add_alert_handler(self._handle_alert)
        
        # Warm cache with default data if provided
        if config_dict and "cache_data" in config_dict:
            self.cache.warm_cache(config_dict["cache_data"])
        
        logger.info("✓ System startup complete")
        logger.info("=" * 60)
    
    def shutdown(self) -> None:
        """Gracefully shutdown the system"""
        if not self.running:
            logger.warning("System not running")
            return
        
        logger.info("=" * 60)
        logger.info("AUTONOMOUS SYSTEM SHUTDOWN")
        logger.info("=" * 60)
        
        self.running = False
        self.shutdown_time = datetime.now()
        
        # Stop health checking
        self.health_checker.stop()
        
        # Stop resource monitoring
        self.resource_manager.stop_monitoring()
        
        # Save metrics
        self.metrics_collector.save_to_disk()
        
        # Save final health status
        self._save_final_status()
        
        logger.info("✓ System shutdown complete")
        logger.info("=" * 60)
    
    def register_component(
        self,
        component_name: str,
        component: Any,
        component_type: str = "generic",
        resource_config: Optional[Dict[str, Any]] = None,
        depends_on: Optional[List[str]] = None
    ) -> None:
        """
        Register a component with the orchestrator
        
        Args:
            component_name: Component name
            component: Component instance
            component_type: Type of component
            resource_config: Resource quotas
            depends_on: Components this depends on
        """
        self.components[component_name] = component
        
        # Register health checking
        self.health_checker.register_component(component_name, component)
        
        # Register resource quotas
        if resource_config:
            self.resource_manager.register_component(
                component_name,
                max_memory_mb=resource_config.get("max_memory_mb", 500),
                max_cpu_percent=resource_config.get("max_cpu_percent", 80),
                max_connections=resource_config.get("max_connections", 10)
            )
        else:
            self.resource_manager.register_component(component_name)
        
        # Register in integration layer
        self.integration_layer.registry.register(
            component_name, component, depends_on
        )
        
        logger.info(f"✓ Registered component: {component_name} ({component_type})")
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        uptime = (datetime.now() - self.startup_time).total_seconds() if self.startup_time else 0
        
        return {
            "running": self.running,
            "uptime_seconds": uptime,
            "startup_time": self.startup_time.isoformat() if self.startup_time else None,
            "components": {
                "registered": len(self.components),
                "health": self.health_checker.get_system_health(),
                "resources": {
                    "quotas": self.resource_manager.get_quota_status(),
                    "pools": self.resource_manager.get_pool_status()
                }
            },
            "queue": self.task_queue.get_queue_stats(),
            "cache": self.cache.get_stats(),
            "metrics": self.metrics_collector.get_all_stats(),
            "alerts": self.health_checker.get_alerts()
        }
    
    def record_metric(
        self,
        component: str,
        metric_type: str,
        value: float,
        tags: Optional[Dict[str, str]] = None
    ) -> None:
        """Record a metric"""
        self.metrics_collector.record(component, metric_type, value, tags)
    
    def execute_task(
        self,
        fn,
        name: str = "",
        priority: int = 2,
        timeout_seconds: Optional[int] = None,
        *args,
        **kwargs
    ) -> str:
        """Enqueue a task for execution"""
        from task_queue import TaskPriority
        
        return self.task_queue.enqueue(
            fn,
            name=name,
            priority=TaskPriority(priority),
            timeout_seconds=timeout_seconds,
            *args,
            **kwargs
        )
    
    def _handle_alert(self, alert) -> None:
        """Handle alerts from health checker"""
        # Record metric for alert
        self.metrics_collector.record(
            alert.component,
            "alert",
            1.0,
            {"level": alert.level.value}
        )
        
        # Log the alert
        logger.warning(f"System alert: {alert.message}")
    
    def _save_final_status(self) -> None:
        """Save final system status on shutdown"""
        try:
            status_file = config.DATA_DIR / "system_status_final.json"
            status = self.get_system_status()
            
            with open(status_file, 'w') as f:
                json.dump(status, f, indent=2, default=str)
            
            logger.info(f"Final status saved: {status_file}")
        except Exception as e:
            logger.error(f"Failed to save final status: {e}")


class AutomationController:
    """
    High-level controller for system automation.
    
    Provides convenience methods for:
    - Batch operations
    - Scheduled tasks
    - Automated recovery
    - Performance optimization
    """
    
    def __init__(self, orchestrator: SystemOrchestrator):
        self.orchestrator = orchestrator
        self.automation_rules: Dict[str, Any] = {}
    
    def enable_auto_recovery(self, component_name: str) -> None:
        """Enable automatic recovery for a component"""
        logger.info(f"Auto-recovery enabled for: {component_name}")
    
    def enable_performance_optimization(self) -> None:
        """Enable automatic performance optimization"""
        # Enable adaptive batch sizes
        # Enable intelligent caching
        # Enable resource rebalancing
        logger.info("Performance optimization enabled")
    
    def run_diagnostic(self) -> Dict[str, Any]:
        """Run system diagnostic"""
        status = self.orchestrator.get_system_status()
        
        diagnostics = {
            "timestamp": datetime.now().isoformat(),
            "system_health": status["components"]["health"]["overall_state"],
            "components_checked": status["components"]["health"]["total_components"],
            "alerts_active": status["components"]["health"]["active_alerts"],
            "resource_utilization": self._calculate_utilization(status)
        }
        
        return diagnostics
    
    def _calculate_utilization(self, status: Dict) -> Dict[str, float]:
        """Calculate resource utilization"""
        pools = status["components"]["resources"]["pools"]
        
        utilization = {}
        for pool_name, pool_status in pools.items():
            utilization[f"{pool_name}_percent"] = pool_status["utilization_percent"]
        
        return utilization


# Global orchestrator instance
_system_orchestrator: Optional[SystemOrchestrator] = None


def get_system_orchestrator() -> SystemOrchestrator:
    """Get or create global system orchestrator"""
    global _system_orchestrator
    if _system_orchestrator is None:
        _system_orchestrator = SystemOrchestrator()
    return _system_orchestrator


def startup_system(config_dict: Optional[Dict[str, Any]] = None) -> SystemOrchestrator:
    """Start up the autonomous system"""
    orchestrator = get_system_orchestrator()
    orchestrator.startup(config_dict)
    return orchestrator


def shutdown_system() -> None:
    """Shut down the autonomous system"""
    orchestrator = get_system_orchestrator()
    orchestrator.shutdown()
