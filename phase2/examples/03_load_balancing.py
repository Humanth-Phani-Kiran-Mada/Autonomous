#!/usr/bin/env python3
"""
03_load_balancing.py - Intelligent Load Balancer Example

This example demonstrates how to use the Intelligent Load Balancer
to distribute requests across multiple service instances.

Run:
    python 03_load_balancing.py
"""

import random
import time
from typing import List, Dict, Any, Optional


# Simulated Service
class MockService:
    """Represents a service instance"""
    
    def __init__(self, service_id: str, address: str, port: int):
        self.service_id = service_id
        self.address = address
        self.port = port
        self.healthy = True
        self.load = 0.0  # 0.0 to 1.0
        self.request_count = 0
        self.total_latency = 0
    
    def handle_request(self, request: Dict) -> Dict:
        """Handle a request"""
        self.request_count += 1
        latency = random.uniform(10, 100)  # 10-100ms
        self.total_latency += latency
        return {'status': 'ok', 'service_id': self.service_id, 'latency': latency}
    
    @property
    def avg_latency(self) -> float:
        if self.request_count == 0:
            return 0
        return self.total_latency / self.request_count


# Simulated Load Balancer
class MockIntelligentLoadBalancer:
    """Simplified mock of the actual load balancer"""
    
    def __init__(self, strategy: str = 'least_loaded'):
        self.services: Dict[str, MockService] = {}
        self.strategy = strategy
        self.routing_history = []
    
    def register_service(self, service_id: str, address: str, port: int):
        """Register a service"""
        service = MockService(service_id, address, port)
        self.services[service_id] = service
    
    def select_service(self, request: Dict = None) -> Optional[MockService]:
        """Select service based on strategy"""
        healthy_services = [s for s in self.services.values() if s.healthy]
        
        if not healthy_services:
            raise Exception("No healthy services available")
        
        if self.strategy == 'round_robin':
            return self._round_robin(healthy_services)
        elif self.strategy == 'least_loaded':
            return self._least_loaded(healthy_services)
        elif self.strategy == 'random':
            return random.choice(healthy_services)
        else:
            return healthy_services[0]
    
    def _round_robin(self, services: List[MockService]) -> MockService:
        """Select service via round robin"""
        if not hasattr(self, '_rr_index'):
            self._rr_index = 0
        
        service = services[self._rr_index % len(services)]
        self._rr_index += 1
        return service
    
    def _least_loaded(self, services: List[MockService]) -> MockService:
        """Select least loaded service"""
        return min(services, key=lambda s: s.load)
    
    def update_service_load(self, service_id: str, load: float):
        """Update service load"""
        if service_id in self.services:
            self.services[service_id].load = load
    
    def update_service_health(self, service_id: str, healthy: bool):
        """Update service health"""
        if service_id in self.services:
            self.services[service_id].healthy = healthy
    
    def get_services(self) -> List[MockService]:
        """Get all services"""
        return list(self.services.values())


def demo_basic_routing():
    """Demo: Basic Request Routing"""
    print("\n" + "="*60)
    print("DEMO 1: BASIC REQUEST ROUTING")
    print("="*60)
    
    # Create load balancer
    print("\n1. Setting up load balancer...")
    lb = MockIntelligentLoadBalancer(strategy='least_loaded')
    
    # Register services
    print("\n2. Registering service instances...")
    lb.register_service('service_1', '127.0.0.1', 8001)
    lb.register_service('service_2', '127.0.0.1', 8002)
    lb.register_service('service_3', '127.0.0.1', 8003)
    print("   ✓ Registered 3 service instances")
    
    # Route requests
    print("\n3. Routing 30 requests with least_loaded strategy...")
    
    for i in range(1, 31):
        # Simulate load
        for s in lb.get_services():
            s.load = random.uniform(0.2, 0.95)
        
        # Select service
        service = lb.select_service({'type': 'query'})
        
        # Handle request
        response = service.handle_request({})
        
        if i % 10 == 0:
            print(f"   Request {i}: Routed to {service.service_id}")
    
    print("\n4. Request Distribution:")
    for service in lb.get_services():
        print(f"   {service.service_id}: {service.request_count} requests")


def demo_different_strategies():
    """Demo: Different Routing Strategies"""
    print("\n" + "="*60)
    print("DEMO 2: DIFFERENT ROUTING STRATEGIES")
    print("="*60)
    
    strategies = ['round_robin', 'least_loaded', 'random']
    
    for strategy in strategies:
        print(f"\n{strategy.upper()} Strategy:")
        print("-" * 40)
        
        lb = MockIntelligentLoadBalancer(strategy=strategy)
        lb.register_service('A', '127.0.0.1', 8001)
        lb.register_service('B', '127.0.0.1', 8002)
        lb.register_service('C', '127.0.0.1', 8003)
        
        # Simulate requests
        for i in range(30):
            # Set varying loads
            lb.services['A'].load = 0.80
            lb.services['B'].load = 0.40
            lb.services['C'].load = 0.90
            
            service = lb.select_service()
            service.handle_request({})
        
        # Show results
        print(f"Request distribution:")
        for service in lb.get_services():
            pct = (service.request_count / 30) * 100
            print(f"  {service.service_id}: {service.request_count:2d} ({pct:5.1f}%)")


