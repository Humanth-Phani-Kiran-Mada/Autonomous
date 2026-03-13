"""
Health Check and Monitoring System: Real-time component health tracking

Provides:
- Periodic health checks for all components
- Component state tracking (healthy, degraded, unhealthy)
- Automatic recovery triggers
- Alert generation
- Resource monitoring
"""
from typing import Dict, Any, List, Optional, Callable, Set
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
import asyncio
import time
import threading
from collections import defaultdict

import config
from logger import logger
from exceptions import AutonomousAIException


class ComponentState(str, Enum):
    """Component lifecycle states"""
    UNINITIALIZED = "uninitialized"
    INITIALIZING = "initializing"
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    RECOVERING = "recovering"
    SHUTTING_DOWN = "shutting_down"


class AlertLevel(str, Enum):
    """Alert severity levels"""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


@dataclass
class HealthMetric:
    """Single health measurement"""
    timestamp: datetime
    component: str
    response_time: float  # milliseconds
    success: bool
    error_message: Optional[str] = None
    resource_usage: Optional[Dict[str, float]] = None  # memory%, cpu%, etc.


@dataclass
class ComponentHealthStatus:
    """Health status of a component"""
    component_name: str
    state: ComponentState = ComponentState.UNINITIALIZED
    last_check: Optional[datetime] = None
    error_count: int = 0
    success_count: int = 0
    last_error: Optional[str] = None
    recovery_attempts: int = 0
    consecutive_failures: int = 0
    avg_response_time: float = 0.0
    uptime_seconds: float = 0.0
    started_at: datetime = field(default_factory=datetime.now)
    metrics_history: List[HealthMetric] = field(default_factory=list)
    
    @property
    def health_score(self) -> float:
        """Calculate health score (0-1) based on success rate"""
        total = self.error_count + self.success_count
        if total == 0:
            return 1.0
        return self.success_count / total
    
    @property
    def is_healthy(self) -> bool:
        """Check if component is healthy"""
        return self.state in (ComponentState.HEALTHY, ComponentState.DEGRADED)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "component": self.component_name,
            "state": self.state.value,
            "health_score": self.health_score,
            "success_rate": f"{self.health_score * 100:.1f}%",
            "error_count": self.error_count,
            "success_count": self.success_count,
            "consecutive_failures": self.consecutive_failures,
            "avg_response_time_ms": round(self.avg_response_time, 2),
            "uptime_seconds": round(self.uptime_seconds, 2),
            "last_error": self.last_error,
            "last_check": self.last_check.isoformat() if self.last_check else None,
            "recovery_attempts": self.recovery_attempts
        }


@dataclass
class Alert:
    """Health alert"""
    component: str
    level: AlertLevel
    message: str
    timestamp: datetime = field(default_factory=datetime.now)
    resolved_at: Optional[datetime] = None
    
    @property
    def is_active(self) -> bool:
        """Check if alert is still active"""
        return self.resolved_at is None


