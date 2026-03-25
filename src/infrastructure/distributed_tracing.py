"""
Phase 2: Distributed Tracing System

Provides end-to-end request tracing across components, with detailed timing,
dependency tracking, and performance analysis.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Any, Dict, List, Optional, Set
from dataclasses import dataclass, field
from datetime import datetime
from collections import defaultdict
import time
import uuid
import json

from src.logger import logger
from src.monitoring_engine import monitoring_engine


@dataclass
class TraceSpan:
    """A single span in a distributed trace"""
    span_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    trace_id: str = ""
    parent_span_id: Optional[str] = None
    component_id: str = ""
    operation: str = ""
    start_time: float = field(default_factory=time.time)
    end_time: Optional[float] = None
    duration: float = 0.0
    status: str = "started"  # started, completed, failed
    error: Optional[str] = None
    tags: Dict[str, Any] = field(default_factory=dict)
    logs: List[Dict[str, Any]] = field(default_factory=list)
    children: List[str] = field(default_factory=list)  # child span IDs
    
    def complete(self, status: str = "completed", error: str = None):
        """Mark span as completed"""
        self.end_time = time.time()
        self.duration = (self.end_time - self.start_time) * 1000  # milliseconds
        self.status = status
        self.error = error
    
    def add_tag(self, key: str, value: Any):
        """Add a tag to the span"""
        self.tags[key] = value
    
    def add_log(self, message: str, level: str = "info", **fields):
        """Add a log entry to the span"""
        self.logs.append({
            "timestamp": datetime.now().isoformat(),
            "level": level,
            "message": message,
            **fields
        })
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert span to dictionary"""
        return {
            "span_id": self.span_id,
            "trace_id": self.trace_id,
            "parent_span_id": self.parent_span_id,
            "component_id": self.component_id,
            "operation": self.operation,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "duration_ms": self.duration,
            "status": self.status,
            "error": self.error,
            "tags": self.tags,
            "logs": self.logs,
            "children": self.children
        }


