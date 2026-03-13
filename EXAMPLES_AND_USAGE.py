"""
Practical Examples: Using the Improved Autonomous AI System

This module demonstrates how to use all the new improvements together
in real-world scenarios.
"""

from typing import List, Dict, Any
from pathlib import Path
import asyncio

# Import new improvements
from src.exceptions import (
    ValidationException, KnowledgeBaseException, CrawlerException
)
from src.utilities import (
    retry_with_backoff, measure_performance, cached,
    CircuitBreaker, get_circuit_breaker
)
from src.validators import (
    validate_url, validate_content, validate_priority,
    ValidationChain
)
from src.types_and_constants import (
    KnowledgeEntry, Goal, SystemConstants,
    MemoryType, GoalStatus
)
from src.knowledge_base import KnowledgeBase
from src.logger import logger


# ============================================================================
# Example 1: Safe Knowledge Base Operations with Error Handling
# ============================================================================

def example_1_safe_kb_operations():
    """
    Example: Safe knowledge base operations with proper error handling.
    
    Shows how to:
    - Use validation functions
    - Handle specific exceptions
    - Provide informative error messages
    """
    logger.info("=" * 70)
    logger.info("Example 1: Safe Knowledge Base Operations")
    logger.info("=" * 70)
    
    kb = KnowledgeBase()
    
    # Example 1.1: Adding knowledge with validation
    try:
        # These will be validated automatically in add_knowledge
        knowledge_id = kb.add_knowledge(
            content="Deep learning is revolutionizing computer vision by enabling systems to learn hierarchical representations of visual data",
            source="https://arxiv.org/papers/deep-learning",
            knowledge_type="article",
            metadata={"domain": "computer_vision", "difficulty": "advanced"}
        )
        logger.info(f"✓ Successfully added knowledge: {knowledge_id}")
    except ValidationException as e:
        logger.error(f"✗ Validation failed: {e.message} (Code: {e.error_code})")
        logger.error(f"  Context: {e.context}")
    except KnowledgeBaseException as e:
        logger.error(f"✗ Knowledge base error: {e.message}")
    
    # Example 1.2: Searching with error handling
    try:
        results = kb.search(query="deep learning", top_k=5, threshold=0.3)
        logger.info(f"✓ Found {len(results)} matching knowledge entries")
        for i, result in enumerate(results, 1):
            score = result.get("similarity_score", "N/A")
            logger.info(f"  {i}. {result['type']}: {score}")
    except KnowledgeBaseException as e:
        logger.error(f"✗ Search failed: {e.message}")
    
    # Example 1.3: Batch operations with validation chain
    try:
        urls = (ValidationChain()
            .validate("https://example.com/page1", validate_url, "URL 1")
            .validate("https://example.com/page2", validate_url, "URL 2")
            .execute())
        
        logger.info(f"✓ Validated {len(urls)} URLs successfully")
    except ValidationException as e:
        logger.error(f"✗ Validation chain failed: {e.message}")


# ============================================================================
# Example 2: Resilient Web Crawling with Circuit Breakers
# ============================================================================

@retry_with_backoff(max_retries=3, initial_delay=1.0)
@measure_performance
async def fetch_with_retry(url: str) -> str:
    """
    Fetch URL with automatic retry and performance monitoring.
    
    The @retry_with_backoff decorator automatically retries with exponential
    backoff. The @measure_performance decorator logs execution time.
    """
    # Simulate async web fetch
    logger.info(f" Fetching: {url}")
    await asyncio.sleep(0.5)
    return f"Content from {url}"


def example_2_resilient_crawling():
    """
    Example: Resilient crawling with circuit breakers and retries.
    
    Shows how to:
    - Use retry decorators
    - Implement circuit breaker pattern
    - Handle transient failures
    """
    logger.info("=" * 70)
    logger.info("Example 2: Resilient Web Crawling")
    logger.info("=" * 70)
    
    # Example 2.1: Simple retry with backoff
    async def demo_retry():
        try:
            result = await fetch_with_retry("https://example.com")
            logger.info(f"✓ Fetch succeeded: {result}")
        except Exception as e:
            logger.error(f"✗ Fetch failed after retries: {e}")
    
    asyncio.run(demo_retry())
    
    # Example 2.2: Circuit breaker for multiple endpoints
    crawler_cb = get_circuit_breaker("crawler")
    
    urls = [
        "https://api.example.com/data1",
        "https://api.example.com/data2",
        "https://api.example.com/data3",
    ]
    
    for url in urls:
        try:
            # Circuit breaker will open if too many failures occur
            # and prevent cascading failures
            logger.info(f"Attempting to fetch from {url}...")
            # In real scenario: crawler_cb.call(fetch_page, url)
            logger.info(f"✓ Successfully fetched {url}")
        except Exception as e:
            logger.warning(f"✗ Failed to fetch {url}: {e}")


