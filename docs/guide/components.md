# Components Reference

Detailed reference for all components.

## Core Components

### WebCrawler
Located: `src/core/web_crawler.py`

**Purpose**: Autonomous web crawling and content discovery

**Methods**:
```python
crawl(start_url, max_depth, filters)  # Start crawling
fetch_page(url)                         # Get single page
extract_content(html)                   # Parse HTML
save_cache()                            # Persist cache
```

---

### KnowledgeBase
Located: `src/core/knowledge_base.py`

**Purpose**: Semantic knowledge storage and retrieval

**Methods**:
```python
store(content, metadata)    # Add knowledge
search(query, top_k)        # Find similar
get_by_type(type_name)      # Filter by type
prune()                     # Clean old entries
get_statistics()            # Usage stats
```

---

### MemoryManager
Located: `src/core/memory_manager.py`

**Purpose**: Multi-layer memory management

**Methods**:
```python
store_short_term(key, value, ttl)      # Temporary
store_long_term(key, value)            # Persistent
recall_short_term(key)                 # Quick access
recall_long_term(key)                  # From disk
consolidate()                          # Migrate data
```

---

### LearningEngine
Located: `src/core/learning_engine.py`

**Purpose**: Knowledge extraction and skill learning

**Methods**:
```python
learn(content)              # Learn from content
extract_patterns()          # Find patterns
improve_skills()            # Enhance skills
get_learning_metrics()      # Progress tracking
```

---

### ReasoningEngine
Located: `src/core/reasoning_engine.py`

**Purpose**: Problem-solving and decision-making

**Methods**:
```python
reason(query)               # Analyze problem
plan_actions()              # Create action plan
make_decision()             # Choose action
evaluate_option()           # Score option
```

---

### AutonomousAgent
Located: `src/core/autonomous_agent.py`

**Purpose**: Main system orchestrator

**Methods**:
```python
initialize()                # Setup system
run_cycle()                 # Run learning cycle
run_autonomous(iterations)  # Run N cycles
shutdown()                  # Clean shutdown
```

---

## Advanced Components

### AdaptiveReasoningEngine
Dynamically adjusts reasoning strategy based on problem type.

### MetaLearner
Learns about learning - tracks algorithm effectiveness.

### EvolutionaryDecisionEngine
Uses genetic algorithms for decision optimization.

### AttentionSystem
Focuses computational resources on important tasks.

### CapabilityExpansionEngine
Identifies and implements new capabilities.

---

## Infrastructure Components

### Exception Hierarchy
```python
AutonomousAIException (base)
├── KnowledgeBaseException
├── MemoryException
├── CrawlerException
├── ReasoningException
├── ValidationException
├── CircuitBreakerOpenException
└── ResourceExhaustedException
```

### Validators
```python
validate_url(url)           # URL validation
validate_content(content)   # Content checking
validate_skill_level(level) # 0-1 range
validate_priority(priority) # Priority values
```

### Utilities (Decorators)
```python
@retry_with_backoff         # Auto-retry
@measure_performance        # Time operations
@cached(ttl)                # Cache results
@ensure_resource_limits     # Enforce limits
```

---

## Integration Layer

### CycleCoordinator
Manages the 5-phase learning cycle.

### SystemOrchestrator
High-level system coordination.

### IntegrationLayer
Binds components together.

### ComponentWrapper
Adds monitoring/health checks to components.

---

## Configuration

See `src/config.py` for detailed configuration options.

Key settings:
- `AUTONOMOUS_MODE_ENABLED` - Auto vs interactive
- `MAX_CRAWL_DEPTH` - Web crawling depth
- `BATCH_SIZE` - Processing batch size
- `LOG_LEVEL` - Logging verbosity

---

See: [usage.md](usage.md), [architecture.md](architecture.md)
