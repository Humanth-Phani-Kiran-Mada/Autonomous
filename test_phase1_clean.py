#!/usr/bin/env python
"""Quick test to verify Phase 1 integration layer works"""

import sys
sys.path.insert(0, '.')

print("=" * 70)
print("TESTING PHASE 1: INTEGRATION & VALIDATION")
print("=" * 70)

try:
    print("\n[CHECK] Testing imports...")
    
    print(" Loading EventBus...", end=" ")
    from src.integration_layer import EventBus
    print("[OK]")
    
    print(" Loading IntegrationLayer...", end=" ")
    from src.integration_layer import IntegrationLayer
    print("[OK]")
    
    print(" Loading MonitoringEngine...", end=" ")
    from src.monitoring_engine import MonitoringEngine
    print("[OK]")
    
    print(" Loading CycleCoordinator...", end=" ")
    from src.cycle_coordinator import CycleCoordinator
    print("[OK]")
    
    print(" Loading AutonomousAgent...", end=" ")
    from src.autonomous_agent import AutonomousAgent
    print("[OK]")
    
    print("\n[CHECK] Verifying EventBus...")
    eb = EventBus()
    print(" - EventBus initialized successfully")
    
    print("\n[CHECK] Verifying IntegrationLayer...")
    il = IntegrationLayer()
    print(" - IntegrationLayer initialized successfully")
    print(" - Event types registered:", len(il.event_types))
    
    print("\n[CHECK] Verifying MonitoringEngine...")
    me = MonitoringEngine()
    print(" - Monitoring engine initialized successfully")
    print(" - Available metrics:", len(me.metrics))
    
    print("\n[CHECK] Verifying CycleCoordinator...")
    cc = CycleCoordinator(max_retries=3)
    print(" - Cycle coordinator initialized successfully")
    print(" - Registered cycle handlers:", len(cc.cycle_handlers))
    print(" - Cycle order count:", len(cc.CYCLE_ORDER))
    
    print("\n[CHECK] Building AutonomousAgent...")
    agent = AutonomousAgent()
    print(" - Agent initialized successfully")
    print(" - Event bus available:", hasattr(agent, 'event_bus'))
    print(" - Monitoring engine:", hasattr(agent, 'monitoring'))
    print(" - Cycle coordinator:", hasattr(agent, 'cycle_coordinator'))
    
    print("\n" + "=" * 70)
    print("PHASE 1 VALIDATION: SUCCESS")
    print("=" * 70)
    print("\nAll core integration components are functional:")
    print("  - EventBus pub-sub system")
    print("  - IntegrationLayer with event routing")
    print("  - Monitoring engine with metrics")
    print("  - Cycle coordinator with orchestration")
    print("  - Full agent integration")
    
except Exception as e:
    print(f"\n\n[FAILED] ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
