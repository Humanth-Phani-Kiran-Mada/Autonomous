#!/usr/bin/env python3
"""
02_distributed_tracing.py - Distributed Tracing System Example

This example demonstrates how to use the Distributed Tracing System
to track requests end-to-end across services.

Run:
    python 02_distributed_tracing.py
"""

import time
import json
from typing import Any, Dict, List, Optional


# Simulated Distributed Tracing System (simplified)
class MockSpan:
    """Represents a span in a trace"""
    
    def __init__(self, span_id: str, name: str, start_time: float):
        self.span_id = span_id
        self.name = name
        self.start_time = start_time
        self.end_time = None
        self.status = None
        self.attributes = {}
        self.events = []
    
    def add_attribute(self, key: str, value: any):
        """Add attribute to span"""
        self.attributes[key] = value
    
    def add_event(self, name: str, attributes: Dict = None):
        """Add event to span"""
        self.events.append({
            'name': name,
            'attributes': attributes or {}
        })
    
    def end(self, status: str = 'success', error: str = None):
        """End the span"""
        self.end_time = time.time()
        self.status = status
        if error:
            self.add_attribute('error', error)
    
    @property
    def duration_ms(self) -> float:
        """Duration in milliseconds"""
        if self.end_time:
            return (self.end_time - self.start_time) * 1000
        return None


class MockTrace:
    """Represents a trace for a request"""
    
    def __init__(self, trace_id: str, service: str):
        self.trace_id = trace_id
        self.service = service
        self.spans = {}
        self.start_time = time.time()
        self.completed = False
    
    def create_span(self, name: str) -> MockSpan:
        """Create a span in this trace"""
        span_id = f"span_{len(self.spans)}"
        span = MockSpan(span_id, name, time.time())
        self.spans[span_id] = span
        return span
    
    def complete(self):
        """Mark trace as complete"""
        self.completed = True
    
    def get_total_duration_ms(self) -> float:
        """Get total trace duration"""
        if not self.spans:
            return 0
        
        start = min(s.start_time for s in self.spans.values())
        end = max(s.end_time for s in self.spans.values() if s.end_time)
        return (end - start) * 1000 if end else 0


class MockDistributedTracingSystem:
    """Simplified mock of the actual tracing system"""
    
    def __init__(self):
        self.traces = {}
        self.completed_traces = []
    
    def start_trace(self, trace_id: str, service: str) -> MockTrace:
        """Start a new trace"""
        trace = MockTrace(trace_id, service)
        self.traces[trace_id] = trace
        return trace
    
    def complete_trace(self, trace: MockTrace):
        """Mark trace as complete and store"""
        if trace.completed:
            self.completed_traces.append(trace)
    
    def get_trace(self, trace_id: str) -> Optional[MockTrace]:
        """Get a trace by ID"""
        # Check completed traces first
        for trace in self.completed_traces:
            if trace.trace_id == trace_id:
                return trace
        
        # Then check active traces
        return self.traces.get(trace_id)
    
    def get_recent_traces(self, n: int = 10) -> List[MockTrace]:
        """Get recent completed traces"""
        return self.completed_traces[-n:]


def demo_basic_tracing():
    """Demo: Basic Request Tracing"""
    print("\n" + "="*60)
    print("DEMO 1: BASIC REQUEST TRACING")
    print("="*60)
    
    tracing = MockDistributedTracingSystem()
    
    print("\n1. Starting trace for request...")
    trace = tracing.start_trace('req_001', 'api_service')
    
    print("\n2. Creating spans for operations...")
    
    # Validate request
    span1 = trace.create_span('validate_request')
    print("   - validate_request span created")
    time.sleep(0.02)  # Simulate 20ms
    span1.end(status='success')
    print(f"     ✓ Completed in {span1.duration_ms:.1f}ms")
    
    # Database query
    span2 = trace.create_span('database_query')
    print("   - database_query span created")
    time.sleep(0.05)  # Simulate 50ms
    span2.add_attribute('query', 'SELECT * FROM users')
    span2.add_attribute('rows_returned', 42)
    span2.end(status='success')
    print(f"     ✓ Completed in {span2.duration_ms:.1f}ms")
    
    # Serialize response
    span3 = trace.create_span('serialize_response')
    print("   - serialize_response span created")
    time.sleep(0.01)  # Simulate 10ms
    span3.end(status='success')
    print(f"     ✓ Completed in {span3.duration_ms:.1f}ms")
    
    print("\n3. Completing trace...")
    trace.complete()
    tracing.complete_trace(trace)
    
    print(f"\n4. Trace Summary:")
    print(f"   Trace ID:        {trace.trace_id}")
    print(f"   Service:         {trace.service}")
    print(f"   Spans:           {len(trace.spans)}")
    print(f"   Total latency:   {trace.get_total_duration_ms():.1f}ms")
    print(f"   Status:          Completed ✓")


