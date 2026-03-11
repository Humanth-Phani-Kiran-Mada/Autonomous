"""
Autonomous AI System - Self-Evolving Intelligence Platform

Core modules for autonomous learning, self-improvement, and adaptive reasoning.
"""

from .logger import logger
from .autonomous_agent import AutonomousAgent
from .self_model import SelfModel
from .meta_learner import MetaLearner
from .bayesian_reasoner import BayesianReasoner
from .autonomous_goal_generator import AutonomousGoalGenerator
from .introspection_engine import IntrospectionEngine
from .memory_consolidation import MemoryConsolidation
from .error_recovery import ErrorRecoverySystem
from .knowledge_base import KnowledgeBase
from .memory_manager import MemoryManager
from .learning_engine import LearningEngine
from .reasoning_engine import ReasoningEngine
from .web_crawler import WebCrawler

__all__ = [
    'logger',
    'AutonomousAgent',
    'SelfModel',
    'MetaLearner',
    'BayesianReasoner',
    'AutonomousGoalGenerator',
    'IntrospectionEngine',
    'MemoryConsolidation',
    'ErrorRecoverySystem',
    'KnowledgeBase',
    'MemoryManager',
    'LearningEngine',
    'ReasoningEngine',
    'WebCrawler'
]

__version__ = "2.0.0-advanced"
