#!/usr/bin/env python
"""Comprehensive system diagnostic and issue detection"""

import sys
import os
sys.path.insert(0, '.')

def test_imports():
    """Test all core modules can be imported"""
    print("\n" + "="*70)
    print(" TESTING MODULE IMPORTS")
    print("="*70)
    
    modules = [
        ('src.logger', 'logger'),
        ('src.config', None),
        ('src.knowledge_base', 'KnowledgeBase'),
        ('src.memory_manager', 'MemoryManager'),
        ('src.learning_engine', 'LearningEngine'),
        ('src.reasoning_engine', 'ReasoningEngine'),
        ('src.web_crawler', 'WebCrawler'),
        ('src.self_model', 'SelfModel'),
        ('src.meta_learner', 'MetaLearner'),
        ('src.bayesian_reasoner', 'BayesianReasoner'),
        ('src.autonomous_goal_generator', 'AutonomousGoalGenerator'),
        ('src.introspection_engine', 'IntrospectionEngine'),
        ('src.memory_consolidation', 'MemoryConsolidation'),
        ('src.error_recovery', 'ErrorRecoverySystem'),
        ('src.integration_layer', 'IntegrationLayer'),
        ('src.monitoring_engine', 'MonitoringEngine'),
        ('src.cycle_coordinator', 'CycleCoordinator'),
        ('src.theory_building_engine', 'TheoryBuildingEngine'),
        ('src.curriculum_learning_system', 'CurriculumLearningSystem'),
        ('src.knowledge_synthesis_engine', 'KnowledgeSynthesisEngine'),
        ('src.adaptive_reasoning_engine', 'AdaptiveReasoningEngine'),
        ('src.capability_expansion_engine', 'CapabilityExpansionEngine'),
        ('src.evolutionary_learning', 'EvolutionaryLearningEngine'),
        ('src.attention_system', 'AttentionSystem'),
        ('src.architectural_modifier', 'ArchitecturalModifier'),
        ('src.autonomous_agent', 'AutonomousAgent'),
    ]
    
    failed = []
    for module_name, class_name in modules:
        try:
            mod = __import__(module_name, fromlist=[class_name] if class_name else [])
            if class_name:
                getattr(mod, class_name)
            print(f"  ✅ {module_name:<45} OK")
        except Exception as e:
            print(f"  ❌ {module_name:<45} ERROR: {str(e)[:60]}")
            failed.append((module_name, str(e)))
    
    return failed

def test_config():
    """Test configuration"""
    print("\n" + "="*70)
    print(" TESTING CONFIGURATION")
    print("="*70)
    
    try:
        import config
        print(f"  ✅ Project root: {config.PROJECT_ROOT}")
        print(f"  ✅ Data dir: {config.DATA_DIR}")
        print(f"  ✅ Logs dir: {config.LOGS_DIR}")
        print(f"  ✅ Autonomous mode: {config.AUTONOMOUS_MODE_ENABLED}")
        return True
    except Exception as e:
        print(f"  ❌ Configuration error: {e}")
        return False

def test_data_directories():
    """Test data directories are created"""
    print("\n" + "="*70)
    print(" TESTING DATA DIRECTORIES")
    print("="*70)
    
    import config
    dirs = [
        config.DATA_DIR,
        config.LOGS_DIR,
        config.MEMORY_DIR,
        config.KNOWLEDGE_DIR,
        config.CACHE_DIR
    ]
    
    for d in dirs:
        exists = d.exists()
        status = "✅" if exists else "❌"
        print(f"  {status} {d}")
        if not exists:
            try:
                d.mkdir(parents=True, exist_ok=True)
                print(f"     → Created")
            except Exception as e:
                print(f"     → Failed to create: {e}")

def test_initialization():
    """Test component initialization"""
    print("\n" + "="*70)
    print(" TESTING COMPONENT INITIALIZATION")
    print("="*70)
    
    try:
        from src.autonomous_agent import AutonomousAgent
        print("  • Initializing AutonomousAgent...")
        agent = AutonomousAgent()
        print("  ✅ AutonomousAgent initialized successfully")
        return agent
    except Exception as e:
        print(f"  ❌ Failed to initialize AutonomousAgent: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    print("\n" + "="*70)
    print(" AUTONOMOUS AI SYSTEM DIAGNOSTIC")
    print("="*70)
    
    # Test imports
    failed_imports = test_imports()
    
    # Test config
    config_ok = test_config()
    
    # Test directories
    test_data_directories()
    
    # Test initialization
    agent = test_initialization()
    
    # Summary
    print("\n" + "="*70)
    print(" DIAGNOSTIC SUMMARY")
    print("="*70)
    
    if failed_imports:
        print(f"\n⚠️  {len(failed_imports)} import failures:")
        for module, error in failed_imports[:5]:
            print(f"   - {module}: {error[:50]}")
    else:
        print("\n✅ All imports successful")
    
    if config_ok:
        print("✅ Configuration loaded")
    else:
        print("❌ Configuration failed")
    
    if agent:
        print("✅ Agent initialization successful")
    else:
        print("❌ Agent initialization failed")
    
    print("\n" + "="*70)

if __name__ == "__main__":
    main()
