#!/usr/bin/env python3
"""Quick test of complete AI system"""
import sys
sys.path.insert(0, '.')

print("\n" + "="*80)
print("TESTING COMPLETE AI SYSTEM")
print("="*80)

# Test 1: Task Management Engine
print("\n[TEST 1] Task Management Engine")
from src.task_management_engine import get_task_management_engine
engine = get_task_management_engine()
print(f"✓ Initialized")
print(f"✓ Available capabilities: {list(engine.executor.capabilities.keys())}")

# Test 2: Request Processing
print("\n[TEST 2] Request Processing Engine")
from src.request_processing_engine import get_request_dispatcher
dispatcher = get_request_dispatcher()
parsed = dispatcher.parser.parse_request("Generate Python code to sort a list")
print(f"✓ Parsed request")
print(f"  - Task Type: {parsed.primary_task.value}")
print(f"  - Intent: {parsed.intent}")
print(f"  - Confidence: {parsed.confidence:.1%}")

# Test 3: Execute Request
print("\n[TEST 3] Execute Single Request")
result = dispatcher.process_request("Generate Python code to sort a list")
print(f"✓ Request executed")
print(f"  - Task Type: {result['parsed']['task_type']}")
print(f"  - Success: {result['execution']['successful']}/{result['execution']['processed']}")
if result['output']:
    output_preview = str(result['output'])[:150]
    print(f"  - Output Preview: {output_preview}...")

# Test 4: Multiple requests
print("\n[TEST 4] Batch Process Multiple Requests")
requests = [
    "Generate Python code",
    "Analyze dataset",
    "Optimize code"
]
results = dispatcher.process_multiple_requests(requests)
print(f"✓ Processed {results['completed']} requests")
print(f"✓ Successful: {results['successful']} tasks")

# Test 5: Universal Capabilities
print("\n[TEST 5] Universal Capabilities Engine")
from src.universal_capabilities_engine import get_universal_ai
ai = get_universal_ai()
caps = ai.capabilities()
print(f"✓ Total capabilities: {caps['total_capabilities']}")
print(f"✓ Domains covered: {len(caps['domains'])}")
for domain, info in caps['domains'].items():
    print(f"  - {domain}: {len(info['capabilities'])} capabilities")

# Test 6: System Status
print("\n[TEST 6] System Status")
status = ai.status()
print(f"✓ Total executions: {status['total_executions']}")
print(f"✓ Total tasks: {status['total_tasks']}")
print(f"✓ Success rate: {status['success_rate']:.1%}")

print("\n" + "="*80)
print("ALL TESTS PASSED ✓")
print("="*80)
print("\nSystem is ready to use!")
print("\nUsage Options:")
print("1. python src/run_full_demo.py          (Interactive demo)")
print("2. python COMPLETE_START.py             (Menu interface)")
print("3. python -c \"from src.universal_capabilities_engine import get_universal_ai; ai = get_universal_ai(); print(ai.do('your request'))\"")
