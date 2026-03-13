#!/usr/bin/env python3
"""
Continuous Autonomous Evolution
Run this to have the system continuously improve itself
"""

import sys
import time
from datetime import datetime

sys.path.insert(0, 'src')

from logger import logger


def print_banner():
    """Print startup banner"""
    print("""
    ╔════════════════════════════════════════════════════════════════╗
    ║                                                                ║
    ║        AUTONOMOUS EVOLUTION SYSTEM - CONTINUOUS MODE          ║
    ║                                                                ║
    ║     The system will now improve itself autonomously in a       ║
    ║     continuous loop. Each cycle takes 30-60 seconds.          ║
    ║                                                                ║
    ║     Press Ctrl+C to stop                                       ║
    ║                                                                ║
    ╚════════════════════════════════════════════════════════════════╝
    """)


def format_time(seconds):
    """Format seconds to readable time"""
    if seconds < 1:
        return f"{seconds*1000:.0f}ms"
    elif seconds < 60:
        return f"{seconds:.1f}s"
    else:
        return f"{seconds/60:.1f}m"


def print_cycle_result(cycle_num, result, total_time):
    """Print formatted cycle result"""
    
    status = "✓" if result['status'] == 'complete' else "✗"
    
    print(f"\n╔═ CYCLE #{cycle_num:03d} {'='*53}╗")
    print(f"║ Status: {status} {result['status']:40}")
    print(f"║ Duration: {format_time(result.get('duration', 0)):45}")
    print(f"║ Total runtime: {format_time(total_time):42}")
    print(f"╠════════════════════════════════════════════════════════════════╣")
    print(f"║ Goals formulated: {result.get('goals_formulated', 0):48}")
    print(f"║ Changes implemented: {result.get('changes_implemented', 0):45}")
    print(f"║ Improvements adopted: {result.get('improvements_adopted', 0):44}")
    print(f"║ Total improvement: {result.get('total_improvement', 0):48.1%}")
    print(f"║ Safety score: {result.get('safety_score', 0):.1%}{' ':47}")
    print(f"╚════════════════════════════════════════════════════════════════╝")


def print_summary(cycles, total_improvement, start_time, improvements_found):
    """Print session summary"""
    runtime = time.time() - start_time
    avg_improvement = total_improvement / max(cycles, 1)
    
    print(f"\n╔════════════════════════════════════════════════════════════════╗")
    print(f"║                   SESSION SUMMARY                             ║")
    print(f"╠════════════════════════════════════════════════════════════════╣")
    print(f"║ Cycles completed: {cycles:50}")
    print(f"║ Total runtime: {format_time(runtime):42}")
    print(f"║ Avg time per cycle: {format_time(runtime/max(cycles, 1)):35}")
    print(f"║ Cycles with improvements: {improvements_found:40}")
    print(f"║ Total system improvement: {total_improvement:37.1%}")
    print(f"║ Avg improvement per cycle: {avg_improvement:37.1%}")
    print(f"╚════════════════════════════════════════════════════════════════╝")


def run_continuous_evolution(intervals=60):
    """
    Run continuous autonomous evolution
    
    Args:
        intervals: seconds between cycles (default 60)
    """
    
    print_banner()
    
    print("Initializing autonomous evolution system...")
    from phase4_integration import get_phase4_integration_layer
    
    evolution = get_phase4_integration_layer()
    print("✓ System initialized\n")
    
    cycles = 0
    total_improvement = 0.0
    improvements_found = 0
    start_time = time.time()
    
    try:
        while True:
            cycles += 1
            cycle_start = time.time()
            
            # Run evolution cycle
            result = evolution.execute_evolution_cycle()
            
            # Track metrics
            total_improvement += result.get('total_improvement', 0)
            if result.get('improvements_adopted', 0) > 0:
                improvements_found += 1
            
            cycle_duration = time.time() - cycle_start
            total_runtime = time.time() - start_time
            
            # Print result
            print_cycle_result(cycles, result, total_runtime)
            
            # Wait for next cycle
            if intervals > 0:
                print(f"\nNext cycle in {intervals} seconds (press Ctrl+C to stop)...", end='', flush=True)
                for i in range(intervals):
                    time.sleep(1)
                    if i % 10 == 0 and i > 0:
                        remaining = intervals - i
                        print(f"\n  {remaining}s remaining...", end='', flush=True)
                print("\r" + " "*60 + "\r", end='', flush=True)
    
    except KeyboardInterrupt:
        print("\n\n" + "="*70)
        print("Interrupted by user")
        print("="*70)
        print_summary(cycles, total_improvement, start_time, improvements_found)
        return 0
    
    except Exception as e:
        logger.error(f"Error during continuous evolution: {e}", exc_info=True)
        print(f"\n✗ Error: {e}")
        print_summary(cycles, total_improvement, start_time, improvements_found)
        return 1


def main():
    """Entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Run autonomous evolution system continuously"
    )
    parser.add_argument(
        '--interval',
        type=int,
        default=60,
        help='Seconds between cycles (default: 60)'
    )
    parser.add_argument(
        '--fast',
        action='store_true',
        help='Fast mode: minimal wait between cycles'
    )
    
    args = parser.parse_args()
    
    interval = 5 if args.fast else args.interval
    
    return run_continuous_evolution(intervals=interval)


if __name__ == "__main__":
    sys.exit(main())
