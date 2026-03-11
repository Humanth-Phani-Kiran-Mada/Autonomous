"""
Configuration for the Self-Evolving AI System
"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Project paths
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
LOGS_DIR = PROJECT_ROOT / "logs"
MEMORY_DIR = DATA_DIR / "memory"
KNOWLEDGE_DIR = DATA_DIR / "knowledge"
CACHE_DIR = DATA_DIR / "cache"

# Create directories if they don't exist
for directory in [DATA_DIR, LOGS_DIR, MEMORY_DIR, KNOWLEDGE_DIR, CACHE_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Logging configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = LOGS_DIR / "ai_evolution.log"

# Web crawler configuration
CRAWLER_TIMEOUT = int(os.getenv("CRAWLER_TIMEOUT", 30))
CRAWLER_MAX_WORKERS = int(os.getenv("CRAWLER_MAX_WORKERS", 5))
CRAWLER_BATCH_SIZE = int(os.getenv("CRAWLER_BATCH_SIZE", 10))
CRAWLER_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

# Knowledge base configuration
KNOWLEDGE_EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
KNOWLEDGE_DIMENSION = 384  # Dimension for all-MiniLM model
MAX_KNOWLEDGE_ENTRIES = int(os.getenv("MAX_KNOWLEDGE", 100000))

# Memory configuration
MEMORY_RETENTION_DAYS = int(os.getenv("MEMORY_RETENTION_DAYS", 90))
MEMORY_COMPRESSION_RATIO = float(os.getenv("MEMORY_COMPRESSION_RATIO", 0.8))
MEMORY_PERSISTENCE_INTERVAL = int(os.getenv("MEMORY_PERSISTENCE_INTERVAL", 300))  # seconds

# Learning configuration
LEARNING_RATE = float(os.getenv("LEARNING_RATE", 0.01))
EXPLORATION_RATE = float(os.getenv("EXPLORATION_RATE", 0.2))
IMPROVEMENT_THRESHOLD = float(os.getenv("IMPROVEMENT_THRESHOLD", 0.05))

# Task execution configuration
MAX_TASK_RETRIES = int(os.getenv("MAX_TASK_RETRIES", 3))
TASK_TIMEOUT = int(os.getenv("TASK_TIMEOUT", 300))
PARALLEL_TASKS = int(os.getenv("PARALLEL_TASKS", 3))

# API Keys (for external models)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
SERPER_API_KEY = os.getenv("SERPER_API_KEY", "")

# Learning sources (websites to crawl and learn from)
LEARNING_SOURCES = [
    "https://en.wikipedia.org",
    "https://www.arxiv.org",
    "https://github.com",
    "https://stackoverflow.com",
    "https://www.khan.academy",
    "https://www.coursera.org",
]

# Self-improvement settings
SELF_IMPROVE_INTERVAL = int(os.getenv("SELF_IMPROVE_INTERVAL", 3600))  # 1 hour
MAX_IMPROVEMENT_ITERATIONS = int(os.getenv("MAX_IMPROVEMENT_ITERATIONS", 100))
KNOWLEDGE_ACQUISITION_RATE = float(os.getenv("KNOWLEDGE_ACQUISITION_RATE", 0.1))

# Resource limits
MAX_MEMORY_MB = int(os.getenv("MAX_MEMORY_MB", 4096))
MAX_CPU_PERCENT = float(os.getenv("MAX_CPU_PERCENT", 80.0))
RATE_LIMIT_PER_SECOND = int(os.getenv("RATE_LIMIT_PER_SECOND", 10))

# Autonomous mode
AUTONOMOUS_MODE_ENABLED = os.getenv("AUTONOMOUS_MODE", "true").lower() == "true"
AUTO_START_LEARNING = os.getenv("AUTO_START_LEARNING", "true").lower() == "true"
AUTO_IMPROVE_ENABLED = os.getenv("AUTO_IMPROVE", "true").lower() == "true"

# Performance monitoring
ENABLE_PERFORMANCE_TRACKING = os.getenv("ENABLE_PERF_TRACKING", "true").lower() == "true"
METRICS_COLLECTION_INTERVAL = int(os.getenv("METRICS_INTERVAL", 60))
