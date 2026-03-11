# Self-Evolving AI System

A sophisticated, autonomous AI system that can:
- **Crawl the web** autonomously to acquire knowledge
- **Learn continuously** from diverse sources
- **Reason** about complex problems
- **Improve itself** without human intervention
- **Build persistent knowledge** across sessions
- **Set and achieve goals** autonomously
- **Evolve capabilities** over time

## Architecture

### Core Components

1. **Web Crawler** (`web_crawler.py`)
 - Autonomous web crawling and content discovery
 - Intelligent link following and content extraction
 - Persistent state management
 - Batch processing and parallel requests

2. **Knowledge Base** (`knowledge_base.py`)
 - Vector embeddings for semantic search
 - Automatic relevance scoring
 - Knowledge pruning and compression
 - Support for multiple knowledge types

3. **Memory Manager** (`memory_manager.py`)
 - Short-term memory with TTL
 - Long-term persistent memory
 - Episodic memory for experiences
 - Automatic memory persistence

4. **Learning Engine** (`learning_engine.py`)
 - Knowledge categorization and concept extraction
 - Skill development and improvement tracking
 - Pattern discovery and learning
 - Improvement metrics and analytics

5. **Reasoning Engine** (`reasoning_engine.py`)
 - Goal setting and decomposition
 - Action planning based on knowledge
 - Decision-making with confidence scoring
 - Problem-solving and reasoning about topics

6. **Autonomous Agent** (`autonomous_agent.py`)
 - Orchestrates all components
 - Runs autonomous learning cycles
 - Manages agent state and persistence
 - Coordinates improvement and maintenance

## Quick Start

### Installation

```bash
# Clone or navigate to the project
cd /path/to/SELF_DEV_AI

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env
```

### Usage

#### Autonomous Mode (Auto-Learning)
```bash
# Run with autonomous learning enabled
python main.py
# Select autonomous mode when prompted
# Enter desired number of iterations
```

#### Interactive Mode
```bash
# Run in interactive mode
# Edit config.py: AUTONOMOUS_MODE_ENABLED = false
python main.py

# Then use commands:
# - learn: Run learning cycle
# - crawl: Crawl web for new knowledge
# - reason: Reasoning cycle
# - improve: Self-improvement cycle
# - query: Ask a question
# - status: Show agent status
# - auto: Run automated iterations
```

## How It Works

### Autonomous Learning Loop

Each iteration consists of 5 cycles:

1. ** Crawling Cycle**
 - Discovers and fetches new web content
 - Extracts structured information
 - Maintains crawling history

2. ** Learning Cycle**
 - Processes discovered knowledge
 - Categorizes and indexes content
 - Learns key concepts and patterns

3. ** Reasoning Cycle**
 - Analyzes acquired knowledge
 - Performs problem-solving tasks
 - Tracks decision-making confidence

4. ** Improvement Cycle**
 - Identifies skill improvement opportunities
 - Practices and refines capabilities
 - Updates capability levels

5. ** Maintenance Cycle**
 - Persists all data to disk
 - Optimizes storage
 - Validates system integrity

### Key Features

#### Intelligent Learning
- **Semantic Search**: Finds relevant knowledge using embeddings
- **Pattern Recognition**: Discovers recurring patterns in data
- **Skill Development**: Tracks and improves capabilities
- **Knowledge Integration**: Combines information from multiple sources

#### Continuous Evolution
- **Self-Improvement**: Identifies and addresses weaknesses
- **Capability Growth**: Develops new skills over time
- **Experience Learning**: Forms memories from actions and outcomes
- **Adaptive Strategy**: Adjusts approach based on past successes

#### Persistent Memory
- **Short-term**: Temporary data with expiration
- **Long-term**: Important information with relevance tracking
- **Episodic**: Experiences and events for learning
- **Vector Storage**: Semantic understanding preservation

#### Autonomous Goal Management
- **Goal Definition**: Set specific objectives
- **Goal Decomposition**: Break down complex goals into steps
- **Action Planning**: Generate steps to achieve goals
- **Progress Tracking**: Monitor goal achievement

## Configuration

Edit `config.py` to customize:

- **Learning Sources**: Websites to crawl
- **Performance Limits**: CPU and memory restrictions
- **Learning Parameters**: Learning rate, exploration rate
- **Autonomous Settings**: Enable/disable autonomous mode
- **Resource Management**: Batch sizes, timeouts

## Data Storage

The system maintains data in:

```
data/
 ├- memory/ # Persistent memory files
 ├- knowledge/ # Knowledge base and embeddings
 ├- cache/ # Cached web content
 ├- crawler_state.json # Crawling history
 ├- learning_metrics.json # Learning progress
 ├- skill_levels.json # Capability levels
 ├- goals.json # Agent goals
 └- agent_state.json # Overall agent state

logs/
 ├- ai_evolution.log # Main operations log
 └- errors.log # Error tracking
```

## Performance Metrics

The system tracks:
- **Knowledge Growth**: Number of learned concepts
- **Skill Development**: Progress in various domains
- **Success Rate**: Action success percentages
- **Memory Usage**: Storage efficiency
- **Learning Efficiency**: Knowledge acquisition rate

## Customization

### Add Custom Learning Sources

Edit `config.py`:
```python
LEARNING_SOURCES = [
 "https://en.wikipedia.org",
 "https://www.arxiv.org",
 # Add more sources
]
```

### Implement Custom Skills

In `learning_engine.py`:
```python
def learn_custom_skill(self, skill_name):
 # Your custom skill learning logic
 pass
```

### Extend Reasoning

In `reasoning_engine.py`:
```python
def custom_reasoning(self, topic):
 # Your custom reasoning logic
 pass
```

## Safety Notes

The system is designed with safety considerations:
- Bounded resource usage (CPU, memory limits)
- Configurable rate limiting
- Timeout protections
- Crawling restrictions
- Memory compression

For production use:
- Monitor resource usage regularly
- Set appropriate limits in `config.py`
- Review learned patterns periodically
- Maintain backups of knowledge base

## Requirements

- Python 3.8+
- Dependencies listed in `requirements.txt`
- Internet connection (for web crawling)
- ~4GB RAM recommended
- Storage for knowledge base (scales with usage)

## Troubleshooting

**Knowledge base loading fails**
- Check data directory permissions
- Verify embeddings model is installed
- Clear cache and restart

**Web crawling is slow**
- Reduce `CRAWLER_MAX_WORKERS` in config
- Increase `CRAWLER_TIMEOUT`
- Check internet connection

**Memory usage growing**
- Reduce `MAX_KNOWLEDGE_ENTRIES`
- Increase `MEMORY_COMPRESSION_RATIO`
- Run maintenance cycle explicitly

## Future Enhancements

- [ ] Multi-agent collaboration
- [ ] Advanced NLP with transformers
- [ ] Reinforcement learning integration
- [ ] Visual learning from images
- [ ] Real-time knowledge sync
- [ ] Federated learning support

## License

MIT License - Feel free to use and modify

## Support

For issues or questions, check the logs directory or review the documentation in individual modules.

---

**Note**: This is a research/development system. Use responsibly and ensure you have proper monitoring in place when running autonomous cycles.