# ============================================================================
# Example 3: Performance Monitoring and Caching
# ============================================================================

@cached(ttl_seconds=300)
def get_expensive_computation(dataset_size: int) -> Dict[str, Any]:
    """
    Simulate expensive computation with caching.
    
    The @cached decorator caches results for 5 minutes.
    Subsequent calls within TTL return cached result immediately.
    """
    logger.info(f"  Computing for dataset size {dataset_size}...")
    # Simulate expensive work
    import time
    time.sleep(0.1)
    return {
        "size": dataset_size,
        "result": dataset_size ** 2,
        "timestamp": str(Path.ctime(Path(__file__)))
    }


@measure_performance
def example_3_performance_monitoring():
    """
    Example: Performance monitoring and caching.
    
    Shows how to:
    - Cache expensive operations
    - Monitor execution time
    - Reduce redundant computations
    """
    logger.info("=" * 70)
    logger.info("Example 3: Performance Monitoring & Caching")
    logger.info("=" * 70)
    
    # First call: computation runs
    logger.info("First call (cache miss):")
    result1 = get_expensive_computation(1000)
    logger.info(f"✓ Result: {result1}")
    
    # Second call: returns cached result immediately
    logger.info("\nSecond call (cache hit):")
    result2 = get_expensive_computation(1000)
    logger.info(f"✓ Result (from cache): {result2}")
    
    # Different parameter: computation runs again
    logger.info("\nThird call (different parameter, cache miss):")
    result3 = get_expensive_computation(2000)
    logger.info(f"✓ Result: {result3}")


# ============================================================================
# Example 4: Type-Safe Data Structures
# ============================================================================

def example_4_type_safe_structures():
    """
    Example: Using type-safe data structures with TypedDict.
    
    Shows how to:
    - Use TypedDict for data validation
    - Leverage IDE autocomplete
    - Maintain type safety throughout code
    """
    logger.info("=" * 70)
    logger.info("Example 4: Type-Safe Data Structures")
    logger.info("=" * 70)
    
    # Creating a goal with type safety
    goal: Goal = {
        "id": 1,
        "name": "Master Deep Learning",
        "description": "Develop expertise in deep learning fundamentals",
        "priority": 0.95,
        "deadline": "2026-12-31",
        "created_at": "2026-03-13T10:00:00",
        "status": GoalStatus.IN_PROGRESS,  # Type checker ensures valid status
        "progress": 0.45,
        "sub_goals": [
            "Learn neural networks",
            "Implement CNNs",
            "Study transformers"
        ]
    }
    
    # IDE provides autocomplete for all keys
    logger.info(f"Goal: {goal['name']}")
    logger.info(f"Priority: {goal['priority']}")
    logger.info(f"Status: {goal['status']}")
    logger.info(f"Progress: {goal['progress']}%")
    
    # Creating a knowledge entry with type safety
    knowledge: KnowledgeEntry = {
        "id": "KB_20260313_001",
        "content": "Neural networks are composed of interconnected layers...",
        "source": "https://example.com/nn-guide",
        "type": "article",
        "created_at": "2026-03-13T10:00:00",
        "accessed_count": 5,
        "relevance_score": 0.85,
        "metadata": {"difficulty": "intermediate", "domain": "deep_learning"}
    }
    
    logger.info(f"✓ Knowledge entry created: {knowledge['id']}")
    logger.info(f"  Score: {knowledge['relevance_score']}")
    logger.info(f"  Type: {knowledge['type']}")
    
    # Using system constants (no magic numbers)
    is_expert_content = knowledge['relevance_score'] > SystemConstants.EXPERT_THRESHOLD
    is_proficient_content = knowledge['relevance_score'] > SystemConstants.PROFICIENT_THRESHOLD
    
    logger.info(f"  Expert level: {is_expert_content}")
    logger.info(f"  Proficient level: {is_proficient_content}")


# ============================================================================
# Example 5: Complex Validation Scenarios
# ============================================================================

