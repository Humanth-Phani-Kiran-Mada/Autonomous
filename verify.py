#!/usr/bin/env python
"""Simple verification that the system can be imported and initialized"""

import sys
sys.path.insert(0, '.')

def main():
    print("\n" + "="*70)
    print(" AUTONOMOUS AI SYSTEM - VERIFICATION TEST")
    print("="*70 + "\n")
    
    # Test 1: Config
    try:
        print("[1/5] Testing configuration...")
        import config
        print(f"     [OK] Config loaded from {config.PROJECT_ROOT}")
    except Exception as e:
        print(f"     [FAIL] Config error: {e}")
        return False
    
    # Test 2: Core modules
    try:
        print("[2/5] Testing core module imports...")
        from src.core.knowledge_base import KnowledgeBase
        from src.core.memory_manager import MemoryManager
        from src.core.learning_engine import LearningEngine
        from src.core.reasoning_engine import ReasoningEngine
        from src.core.web_crawler import WebCrawler
        print("     [OK] All core modules imported")
    except Exception as e:
        print(f"     [FAIL] Import error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test 3: Advanced modules
    try:
        print("[3/5] Testing advanced module imports...")
        from src.autonomous_agent import AutonomousAgent
        from src.meta_learner import MetaLearner
        from src.introspection_engine import IntrospectionEngine
        print("     [OK] All advanced modules imported")
    except Exception as e:
        print(f"     [FAIL] Advanced import error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test 4: Integration layer
    try:
        print("[4/5] Testing integration layer...")
        from src.integration_layer import integration_layer, IntegrationLayer
        from src.monitoring_engine import monitoring_engine, MonitoringEngine
        from src.cycle_coordinator import cycle_coordinator, CycleCoordinator
        print("     [OK] Integration layer imported")
    except Exception as e:
        print(f"     [FAIL] Integration error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test 5: Agent initialization (brief)
    try:
        print("[5/5] Testing agent initialization...")
        from src.autonomous_agent import AutonomousAgent
        agent = AutonomousAgent()
        print("     [OK] AutonomousAgent initialized successfully")
    except Exception as e:
        print(f"     [FAIL] Agent initialization error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n" + "="*70)
    print(" SUCCESS - ALL TESTS PASSED - SYSTEM READY")
    print("="*70 + "\n")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
