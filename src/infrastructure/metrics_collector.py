"""
Centralized Metrics Collection and Analysis System

Provides:
- Standardized metrics collection from all components
- Time-series storage and aggregation
- Real-time statistics and alerting
- Performance trending
- Resource usage tracking
"""
from typing import Dict, List, Any, Optional, Callable, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from collections import defaultdict
import statistics
import json
from pathlib import Path

import config
from logger import logger


@dataclass
class MetricPoint:
    """Single metric data point"""
    timestamp: datetime
    value: float
    component: str
    metric_type: str  # operation_time, error_rate, throughput, resource_usage, etc.
    tags: Dict[str, str] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp.isoformat(),
            "value": self.value,
            "component": self.component,
            "metric_type": self.metric_type,
            "tags": self.tags
        }


@dataclass
class MetricStats:
    """Statistics for a metric"""
    count: int = 0
    min: float = float('inf')
    max: float = float('-inf')
    sum: float = 0.0
    mean: float = 0.0
    median: float = 0.0
    stdev: float = 0.0
    p95: float = 0.0
    p99: float = 0.0
    
    def to_dict(self) -> Dict[str, float]:
        return {
            "count": self.count,
            "min": self.min if self.min != float('inf') else None,
            "max": self.max if self.max != float('-inf') else None,
            "mean": self.mean,
            "median": self.median,
            "stdev": self.stdev,
            "p95": self.p95,
            "p99": self.p99
        }


