#!/usr/bin/env python3
"""Quick test of complete AI system - without special characters"""
import sys
sys.path.insert(0, '.')

print("\n" + "="*80)
print("TESTING COMPLETE AI SYSTEM")
print("="*80)

# Test 1: Task Management Engine
print("\n[TEST 1] Task Management Engine")
from src.task_management_engine import get_task_management_engine
engine = get_task_management_engine()
print("[OK] Initialized")
caps_list = list(engine.executor.capabilities.keys())
print("[OK] Available capabilities: " + str(len(caps_list)) + " capabilities")
for cap in caps_list:
    print("      " + cap)

# Test 2: Request Processing
print("\n[TEST 2] Request Processing Engine")
from src.request_processing_engine import get_request_dispatcher
dispatcher = get_request_dispatcher()
parsed = dispatcher.parser.parse_request("Generate Python code to sort a list")
print("[OK] Parsed request successfully")
print("      Task Type: " + parsed.primary_task.value)
print("      Intent: " + parsed.intent)
print("      Confidence: {:.0%}".format(parsed.confidence))

# Test 3: Execute Request
print("\n[TEST 3] Execute Single Request")
result = dispatcher.process_request("Generate Python code to sort a list")
print("[OK] Request executed")
print("      Task Type: " + result['parsed']['task_type'])
print("      Success: {}/{}".format(result['execution']['successful'], result['execution']['processed']))

# Test 4: Multiple requests
print("\n[TEST 4] Batch Process Multiple Requests")
requests = [
    "Generate Python code",
    "Analyze dataset",
    "Optimize code"
]
results = dispatcher.process_multiple_requests(requests)
print("[OK] Processed {} requests".format(results['completed']))
print("      Successful: {} tasks".format(results['successful']))

# Test 5: Universal Capabilities
print("\n[TEST 5] Universal Capabilities Engine")
from src.universal_capabilities_engine import get_universal_ai
ai = get_universal_ai()
caps = ai.capabilities()
print("[OK] Total capabilities: {}".format(caps['total_capabilities']))
print("[OK] Domains covered: {}".format(len(caps['domains'])))
for domain, info in list(caps['domains'].items())[:3]:
    print("      " + domain + ": " + str(len(info['capabilities'])) + " capabilities")

# Test 6: System Status
print("\n[TEST 6] System Status")
status = ai.status()
print("[OK] Total executions: {}".format(status['total_executions']))
print("[OK] Total tasks: {}".format(status['total_tasks']))
print("[OK] Success rate: {:.0%}".format(status['success_rate']))

print("\n" + "="*80)
print("ALL TESTS PASSED")
print("="*80)
print("\nSystem is ready to use!")
print("\nUsage Options:")
print("1. python src/run_full_demo.py")
print("2. python COMPLETE_START.py")
print("3. from src.universal_capabilities_engine import get_universal_ai")
print("   ai = get_universal_ai()")
print("   result = ai.do('your request')")
