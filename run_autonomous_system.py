#!/usr/bin/env python3
"""
Complete guide to using the autonomous evolution system

This demonstrates all the key features and how to run them.
"""

import sys
import time
import json
from datetime import datetime

# Add src to path
sys.path.insert(0, 'src')

from logger import logger


def print_header(title):
    """Print a formatted header"""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")


def demo_basic_usage():
    """Demo 1: Basic autonomous evolution"""
    print_header("DEMO 1: Basic Autonomous Evolution")
    
    print("Importing the autonomous system...")
    from phase4_integration import get_phase4_integration_layer
    
    print("✓ Creating evolution system...\n")
    evolution = get_phase4_integration_layer()
    
    print("Running ONE autonomous evolution cycle...\n")
    result = evolution.execute_evolution_cycle()
    
    print("\nRESULT:")
    print(f"  Status: {result['status']}")
    print(f"  Duration: {result['duration']:.1f} seconds")
    print(f"  Goals formulated: {result['goals_formulated']}")
    print(f"  Changes implemented: {result['changes_implemented']}")
    print(f"  Improvements adopted: {result['improvements_adopted']}")
    print(f"  Total improvement: {result['total_improvement']:.1%}")
    print(f"  Safety score: {result['safety_score']:.1%}")
    
    return evolution


def demo_check_status(evolution):
    """Demo 2: Check system status"""
    print_header("DEMO 2: Check System Status")
    
    status = evolution.get_evolution_status()
    
    print("Current System Status:")
    print(f"  Cycles completed: {status['cycles_completed']}")
    print(f"  Total improvements: {status['total_improvements']}")
    print(f"  Average safety score: {status['avg_safety_score']:.1%}")
    print(f"  Active goals: {status['active_goals']}")
    
    if status['last_cycle']:
        print("\nLast Cycle Performance:")
        print(f"  Goals formulated: {status['last_cycle']['goals_formulated']}")
        print(f"  Changes implemented: {status['last_cycle']['changes_implemented']}")
        print(f"  Improvements adopted: {status['last_cycle']['improvements_adopted']}")
        print(f"  Total improvement: {status['last_cycle']['total_improvement']:.1%}")
    
    return status


def demo_multiple_cycles(evolution, num_cycles=3):
    """Demo 3: Run multiple cycles"""
    print_header(f"DEMO 3: Run {num_cycles} Autonomous Cycles")
    
    print(f"Running {num_cycles} evolution cycles...\n")
    
    total_improvement = 0
    improvements_found = 0
    
    for i in range(num_cycles):
        print(f"[Cycle {i+1}/{num_cycles}] Starting...")
        
        result = evolution.execute_evolution_cycle()
        
        total_improvement += result['total_improvement']
        if result['improvements_adopted'] > 0:
            improvements_found += 1
        
        print(f"  Result: +{result['total_improvement']:.1%} improvement")
        print(f"  Adopted: {result['improvements_adopted']} improvements\n")
    
    avg_improvement = total_improvement / num_cycles
    
    print("\nSUMMARY:")
    print(f"  Total cycles: {num_cycles}")
    print(f"  Average improvement per cycle: {avg_improvement:.1%}")
    print(f"  Cycles with improvements: {improvements_found}")
    print(f"  Cumulative improvement: {total_improvement:.1%}")


def demo_self_model(evolution):
    """Demo 4: Check self-awareness"""
    print_header("DEMO 4: Self-Model (System Self-Awareness)")
    
    print("Analyzing system state...\n")
    
    snapshot = evolution.self_model.analyze_self()
    
    print("SYSTEM SNAPSHOT:")
    print(f"  Components analyzed: {len(snapshot.components) if snapshot.components else 'N/A'}")
    print(f"  Current efficiency: {snapshot.efficiency:.1%}")
    print(f"  Health score: {snapshot.health_score:.1%}")
    print(f"  Bottlenecks identified: {len(snapshot.bottlenecks) if snapshot.bottlenecks else 'None'}")
    
    weaknesses = evolution.self_model.get_weaknesses()
    print(f"\nWeaknesses found:")
    if weaknesses:
        for i, (weakness, severity) in enumerate(weaknesses[:3], 1):
            print(f"  {i}. {weakness} (severity: {severity:.1%})")
    else:
        print("  None detected ✓")


def demo_value_alignment(evolution):
    """Demo 5: Check safety & values"""
    print_header("DEMO 5: Value Alignment & Safety")
    
    print("Checking alignment report...\n")
    
    report = evolution.value_engine.get_alignment_report()
    
    print("CORE VALUES:")
    for value, score in report['values'].items():
        print(f"  {value:20} : {score:.2f}")
    
    print("\nSAFETY CONSTRAINTS:")
    for constraint in report['constraints']:
        print(f"  ✓ {constraint}")
    
    print("\nDRIFT ANALYSIS:")
    drift = report['drift_analysis']
    print(f"  Drift detected: {drift.get('drift_detected', False)}")
    print(f"  Average alignment: {drift.get('avg_alignment', 0):.2f}")
    print(f"  Safety violations: {drift.get('safety_violations', 0)}")
    
    if drift.get('issues'):
        print("\n  Issues detected:")
        for issue in drift['issues']:
            print(f"    - {issue}")


