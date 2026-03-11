#!/usr/bin/env python
"""Quick test to verify Phase 1 integration layer works"""

import sys
sys.path.insert(0, '.')

print("=" * 70)
print("TESTING PHASE 1: INTEGRATION & VALIDATION")
print("=" * 70)

try:
    print("\n📦 Testing imports...")
    
    print("  Loading monitoring_engine...", end=" ")
    from src.monitoring_engine import monitoring_engine, MonitoringEngine
    print("✅")
    
    print("  Loading integration_layer...", end=" ")
    from src.integration_layer import integration_layer, IntegrationLayer
    print("✅")
    
    print("  Loading cycle_coordinator...", end=" ")
    from src.cycle_coordinator import cycle_coordinator, CycleCoordinator
    print("✅")
    
    print("\n🔧 Testing monitoring engine...")
    print(f"  • Metrics count: {len(monitoring_engine.metrics)}")
    print(f"  • System Health: {monitoring_engine.get_system_health_score():.1f}/100")
    print("  ✅ MonitoringEngine functional")
    
    print("\n📡 Testing integration layer...")
    print(f"  • Event bus subscribers: {len(integration_layer.event_bus.subscribers)}")
    print(f"  • Event history: {len(integration_layer.event_bus.event_history)}")
    print("  ✅ IntegrationLayer functional")
    
    print("\n🔄 Testing cycle coordinator...")
    print(f"  • Defined cycles: {len(cycle_coordinator.CYCLE_ORDER)}")
    print(f"  • Registered handlers: {len(cycle_coordinator.cycle_handlers)}")
    print(f"  • Cycle order: {', '.join(cycle_coordinator.CYCLE_ORDER)}")
    print("  ✅ CycleCoordinator functional")
    
    print("\n" + "=" * 70)
    print("✅✅✅ PHASE 1 VALIDATION COMPLETE - ALL SYSTEMS READY")
    print("=" * 70)

except ImportError as e:
    print(f"\n❌ Import Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