class MetricsCollector:
    """
    Centralized metrics collection and aggregation system.
    
    Features:
    - Standardized metric recording
    - Automatic time-series aggregation
    - Statistics calculation
    - Performance trending
    - Metric retention policies
    """
    
    def __init__(self, retention_hours: int = 24, cleanup_interval: int = 3600):
        """
        Initialize metrics collector
        
        Args:
            retention_hours: How long to keep metrics (default: 24 hours)
            cleanup_interval: How often to cleanup (default: 3600 seconds = 1 hour)
        """
        self.metrics: List[MetricPoint] = []
        self.retention_hours = retention_hours
        self.cleanup_interval = cleanup_interval
        self.last_cleanup = datetime.now()
        self.metrics_file = config.DATA_DIR / "metrics.json"
        self.alerts: Dict[str, Callable] = {}  # Metric alerts
        
        # Aggregation
        self.aggregated: Dict[str, Dict[str, List[float]]] = defaultdict(
            lambda: defaultdict(list)
        )
        self.stats_cache: Dict[str, Dict[str, MetricStats]] = defaultdict(
            lambda: defaultdict(MetricStats)
        )
        
        logger.info("✓ Metrics Collector initialized")
    
    def record(
        self,
        component: str,
        metric_type: str,
        value: float,
        tags: Optional[Dict[str, str]] = None
    ) -> None:
        """
        Record a metric
        
        Args:
            component: Component name
            metric_type: Type of metric (operation_time, error_count, memory_usage, etc.)
            value: Metric value
            tags: Optional tags for filtering (operation, endpoint, user, etc.)
        """
        if tags is None:
            tags = {}
        
        point = MetricPoint(
            timestamp=datetime.now(),
            value=value,
            component=component,
            metric_type=metric_type,
            tags=tags
        )
        
        self.metrics.append(point)
        self.aggregated[component][metric_type].append(value)
        
        # Update stats cache
        self._update_stats(component, metric_type, value)
        
        # Check alerts
        self._check_alerts(component, metric_type, value)
        
        # Periodic cleanup
        if (datetime.now() - self.last_cleanup).total_seconds() > self.cleanup_interval:
            self._cleanup_old_metrics()
    
    def _update_stats(self, component: str, metric_type: str, value: float) -> None:
        """Update running statistics"""
        stats = self.stats_cache[component][metric_type]
        stats.count += 1
        stats.min = min(stats.min, value)
        stats.max = max(stats.max, value)
        stats.sum += value
        stats.mean = stats.sum / stats.count
        
        # Recalculate percentiles and stdev with all values
        values = self.aggregated[component][metric_type]
        if values:
            if len(values) > 1:
                stats.stdev = statistics.stdev(values)
            stats.median = statistics.median(values)
            stats.p95 = self._percentile(values, 95)
            stats.p99 = self._percentile(values, 99)
    
    @staticmethod
    def _percentile(values: List[float], p: int) -> float:
        """Calculate percentile"""
        if not values:
            return 0.0
        sorted_values = sorted(values)
        index = int((p / 100) * len(sorted_values))
        return sorted_values[min(index, len(sorted_values) - 1)]
    
    def _check_alerts(self, component: str, metric_type: str, value: float) -> None:
        """Check metric alerts"""
        alert_key = f"{component}:{metric_type}"
        if alert_key in self.alerts:
            try:
                self.alerts[alert_key](value)
            except Exception as e:
                logger.error(f"Error in metric alert: {e}")
    
    def register_alert(
        self,
        component: str,
        metric_type: str,
        threshold: float,
        condition: str = ">"
    ) -> None:
        """
        Register a metric alert
        
        Args:
            component: Component name
            metric_type: Metric type
            threshold: Threshold value
            condition: Condition (">" or "<")
        """
        alert_key = f"{component}:{metric_type}"
        
        def check_alert(value: float) -> None:
            if condition == ">" and value > threshold:
                logger.warning(f"🚨 Metric alert: {alert_key} = {value} > {threshold}")
            elif condition == "<" and value < threshold:
                logger.warning(f"🚨 Metric alert: {alert_key} = {value} < {threshold}")
        
        self.alerts[alert_key] = check_alert
        logger.info(f"✓ Registered metric alert: {alert_key} {condition} {threshold}")
    
    def get_stats(
        self,
        component: str,
        metric_type: str,
        time_window_hours: Optional[int] = None
    ) -> Optional[MetricStats]:
        """
        Get statistics for a metric
        
        Args:
            component: Component name
            metric_type: Metric type
            time_window_hours: Optional time window (default: all)
        
        Returns:
            MetricStats object or None
        """
        if time_window_hours:
            # Recalculate for time window
            cutoff = datetime.now() - timedelta(hours=time_window_hours)
            values = [
                m.value for m in self.metrics
                if m.component == component
                and m.metric_type == metric_type
                and m.timestamp > cutoff
            ]
        else:
            values = self.aggregated[component][metric_type]
        
        if not values:
            return None
        
        stats = MetricStats(
            count=len(values),
            min=min(values),
            max=max(values),
            sum=sum(values),
            mean=sum(values) / len(values),
            median=statistics.median(values)
        )
        
        if len(values) > 1:
            stats.stdev = statistics.stdev(values)
        
        stats.p95 = self._percentile(values, 95)
        stats.p99 = self._percentile(values, 99)
        
        return stats
    
    def get_all_stats(
        self,
        time_window_hours: Optional[int] = None
    ) -> Dict[str, Dict[str, Dict[str, Any]]]:
        """
        Get all collected statistics
        
        Args:
            time_window_hours: Optional time window
        
        Returns:
            Nested dictionary of all stats
        """
        stats = {}
        
        for component, metrics in self.aggregated.items():
            stats[component] = {}
            for metric_type in metrics:
                metric_stats = self.get_stats(component, metric_type, time_window_hours)
                if metric_stats:
                    stats[component][metric_type] = metric_stats.to_dict()
        
        return stats
    
    def get_component_stats(self, component: str) -> Dict[str, Dict[str, Any]]:
        """Get all statistics for a component"""
        stats = {}
        if component in self.aggregated:
            for metric_type in self.aggregated[component]:
                metric_stats = self.get_stats(component, metric_type)
                if metric_stats:
                    stats[metric_type] = metric_stats.to_dict()
        return stats
    
    def get_trend(
        self,
        component: str,
        metric_type: str,
        bucket_size_minutes: int = 5,
        num_buckets: int = 12
    ) -> List[Dict[str, Any]]:
        """
        Get trending data for visualization
        
        Args:
            component: Component name
            metric_type: Metric type
            bucket_size_minutes: Size of time buckets
            num_buckets: Number of buckets to return
        
        Returns:
            List of trend data points
        """
        trend = []
        now = datetime.now()
        bucket_size = timedelta(minutes=bucket_size_minutes)
        
        for i in range(num_buckets - 1, -1, -1):
            bucket_start = now - (bucket_size * (i + 1))
            bucket_end = bucket_start + bucket_size
            
            values = [
                m.value for m in self.metrics
                if m.component == component
                and m.metric_type == metric_type
                and bucket_start <= m.timestamp <= bucket_end
            ]
            
            if values:
                trend.append({
                    "timestamp": bucket_start.isoformat(),
                    "count": len(values),
                    "avg": sum(values) / len(values),
                    "min": min(values),
                    "max": max(values)
                })
        
        return trend
    
    def _cleanup_old_metrics(self) -> None:
        """Remove old metrics exceeding retention period"""
        cutoff = datetime.now() - timedelta(hours=self.retention_hours)
        initial_count = len(self.metrics)
        
        self.metrics = [m for m in self.metrics if m.timestamp > cutoff]
        
        removed_count = initial_count - len(self.metrics)
        if removed_count > 0:
            logger.debug(f"Cleaned up {removed_count} old metrics")
        
        self.last_cleanup = datetime.now()
    
    def save_to_disk(self) -> None:
        """Persist metrics to disk"""
        try:
            stats = self.get_all_stats()
            
            # Convert to JSON-serializable format
            data = {
                "timestamp": datetime.now().isoformat(),
                "metrics_count": len(self.metrics),
                "stats": stats
            }
            
            with open(self.metrics_file, 'w') as f:
                json.dump(data, f, indent=2, default=str)
            
            logger.debug(f"Metrics saved to disk ({self.metrics_file})")
        except Exception as e:
            logger.error(f"Failed to save metrics: {e}")
    
    def load_from_disk(self) -> None:
        """Load metrics from disk"""
        try:
            if self.metrics_file.exists():
                with open(self.metrics_file, 'r') as f:
                    data = json.load(f)
                logger.debug(f"Loaded metrics from disk")
        except Exception as e:
            logger.error(f"Failed to load metrics: {e}")


# Global metrics collector instance
_metrics_collector: Optional[MetricsCollector] = None


def get_metrics_collector(retention_hours: int = 24) -> MetricsCollector:
    """Get or create global metrics collector"""
    global _metrics_collector
    if _metrics_collector is None:
        _metrics_collector = MetricsCollector(retention_hours)
    return _metrics_collector
