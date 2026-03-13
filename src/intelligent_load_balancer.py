"""
Phase 2: Intelligent Load Balancer

Intelligently routes requests across components based on current load,
performance metrics, and availability.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Any, Dict, List, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
import time
import random
import statistics

from src.logger import logger
from src.monitoring_engine import monitoring_engine


class LoadBalancingStrategy(Enum):
    """Load balancing strategies"""
    ROUND_ROBIN = "round_robin"
    LEAST_CONNECTIONS = "least_connections"
    WEIGHTED_ROUND_ROBIN = "weighted_round_robin"
    PERFORMANCE_BASED = "performance_based"
    RANDOM = "random"


class ComponentHealth(Enum):
    """Health status of a component"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    CIRCUIT_OPEN = "circuit_open"


@dataclass
class ComponentLoadInfo:
    """Current load information for a component"""
    component_id: str
    current_load: float = 0.0  # 0.0-1.0
    active_connections: int = 0
    total_requests: int = 0
    failed_requests: int = 0
    avg_latency: float = 0.0
    min_latency: float = float('inf')
    max_latency: float = 0.0
    last_updated: datetime = field(default_factory=datetime.now)
    health_status: ComponentHealth = ComponentHealth.HEALTHY
    
    def update_load(self, latency: float, success: bool = True):
        """Update load information"""
        self.total_requests += 1
        
        if success:
            if self.total_requests > 0:
                # Update average latency (exponential moving average)
                alpha = 0.3
                self.avg_latency = alpha * latency + (1 - alpha) * self.avg_latency
                self.min_latency = min(self.min_latency, latency)
                self.max_latency = max(self.max_latency, latency)
        else:
            self.failed_requests += 1
        
        # Calculate load (0.0-1.0)
        success_rate = (self.total_requests - self.failed_requests) / self.total_requests
        latency_factor = min(self.avg_latency / 1000.0, 1.0)  # Normalize to 1s
        self.current_load = (1.0 - success_rate) * 0.5 + latency_factor * 0.5
        
        self.last_updated = datetime.now()
    
    def get_success_rate(self) -> float:
        """Get success rate percentage"""
        if self.total_requests == 0:
            return 1.0
        return (self.total_requests - self.failed_requests) / self.total_requests
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "component_id": self.component_id,
            "current_load": self.current_load,
            "active_connections": self.active_connections,
            "total_requests": self.total_requests,
            "failed_requests": self.failed_requests,
            "avg_latency": self.avg_latency,
            "success_rate": self.get_success_rate(),
            "health_status": self.health_status.value,
            "last_updated": self.last_updated.isoformat()
        }


@dataclass
class CircuitBreakerState:
    """State of a circuit breaker"""
    component_id: str
    state: str = "closed"  # closed, open, half_open
    failure_count: int = 0
    success_count: int = 0
    last_failure: Optional[datetime] = None
    last_state_change: datetime = field(default_factory=datetime.now)
    
    failure_threshold: int = 5  # Open after 5 failures
    reset_timeout: int = 60  # Reset after 60 seconds
    success_threshold: int = 2  # Close after 2 successes in half-open
    
    def record_success(self):
        """Record a successful request"""
        self.failure_count = 0
        
        if self.state == "half_open":
            self.success_count += 1
            if self.success_count >= self.success_threshold:
                self.set_closed()
    
    def record_failure(self):
        """Record a failed request"""
        self.failure_count += 1
        self.last_failure = datetime.now()
        
        if self.state == "closed" and self.failure_count >= self.failure_threshold:
            self.set_open()
        elif self.state == "half_open":
            self.set_open()
    
    def set_closed(self):
        """Close the circuit"""
        self.state = "closed"
        self.failure_count = 0
        self.success_count = 0
        self.last_state_change = datetime.now()
    
    def set_open(self):
        """Open the circuit"""
        self.state = "open"
        self.last_state_change = datetime.now()
    
    def set_half_open(self):
        """Set circuit to half-open"""
        self.state = "half_open"
        self.failure_count = 0
        self.success_count = 0
        self.last_state_change = datetime.now()
    
    def can_attempt(self) -> bool:
        """Check if request can be attempted"""
        if self.state == "closed":
            return True
        
        if self.state == "open":
            # Check if reset timeout has passed
            elapsed = (datetime.now() - self.last_state_change).total_seconds()
            if elapsed > self.reset_timeout:
                self.set_half_open()
                return True
            return False
        
        # half_open: allow attempts
        return True


