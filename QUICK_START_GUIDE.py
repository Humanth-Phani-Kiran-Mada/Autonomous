#!/usr/bin/env python3
"""
Simple one-shot demo - no complex imports
Just show basic functionality
"""

import sys
import os

# Set Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

print("\n" + "="*70)
print("  AUTONOMOUS EVOLUTION SYSTEM - QUICK DEMO")
print("="*70 + "\n")

# Try to import
print("Step 1: Import the autonomous system...")
try:
    # Import core components directly
    exec("""
import sys
sys.path.insert(0, 'src')

from learning_loop import AutonomousLearningLoop
from self_model import SystemSelfModel
from autonomous_goal_generator import AutonomousGoalGenerator
from code_modification_engine import CodeModificationEngine
from experimentation_framework import ExperimentationFramework
from meta_reasoning_engine import MetaReasoningEngine
from parameter_auto_tuner import ParameterAutoTuner
from resource_reallocator import ResourceReallocator
from knowledge_integrator import KnowledgeIntegrator
from value_alignment_engine import ValueAlignmentEngine
from logger import logger

print("  ✓ All components imported successfully")
""")
    
except Exception as e:
    print(f"  ❌ Import failed: {e}")
    print("\n  Trying alternative approach...")
    print("  Please run: python run_simple_demo.py")
    sys.exit(1)

print("\nStep 2: What you can do with this system")
print("-" * 70)

print("""
Three simple ways to use the autonomous system:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

METHOD 1: RUN THE FULL DEMO (Recommended)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Create a file called 'demo.py' with:

    from phase4_integration import get_phase4_integration_layer
    
    evolution = get_phase4_integration_layer()
    result = evolution.execute_evolution_cycle()
    
    print(f"Improvements: {result['improvements_adopted']}")
    print(f"Safety: {result['safety_score']:.1%}")

Then run:
    python demo.py

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

METHOD 2: CONTINUOUS EVOLUTION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Run the endless loop script:

    python run_continuous_evolution.py

The system will keep improving itself every 60 seconds until you
press Ctrl+C. It will show progress for each cycle.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

METHOD 3: DETAILED WALKTHROUGH
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Read: HOW_TO_USE_AND_RUN.md

This has step-by-step examples, customization options, and
troubleshooting.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

What the system does:

    1. OBSERVE           -> Analyzes itself
    2. FORMULATE_GOALS   -> Identifies improvements
    3. GENERATE_OPTIONS  -> Creates solutions
    4. EVALUATE_OPTIONS  -> Checks safety
    5. IMPLEMENT         -> Applies changes
    6. EXPERIMENT        -> Tests safely
    7. MEASURE           -> Quantifies impact
    8. INTEGRATE         -> Adopts winners
    9. REFLECT           -> Learns for next cycle

Then REPEATS... continuously getting smarter!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

System Features:

    ✅ Fully autonomous - no human intervention needed
    ✅ Continuous loops - keeps improving forever
    ✅ Safe by design - all changes validated
    ✅ Measurable - tracks every improvement
    ✅ Explainable - you can audit every decision
    ✅ Reversible - all changes can be rolled back
    ✅ Value-aligned - respects human values

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

QUICK START RIGHT NOW:

1. Open a terminal

2. Run:
   
   cd c:\\Users\\hphaniki\\Downloads\\Autonomous
   python run_continuous_evolution.py

3. Watch the system improve itself!

   To stop: Press Ctrl+C

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

print("\n✅ System is ready to use!")
print("\nNext steps:")
print("  1. Look at: HOW_TO_USE_AND_RUN.md")
print("  2. Run: python run_continuous_evolution.py")
print("  3. Personalize in: src/value_alignment_engine.py")
print("="*70 + "\n")
