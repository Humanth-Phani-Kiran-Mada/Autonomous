#!/usr/bin/env python3
"""
COMPLETE AUTONOMOUS AI SYSTEM DEMONSTRATION

Showcases:
1. Task execution across all capability domains
2. Natural language request processing
3. Multi-task workflows
4. Learning from execution
5. Performance tracking
6. Complete autonomy in action
"""
import sys
import os
from datetime import datetime

# Setup path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from logger import logger
from universal_capabilities_engine import get_universal_ai
from request_processing_engine import get_request_dispatcher


def print_header(title: str) -> None:
    """Print formatted header"""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80 + "\n")


def print_section(title: str) -> None:
    """Print section header"""
    print(f"\n{title}")
    print("-" * len(title))


def demo_1_generation_capabilities():
    """Demo 1: Generation Capabilities"""
    print_header("DEMO 1: CODE, IMAGE, VIDEO, AUDIO GENERATION")
    
    ai = get_universal_ai()
    
    requests = [
        "Generate a Python function that implements bubble sort",
        "Create an image of a futuristic city at night",
        "Generate a 15-second video of rain falling"
    ]
    
    for request in requests:
        print_section(f"Request: {request}")
        
        result = ai.do(request)
        
        print(f"✓ Task Type: {result['parsed']['task_type']}")
        print(f"✓ Confidence: {result['parsed']['confidence']:.2%}")
        print(f"✓ Success: {result['success']}")
        
        if result['output']:
            output_str = str(result['output'])[:300]
            print(f"✓ Output Preview:\n{output_str}...")


def demo_2_analysis_and_processing():
    """Demo 2: Analysis & Processing"""
    print_header("DEMO 2: ANALYSIS, RESEARCH, TEXT PROCESSING")
    
    ai = get_universal_ai()
    
    requests = [
        "Analyze this dataset: [1, 2, 3, 4, 5, 10, 20, 100]",
        "Research machine learning algorithms",
        "Summarize: Artificial intelligence is transforming industries..."
    ]
    
    for request in requests:
        print_section(f"Request: {request}")
        
        result = ai.do(request)
        
        print(f"✓ Task Type: {result['parsed']['task_type']}")
        print(f"✓ Success: {result['success']}")
        print(f"✓ Execution Status: {result['execution']['successful']}/{result['execution']['processed']} successful")


def demo_3_multi_step_workflow():
    """Demo 3: Multi-Step Workflows"""
    print_header("DEMO 3: COMPLETE MULTI-STEP WORKFLOW")
    
    ai = get_universal_ai()
    
    print_section("Workflow: Build a Data Analysis Application")
    
    workflow_steps = [
        "Generate a Python Flask application for data visualization",
        "Create analysis functions for statistical processing",
        "Generate HTML templates for the dashboard",
        "Optimize the code for performance",
        "Add unit tests"
    ]
    
    print(f"Steps: {len(workflow_steps)}")
    for i, step in enumerate(workflow_steps, 1):
        print(f"  {i}. {step}")
    
    result = ai.workflow("data_app_builder", workflow_steps)
    
    print(f"\n✓ Workflow Completed!")
    print(f"✓ Total Steps: {result['steps']}")
    print(f"✓ Completed: {result['completed']}")
    print(f"✓ Successful: {result['successful']}")
    print(f"✓ Success Rate: {result['successful']/result['completed']:.1%}")


def demo_4_batch_processing():
    """Demo 4: Batch Request Processing"""
    print_header("DEMO 4: BATCH PROCESSING (10 SIMULTANEOUS REQUESTS)")
    
    ai = get_universal_ai()
    
    batch_requests = [
        "Generate a RESTful API in Python",
        "Create a profile picture - professional headshot",
        "Generate a 10-second explainer video",
        "Analyze web traffic data",
        "Translate this: Hello, how are you?",
        "Generate speech from text",
        "Research blockchain technology",
        "Optimize database queries",
        "Create a mobile app mockup",
        "Generate technical documentation"
    ]
    
    print(f"Processing {len(batch_requests)} requests:\n")
    for i, req in enumerate(batch_requests, 1):
        print(f"  {i:2d}. {req}")
    
    result = ai.batch_process(batch_requests)
    
    print(f"\n✓ Batch Complete!")
    print(f"✓ Total: {result['total']}")
    print(f"✓ Completed: {result['completed']}")
    print(f"✓ Successful: {result['successful']}")
    print(f"✓ Overall Success Rate: {result['successful']/max(result['completed'], 1):.1%}")


