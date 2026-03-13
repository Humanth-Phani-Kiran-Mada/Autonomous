#!/usr/bin/env python3
"""
run_all_examples.py - Run All Phase 2 Examples

This script runs all Phase 2 examples in sequence, demonstrating
each component and their integration.

Run:
    python run_all_examples.py
"""

import subprocess
import sys
import os
from pathlib import Path


def print_header(title: str, char: str = "="):
    """Print a formatted header"""
    width = 70
    line = char * width
    print(f"\n{line}")
    print(f"{title:^{width}}")
    print(f"{line}")


def run_example(script_name: str, description: str) -> bool:
    """Run a single example script"""
    print_header(f"Running: {description}", "-")
    
    try:
        # Get script path
        script_path = Path(__file__).parent / script_name
        
        if not script_path.exists():
            print(f"✗ Script not found: {script_path}")
            return False
        
        # Run script
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=False,
            check=False
        )
        
        return result.returncode == 0
    
    except Exception as e:
        print(f"✗ Error running {script_name}: {e}")
        return False


def main():
    """Run all examples"""
    print_header("PHASE 2 - COMPLETE EXAMPLES RUN", "=")
    
    examples = [
        ('01_basic_wrapping.py', 'Component Wrapper Factory Examples'),
        ('02_distributed_tracing.py', 'Distributed Tracing System Examples'),
        ('03_load_balancing.py', 'Intelligent Load Balancer Examples'),
        ('04_full_integration.py', 'Full Phase 2 Integration Example'),
    ]
    
    results = {}
    
    print("\nRunning examples...\n")
    
    for script, description in examples:
        success = run_example(script, description)
        results[script] = success
    
    # Print summary
    print_header("EXAMPLES SUMMARY", "=")
    
    print("\nResults:")
    for script, description in examples:
        status = "✓ PASSED" if results[script] else "✗ FAILED"
        print(f"  {status}: {description}")
    
    # Overall result
    print("\n" + "-" * 70)
    all_passed = all(results.values())
    
    if all_passed:
        print("✓ ALL EXAMPLES COMPLETED SUCCESSFULLY")
        print("\nYou now understand:")
        print("  1. How Component Wrapper caches and optimizes")
        print("  2. How Distributed Tracing tracks requests")
        print("  3. How Load Balancer distributes traffic")
        print("  4. How all three work together")
    else:
        print("✗ Some examples failed. Check output above.")
    
    print("\nNext Steps:")
    print("  1. Review the example code")
    print("  2. Read the component guides in guides/ folder")
    print("  3. Integrate Phase 2 into your application")
    print("  4. Monitor metrics from docs/PERFORMANCE.md")
    
    print("\nDocumentation:")
    print("  - README.md - Start here")
    print("  - QUICK_START.md - 5 minute overview")
    print("  - GETTING_STARTED.md - 15 minute guide")
    print("  - guides/ - Component-specific guides")
    print("  - docs/ - Complete reference documentation")
    
    print("\n" + "="*70 + "\n")
    
    return 0 if all_passed else 1


if __name__ == '__main__':
    sys.exit(main())