class HealthChecker:
    """
    Periodic health checker for system components.
    
    Features:
    - Real-time component state tracking
    - Automatic recovery triggers
    - Alert management
    - Health metrics collection
    - Resource monitoring
    """
    
    def __init__(self, check_interval: int = 10):
        """
        Initialize health checker
        
        Args:
            check_interval: Check interval in seconds
        """
        self.check_interval = check_interval
        self.components: Dict[str, Any] = {}
        self.health_status: Dict[str, ComponentHealthStatus] = {}
        self.alerts: List[Alert] = []
        self.active_alerts: Dict[str, Alert] = {}
        self.alert_handlers: List[Callable[[Alert], None]] = []
        self.recovery_handlers: Dict[str, Callable] = {}
        self.check_functions: Dict[str, Callable] = {}
        self.running = False
        self.check_thread: Optional[threading.Thread] = None
        self.metric_retention_hours = 24
        self.all_metrics: List[HealthMetric] = []
        
        logger.info("✓ Health Checker initialized")
    
    def register_component(
        self,
        name: str,
        component: Any,
        check_function: Optional[Callable] = None,
        recovery_function: Optional[Callable] = None
    ) -> None:
        """
        Register a component for health checking
        
        Args:
            name: Component name
            component: Component instance
            check_function: Custom health check function (optional)
            recovery_function: Recovery function if component unhealthy (optional)
        """
        self.components[name] = component
        self.health_status[name] = ComponentHealthStatus(name)
        
        if check_function:
            self.check_functions[name] = check_function
        
        if recovery_function:
            self.recovery_handlers[name] = recovery_function
        
        logger.info(f"✓ Registered component for health checks: {name}")
    
    def add_alert_handler(self, handler: Callable[[Alert], None]) -> None:
        """Add handler to be called when alerts are generated"""
        self.alert_handlers.append(handler)
        logger.debug(f"Added alert handler: {handler.__name__}")
    
    def start(self) -> None:
        """Start background health checking"""
        if self.running:
            logger.warning("Health checker already running")
            return
        
        self.running = True
        self.check_thread = threading.Thread(target=self._check_loop, daemon=True)
        self.check_thread.start()
        logger.info(f"✓ Health checker started (interval: {self.check_interval}s)")
    
    def stop(self) -> None:
        """Stop background health checking"""
        self.running = False
        if self.check_thread:
            self.check_thread.join(timeout=5)
        logger.info("Health checker stopped")
    
    def _check_loop(self) -> None:
        """Background loop for periodic health checks"""
        while self.running:
            try:
                self._perform_checks()
                time.sleep(self.check_interval)
            except Exception as e:
                logger.error(f"Error in health check loop: {e}")
                time.sleep(1)
    
    def _perform_checks(self) -> None:
        """Perform health checks on all components"""
        for component_name, component in self.components.items():
            try:
                self._check_single_component(component_name, component)
            except Exception as e:
                logger.error(f"Error checking component {component_name}: {e}")
    
    def _check_single_component(self, name: str, component: Any) -> None:
        """Check health of a single component"""
        status = self.health_status[name]
        start = time.time()
        
        try:
            # Run custom check function if available
            if name in self.check_functions:
                result = self.check_functions[name]()
            else:
                # Default: check for common methods
                result = self._default_check(component)
            
            response_time = (time.time() - start) * 1000  # Convert to ms
            
            # Record successful check
            metric = HealthMetric(
                timestamp=datetime.now(),
                component=name,
                response_time=response_time,
                success=True,
                resource_usage=self._get_resource_usage()
            )
            self.all_metrics.append(metric)
            status.metrics_history.append(metric)
            
            # Update status
            status.last_check = datetime.now()
            status.success_count += 1
            status.consecutive_failures = 0
            status.avg_response_time = (
                (status.avg_response_time * (status.success_count - 1) + response_time) /
                status.success_count
            )
            
            # Transition to healthy if was degraded/recovering
            if status.state in (ComponentState.DEGRADED, ComponentState.RECOVERING):
                status.state = ComponentState.HEALTHY
                self._resolve_alert(name)
                logger.info(f"✓ {name} recovered to HEALTHY")
            elif status.state == ComponentState.UNINITIALIZED:
                status.state = ComponentState.HEALTHY
            
        except Exception as e:
            response_time = (time.time() - start) * 1000
            
            # Record failed check
            metric = HealthMetric(
                timestamp=datetime.now(),
                component=name,
                response_time=response_time,
                success=False,
                error_message=str(e)
            )
            self.all_metrics.append(metric)
            status.metrics_history.append(metric)
            
            # Update status
            status.last_check = datetime.now()
            status.error_count += 1
            status.consecutive_failures += 1
            status.last_error = str(e)
            
            # Determine transition
            if status.consecutive_failures == 1:
                status.state = ComponentState.DEGRADED
                self._create_alert(name, AlertLevel.WARNING, 
                                  f"{name} degraded: {e}")
            elif status.consecutive_failures >= 3:
                status.state = ComponentState.UNHEALTHY
                self._create_alert(name, AlertLevel.CRITICAL,
                                  f"{name} unhealthy after {status.consecutive_failures} failures")
                
                # Attempt recovery
                if name in self.recovery_handlers:
                    logger.info(f"⚙️ Attempting recovery for {name}...")
                    status.state = ComponentState.RECOVERING
                    try:
                        self.recovery_handlers[name]()
                        status.recovery_attempts += 1
                        logger.info(f"✓ Recovery attempted for {name}")
                    except Exception as recovery_error:
                        logger.error(f"Recovery failed for {name}: {recovery_error}")
    
    def _default_check(self, component: Any) -> bool:
        """Default health check for components"""
        # Check for common healthy indicators
        if hasattr(component, 'is_healthy'):
            return component.is_healthy()
        
        if hasattr(component, 'get_statistics'):
            component.get_statistics()  # Should not raise
            return True
        
        return True  # Assume healthy if no checks available
    
    def _get_resource_usage(self) -> Dict[str, float]:
        """Get current system resource usage"""
        try:
            import psutil
            process = psutil.Process()
            return {
                "memory_percent": process.memory_percent(),
                "cpu_percent": process.cpu_percent(interval=0.1)
            }
        except ImportError:
            return {}
    
    def _create_alert(self, component: str, level: AlertLevel, message: str) -> None:
        """Create an alert for a component"""
        # Don't duplicate active alerts
        existing = self.active_alerts.get(component)
        if existing and existing.is_active:
            return
        
        alert = Alert(component=component, level=level, message=message)
        self.alerts.append(alert)
        self.active_alerts[component] = alert
        
        # Notify alert handlers
        for handler in self.alert_handlers:
            try:
                handler(alert)
            except Exception as e:
                logger.error(f"Error in alert handler: {e}")
        
        logger.warning(f"🚨 [{level.value.upper()}] {message}")
    
    def _resolve_alert(self, component: str) -> None:
        """Resolve active alert for a component"""
        if component in self.active_alerts:
            alert = self.active_alerts[component]
            if alert.is_active:
                alert.resolved_at = datetime.now()
                logger.info(f"✓ Alert resolved for {component}")
                del self.active_alerts[component]
    
    def get_component_health(self, component_name: str) -> Optional[ComponentHealthStatus]:
        """Get health status of specific component"""
        return self.health_status.get(component_name)
    
    def get_system_health(self) -> Dict[str, Any]:
        """Get overall system health"""
        components_status = {}
        unhealthy_count = 0
        degraded_count = 0
        
        for name, status in self.health_status.items():
            components_status[name] = status.to_dict()
            if status.state == ComponentState.UNHEALTHY:
                unhealthy_count += 1
            elif status.state == ComponentState.DEGRADED:
                degraded_count += 1
        
        overall_state = (
            ComponentState.UNHEALTHY if unhealthy_count > 0
            else ComponentState.DEGRADED if degraded_count > 0
            else ComponentState.HEALTHY
        )
        
        return {
            "overall_state": overall_state.value,
            "healthy_count": len(self.health_status) - unhealthy_count - degraded_count,
            "degraded_count": degraded_count,
            "unhealthy_count": unhealthy_count,
            "total_components": len(self.health_status),
            "active_alerts": len(self.active_alerts),
            "components": components_status,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_alerts(self, include_resolved: bool = False) -> List[Dict[str, Any]]:
        """Get alerts"""
        alerts = []
        for alert in self.alerts:
            if include_resolved or alert.is_active:
                alerts.append({
                    "component": alert.component,
                    "level": alert.level.value,
                    "message": alert.message,
                    "timestamp": alert.timestamp.isoformat(),
                    "resolved_at": alert.resolved_at.isoformat() if alert.resolved_at else None,
                    "active": alert.is_active
                })
        return alerts
    
    def _cleanup_old_metrics(self) -> None:
        """Remove old metrics exceeding retention period"""
        cutoff = datetime.now() - timedelta(hours=self.metric_retention_hours)
        initial_count = len(self.all_metrics)
        
        self.all_metrics = [m for m in self.all_metrics if m.timestamp > cutoff]
        
        removed_count = initial_count - len(self.all_metrics)
        if removed_count > 0:
            logger.debug(f"Cleaned up {removed_count} old health metrics")


# Global health checker instance
_health_checker: Optional[HealthChecker] = None


def get_health_checker(check_interval: int = 10) -> HealthChecker:
    """Get or create global health checker"""
    global _health_checker
    if _health_checker is None:
        _health_checker = HealthChecker(check_interval)
    return _health_checker