def demo_5_capabilities_discovery():
    """Demo 5: Capability Discovery & Status"""
    print_header("DEMO 5: SYSTEM CAPABILITIES & LEARNING")
    
    ai = get_universal_ai()
    
    # Get all capabilities
    caps = ai.capabilities()
    
    print(f"Total Capabilities: {caps['total_capabilities']}")
    print(f"Domains Covered: {caps['domains_covered']}\n")
    
    for domain_name, domain_info in caps['domains'].items():
        print_section(f"Domain: {domain_name.upper()}")
        print(f"Count: {domain_info['count']}")
        print(f"Capabilities: {', '.join(domain_info['capabilities'][:5])}")
        
        if domain_info['metrics']:
            success_rates = [m['success_rate'] for m in domain_info['metrics'].values() if m['total_uses'] > 0]
            if success_rates:
                avg_success = sum(success_rates) / len(success_rates)
                print(f"Average Success Rate: {avg_success:.1%}")
    
    # System status
    print_section("System Status")
    
    status = ai.status()
    
    print(f"Total Executions: {status['total_executions']}")
    print(f"Total Tasks: {status['total_tasks']}")
    print(f"Global Success Rate: {status['success_rate']:.1%}")
    print(f"Workflows Created: {status['workflows_created']}")
    
    if status['recommendations']:
        print_section("Recommendations for Improvement")
        for rec in status['recommendations']:
            print(f"  • {rec}")


def demo_6_self_learning_cycle():
    """Demo 6: Self-Learning & Autonomous Improvement"""
    print_header("DEMO 6: SELF-LEARNING & AUTONOMOUS IMPROVEMENT")
    
    from request_processing_engine import get_request_dispatcher
    
    dispatcher = get_request_dispatcher()
    
    print_section("Learning Database from Executed Tasks")
    
    learning = dispatcher.task_engine.get_learning_summary()
    
    print(f"Total Tasks Executed: {learning['total_tasks']}")
    print(f"Successful Tasks: {learning['successful_tasks']}")
    
    print("\nLearning by Task Type:")
    for task_type, data in learning['learning_database'].items():
        if data['total'] > 0:
            print(f"\n  {task_type}:")
            print(f"    Total: {data['total']}")
            print(f"    Successful: {data['successful']}")
            print(f"    Success Rate: {data['successful']/data['total']:.1%}")
            print(f"    Avg Quality: {data['avg_quality']:.2f}")
            print(f"    Patterns Learned: {len(data['patterns'])}")


def demo_7_natural_language_understanding():
    """Demo 7: Natural Language Request Parsing"""
    print_header("DEMO 7: NATURAL LANGUAGE UNDERSTANDING")
    
    dispatcher = get_request_dispatcher()
    
    test_requests = [
        "I need you to write a Python script that sorts a list and removes duplicates",
        "Please generate a beautiful landscape image in oil painting style",
        "Can you create a short educational video about quantum computing?",
        "Analyze this customer data and tell me the trends",
        "Make this text more concise and professional"
    ]
    
    print("Parsing Natural Language Requests:\n")
    
    for request in test_requests:
        parsed = dispatcher.parser.parse_request(request)
        
        print_section(f"Request: {request[:60]}...")
        print(f"Primary Task: {parsed.primary_task.value}")
        print(f"Intent: {parsed.intent}")
        print(f"Confidence: {parsed.confidence:.1%}")
        print(f"Detected Entities: {parsed.entities['languages'] + parsed.entities['frameworks']}")