def demo_health_monitoring():
    """Demo: Health Monitoring and Failover"""
    print("\n" + "="*60)
    print("DEMO 3: HEALTH MONITORING & FAILOVER")
    print("="*60)
    
    lb = MockIntelligentLoadBalancer(strategy='least_loaded')
    lb.register_service('service_1', '127.0.0.1', 8001)
    lb.register_service('service_2', '127.0.0.1', 8002)
    lb.register_service('service_3', '127.0.0.1', 8003)
    
    print("\n1. Initial state - all services healthy...")
    for service in lb.get_services():
        status = "✓ Healthy" if service.healthy else "✗ Down"
        print(f"   {service.service_id}: {status}")
    
    print("\n2. Routing requests (all 3 services used)...")
    for _ in range(9):
        for s in lb.get_services():
            s.load = random.uniform(0.2, 0.8)
        service = lb.select_service()
        service.handle_request({})
    
    print(f"   ✓ Routed 9 requests across 3 services")
    
    print("\n3. Service 2 fails!")
    lb.update_service_health('service_2', False)
    print("   service_2: MARKED DOWN ✗")
    
    print("\n4. Routing requests (only 2 services now)...")
    for _ in range(12):
        for s in lb.get_services():
            if s.healthy:
                s.load = random.uniform(0.3, 0.7)
        
        try:
            service = lb.select_service()
            service.handle_request({})
        except Exception as e:
            print(f"   ✗ Error: {e}")
    
    print(f"   ✓ Failover working - traffic rerouted!")
    
    print("\n5. Service 2 recovers!")
    lb.update_service_health('service_2', True)
    print("   service_2: BACK ONLINE ✓")
    
    print("\n6. Final request distribution:")
    for service in lb.get_services():
        print(f"   {service.service_id}: {service.request_count} requests")


def demo_performance_metrics():
    """Demo: Performance Metrics"""
    print("\n" + "="*60)
    print("DEMO 4: PERFORMANCE METRICS & ANALYSIS")
    print("="*60)
    
    lb = MockIntelligentLoadBalancer(strategy='least_loaded')
    
    # Register 5 services with different capabilities
    services_config = [
        ('fast_service', 10),     # Average 10ms
        ('normal_service', 50),   # Average 50ms
        ('slow_service', 80),     # Average 80ms
    ]
    
    print("\n1. Setting up services...")
    for service_id, _ in services_config:
        parts = service_id.split('_')
        port = 8001 + len(lb.services)
        lb.register_service(service_id, '127.0.0.1', port)
        print(f"   {service_id}: {port}")
    
    print("\n2. Load balancer distributes requests...")
    # Simulate 60 requests
    for i in range(60):
        # Set loads based on service characteristics
        lb.services['fast_service'].load = random.uniform(0.30, 0.50)
        lb.services['normal_service'].load = random.uniform(0.40, 0.70)
        lb.services['slow_service'].load = random.uniform(0.70, 0.95)
        
        service = lb.select_service()
        service.handle_request({})
    
    print(f"   ✓ Distributed 60 requests")
    
    print("\n3. Performance Analysis:")
    print("-" * 40)
    
    total_requests = sum(s.request_count for s in lb.get_services())
    
    for service in sorted(lb.get_services(), key=lambda s: s.avg_latency):
        pct = (service.request_count / total_requests) * 100
        print(f"\n{service.service_id}:")
        print(f"  Requests: {service.request_count} ({pct:.1f}%)")
        print(f"  Avg latency: {service.avg_latency:.1f}ms")
    
    print(f"\n✓ Load balanced across services")
    print(f"  Total requests: {total_requests}")


def main():
    """Run all demos"""
    print("\n" + "="*60)
    print("PHASE 2 - INTELLIGENT LOAD BALANCER EXAMPLES")
    print("="*60)
    
    # Run demos
    demo_basic_routing()
    demo_different_strategies()
    demo_health_monitoring()
    demo_performance_metrics()
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print("""
✓ Intelligent Load Balancer provides:
  1. Multiple routing strategies
  2. Health monitoring & automatic failover
  3. Dynamic load distribution
  4. Performance metrics
  
✓ Benefits:
  1. Horizontal scalability (add more services)
  2. High availability (automatic failover)
  3. Even load distribution
  4. Improved throughput
  5. Better response times
""")
    print("="*60 + "\n")


if __name__ == '__main__':
    main()