def example_5_validation_scenarios():
    """
    Example: Complex validation with ValidationChain.
    
    Shows how to:
    - Validate multiple inputs at once
    - Handle validation errors
    - Create readable validation pipelines
    """
    logger.info("=" * 70)
    logger.info("Example 5: Complex Validation Scenarios")
    logger.info("=" * 70)
    
    # Scenario: Creating a new knowledge base entry from user input
    user_inputs = {
        "url": "https://arxiv.org/abs/2103.14030",
        "content": "This paper introduces a novel approach to transformer architectures that significantly improves efficiency",
        "priority": 0.85,
        "type": "article"
    }
    
    try:
        # Validate all inputs in sequence
        validated = (ValidationChain()
            .validate(user_inputs["url"], validate_url, "Source URL")
            .validate(user_inputs["content"], validate_content, "Content")
            .validate(user_inputs["priority"], validate_priority, "Priority")
            .execute())
        
        url, content, priority = validated
        
        logger.info("✓ All validations passed!")
        logger.info(f"  URL: {url}")
        logger.info(f"  Content length: {len(content)} chars")
        logger.info(f"  Priority: {priority}")
        
        # Now safe to add to KB
        kb = KnowledgeBase()
        kid = kb.add_knowledge(
            content=content,
            source=url,
            knowledge_type=user_inputs["type"],
            metadata={"priority": priority}
        )
        logger.info(f"✓ Successfully added knowledge: {kid}")
        
    except ValidationException as e:
        logger.error(f"✗ Validation failed: {e.message}")
        logger.error(f"  Error code: {e.error_code}")


# ============================================================================
# Example 6: Complete Workflow
# ============================================================================

def example_6_complete_workflow():
    """
    Example: Complete workflow combining all improvements.
    
    Shows a realistic scenario using:
    - Validation
    - Type safety
    - Error handling
    - Performance monitoring
    - Circuit breakers
    """
    logger.info("=" * 70)
    logger.info("Example 6: Complete Integrated Workflow")
    logger.info("=" * 70)
    
    # Step 1: Validate input
    logger.info("\nStep 1: Validating inputs...")
    try:
        url = validate_url("https://example.com/research")
        content = validate_content("A comprehensive guide to transformer models and their applications")
        logger.info("✓ Inputs validated")
    except ValidationException as e:
        logger.error(f"✗ Validation failed: {e.message}")
        return
    
    # Step 2: Initialize knowledge base with error handling
    logger.info("\nStep 2: Initializing knowledge base...")
    try:
        kb = KnowledgeBase()
        stats = kb.get_statistics()
        logger.info(f"✓ KB initialized with {stats['total_entries']} entries")
    except KnowledgeBaseException as e:
        logger.error(f"✗ KB init failed: {e.message}")
        return
    
    # Step 3: Add knowledge with all safety features
    logger.info("\nStep 3: Adding knowledge...")
    try:
        knowledge_id = kb.add_knowledge(
            content=content,
            source=url,
            knowledge_type="article",
            metadata={
                "topic": "transformers",
                "difficulty": "advanced"
            }
        )
        logger.info(f"✓ Added knowledge: {knowledge_id}")
    except (ValidationException, KnowledgeBaseException) as e:
        logger.error(f"✗ Add knowledge failed: {e.message}")
        return
    
    # Step 4: Search with monitoring
    logger.info("\nStep 4: Searching knowledge base...")
    try:
        results = kb.search("transformers", top_k=5)
        logger.info(f"✓ Found {len(results)} relevant entries")
    except KnowledgeBaseException as e:
        logger.error(f"✗ Search failed: {e.message}")
        return
    
    # Step 5: Update relevance with type safety
    logger.info("\nStep 5: Updating relevance scores...")
    try:
        kb.update_relevance_score(knowledge_id, 0.95)
        logger.info(f"✓ Updated relevance to 0.95")
    except KnowledgeBaseException as e:
        logger.error(f"✗ Update failed: {e.message}")
        return
    
    # Step 6: Get final statistics
    logger.info("\nStep 6: Final statistics...")
    stats = kb.get_statistics()
    logger.info(f"✓ Knowledge base statistics:")
    logger.info(f"  Total entries: {stats['total_entries']}")
    logger.info(f"  Capacity used: {stats.get('capacity_used_percent', 0):.1f}%")
    logger.info(f"  Types available: {len(stats['types'])}")


# ============================================================================
# Main: Run all examples
# ============================================================================

if __name__ == "__main__":
    logger.info("\n" + "=" * 70)
    logger.info("AUTONOMOUS AI SYSTEM - CODE QUALITY IMPROVEMENTS EXAMPLES")
    logger.info("=" * 70 + "\n")
    
    try:
        example_1_safe_kb_operations()
        example_2_resilient_crawling()
        example_3_performance_monitoring()
        example_4_type_safe_structures()
        example_5_validation_scenarios()
        example_6_complete_workflow()
        
        logger.info("\n" + "=" * 70)
        logger.info("✓ All examples completed successfully!")
        logger.info("=" * 70 + "\n")
        
    except Exception as e:
        logger.error(f"\n✗ Error running examples: {e}")
        import traceback
        traceback.print_exc()
