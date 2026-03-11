"""
Monitoring Engine - Comprehensive Real-Time Metrics Collection

Tracks 50+ KPIs across all autonomous system components including capability
levels, learning effectiveness, goal fulfillment, error recovery, memory
preservation, reasoning quality, and introspection depth.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from collections import defaultdict, deque
import json
from pathlib import Path
import config
from .logger import logger


class MetricPoint:
    """Single metric data point"""
    
    def __init__(self, name: str, value: float, timestamp: datetime = None,
                 component: str = "", tags: Dict[str, str] = None):
        self.name = name
        self.value = value
        self.timestamp = timestamp or datetime.now()
        self.component = component
        self.tags = tags or {}
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "value": self.value,
            "timestamp": self.timestamp.isoformat(),
            "component": self.component,
            "tags": self.tags
        }


class MetricsSeries:
    """Time series for a metric"""
    
    def __init__(self, name: str, max_points: int = 1000):
        self.name = name
        self.points: deque = deque(maxlen=max_points)
        self.current_value = 0.0
        self.min_value = float('inf')
        self.max_value = float('-inf')
        self.sum_value = 0.0
        self.count = 0
    
    def add(self, value: float, timestamp: datetime = None):
        """Add a data point"""
        point = MetricPoint(self.name, value, timestamp)
        self.points.append(point)
        self.current_value = value
        self.min_value = min(self.min_value, value)
        self.max_value = max(self.max_value, value)
        self.sum_value += value
        self.count += 1
    
    def get_average(self) -> float:
        """Get average value"""
        if not self.points:
            return 0.0
        return self.sum_value / self.count
    
    def get_trend(self) -> str:
        """Get trend: 'up', 'down', 'stable'"""
        if len(self.points) < 2:
            return "stable"
        
        recent = list(self.points)[-10:]
        start_avg = sum(p.value for p in recent[:5]) / 5
        end_avg = sum(p.value for p in recent[5:]) / 5
        
        diff = end_avg - start_avg
        if abs(diff) < 0.01:
            return "stable"
        return "up" if diff > 0 else "down"
    
    def get_summary(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "current": self.current_value,
            "average": self.get_average(),
            "min": self.min_value,
            "max": self.max_value,
            "count": self.count,
            "trend": self.get_trend(),
            "history_size": len(self.points)
        }


class MonitoringEngine:
    """Central metrics collection and monitoring system"""
    
    def __init__(self):
        self.metrics: Dict[str, MetricsSeries] = {}
        self.alerts: List[Dict[str, Any]] = []
        self.max_alerts = 100
        self.component_health: Dict[str, str] = {}
        self.persistence_file = config.DATA_DIR / "monitoring_metrics.json"
        self.last_save = datetime.now()
        self.save_interval = timedelta(minutes=5)
        
        # Initialize core metric categories
        self._initialize_metrics()
    
    def _initialize_metrics(self):
        """Initialize all 50+ core metrics"""
        
        # Self-Model Metrics (8)
        self._create_metrics([
            ("self_model.capability_count", "Number of registered capabilities"),
            ("self_model.avg_confidence", "Average confidence in self-assessment (0-1)"),
            ("self_model.limitations_detected", "Number of limitations detected"),
            ("self_model.improvement_rate", "Average capability improvement rate"),
            ("self_model.diagnostic_health", "Overall diagnostic health score (0-1)"),
            ("self_model.active_capabilities", "Number of actively used capabilities"),
            ("self_model.error_recovery_score", "Error recovery effectiveness (0-1)"),
            ("self_model.calibration_accuracy", "Accuracy of self-assessment (0-1)"),
        ])
        
        # Learning & Meta-Learning Metrics (8)
        self._create_metrics([
            ("learning.total_events", "Total learning events processed"),
            ("learning.patterns_learned", "Patterns discovered through learning"),
            ("learning.skills_developed", "Number of skills developed"),
            ("learning.avg_proficiency", "Average skill proficiency (0-1)"),
            ("meta_learning.strategy_count", "Number of active learning strategies"),
            ("meta_learning.strategy_effectiveness", "Average strategy effectiveness (0-1)"),
            ("meta_learning.domain_experts", "Number of domain expert models"),
            ("meta_learning.adaptation_speed", "Speed of parameter adaptation (0-1)"),
        ])
        
        # Knowledge & Reasoning Metrics (8)
        self._create_metrics([
            ("knowledge.total_entries", "Total entries in knowledge base"),
            ("knowledge.semantic_clusters", "Number of semantic clusters"),
            ("knowledge.avg_relevance", "Average knowledge relevance (0-1)"),
            ("reasoning.total_actions", "Total reasoning actions performed"),
            ("reasoning.success_rate", "Reasoning success rate (0-1)"),
            ("reasoning.avg_confidence", "Average reasoning confidence (0-1)"),
            ("reasoning.decision_quality", "Quality of decisions made (0-1)"),
            ("reasoning.goal_fulfillment", "Goal fulfillment rate (0-1)"),
        ])
        
        # Goal Generation & Autonomy Metrics (6)
        self._create_metrics([
            ("goals.total_generated", "Total autonomous goals generated"),
            ("goals.active_count", "Number of actively pursued goals"),
            ("goals.fulfillment_rate", "Rate of goal completion (0-1)"),
            ("goals.autonomy_score", "Autonomy in goal generation (0-1)"),
            ("goals.motivation_diversity", "Diversity of motivation sources (0-1)"),
            ("goals.priority_balance", "Balance in goal priorities (0-1)"),
        ])
        
        # Introspection & Self-Awareness Metrics (6)
        self._create_metrics([
            ("introspection.depth_score", "Depth of self-analysis (0-1)"),
            ("introspection.biases_detected", "Cognitive biases detected"),
            ("introspection.anomalies_found", "Anomalies in reasoning detected"),
            ("introspection.self_awareness", "Self-awareness level (0-1)"),
            ("introspection.reasoning_quality", "Quality of own reasoning (0-1)"),
            ("introspection.decision_quality", "Quality of own decisions (0-1)"),
        ])
        
        # Memory & Consolidation Metrics (6)
        self._create_metrics([
            ("memory.long_term_entries", "Long-term memory entries"),
            ("memory.episodic_entries", "Episodic memory entries"),
            ("memory.forgetting_rate", "Rate of memory loss (0-1)"),
            ("consolidation.rehearsal_count", "Memory rehearsals performed"),
            ("consolidation.stability_avg", "Average memory stability (0-1)"),
            ("consolidation.consolidation_efficiency", "Memory consolidation efficiency (0-1)"),
        ])
        
        # Error Recovery Metrics (5)
        self._create_metrics([
            ("errors.total_count", "Total errors encountered"),
            ("errors.recovery_success_rate", "Error recovery success rate (0-1)"),
            ("errors.recovery_time", "Average recovery time (seconds)"),
            ("errors.pattern_frequency", "Frequency of error patterns"),
            ("errors.prevention_score", "Error prevention effectiveness (0-1)"),
        ])
        
        # Cycle & System Metrics (8)
        self._create_metrics([
            ("cycles.total_completed", "Total autonomous cycles completed"),
            ("cycles.avg_duration", "Average cycle duration (seconds)"),
            ("cycles.success_rate", "Cycle completion success rate (0-1)"),
            ("system.memory_usage", "System memory usage (MB)"),
            ("system.cpu_usage", "System CPU usage (%)"),
            ("system.uptime", "System uptime (hours)"),
            ("system.overall_health", "Overall system health score (0-1)"),
            ("system.capability_score", "Overall capability score (0-100)"),
        ])
    
    def _create_metrics(self, metric_specs: List[tuple]):
        """Create multiple metrics from specifications"""
        for metric_name, description in metric_specs:
            if metric_name not in self.metrics:
                self.metrics[metric_name] = MetricsSeries(metric_name)
    
    def record_metric(self, metric_name: str, value: float,
                     component: str = "", tags: Dict[str, str] = None):
        """Record a metric value"""
        if metric_name not in self.metrics:
            self.metrics[metric_name] = MetricsSeries(metric_name)
        
        self.metrics[metric_name].add(value)
        logger.debug(f"📊 Recorded {metric_name}={value}")
        
        # Check for alerts
        self._check_alerts(metric_name, value)
    
    def _check_alerts(self, metric_name: str, value: float):
        """Check if metric exceeds thresholds"""
        # Alert thresholds
        thresholds = {
            "errors.recovery_success_rate": (0.5, False),  # (threshold, high_is_bad)
            "system.memory_usage": (3000, True),  # MB
            "system.cpu_usage": (90, True),  # %
            "memory.forgetting_rate": (0.3, True),
            "cycles.success_rate": (0.7, False),
            "reasoning.success_rate": (0.6, False),
        }
        
        if metric_name in thresholds:
            threshold, high_is_bad = thresholds[metric_name]
            should_alert = (value > threshold) if high_is_bad else (value < threshold)
            
            if should_alert:
                self.create_alert(
                    severity="warning" if abs(value - threshold) < threshold * 0.1 else "critical",
                    component=metric_name.split(".")[0],
                    message=f"{metric_name} = {value} (threshold: {threshold})",
                    metric_name=metric_name,
                    metric_value=value
                )
    
    def create_alert(self, severity: str, component: str, message: str,
                   metric_name: str = "", metric_value: float = 0.0):
        """Create an alert"""
        alert = {
            "severity": severity,  # info, warning, critical
            "component": component,
            "message": message,
            "metric_name": metric_name,
            "metric_value": metric_value,
            "timestamp": datetime.now().isoformat()
        }
        self.alerts.append(alert)
        
        if len(self.alerts) > self.max_alerts:
            self.alerts = self.alerts[-self.max_alerts:]
        
        log_level = "warning" if severity == "warning" else "error"
        logger.warning(f"⚠️ ALERT [{severity.upper()}] {component}: {message}")
    
    def update_component_health(self, component: str, status: str):
        """Update component health status"""
        self.component_health[component] = status
    
    def get_metric_summary(self, metric_name: str) -> Optional[Dict[str, Any]]:
        """Get summary for a specific metric"""
        if metric_name in self.metrics:
            return self.metrics[metric_name].get_summary()
        return None
    
    def get_component_metrics(self, component: str) -> Dict[str, Dict[str, Any]]:
        """Get all metrics for a specific component"""
        component_metrics = {}
        for name, series in self.metrics.items():
            if name.startswith(component):
                component_metrics[name] = series.get_summary()
        return component_metrics
    
    def get_all_metrics_summary(self) -> Dict[str, Dict[str, Any]]:
        """Get summary of all metrics"""
        return {name: series.get_summary() for name, series in self.metrics.items()}
    
    def get_system_health_score(self) -> float:
        """Calculate overall system health (0-100)"""
        try:
            # Key health indicators
            indicators = [
                ("cycles.success_rate", 1.0),
                ("reasoning.success_rate", 1.0),
                ("errors.recovery_success_rate", 1.0),
                ("goals.fulfillment_rate", 0.8),
                ("learning.avg_proficiency", 0.8),
                ("memory.forgetting_rate", -1.0),  # Negative because lower is better
                ("introspection.self_awareness", 0.6),
            ]
            
            total_score = 0.0
            total_weight = 0.0
            
            for metric_name, weight in indicators:
                if metric_name in self.metrics:
                    value = self.metrics[metric_name].current_value
                    # Invert negative weights
                    if weight < 0:
                        value = 1.0 - value
                    total_score += value * abs(weight)
                    total_weight += abs(weight)
            
            if total_weight > 0:
                return min(100.0, (total_score / total_weight) * 100)
            return 0.0
        except Exception as e:
            logger.error(f"Error calculating health score: {e}")
            return 0.0
    
    def get_recent_alerts(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get recent alerts"""
        return self.alerts[-limit:]
    
    def get_critical_alerts(self) -> List[Dict[str, Any]]:
        """Get all critical alerts"""
        return [a for a in self.alerts if a.get("severity") == "critical"]
    
    def get_dashboard_data(self) -> Dict[str, Any]:
        """Get comprehensive dashboard data"""
        return {
            "timestamp": datetime.now().isoformat(),
            "system_health": self.get_system_health_score(),
            "component_health": self.component_health,
            "key_metrics": {
                "capability_score": self.metrics.get("system.capability_score", 
                                                    MetricsSeries("dummy")).current_value,
                "goal_fulfillment": self.metrics.get("goals.fulfillment_rate",
                                                    MetricsSeries("dummy")).current_value,
                "memory_stability": 1.0 - self.metrics.get("memory.forgetting_rate",
                                                          MetricsSeries("dummy")).current_value,
                "reasoning_quality": self.metrics.get("reasoning.success_rate",
                                                     MetricsSeries("dummy")).current_value,
                "self_awareness": self.metrics.get("introspection.self_awareness",
                                                  MetricsSeries("dummy")).current_value,
            },
            "recent_alerts": self.get_recent_alerts(10),
            "cycle_metrics": {
                "total_completed": self.metrics.get("cycles.total_completed",
                                                   MetricsSeries("dummy")).current_value,
                "success_rate": self.metrics.get("cycles.success_rate",
                                                MetricsSeries("dummy")).current_value,
                "avg_duration": self.metrics.get("cycles.avg_duration",
                                                MetricsSeries("dummy")).current_value,
            }
        }
    
    def save_metrics(self):
        """Persist metrics to disk"""
        try:
            # Only save if interval has passed
            if datetime.now() - self.last_save < self.save_interval:
                return
            
            metrics_data = {
                "timestamp": datetime.now().isoformat(),
                "system_health": self.get_system_health_score(),
                "all_metrics": self.get_all_metrics_summary(),
                "component_health": self.component_health,
                "recent_alerts": self.get_recent_alerts(50)
            }
            
            with open(self.persistence_file, 'w') as f:
                json.dump(metrics_data, f, indent=2)
            
            self.last_save = datetime.now()
            logger.debug("💾 Metrics saved to disk")
        except Exception as e:
            logger.error(f"Error saving metrics: {e}")


# Global monitoring engine instance
monitoring_engine = MonitoringEngine()