class IntelligentLoadBalancer:
    """Intelligent load balancer for routing requests across components"""
    
    def __init__(self,
                 strategy: LoadBalancingStrategy = LoadBalancingStrategy.PERFORMANCE_BASED,
                 health_check_interval: int = 30):
        
        self.strategy = strategy
        self.health_check_interval = health_check_interval
        
        self.components: Dict[str, Any] = {}  # component_id -> component instance
        self.load_info: Dict[str, ComponentLoadInfo] = {}  # component_id -> load info
        self.circuit_breakers: Dict[str, CircuitBreakerState] = {}  # component_id -> CB state
        self.weights: Dict[str, float] = {}  # component_id -> weight for weighted strategies
        
        self.round_robin_index = 0
        self.routing_history: List[Dict[str, Any]] = []
        self.max_history = 1000
        
        logger.info(f"✓ Intelligent Load Balancer initialized (strategy: {strategy.value})")
    
    def register_component(self,
                          component_id: str,
                          component: Any,
                          weight: float = 1.0):
        """Register a component"""
        self.components[component_id] = component
        self.load_info[component_id] = ComponentLoadInfo(component_id=component_id)
        self.circuit_breakers[component_id] = CircuitBreakerState(component_id=component_id)
        self.weights[component_id] = weight
        
        logger.info(f"✓ Registered component: {component_id} (weight: {weight})")
    
    def register_components_batch(self,
                                 components: Dict[str, Any],
                                 weights: Dict[str, float] = None):
        """Register multiple components"""
        weights = weights or {}
        
        for component_id, component in components.items():
            weight = weights.get(component_id, 1.0)
            self.register_component(component_id, component, weight)
        
        logger.info(f"✓ Registered {len(components)} components")
    
    def get_component(self) -> Optional[str]:
        """Get next component ID based on load balancing strategy"""
        available = self._get_available_components()
        
        if not available:
            logger.warning("No available components")
            return None
        
        if self.strategy == LoadBalancingStrategy.ROUND_ROBIN:
            return self._round_robin_select(available)
        
        elif self.strategy == LoadBalancingStrategy.LEAST_CONNECTIONS:
            return self._least_connections_select(available)
        
        elif self.strategy == LoadBalancingStrategy.WEIGHTED_ROUND_ROBIN:
            return self._weighted_round_robin_select(available)
        
        elif self.strategy == LoadBalancingStrategy.PERFORMANCE_BASED:
            return self._performance_based_select(available)
        
        elif self.strategy == LoadBalancingStrategy.RANDOM:
            return random.choice(available)
        
        return available[0]
    
    def _get_available_components(self) -> List[str]:
        """Get list of available components"""
        available = []
        
        for component_id, cb in self.circuit_breakers.items():
            if cb.can_attempt():
                available.append(component_id)
        
        return available
    
    def _round_robin_select(self, available: List[str]) -> str:
        """Select component using round-robin"""
        component_id = available[self.round_robin_index % len(available)]
        self.round_robin_index += 1
        return component_id
    
    def _least_connections_select(self, available: List[str]) -> str:
        """Select component with least active connections"""
        return min(
            available,
            key=lambda cid: self.load_info[cid].active_connections
        )
    
    def _weighted_round_robin_select(self, available: List[str]) -> str:
        """Select component using weighted round-robin"""
        # Build weighted list
        weighted = []
        for cid in available:
            weight = int(self.weights.get(cid, 1.0))
            weighted.extend([cid] * weight)
        
        if not weighted:
            return available[0]
        
        component_id = weighted[self.round_robin_index % len(weighted)]
        self.round_robin_index += 1
        return component_id
    
    def _performance_based_select(self, available: List[str]) -> str:
        """Select component based on performance metrics"""
        # Score each component (lower is better)
        scores = {}
        
        for component_id in available:
            load_info = self.load_info[component_id]
            
            # Composite score: load (0.5) + success rate penalty (0.3) + latency (0.2)
            load_score = load_info.current_load * 0.5
            success_score = (1.0 - load_info.get_success_rate()) * 0.3
            latency_score = min(load_info.avg_latency / 1000.0, 1.0) * 0.2
            
            scores[component_id] = load_score + success_score + latency_score
        
        # Return component with lowest score
        return min(scores, key=scores.get)
    
    def record_request(self,
                      component_id: str,
                      latency: float,
                      success: bool = True):
        """Record request metrics"""
        if component_id not in self.load_info:
            logger.warning(f"Component not found: {component_id}")
            return
        
        # Update load info
        self.load_info[component_id].update_load(latency, success)
        
        # Update circuit breaker
        cb = self.circuit_breakers[component_id]
        if success:
            cb.record_success()
        else:
            cb.record_failure()
        
        # Update health status
        self._update_health_status(component_id)
        
        # Log routing decision
        self.routing_history.append({
            "timestamp": datetime.now(),
            "component_id": component_id,
            "latency": latency,
            "success": success
        })
        
        # Keep history bounded
        if len(self.routing_history) > self.max_history:
            self.routing_history = self.routing_history[-self.max_history:]
    
    def _update_health_status(self, component_id: str):
        """Update health status based on metrics"""
        load_info = self.load_info[component_id]
        success_rate = load_info.get_success_rate()
        
        if success_rate < 0.7:
            load_info.health_status = ComponentHealth.UNHEALTHY
        elif success_rate < 0.9:
            load_info.health_status = ComponentHealth.DEGRADED
        else:
            load_info.health_status = ComponentHealth.HEALTHY
    
    def get_component_status(self, component_id: str) -> Dict[str, Any]:
        """Get detailed status of a component"""
        if component_id not in self.load_info:
            return {}
        
        load_info = self.load_info[component_id]
        cb = self.circuit_breakers[component_id]
        
        return {
            "component_id": component_id,
            "load_info": load_info.to_dict(),
            "circuit_breaker": {
                "state": cb.state,
                "failure_count": cb.failure_count,
                "success_count": cb.success_count,
                "last_failure": cb.last_failure.isoformat() if cb.last_failure else None
            }
        }
    
    def get_all_status(self) -> Dict[str, Dict[str, Any]]:
        """Get status of all components"""
        return {
            cid: self.get_component_status(cid)
            for cid in self.components.keys()
        }
    
    def get_routing_statistics(self) -> Dict[str, Any]:
        """Get routing statistics"""
        if not self.routing_history:
            return {}
        
        latencies = [r["latency"] for r in self.routing_history]
        successful = sum(1 for r in self.routing_history if r["success"])
        
        return {
            "total_requests": len(self.routing_history),
            "successful_requests": successful,
            "failed_requests": len(self.routing_history) - successful,
            "success_rate": successful / len(self.routing_history),
            "avg_latency": statistics.mean(latencies),
            "median_latency": statistics.median(latencies),
            "min_latency": min(latencies),
            "max_latency": max(latencies),
            "p95_latency": sorted(latencies)[int(len(latencies) * 0.95)] if latencies else 0,
            "p99_latency": sorted(latencies)[int(len(latencies) * 0.99)] if latencies else 0,
        }
    
    def rebalance(self):
        """Rebalance load across components"""
        # This could implement more sophisticated rebalancing strategies
        available = self._get_available_components()
        
        if len(available) <= 1:
            return
        
        # Log rebalancing
        logger.info(f"Rebalancing across {len(available)} components")
    
    def print_status(self):
        """Print load balancer status"""
        logger.info("\n" + "="*80)
        logger.info("INTELLIGENT LOAD BALANCER STATUS")
        logger.info("="*80)
        logger.info(f"Strategy: {self.strategy.value}")
        logger.info(f"Total Components: {len(self.components)}")
        
        for component_id in self.components.keys():
            status = self.get_component_status(component_id)
            info = status["load_info"]
            cb = status["circuit_breaker"]
            
            logger.info(f"\n{component_id}:")
            logger.info(f"  Load: {info['current_load']:.1%}")
            logger.info(f"  Requests: {info['total_requests']} (Success: {info['success_rate']:.1%})")
            logger.info(f"  Avg Latency: {info['avg_latency']:.2f}ms")
            logger.info(f"  Health: {info['health_status']}")
            logger.info(f"  Circuit Breaker: {cb['state']}")


# Global load balancer instance
intelligent_load_balancer = IntelligentLoadBalancer()


def get_load_balancer(strategy: LoadBalancingStrategy = LoadBalancingStrategy.PERFORMANCE_BASED) -> IntelligentLoadBalancer:
    """Get the global load balancer"""
    if intelligent_load_balancer.strategy != strategy:
        intelligent_load_balancer.strategy = strategy
    
    return intelligent_load_balancer


class LoadBalancedComponent:
    """Wrapper that provides load-balanced access to a component"""
    
    def __init__(self,
                 component_id: str,
                 component: Any,
                 load_balancer: IntelligentLoadBalancer):
        
        self.component_id = component_id
        self.component = component
        self.load_balancer = load_balancer
    
    def __call__(self, *args, **kwargs) -> Any:
        """Call the component and record metrics"""
        start = time.time()
        
        try:
            result = self.component(*args, **kwargs)
            latency = (time.time() - start) * 1000
            self.load_balancer.record_request(self.component_id, latency, success=True)
            return result
        except Exception as e:
            latency = (time.time() - start) * 1000
            self.load_balancer.record_request(self.component_id, latency, success=False)
            raise
