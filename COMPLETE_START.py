#!/usr/bin/env python3
"""
COMPLETE AI SYSTEM - START HERE

Your autonomous AI system is ready. Choose how to use it:

1. See it in action (Interactive Demo)
2. Run specific request
3. Build a workflow
4. Autonomous operation
"""
import sys
import os

# Setup path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from logger import logger
from universal_capabilities_engine import get_universal_ai
from complete_ai_system import get_complete_ai_system


def print_banner():
    """Print welcome banner"""
    print("\n" + "╔" + "="*78 + "╗")
    print("║" + " "*78 + "║")
    print("║" + "  COMPLETE AUTONOMOUS AI SYSTEM - READY TO USE  ".center(78) + "║")
    print("║" + " "*78 + "║")
    print("║" + "  Generate • Analyze • Transform • Automate • Learn  ".center(78) + "║")
    print("║" + " "*78 + "║")
    print("╚" + "="*78 + "╝")


def menu_full_demo():
    """Option 1: Run full demonstration"""
    print("\n" + "="*80)
    print("  OPTION 1: INTERACTIVE DEMONSTRATION")
    print("="*80)
    print("""
This will show you:
  1. Code, Image, Video, Audio Generation
  2. Data Analysis & Processing
  3. Multi-Step Workflows
  4. Batch Processing (10 tasks)
  5. Capability Discovery
  6. Self-Learning from Tasks
  7. Natural Language Understanding
  8. Complete Real-World Workflow
    """)
    
    choice = input("Run full demo? (y/n): ").strip().lower()
    if choice == 'y':
        os.system("python src/run_full_demo.py")


def menu_single_request():
    """Option 2: Execute single request"""
    print("\n" + "="*80)
    print("  OPTION 2: SINGLE REQUEST")
    print("="*80)
    print("""
Examples:
  • Generate Python code to implement binary search
  • Create an image of a futuristic space city
  • Generate a video of ocean waves
  • Analyze this dataset: [1, 2, 3, 4, 5, 10, 100]
  • Summarize machine learning algorithms
  • Optimize database queries
  • Generate unit tests for a class
  • Create a landing page design
    """)
    
    request = input("\nEnter your request: ").strip()
    
    if request:
        print("\n" + "-"*80)
        print("Processing request...\n")
        
        ai = get_universal_ai()
        result = ai.do(request)
        
        print(f"✓ Task Type: {result['parsed']['task_type']}")
        print(f"✓ Confidence: {result['parsed']['confidence']:.1%}")
        print(f"✓ Success: {result['success']}")
        
        if result['output']:
            print(f"\n✓ Output Preview:")
            output_str = str(result['output'])
            if len(output_str) > 500:
                print(output_str[:500] + "\n...(truncated)")
            else:
                print(output_str)


def menu_workflow():
    """Option 3: Build and execute workflow"""
    print("\n" + "="*80)
    print("  OPTION 3: MULTI-STEP WORKFLOW")
    print("="*80)
    print("""
Example Workflows:

1. Build a Web API
   - Generate FastAPI application skeleton
   - Add database models
   - Create authentication endpoints
   - Add error handling
   - Generate documentation

2. Content Creation
   - Generate article about a topic
   - Create related images
   - Generate video script
   - Create social media content

3. Data Analysis
   - Load and analyze dataset
   - Generate visualizations
   - Create report
   - Suggest optimizations
    """)
    
    name = input("Workflow name (or 'skip'): ").strip()
    
    if name.lower() != 'skip' and name:
        print(f"\nDescribe workflow steps (one per line, empty to finish):")
        steps = []
        
        while True:
            step = input(f"Step {len(steps)+1}: ").strip()
            if not step:
                break
            steps.append(step)
        
        if steps:
            print("\n" + "-"*80)
            print(f"Executing workflow: {name}\n")
            
            ai = get_universal_ai()
            result = ai.workflow(name, steps)
            
            print(f"✓ Workflow: {result['workflow']}")
            print(f"✓ Steps: {result['completed']}")
            print(f"✓ Successful: {result['successful']}")
            print(f"✓ Success Rate: {result['successful']/result['completed']:.1%}")


