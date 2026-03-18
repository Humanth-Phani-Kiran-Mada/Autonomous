"""
Autonomous AI System - Core Package
Core components for web crawling, knowledge management, memory, learning, and reasoning.
"""

from src.core.web_crawler import WebCrawler
from src.core.knowledge_base import KnowledgeBase
from src.core.memory_manager import MemoryManager
from src.core.learning_engine import LearningEngine
from src.core.reasoning_engine import ReasoningEngine
from src.core.autonomous_agent import AutonomousAgent

__all__ = [
    'WebCrawler',
    'KnowledgeBase',
    'MemoryManager',
    'LearningEngine',
    'ReasoningEngine',
    'AutonomousAgent',
]
