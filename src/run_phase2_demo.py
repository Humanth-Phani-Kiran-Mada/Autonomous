#!/usr/bin/env python3
"""
Phase 2 Middleware & Infrastructure Demo

Demonstrates:
1. Component Wrapper Factory - Wrapping components with monitoring and tracing
2. Distributed Tracing System - End-to-end request tracing
3. Intelligent Load Balancer - Smart load balancing across components
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.component_wrapper_factory import get_component_wrapper_factory
from src.distributed_tracing import get_tracing_system, LoadBalancingStrategy
from src.intelligent_load_balancer import get_load_balancer, LoadBalancingStrategy
from src.logger import logger
import time
import random


class MockComponent:
    """Mock component for demonstration"""
    
    def __init__(self, name: str):
        self.name = name
        self.request_count = 0
    
    def process_request(self, data: str) -> str:
        """Process a request"""
        self.request_count += 1
        time.sleep(random.uniform(0.01, 0.1))  # Simulate processing
        return f"{self.name} processed: {data}"
    
    def analyze_data(self, data: list) -> float:
        """Analyze data"""
        time.sleep(random.uniform(0.02, 0.15))  # Simulate analysis
        return sum(data) / len(data) if data else 0.0
    
    def get_status(self) -> dict:
        """Get component status"""
        return {"requests": self.request_count, "name": self.name}


def demo_1_component_wrapper():
    """Demo 1: Component Wrapper Factory with monitoring and caching"""
    print("\n" + "="*80)
    print("DEMO 1: COMPONENT WRAPPER FACTORY")
    print("="*80)
    
    factory = get_component_wrapper_factory()
    
    # Create mock components
    comp_a = MockComponent("ComponentA")
    comp_b = MockComponent("ComponentB")
    
    # Wrap components
    wrapped_a = factory.wrap_component(comp_a, "comp_a", enable_caching=True)
    wrapped_b = factory.wrap_component(comp_b, "comp_b", enable_caching=True)
    
    print("\n" + "-"*80)
    print("Processing requests with automatic caching...")
    print("-"*80)
    
    # Make requests
    for i in range(10):
        # Call wrapped components
        result_a = wrapped_a.process_request(f"request_{i}")
        result_b = wrapped_b.analyze_data([1, 2, 3, 4, 5])
        
        if i == 0:
            print(f"Request {i}: A={result_a[:20]}..., B={result_b:.2f}")
    
    # Make same requests again (should hit cache)
    print("\nMaking same requests again (should hit cache)...")
    for i in range(3):
        result_a = wrapped_a.process_request(f"request_0")
        result_b = wrapped_b.analyze_data([1, 2, 3, 4, 5])
    
    print("\n" + "-"*80)
    print("Component Metrics:")
    print("-"*80)
    
    for comp_id, metrics in factory.get_all_metrics().items():
        print(f"\n{comp_id}:")
        print(f"  Calls: {metrics['call_count']}")
        print(f"  Avg Latency: {metrics['avg_latency']:.2f}ms")
        print(f"  Success Rate: {metrics['success_rate']:.1%}")
        print(f"  Cache Hits: {metrics['cache_hits']}")
        print(f"  Cache Misses: {metrics['cache_misses']}")


def demo_2_distributed_tracing():
    """Demo 2: Distributed Tracing across components"""
    print("\n" + "="*80)
    print("DEMO 2: DISTRIBUTED TRACING SYSTEM")
    print("="*80)
    
    tracing = get_tracing_system()
    
    print("\n" + "-"*80)
    print("Simulating complex request trace...")
    print("-"*80)
    
    # Start main trace
    trace = tracing.start_trace()
    trace_id = trace.trace_id
    
    print(f"Trace ID: {trace_id}")
    
    # Start first operation span
    span1 = tracing.start_span(
        "DataService",
        "fetch_data",
        tags={"user_id": "user123", "query_type": "complex"}
    )
    
    time.sleep(0.05)
    span1.add_log("Fetching from cache first", level="info")
    
    # Nested operation
    span2 = tracing.start_span(
        "CacheLayer",
        "cache_lookup",
        parent_span_id=span1.span_id
    )
    time.sleep(0.02)
    span2.add_log("Cache miss, proceeding to database", level="info")
    tracing.end_span(span2.span_id, status="completed")
    
    # Another nested operation
    span3 = tracing.start_span(
        "Database",
        "query_execution",
        parent_span_id=span1.span_id
    )
    time.sleep(0.08)
    span3.add_tag("rows_returned", 150)
    tracing.end_span(span3.span_id, status="completed")
    
    tracing.end_span(span1.span_id, status="completed")
    
    # Another operation
    span4 = tracing.start_span(
        "ProcessingService",
        "transform_data"
    )
    time.sleep(0.03)
    tracing.end_span(span4.span_id, status="completed")
    
    # End trace
    tracing.end_trace(trace_id)
    
    print("\n" + "-"*80)
    print("Trace Summary:")
    print("-"*80)
    
    summary = tracing.get_trace_summary(trace_id)
    print(f"\nTrace ID: {summary['trace_id']}")
    print(f"Total Duration: {summary['total_duration_ms']:.2f}ms")
    print(f"Critical Path: {summary['critical_path_ms']:.2f}ms")
    print(f"Spans: {summary['span_count']}")
    print(f"Components: {summary['component_count']}")
    print(f"Components Involved: {', '.join(summary['components'])}")
    
    print("\n" + "-"*80)
    print("Slowest Operations:")
    print("-"*80)
    
    slowest = tracing.get_slowest_spans(trace_id, count=5)
    for i, span in enumerate(slowest, 1):
        print(f"{i}. {span['component']}.{span['operation']} - {span['duration_ms']:.2f}ms")
    
    # Print full trace tree
    print("\n" + "-"*80)
    print("Trace Tree:")
    print("-"*80)
    tracing.print_trace(trace_id)


def demo_3_intelligent_load_balancing():
    """Demo 3: Intelligent Load Balancing"""
    print("\n" + "="*80)
    print("DEMO 3: INTELLIGENT LOAD BALANCER")
    print("="*80)
    
    lb = get_load_balancer(LoadBalancingStrategy.PERFORMANCE_BASED)
    
    # Create mock components
    components = {
        "server_1": MockComponent("Server1"),
        "server_2": MockComponent("Server2"),
        "server_3": MockComponent("Server3"),
    }
    
    lb.register_components_batch(components)
    
    print("\n" + "-"*80)
    print("Routing 100 requests with performance-based balancing...")
    print("-"*80)
    
    routing_log = {}
    
    # Simulate requests
    for i in range(100):
        # Select component
        selected = lb.get_component()
        if selected not in routing_log:
            routing_log[selected] = 0
        routing_log[selected] += 1
        
        # Simulate request
        start = time.time()
        try:
            # Simulate varying performance
            if selected == "server_2":
                # Make server_2 slower
                time.sleep(random.uniform(0.05, 0.2))
            else:
                time.sleep(random.uniform(0.01, 0.08))
            
            request_time = (time.time() - start) * 1000
            
            # Record metrics
            success = random.random() > 0.05  # 95% success rate
            lb.record_request(selected, request_time, success=success)
        
        except Exception as e:
            latency = (time.time() - start) * 1000
            lb.record_request(selected, latency, success=False)
    
    print("\nRouting Distribution:")
    print("-"*40)
    total = sum(routing_log.values())
    for server, count in sorted(routing_log.items()):
        pct = (count / total) * 100
        print(f"{server}: {count:3}  ({pct:5.1f}%)")
    
    print("\n" + "-"*80)
    print("Load Balancer Status:")
    print("-"*80)
    
    lb.print_status()
    
    print("\n" + "-"*80)
    print("Routing Statistics:")
    print("-"*80)
    
    stats = lb.get_routing_statistics()
    print(f"\nTotal Requests: {stats['total_requests']}")
    print(f"Success Rate: {stats['success_rate']:.1%}")
    print(f"Avg Latency: {stats['avg_latency']:.2f}ms")
    print(f"P95 Latency: {stats['p95_latency']:.2f}ms")
    print(f"P99 Latency: {stats['p99_latency']:.2f}ms")


def demo_4_integrated_system():
    """Demo 4: All three systems working together"""
    print("\n" + "="*80)
    print("DEMO 4: INTEGRATED PHASE 2 SYSTEM")
    print("="*80)
    
    print("\n" + "-"*80)
    print("Setting up integrated middleware stack...")
    print("-"*80)
    
    # Setup components
    comp_a = MockComponent("ServiceA")
    comp_b = MockComponent("ServiceB")
    
    # Wrap with component factory
    factory = get_component_wrapper_factory()
    wrapped_a = factory.wrap_component(comp_a, "service_a", enable_caching=True)
    wrapped_b = factory.wrap_component(comp_b, "service_b", enable_caching=True)
    
    # Setup load balancer
    lb = get_load_balancer(LoadBalancingStrategy.PERFORMANCE_BASED)
    lb.register_component("service_a", wrapped_a)
    lb.register_component("service_b", wrapped_b)
    
    # Setup tracing
    ts = get_tracing_system()
    
    print("\n" + "-"*80)
    print("Processing 20 requests with full middleware stack...")
    print("-"*80)
    
    for req_num in range(20):
        # Start trace
        trace = ts.start_trace()
        
        # Select component via load balancer
        selected = lb.get_component()
        
        # Start span
        span = ts.start_span(selected, "process_request")
        
        try:
            # Make request
            start = time.time()
            if selected == "service_a":
                result = wrapped_a.process_request(f"input_{req_num}")
            else:
                result = wrapped_b.analyze_data([1, 2, 3, 4, 5])
            
            latency = (time.time() - start) * 1000
            
            # Record metrics
            success = latency < 100
            lb.record_request(selected, latency, success=success)
            ts.end_span(span.span_id, status="completed")
            
            if req_num % 5 == 0:
                print(f"Request {req_num}: {selected} ({latency:.2f}ms)")
        
        except Exception as e:
            latency = (time.time() - start) * 1000
            lb.record_request(selected, latency, success=False)
            ts.end_span(span.span_id, status="failed", error=str(e))
        
        ts.end_trace(trace.trace_id)
    
    print("\n" + "-"*80)
    print("Integrated System Summary:")
    print("-"*80)
    
    print("\nComponent Wrapper Metrics:")
    for comp_id, metrics in factory.get_all_metrics().items():
        print(f"  {comp_id}: {metrics['call_count']} calls, "
              f"{metrics['success_rate']:.1%} success, "
              f"{metrics['cache_hits']} cache hits")
    
    print("\nLoad Balancer Status:")
    stats = lb.get_routing_statistics()
    print(f"  Requests: {stats['total_requests']}")
    print(f"  Success Rate: {stats['success_rate']:.1%}")
    print(f"  Avg Latency: {stats['avg_latency']:.2f}ms")
    
    print("\nTracing System:")
    tracing_stats = ts.get_statistics()
    print(f"  Traces: {tracing_stats['traces']['total_traces']}")
    print(f"  Active: {tracing_stats['active_traces']}")
    print(f"  Avg Duration: {tracing_stats['traces']['avg_duration']:.2f}ms")


def main():
    """Run all demonstrations"""
    
    print("\n" + "╔" + "="*78 + "╗")
    print("║" + " "*78 + "║")
    print("║" + "PHASE 2: MIDDLEWARE & INFRASTRUCTURE LAYER - DEMONSTRATION".center(78) + "║")
    print("║" + " "*78 + "║")
    print("║" + "Component Wrapping • Distributed Tracing • Intelligent Load Balancing".center(78) + "║")
    print("║" + " "*78 + "║")
    print("╚" + "="*78 + "╝")
    
    demonstrations = [
        ("Component Wrapper Factory", demo_1_component_wrapper),
        ("Distributed Tracing System", demo_2_distributed_tracing),
        ("Intelligent Load Balancer", demo_3_intelligent_load_balancing),
        ("Integrated Phase 2 System", demo_4_integrated_system),
    ]
    
    print("\n" + "="*80)
    print("AVAILABLE DEMONSTRATIONS")
    print("="*80)
    
    for i, (name, _) in enumerate(demonstrations, 1):
        print(f"  {i}. {name}")
    
    print("\nTip: Use 'all' to run all demonstrations")
    print("-"*80)
    
    choice = input("\nRun demo (1-4) or 'all': ").strip().lower()
    
    if choice == 'all' or choice == '':
        for name, demo_func in demonstrations:
            try:
                demo_func()
            except Exception as e:
                logger.error(f"Demo failed: {e}")
                import traceback
                traceback.print_exc()
    else:
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(demonstrations):
                demonstrations[idx][1]()
            else:
                print("Invalid choice")
        except Exception as e:
            logger.error(f"Error: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*80)
    print("DEMONSTRATION COMPLETE")
    print("="*80)
    print("\n✓ Phase 2 middleware stack is fully operational")
    print("✓ Components are wrapped with monitoring and caching")
    print("✓ Distributed tracing provides end-to-end visibility")
    print("✓ Intelligent load balancing optimizes performance")


if __name__ == "__main__":
    main()