def menu_autonomous():
    """Option 4: Continuous autonomous operation"""
    print("\n" + "="*80)
    print("  OPTION 4: AUTONOMOUS OPERATION")
    print("="*80)
    print("""
The system will autonomously improve itself by:

1. Running Phase 4 Evolution (self-analysis)
2. Identifying capability gaps
3. Executing enhancement tasks
4. Learning from execution
5. Generating improvement goals
6. Integrating learnings back
7. Repeating indefinitely

This enables true autonomous self-improvement!

Features:
  ✓ Every 60 seconds: Complete evolution cycle
  ✓ Continuous learning from all tasks
  ✓ Autonomous goal generation
  ✓ Self-optimization
  ✓ Full safety alignment

Status tracking shows:
  - Current evolution phase
  - Tasks completed per cycle
  - Learning extracted
  - Improvements made
  - Autonomous goals generated
    """)
    
    choice = input("Start autonomous operation? (y/n): ").strip().lower()
    
    if choice == 'y':
        print("\n" + "-"*80)
        print("Starting autonomous operation...")
        print("(Press Ctrl+C to stop)\n")
        
        system = get_complete_ai_system()
        system.run_continuous_autonomous_cycle()


def menu_capabilities():
    """Option 5: Show all capabilities"""
    print("\n" + "="*80)
    print("  SYSTEM CAPABILITIES")
    print("="*80)
    
    ai = get_universal_ai()
    
    caps = ai.capabilities()
    
    print(f"\nTotal Capabilities: {caps['total_capabilities']}")
    print(f"Domains: {caps['domains_covered']}\n")
    
    for domain_name, domain_info in caps['domains'].items():
        print(f"\n{domain_name.upper()}")
        print("-" * 40)
        for cap in domain_info['capabilities']:
            metrics = domain_info['metrics'].get(cap, {})
            if metrics.get('total_uses', 0) > 0:
                success = metrics['success_rate']
                print(f"  • {cap}: {success:.1%} success")
            else:
                print(f"  • {cap}")


def menu_system_status():
    """Option 6: System status"""
    print("\n" + "="*80)
    print("  SYSTEM STATUS & RECOMMENDATIONS")
    print("="*80)
    
    ai = get_universal_ai()
    status = ai.status()
    
    print(f"\nTimestamp: {status['timestamp']}")
    print(f"Total Executions: {status['total_executions']}")
    print(f"Total Tasks: {status['total_tasks']}")
    print(f"Success Rate: {status['success_rate']:.1%}")
    print(f"Workflows: {status['workflows_created']}")
    
    print(f"\nCapabilities: {status['total_capabilities']}")
    print(f"Domains: {status['domains_covered']}")
    
    if status['recommendations']:
        print("\nRecommendations:")
        for rec in status['recommendations']:
            print(f"  • {rec}")


def main():
    """Main menu"""
    print_banner()
    
    while True:
        print("\n" + "="*80)
        print("  MAIN MENU")
        print("="*80)
        print("""
1. ⚡ INTERACTIVE DEMO          (See all capabilities)
2. 🎯 SINGLE REQUEST            (Generate code/images/etc)
3. 🔄 MULTI-STEP WORKFLOW       (Build complex solutions)
4. 🤖 AUTONOMOUS OPERATION      (Self-improving AI)
5. 📊 SHOW CAPABILITIES         (What can it do?)
6. 📈 SYSTEM STATUS             (Health & recommendations)
7. 📖 HELP & DOCUMENTATION      (Learn more)
0. ❌ EXIT

        """)
        
        choice = input("Select option (0-7): ").strip()
        
        if choice == '1':
            menu_full_demo()
        elif choice == '2':
            menu_single_request()
        elif choice == '3':
            menu_workflow()
        elif choice == '4':
            menu_autonomous()
        elif choice == '5':
            menu_capabilities()
        elif choice == '6':
            menu_system_status()
        elif choice == '7':
            print("""
DOCUMENTATION:
  • QUICK START:    python src/run_full_demo.py
  • SINGLE REQUEST: ai.do("your request")
  • WORKFLOWS:      ai.workflow("name", [steps])
  • AUTONOMOUS:     system.run_continuous_autonomous_cycle()

EXAMPLES:
  ai.do("Generate Python code to sort a list")
  ai.do("Create an image of a sunset")
  ai.do("Analyze this data: [1,2,3,4,5]")
  ai.workflow("api", ["Generate Flask app", "Add routes", "Add docs"])

FILES:
  COMPLETE_AI_SYSTEM_GUIDE.md     (Full documentation)
  src/complete_ai_system.py       (Master engine)
  src/universal_capabilities_engine.py  (All capabilities)
  src/request_processing_engine.py      (NLP parsing)
  src/task_management_engine.py         (Execution)
            """)
        elif choice == '0':
            print("\n✓ System shutdown. Goodbye!\n")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✓ Interrupted by user")
    except Exception as e:
        logger.error(f"Error: {e}")
        import traceback
        traceback.print_exc()