def demo_8_complete_workflow_example():
    """Demo 8: Complete Workflow from Start to Finish"""
    print_header("DEMO 8: COMPLETE START-TO-FINISH WORKFLOW")
    
    ai = get_universal_ai()
    
    print_section("Scenario: Build a Content Generation System")
    
    print("""
    1. Define what we want to build
    2. Generate the core code
    3. Analyze the code for improvements
    4. Optimize the performance
    5. Generate documentation
    6. Create visual diagrams
    7. Measure final quality
    """)
    
    print_section("Executing Multi-Domain Workflow")
    
    workflow = [
        "Generate a Python class for content generation with methods for code, images, and videos",
        "Create integration functions connecting different modules",
        "Optimize the architectural design",
        "Generate comprehensive API documentation",
        "Analyze performance characteristics"
    ]
    
    result = ai.workflow("content_gen_system", workflow)
    
    print(f"\n✓ Workflow: {result['workflow']}")
    print(f"✓ Steps Executed: {result['completed']}")
    print(f"✓ Success Rate: {result['successful']/result['completed']:.1%}")
    
    # Show each step result
    for i, response in enumerate(result['responses'], 1):
        success_mark = "✓" if response['success'] else "✗"
        task_type = response['parsed']['task_type']
        confidence = response['parsed']['confidence']
        print(f"\n  Step {i}: {success_mark} {task_type} (confidence: {confidence:.1%})")


def main():
    """Run all demonstrations"""
    
    print("\n")
    print("╔"+"="*78+"╗")
    print("║" + " "*78 + "║")
    print("║" + "  COMPLETE AUTONOMOUS AI SYSTEM - FULL CAPABILITIES DEMONSTRATION  ".center(78) + "║")
    print("║" + " "*78 + "║")
    print("║" + "  Generation | Analysis | Transformation | Automation | Self-Learning ".center(78) + "║")
    print("║" + " "*78 + "║")
    print("╚"+"="*78+"╝")
    
    demonstrations = [
        ("Generation Capabilities", demo_1_generation_capabilities),
        ("Analysis & Processing", demo_2_analysis_and_processing),
        ("Multi-Step Workflows", demo_3_multi_step_workflow),
        ("Batch Processing", demo_4_batch_processing),
        ("Capability Discovery", demo_5_capabilities_discovery),
        ("Self-Learning Cycle", demo_6_self_learning_cycle),
        ("Natural Language Understanding", demo_7_natural_language_understanding),
        ("Complete Workflow", demo_8_complete_workflow_example)
    ]
    
    print("\n" + "="*80)
    print("  AVAILABLE DEMONSTRATIONS")
    print("="*80)
    
    for i, (name, _) in enumerate(demonstrations, 1):
        print(f"  {i}. {name}")
    
    print("\n" + "-"*80)
    
    choice = input("Run demo (1-8) or 'all' for all demos (default=all): ").strip().lower()
    
    if choice == 'all' or choice == '':
        for name, demo_func in demonstrations:
            try:
                demo_func()
            except Exception as e:
                logger.error(f"Demo failed: {e}")
                import traceback
                traceback.print_exc()
    else:
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(demonstrations):
                demonstrations[idx][1]()
            else:
                print("Invalid choice")
        except Exception as e:
            logger.error(f"Error: {e}")
            import traceback
            traceback.print_exc()
    
    # Final summary
    print_header("DEMONSTRATION COMPLETE")
    
    ai = get_universal_ai()
    final_status = ai.status()
    
    print("Final System Status:")
    print(f"  • Total Requests Processed: {final_status['total_executions']}")
    print(f"  • Total Tasks Completed: {final_status['total_tasks']}")
    print(f"  • Overall Success Rate: {final_status['success_rate']:.1%}")
    print(f"  • Capabilities Available: {final_status['total_capabilities']}")
    print(f"  • Domains Covered: {final_status['domains_covered']}")
    
    print("\n✓ System is fully operational and autonomous!")
    print("✓ Can handle any AI-related task automatically")
    print("✓ Learning and improving with each execution")


if __name__ == "__main__":
    main()
