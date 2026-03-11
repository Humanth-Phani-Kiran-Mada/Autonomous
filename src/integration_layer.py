"""
Integration Layer - Event Bus and Cross-Component Communication

Provides a publish-subscribe pattern for tight coupling between autonomous cycles
and enables real-time communication between self-model, goal generator, learning
engine, and other components.
"""

from typing import Callable, Dict, List, Any, Set
from datetime import datetime
from collections import defaultdict
import json
from pathlib import Path
import config
from .logger import logger


class Event:
    """Represents an event in the autonomous system"""
    
    def __init__(self, event_type: str, source: str, data: Dict[str, Any], 
                 timestamp: datetime = None, priority: int = 5):
        self.event_type = event_type
        self.source = source
        self.data = data
        self.timestamp = timestamp or datetime.now()
        self.priority = priority  # 1-10, higher = more important
        self.processed_by: Set[str] = set()
        self.responses: Dict[str, Any] = {}
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_type": self.event_type,
            "source": self.source,
            "data": self.data,
            "timestamp": self.timestamp.isoformat(),
            "priority": self.priority,
            "processed_by": list(self.processed_by)
        }
    
    def __repr__(self) -> str:
        return f"Event({self.event_type}, src={self.source}, priority={self.priority})"


class EventBus:
    """Central pub-sub event bus for autonomous system communication"""
    
    def __init__(self):
        self.subscribers: Dict[str, List[Callable]] = defaultdict(list)
        self.event_history: List[Event] = []
        self.max_history = 1000
        self.statistics = {
            "total_events": 0,
            "events_by_type": defaultdict(int),
            "events_by_source": defaultdict(int)
        }
        self.persistence_file = config.DATA_DIR / "event_bus_history.json"
    
    def subscribe(self, event_type: str, handler: Callable, priority: int = 5) -> str:
        """
        Subscribe to an event type
        
        Args:
            event_type: Type of event to subscribe to
            handler: Function to call when event occurs
            priority: Execution priority (higher runs first)
        
        Returns:
            Subscription ID
        """
        self.subscribers[event_type].append((handler, priority))
        # Sort by priority descending
        self.subscribers[event_type].sort(key=lambda x: x[1], reverse=True)
        sub_id = f"{event_type}_{id(handler)}"
        logger.debug(f"📡 Subscribed {handler.__name__} to {event_type}")
        return sub_id
    
    def unsubscribe(self, event_type: str, handler: Callable):
        """Unsubscribe from an event type"""
        if event_type in self.subscribers:
            self.subscribers[event_type] = [
                (h, p) for h, p in self.subscribers[event_type] 
                if h != handler
            ]
    
    def publish(self, event: Event) -> Dict[str, Any]:
        """
        Publish an event to all subscribers
        
        Args:
            event: Event to publish
        
        Returns:
            Dictionary of responses from subscribers
        """
        self.statistics["total_events"] += 1
        self.statistics["events_by_type"][event.event_type] += 1
        self.statistics["events_by_source"][event.source] += 1
        
        handlers = self.subscribers.get(event.event_type, [])
        self.event_history.append(event)
        
        if len(self.event_history) > self.max_history:
            self.event_history = self.event_history[-self.max_history:]
        
        logger.debug(f"📣 Publishing {event} to {len(handlers)} handlers")
        
        # Execute all handlers for this event type
        for handler, priority in handlers:
            try:
                response = handler(event)
                event.processed_by.add(handler.__name__)
                if response:
                    event.responses[handler.__name__] = response
            except Exception as e:
                logger.error(f"❌ Error in handler {handler.__name__}: {e}")
                event.responses[handler.__name__] = {"error": str(e)}
        
        return event.responses
    
    def publish_event(self, event_type: str, source: str, data: Dict[str, Any],
                     priority: int = 5) -> Dict[str, Any]:
        """Convenience method to create and publish an event"""
        event = Event(event_type, source, data, priority=priority)
        return self.publish(event)
    
    def get_event_history(self, event_type: str = None, 
                         limit: int = 50) -> List[Event]:
        """Get event history, optionally filtered by type"""
        if event_type:
            history = [e for e in self.event_history if e.event_type == event_type]
        else:
            history = self.event_history
        return history[-limit:]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get event bus statistics"""
        return {
            "total_events": self.statistics["total_events"],
            "unique_event_types": len(self.statistics["events_by_type"]),
            "events_by_type": dict(self.statistics["events_by_type"]),
            "events_by_source": dict(self.statistics["events_by_source"]),
            "subscribers": {k: len(v) for k, v in self.subscribers.items()},
            "history_size": len(self.event_history)
        }
    
    def save_history(self):
        """Persist event history to disk"""
        try:
            history_data = {
                "events": [e.to_dict() for e in self.event_history[-100:]],
                "statistics": {
                    "total_events": self.statistics["total_events"],
                    "events_by_type": dict(self.statistics["events_by_type"]),
                    "events_by_source": dict(self.statistics["events_by_source"])
                },
                "persisted_at": datetime.now().isoformat()
            }
            with open(self.persistence_file, 'w') as f:
                json.dump(history_data, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving event history: {e}")


class IntegrationLayer:
    """
    High-level integration layer providing standard event types and patterns
    for the autonomous system
    """
    
    # Standard event types
    CAPABILITY_DETECTED = "capability.detected"
    CAPABILITY_IMPROVED = "capability.improved"
    CAPABILITY_DEGRADED = "capability.degraded"
    
    GOAL_GENERATED = "goal.generated"
    GOAL_ACHIEVED = "goal.achieved"
    GOAL_FAILED = "goal.failed"
    
    LEARNING_COMPLETED = "learning.completed"
    LEARNING_FAILED = "learning.failed"
    KNOWLEDGE_ACQUIRED = "knowledge.acquired"
    
    REASONING_COMPLETE = "reasoning.complete"
    DECISION_MADE = "decision.made"
    
    ERROR_OCCURRED = "error.occurred"
    ERROR_RECOVERED = "error.recovered"
    
    MEMORY_CONSOLIDATED = "memory.consolidated"
    MEMORY_LOSS_DETECTED = "memory.loss.detected"
    
    BIAS_DETECTED = "bias.detected"
    ANOMALY_DETECTED = "anomaly.detected"
    
    CYCLE_STARTED = "cycle.started"
    CYCLE_COMPLETED = "cycle.completed"
    CYCLE_FAILED = "cycle.failed"
    
    def __init__(self):
        self.event_bus = EventBus()
        self.cycle_status: Dict[str, str] = {}
        self.cycle_results: Dict[str, Dict[str, Any]] = {}
        self.cycle_timing: Dict[str, float] = {}
    
    def register_cycle_handler(self, cycle_name: str, handler: Callable):
        """Register a handler for cycle completion events"""
        self.event_bus.subscribe(self.CYCLE_COMPLETED, handler)
    
    def report_cycle_start(self, cycle_name: str, metadata: Dict[str, Any] = None):
        """Report that a cycle is starting"""
        self.cycle_status[cycle_name] = "running"
        self.event_bus.publish_event(
            self.CYCLE_STARTED,
            cycle_name,
            {"cycle": cycle_name, "metadata": metadata or {}},
            priority=6
        )
    
    def report_cycle_complete(self, cycle_name: str, result: Dict[str, Any],
                            execution_time: float):
        """Report that a cycle has completed successfully"""
        self.cycle_status[cycle_name] = "completed"
        self.cycle_results[cycle_name] = result
        self.cycle_timing[cycle_name] = execution_time
        
        self.event_bus.publish_event(
            self.CYCLE_COMPLETED,
            cycle_name,
            {
                "cycle": cycle_name,
                "result": result,
                "execution_time": execution_time
            },
            priority=7
        )
    
    def report_cycle_error(self, cycle_name: str, error: Exception,
                          context: Dict[str, Any] = None):
        """Report that a cycle failed"""
        self.cycle_status[cycle_name] = "failed"
        self.event_bus.publish_event(
            self.CYCLE_FAILED,
            cycle_name,
            {
                "cycle": cycle_name,
                "error": str(error),
                "context": context or {}
            },
            priority=9  # High priority for failures
        )
    
    def report_goal_generated(self, goal_id: str, goal_name: str, 
                            priority: float, motivation: str):
        """Report a new goal generated"""
        self.event_bus.publish_event(
            self.GOAL_GENERATED,
            "goal_generator",
            {
                "goal_id": goal_id,
                "goal_name": goal_name,
                "priority": priority,
                "motivation": motivation
            },
            priority=6
        )
    
    def report_knowledge_acquired(self, knowledge_id: str, source: str,
                                 knowledge_type: str, categories: List[str]):
        """Report new knowledge acquired"""
        self.event_bus.publish_event(
            self.KNOWLEDGE_ACQUIRED,
            "knowledge_base",
            {
                "knowledge_id": knowledge_id,
                "source": source,
                "type": knowledge_type,
                "categories": categories
            },
            priority=5
        )
    
    def report_capability_improved(self, capability_name: str, old_level: float,
                                  new_level: float, domain: str):
        """Report a capability improvement"""
        improvement = new_level - old_level
        self.event_bus.publish_event(
            self.CAPABILITY_IMPROVED,
            "learning_engine",
            {
                "capability": capability_name,
                "old_level": old_level,
                "new_level": new_level,
                "improvement": improvement,
                "domain": domain
            },
            priority=6
        )
    
    def report_error_occurred(self, error_type: str, component: str,
                            context: Dict[str, Any] = None):
        """Report an error"""
        self.event_bus.publish_event(
            self.ERROR_OCCURRED,
            component,
            {
                "error_type": error_type,
                "component": component,
                "context": context or {}
            },
            priority=8
        )
    
    def report_bias_detected(self, bias_type: str, severity: float,
                           context: Dict[str, Any] = None):
        """Report a detected cognitive bias"""
        self.event_bus.publish_event(
            self.BIAS_DETECTED,
            "introspection_engine",
            {
                "bias_type": bias_type,
                "severity": severity,
                "context": context or {}
            },
            priority=7
        )
    
    def get_event_history(self, event_type: str = None,
                         limit: int = 50) -> List[Event]:
        """Get event history"""
        return self.event_bus.get_event_history(event_type, limit)
    
    def get_integration_status(self) -> Dict[str, Any]:
        """Get overall integration status"""
        return {
            "cycle_status": self.cycle_status,
            "cycle_timing": self.cycle_timing,
            "event_bus_stats": self.event_bus.get_statistics(),
            "completed_cycles": sum(1 for s in self.cycle_status.values() 
                                    if s == "completed"),
            "failed_cycles": sum(1 for s in self.cycle_status.values() 
                                if s == "failed"),
            "running_cycles": sum(1 for s in self.cycle_status.values() 
                                 if s == "running")
        }
    
    def save_integration_state(self):
        """Persist integration layer state"""
        try:
            state = {
                "cycle_status": self.cycle_status,
                "cycle_timing": self.cycle_timing,
                "event_bus_stats": self.event_bus.get_statistics(),
                "saved_at": datetime.now().isoformat()
            }
            state_file = config.DATA_DIR / "integration_state.json"
            with open(state_file, 'w') as f:
                json.dump(state, f, indent=2)
            
            # Also save event history
            self.event_bus.save_history()
        except Exception as e:
            logger.error(f"Error saving integration state: {e}")


# Global integration layer instance
integration_layer = IntegrationLayer()