@dataclass
class DistributedTrace:
    """A complete distributed trace"""
    trace_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    root_span_id: str = ""
    start_time: float = field(default_factory=time.time)
    end_time: Optional[float] = None
    total_duration: float = 0.0
    spans: Dict[str, TraceSpan] = field(default_factory=dict)
    components_involved: Set[str] = field(default_factory=set)
    
    def get_total_components(self) -> int:
        """Get number of unique components in trace"""
        return len(self.components_involved)
    
    def get_critical_path_duration(self) -> float:
        """Get critical path duration (longest path through spans)"""
        if not self.spans:
            return 0.0
        
        # Find root span
        root = next((s for s in self.spans.values() if s.parent_span_id is None), None)
        if not root:
            return 0.0
        
        return self._calculate_critical_path(root)
    
    def _calculate_critical_path(self, span: TraceSpan, accumulated: float = 0.0) -> float:
        """Recursively calculate critical path"""
        accumulated += span.duration
        
        if not span.children:
            return accumulated
        
        max_path = accumulated
        for child_id in span.children:
            if child_id in self.spans:
                child_span = self.spans[child_id]
                path = self._calculate_critical_path(child_span, 0.0)
                max_path = max(max_path, accumulated + path)
        
        return max_path
    
    def get_span_tree(self, max_depth: int = 10) -> Dict[str, Any]:
        """Get hierarchical span tree"""
        # Find root
        root = next((s for s in self.spans.values() if s.parent_span_id is None), None)
        if not root:
            return {}
        
        return self._build_tree(root, max_depth, 0)
    
    def _build_tree(self, span: TraceSpan, max_depth: int, current_depth: int) -> Dict[str, Any]:
        """Build tree recursively"""
        if current_depth >= max_depth:
            return {}
        
        tree = {
            "span": span.to_dict(),
            "children": []
        }
        
        for child_id in span.children:
            if child_id in self.spans:
                child_span = self.spans[child_id]
                tree["children"].append(self._build_tree(child_span, max_depth, current_depth + 1))
        
        return tree
    
    def complete(self):
        """Mark trace as complete"""
        self.end_time = time.time()
        self.total_duration = (self.end_time - self.start_time) * 1000
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert trace to dictionary"""
        return {
            "trace_id": self.trace_id,
            "root_span_id": self.root_span_id,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "total_duration_ms": self.total_duration,
            "components_involved": list(self.components_involved),
            "span_count": len(self.spans),
            "spans": {sid: s.to_dict() for sid, s in self.spans.items()}
        }


class DistributedTracingSystem:
    """System for distributed tracing across components"""
    
    def __init__(self, max_traces: int = 1000):
        self.max_traces = max_traces
        self.traces: Dict[str, DistributedTrace] = {}
        self.active_traces: Set[str] = set()
        self.current_trace_id: Optional[str] = None
        self.current_span_stack: List[str] = []  # Stack of span IDs
        
        self.trace_statistics = {
            "total_traces": 0,
            "total_spans": 0,
            "total_duration": 0.0,
            "avg_duration": 0.0,
            "min_duration": float('inf'),
            "max_duration": 0.0,
        }
        
        logger.info("✓ Distributed Tracing System initialized")
    
    def start_trace(self, trace_id: str = None) -> DistributedTrace:
        """Start a new trace"""
        if trace_id is None:
            trace_id = str(uuid.uuid4())
        
        trace = DistributedTrace(trace_id=trace_id)
        self.traces[trace_id] = trace
        self.active_traces.add(trace_id)
        self.current_trace_id = trace_id
        self.current_span_stack = []
        
        logger.debug(f"[TRACE] Started trace {trace_id}")
        
        return trace
    
    def end_trace(self, trace_id: str = None):
        """End a trace"""
        if trace_id is None:
            trace_id = self.current_trace_id
        
        if trace_id not in self.traces:
            logger.warning(f"Trace not found: {trace_id}")
            return
        
        trace = self.traces[trace_id]
        trace.complete()
        
        self.active_traces.discard(trace_id)
        
        # Update statistics
        self.trace_statistics["total_traces"] += 1
        self.trace_statistics["total_spans"] += len(trace.spans)
        self.trace_statistics["total_duration"] += trace.total_duration
        self.trace_statistics["avg_duration"] = (
            self.trace_statistics["total_duration"] / self.trace_statistics["total_traces"]
        )
        self.trace_statistics["min_duration"] = min(
            self.trace_statistics["min_duration"],
            trace.total_duration
        )
        self.trace_statistics["max_duration"] = max(
            self.trace_statistics["max_duration"],
            trace.total_duration
        )
        
        # Publish event
        from src.integration_layer import integration_layer
        integration_layer.event_bus.publish_event(
            "trace.completed",
            "tracing_system",
            {"trace_id": trace_id, "duration_ms": trace.total_duration},
            priority=5
        )
        
        logger.debug(f"[TRACE] Ended trace {trace_id} (duration: {trace.total_duration:.2f}ms)")
    
    def start_span(self,
                  component_id: str,
                  operation: str,
                  trace_id: str = None,
                  parent_span_id: str = None,
                  tags: Dict[str, Any] = None) -> TraceSpan:
        """Start a new span"""
        if trace_id is None:
            trace_id = self.current_trace_id
        
        if trace_id is None:
            trace_id = self.start_trace().trace_id
        
        if trace_id not in self.traces:
            logger.warning(f"Trace not found: {trace_id}")
            return None
        
        trace = self.traces[trace_id]
        
        # Use parent from stack if not provided
        if parent_span_id is None and self.current_span_stack:
            parent_span_id = self.current_span_stack[-1]
        
        # Create span
        span = TraceSpan(
            trace_id=trace_id,
            component_id=component_id,
            operation=operation,
            parent_span_id=parent_span_id,
            tags=tags or {}
        )
        
        # Add to trace
        trace.spans[span.span_id] = span
        trace.components_involved.add(component_id)
        
        # Set root span if first
        if not trace.root_span_id:
            trace.root_span_id = span.span_id
        
        # Add to parent
        if parent_span_id and parent_span_id in trace.spans:
            trace.spans[parent_span_id].children.append(span.span_id)
        
        # Update stack
        self.current_span_stack.append(span.span_id)
        
        logger.debug(f"[TRACE] Started span {span.span_id[:8]} in {component_id}.{operation}")
        
        return span
    
    def end_span(self,
                span_id: str,
                status: str = "completed",
                error: str = None) -> Optional[TraceSpan]:
        """End a span"""
        if not self.current_trace_id:
            return None
        
        trace = self.traces.get(self.current_trace_id)
        if not trace or span_id not in trace.spans:
            logger.warning(f"Span not found: {span_id}")
            return None
        
        span = trace.spans[span_id]
        span.complete(status=status, error=error)
        
        # Pop from stack
        if self.current_span_stack and self.current_span_stack[-1] == span_id:
            self.current_span_stack.pop()
        
        logger.debug(f"[TRACE] Ended span {span_id[:8]} ({status})")
        
        return span
    
    def add_span_tag(self, span_id: str, key: str, value: Any, trace_id: str = None):
        """Add tag to a span"""
        if trace_id is None:
            trace_id = self.current_trace_id
        
        if trace_id not in self.traces:
            return
        
        trace = self.traces[trace_id]
        if span_id in trace.spans:
            trace.spans[span_id].add_tag(key, value)
    
    def add_span_log(self, span_id: str, message: str, level: str = "info", 
                     trace_id: str = None, **fields):
        """Add log to a span"""
        if trace_id is None:
            trace_id = self.current_trace_id
        
        if trace_id not in self.traces:
            return
        
        trace = self.traces[trace_id]
        if span_id in trace.spans:
            trace.spans[span_id].add_log(message, level, **fields)
    
    def get_trace(self, trace_id: str) -> Optional[DistributedTrace]:
        """Get a trace"""
        return self.traces.get(trace_id)
    
    def get_trace_summary(self, trace_id: str) -> Dict[str, Any]:
        """Get summary of a trace"""
        trace = self.traces.get(trace_id)
        if not trace:
            return {}
        
        return {
            "trace_id": trace_id,
            "total_duration_ms": trace.total_duration,
            "critical_path_ms": trace.get_critical_path_duration(),
            "span_count": len(trace.spans),
            "component_count": trace.get_total_components(),
            "components": list(trace.components_involved),
            "status": "completed" if trace.end_time else "active"
        }
    
    def get_slowest_spans(self, trace_id: str, count: int = 10) -> List[Dict[str, Any]]:
        """Get slowest spans in a trace"""
        trace = self.traces.get(trace_id)
        if not trace:
            return []
        
        spans = sorted(
            trace.spans.values(),
            key=lambda s: s.duration,
            reverse=True
        )[:count]
        
        return [
            {
                "component": s.component_id,
                "operation": s.operation,
                "duration_ms": s.duration,
                "status": s.status
            }
            for s in spans
        ]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get tracing statistics"""
        return {
            "traces": self.trace_statistics.copy(),
            "active_traces": len(self.active_traces),
            "stored_traces": len(self.traces),
            "max_traces": self.max_traces
        }
    
    def cleanup_old_traces(self, keep_count: int = 100):
        """Remove oldest traces to stay within limit"""
        if len(self.traces) > keep_count:
            sorted_traces = sorted(
                self.traces.items(),
                key=lambda x: x[1].start_time
            )
            
            for trace_id, _ in sorted_traces[:-keep_count]:
                del self.traces[trace_id]
            
            logger.info(f"Cleaned up traces, keeping {keep_count}")
    
    def print_trace(self, trace_id: str, max_depth: int = 5):
        """Print trace in readable format"""
        trace = self.traces.get(trace_id)
        if not trace:
            logger.warning(f"Trace not found: {trace_id}")
            return
        
        logger.info(f"\n{'='*80}")
        logger.info(f"TRACE: {trace_id}")
        logger.info(f"Duration: {trace.total_duration:.2f}ms")
        logger.info(f"Components: {', '.join(trace.components_involved)}")
        logger.info(f"{'='*80}")
        
        self._print_span_tree(trace, max_depth)
    
    def _print_span_tree(self, trace: DistributedTrace, max_depth: int, depth: int = 0):
        """Print span tree recursively"""
        root = trace.spans.get(trace.root_span_id)
        if root:
            self._print_span_recursive(root, trace, max_depth, depth)
    
    def _print_span_recursive(self, span: TraceSpan, trace: DistributedTrace,
                             max_depth: int, depth: int):
        """Print span and children recursively"""
        if depth >= max_depth:
            return
        
        indent = "  " * depth
        status_symbol = "✓" if span.status == "completed" else "✗" if span.status == "failed" else "→"
        
        logger.info(
            f"{indent}{status_symbol} {span.component_id}.{span.operation} "
            f"({span.duration:.2f}ms)"
        )
        
        for child_id in span.children:
            child = trace.spans.get(child_id)
            if child:
                self._print_span_recursive(child, trace, max_depth, depth + 1)


# Global tracing system instance
distributed_tracing_system = DistributedTracingSystem()


def get_tracing_system() -> DistributedTracingSystem:
    """Get the global distributed tracing system"""
    return distributed_tracing_system


def trace_operation(component_id: str, operation: str):
    """Decorator to trace an operation"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            trace_system = get_tracing_system()
            span = trace_system.start_span(component_id, operation)
            
            try:
                result = func(*args, **kwargs)
                trace_system.end_span(span.span_id, status="completed")
                return result
            except Exception as e:
                trace_system.end_span(span.span_id, status="failed", error=str(e))
                raise
        
        return wrapper
    return decorator