def demo_nested_spans():
    """Demo: Nested Spans (Service Calls)"""
    print("\n" + "="*60)
    print("DEMO 2: NESTED SPANS - MULTI-SERVICE CALLS")
    print("="*60)
    
    tracing = MockDistributedTracingSystem()
    
    print("\n1. Starting trace for client request...")
    trace = tracing.start_trace('req_002', 'frontend')
    
    print("\n2. Simulating Service Call Chain:")
    print("   Frontend → AuthService → Database")
    
    # Frontend operation
    span_frontend = trace.create_span('frontend_call')
    print("\n   [Frontend Service]")
    time.sleep(0.02)
    
    # AuthService call (child span)
    span_auth = trace.create_span('auth_service_call')
    print("   └─ [Auth Service]")
    time.sleep(0.03)
    
    # Database call (grandchild span)
    span_db = trace.create_span('database_query')
    print("      └─ [Database]")
    time.sleep(0.02)
    span_db.add_attribute('query', 'SELECT * FROM permissions')
    span_db.end(status='success')
    print(f"         ✓ Query completed in {span_db.duration_ms:.1f}ms")
    
    # Auth completes
    span_auth.end(status='success')
    print(f"       ✓ Auth completed in {span_auth.duration_ms:.1f}ms")
    
    # Frontend completes
    span_frontend.end(status='success')
    print(f"   ✓ Frontend request completed in {span_frontend.duration_ms:.1f}ms")
    
    trace.complete()
    tracing.complete_trace(trace)
    
    print(f"\n3. Complete Trace View:")
    print(f"   Total latency: {trace.get_total_duration_ms():.1f}ms")
    print(f"   Spans: {len(trace.spans)}")


def demo_error_tracking():
    """Demo: Error Tracking in Traces"""
    print("\n" + "="*60)
    print("DEMO 3: ERROR TRACKING")
    print("="*60)
    
    tracing = MockDistributedTracingSystem()
    
    print("\n1. Starting trace...")
    trace = tracing.start_trace('req_003', 'api_service')
    
    print("\n2. Executing operations...")
    
    # Successful operation
    span1 = trace.create_span('validate_input')
    time.sleep(0.01)
    span1.end(status='success')
    print("   ✓ validate_input: SUCCESS")
    
    # Operation with error
    span2 = trace.create_span('authenticate_user')
    print("   ⟳ authenticate_user: executing...")
    time.sleep(0.02)
    
    # Simulate error
    error_msg = "Invalid credentials"
    span2.end(status='failure', error=error_msg)
    print(f"   ✗ authenticate_user: FAILURE - {error_msg}")
    
    # Retry operation
    span3 = trace.create_span('retry_auth')
    time.sleep(0.01)
    span3.end(status='success')
    print("   ✓ retry_auth: SUCCESS (after retry)")
    
    trace.complete()
    tracing.complete_trace(trace)
    
    print(f"\n3. Error Summary:")
    print(f"   Total spans: {len(trace.spans)}")
    failed_spans = [s for s in trace.spans.values() if s.status == 'failure']
    print(f"   Failed spans: {len(failed_spans)}")
    for span in failed_spans:
        print(f"     - {span.name}: {span.attributes.get('error', 'Unknown')}")


def demo_trace_querying():
    """Demo: Querying Traces"""
    print("\n" + "="*60)
    print("DEMO 4: TRACE QUERYING AND ANALYSIS")
    print("="*60)
    
    tracing = MockDistributedTracingSystem()
    
    print("\n1. Generating sample traces...")
    
    # Generate multiple traces
    traces_data = [
        ('req_001', 30),
        ('req_002', 45),
        ('req_003', 25),
        ('req_004', 150),  # Slow request
        ('req_005', 35),
    ]
    
    for trace_id, latency_ms in traces_data:
        trace = tracing.start_trace(trace_id, 'api_service')
        
        # Create a span
        span = trace.create_span('process_request')
        time.sleep(latency_ms / 1000)
        span.add_attribute('latency_ms', latency_ms)
        span.end(status='success')
        
        trace.complete()
        tracing.complete_trace(trace)
    
    print(f"   ✓ Generated {len(traces_data)} traces")
    
    print("\n2. Querying traces...")
    
    # Get all traces
    all_traces = tracing.get_recent_traces(n=10)
    print(f"\n   Total traces: {len(all_traces)}")
    
    # Analyze latencies
    latencies = [t.get_total_duration_ms() for t in all_traces]
    print(f"\n   Latency Analysis:")
    print(f"     Min:    {min(latencies):.1f}ms")
    print(f"     Max:    {max(latencies):.1f}ms")
    print(f"     Avg:    {sum(latencies)/len(latencies):.1f}ms")
    
    # Find slow traces
    slow_traces = [t for t in all_traces if t.get_total_duration_ms() > 100]
    print(f"\n   Slow Traces (> 100ms): {len(slow_traces)}")
    for trace in slow_traces:
        print(f"     - {trace.trace_id}: {trace.get_total_duration_ms():.1f}ms")


def main():
    """Run all demos"""
    print("\n" + "="*60)
    print("PHASE 2 - DISTRIBUTED TRACING EXAMPLES")
    print("="*60)
    
    # Run demos
    demo_basic_tracing()
    demo_nested_spans()
    demo_error_tracking()
    demo_trace_querying()
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print("""
✓ Distributed Tracing provides:
  1. End-to-end request tracking
  2. Nested spans for service calls
  3. Error and event tracking
  4. Complete trace querying
  
✓ Benefits:
  1. Full visibility into request flow
  2. Easy identification of bottlenecks
  3. Error correlation across services
  4. Complete request audit trail
  5. Performance analysis and optimization
""")
    print("="*60 + "\n")


if __name__ == '__main__':
    main()