def demo_goals(evolution):
    """Demo 6: Check autonomous goals"""
    print_header("DEMO 6: Autonomous Goals")
    
    print("Checking active goals...\n")
    
    active_goals = evolution.goal_generator.get_active_goals()
    
    if active_goals:
        print(f"Active Goals ({len(active_goals)}):")
        for i, goal in enumerate(active_goals[:5], 1):
            print(f"\n  {i}. {goal.title}")
            print(f"     Type: {goal.goal_type.value}")
            print(f"     Priority: {goal.priority}/10")
            print(f"     Progress: {goal.progress*100:.1f}%")
            print(f"     Current: {goal.current_value:.1f}")
            print(f"     Target:  {goal.target_value:.1f} {goal.unit}")
    else:
        print("No active goals. Run a cycle to generate goals.")


def demo_reasoning_stats(evolution):
    """Demo 7: Reasoning performance"""
    print_header("DEMO 7: Meta-Reasoning Performance")
    
    stats = evolution.meta_reasoner.get_reasoning_stats()
    
    print("REASONING STATISTICS:")
    print(f"  Total reasoning traces: {stats.get('total_reasoning_traces', 0)}")
    print(f"  Successful: {stats.get('successful', 0)}")
    print(f"  Success rate: {stats.get('success_rate', 'N/A')}")
    print(f"  Avg trace duration: {stats.get('avg_trace_duration', 'N/A')}")
    print(f"  Avg trace steps: {stats.get('avg_trace_steps', 'N/A')}")
    print(f"  Total reasoning time: {stats.get('total_reasoning_time', 'N/A')}")
    
    if 'strategy_performance' in stats:
        print("\n  Strategy Performance:")
        for strategy, perf in stats['strategy_performance'].items():
            print(f"    {strategy}: {perf}")


def demo_knowledge_integration(evolution):
    """Demo 8: Knowledge integration"""
    print_header("DEMO 8: Knowledge Integration")
    
    status = evolution.knowledge_integrator.get_knowledge_status()
    
    print("KNOWLEDGE BASE STATUS:")
    print(f"  Total knowledge items: {status['total_knowledge']}")
    print(f"  Integrated: {status['integrated']}")
    print(f"  Pending: {status['pending']}")
    print(f"  Knowledge sources: {status['sources']}")
    
    if 'by_type' in status:
        print("\n  Knowledge by Type:")
        for ktype, info in status['by_type'].items():
            print(f"    {ktype}: {info['total']} total, " +
                  f"{info['integrated']} integrated, " +
                  f"avg impact: {info.get('avg_impact', 0):.2f}")


def main():
    """Run all demos"""
    print("\n" + "="*70)
    print("  AUTONOMOUS EVOLUTION SYSTEM - COMPLETE DEMO")
    print("="*70)
    
    try:
        # Demo 1: Basic usage
        evolution = demo_basic_usage()
        time.sleep(1)
        
        # Demo 2: Check status
        demo_check_status(evolution)
        time.sleep(1)
        
        # Demo 3: Multiple cycles
        demo_multiple_cycles(evolution, num_cycles=2)
        time.sleep(1)
        
        # Demo 4: Self-model
        demo_self_model(evolution)
        time.sleep(1)
        
        # Demo 5: Value alignment
        demo_value_alignment(evolution)
        time.sleep(1)
        
        # Demo 6: Goals
        demo_goals(evolution)
        time.sleep(1)
        
        # Demo 7: Reasoning stats
        demo_reasoning_stats(evolution)
        time.sleep(1)
        
        # Demo 8: Knowledge
        demo_knowledge_integration(evolution)
        
        # Final summary
        print_header("Demo Complete!")
        print("✓ All demonstrations completed successfully!")
        print("\nYou've seen:")
        print("  ✓ How to initialize the autonomous system")
        print("  ✓ How to run evolution cycles")
        print("  ✓ How to check system status")
        print("  ✓ How to review self-awareness")
        print("  ✓ How to verify safety and values")
        print("  ✓ How to track autonomous goals")
        print("  ✓ How to monitor reasoning quality")
        print("  ✓ How to manage knowledge integration")
        print("\nNEXT STEPS:")
        print("  1. Review PHASE4_QUICKSTART.md for detailed API")
        print("  2. Try run_continuous_evolution.py for endless improvement")
        print("  3. Customize values in value_alignment_engine.py")
        print("  4. Register knowledge sources in knowledge_integrator.py")
        
    except Exception as e:
        logger.error(f"Error during demo: {e}", exc_info=True)
        print(f"\n❌ Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
