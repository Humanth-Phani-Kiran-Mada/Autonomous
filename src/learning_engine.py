"""
Advanced Learning Engine with self-improvement capabilities
"""
import json
from typing import Dict, List, Tuple
from datetime import datetime
import numpy as np
from pathlib import Path
import config
from .logger import logger

class LearningEngine:
    """Autonomous learning engine that improves AI capabilities over time"""
    
    def __init__(self, knowledge_base, memory_manager):
        self.kb = knowledge_base
        self.memory = memory_manager
        self.learning_metrics: List[Dict] = []
        self.skill_levels: Dict[str, float] = {}
        self.learned_patterns: List[Dict] = []
        self.improvement_history: List[Dict] = []
        
        self.metrics_file = config.DATA_DIR / "learning_metrics.json"
        self.skills_file = config.DATA_DIR / "skill_levels.json"
        
        self.load_metrics()
        logger.info(" Learning Engine initialized")
    
    def load_metrics(self):
        """Load learning metrics from disk"""
        try:
            if self.metrics_file.exists():
                with open(self.metrics_file, 'r') as f:
                    self.learning_metrics = json.load(f)
            
            if self.skills_file.exists():
                with open(self.skills_file, 'r') as f:
                    self.skill_levels = json.load(f)
        except Exception as e:
            logger.error(f"Error loading metrics: {e}")
    
    def save_metrics(self):
        """Save learning metrics to disk"""
        try:
            with open(self.metrics_file, 'w') as f:
                json.dump(self.learning_metrics[-1000:], f, indent=2)  # Keep last 1000
            
            with open(self.skills_file, 'w') as f:
                json.dump(self.skill_levels, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving metrics: {e}")
    
    def learn_from_knowledge(self, knowledge_item: Dict) -> Dict:
        """Process and learn from a knowledge item"""
        logger.info(f" Learning from: {knowledge_item.get('content', '')[:50]}")
        
        learning_result = {
            "timestamp": datetime.now().isoformat(),
            "knowledge_id": knowledge_item.get("id", "unknown"),
            "categories": self._categorize_knowledge(knowledge_item),
            "key_concepts": self._extract_concepts(knowledge_item),
            "applicability": self._assess_applicability(knowledge_item),
            "improvement_potential": self._calculate_improvement_potential(knowledge_item)
        }
        
        self.learning_metrics.append(learning_result)
        
        # Store in episodic memory
        self.memory.store_episode(
            description=f"Learned from: {knowledge_item.get('source', 'unknown')}",
            actions=[f"Read: {knowledge_item.get('type', 'unknown')}", "Analyzed"],
            outcomes=learning_result["categories"]
        )
        
        logger.info(f" Learning result: {learning_result['categories']}")
        return learning_result
    
    def improve_skill(self, skill_name: str, practice_data: List[Dict]) -> Dict:
        """Improve a specific skill through practice and feedback"""
        current_level = self.skill_levels.get(skill_name, 0.0)
        
        # Calculate improvement
        success_rate = sum(1 for d in practice_data if d.get("success", False)) / len(practice_data) if practice_data else 0
        improvement = success_rate * config.LEARNING_RATE
        new_level = min(current_level + improvement, 1.0)
        
        improvement_record = {
            "timestamp": datetime.now().isoformat(),
            "skill": skill_name,
            "old_level": current_level,
            "new_level": new_level,
            "improvement": improvement,
            "practice_iterations": len(practice_data),
            "success_rate": success_rate
        }
        
        self.skill_levels[skill_name] = new_level
        self.improvement_history.append(improvement_record)
        
        logger.info(f" Improved skill '{skill_name}': {current_level:.2%} → {new_level:.2%}")
        
        # Store as learning episode
        self.memory.store_episode(
            description=f"Skill improvement: {skill_name}",
            actions=["Practice", "Analyze", "Improve"],
            outcomes=[f"Success rate: {success_rate:.2%}", f"New level: {new_level:.2%}"],
            importance=improvement
        )
        
        return improvement_record
    
    def discover_pattern(self, pattern_name: str, conditions: Dict, outcomes: List[str]) -> Dict:
        """Discover and learn patterns from experience"""
        pattern = {
            "id": len(self.learned_patterns),
            "name": pattern_name,
            "discovered_at": datetime.now().isoformat(),
            "conditions": conditions,
            "outcomes": outcomes,
            "confidence": 0.5,
            "times_observed": 1
        }
        
        # Check if pattern already exists
        for existing in self.learned_patterns:
            if existing["name"] == pattern_name:
                existing["times_observed"] += 1
                existing["confidence"] = min(existing["confidence"] + 0.1, 1.0)
                logger.info(f" Pattern reinforced: {pattern_name}")
                return existing
        
        self.learned_patterns.append(pattern)
        logger.info(f" New pattern discovered: {pattern_name}")
        
        # Store pattern knowledge
        self.kb.add_knowledge(
            content=f"Pattern: {pattern_name}\nConditions: {json.dumps(conditions)}\nOutcomes: {outcomes}",
            source="learned_pattern",
            knowledge_type="pattern",
            metadata={"confidence": pattern["confidence"]}
        )
        
        return pattern
    
    def _categorize_knowledge(self, knowledge_item: Dict) -> List[str]:
        """Categorize knowledge by domain and type"""
        categories = []
        content = (knowledge_item.get("content", "") + knowledge_item.get("title", "")).lower()
        
        domain_keywords = {
            "ai_ml": ["ai", "machine learning", "neural", "model", "algorithm", "training"],
            "web_tech": ["html", "javascript", "web", "api", "http", "frontend", "backend"],
            "science": ["physics", "chemistry", "biology", "research", "experiment", "study"],
            "programming": ["code", "function", "class", "variable", "debug", "algorithm"],
            "data": ["data", "database", "sql", "analytics", "data science", "statistics"]
        }
        
        for domain, keywords in domain_keywords.items():
            if any(keyword in content for keyword in keywords):
                categories.append(domain)
        
        return categories if categories else ["general"]
    
    def _extract_concepts(self, knowledge_item: Dict) -> List[str]:
        """Extract key concepts from knowledge"""
        content = (knowledge_item.get("content", "") + knowledge_item.get("title", "")).lower()
        words = content.split()
        
        # Simple noun extraction (placeholder for real NLP)
        common_words = {"the", "a", "is", "and", "or", "in", "of", "to", "for", "as", "by"}
        concepts = [w for w in set(words) if len(w) > 4 and w not in common_words]
        
        return concepts[:10]  # Return top 10
    
    def _assess_applicability(self, knowledge_item: Dict) -> str:
        """Assess how applicable this knowledge is"""
        content_len = len(knowledge_item.get("content", ""))
        source = knowledge_item.get("source", "")
        
        if content_len > 500 and any(domain in source for domain in ["arxiv", "github", "wikipedia"]):
            return "high"
        elif content_len > 100:
            return "medium"
        else:
            return "low"
    
    def _calculate_improvement_potential(self, knowledge_item: Dict) -> float:
        """Calculate potential for self-improvement from this knowledge"""
        source_weight = 1.0
        if "arxiv" in knowledge_item.get("source", ""):
            source_weight = 1.5
        elif "github" in knowledge_item.get("source", ""):
            source_weight = 1.2
        
        content_quality = min(len(knowledge_item.get("content", "")) / 1000, 1.0)
        
        return min(content_quality * source_weight * config.KNOWLEDGE_ACQUISITION_RATE, 1.0)
    
    def get_learning_summary(self) -> Dict:
        """Get comprehensive learning summary"""
        return {
            "total_learning_events": len(self.learning_metrics),
            "skills": {name: level for name, level in self.skill_levels.items()},
            "patterns_learned": len(self.learned_patterns),
            "avg_improvement": np.mean([h["improvement"] for h in self.improvement_history]) if self.improvement_history else 0,
            "most_learned_domains": self._get_top_domains(),
            "recent_improvements": self.improvement_history[-5:]
        }
    
    def _get_top_domains(self) -> List[str]:
        """Get most frequently learned domains"""
        domain_counts = {}
        for metric in self.learning_metrics:
            for category in metric.get("categories", []):
                domain_counts[category] = domain_counts.get(category, 0) + 1
        
        return sorted(domain_counts.items(), key=lambda x: x[1], reverse=True)[:5]
