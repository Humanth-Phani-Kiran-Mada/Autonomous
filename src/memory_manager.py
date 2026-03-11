"""
Advanced Memory Management with persistence and compression
"""
import json
from typing import Dict, List, Any
from datetime import datetime, timedelta
from pathlib import Path
import numpy as np
import config
from .logger import logger

class MemoryManager:
    """Manages short-term, long-term, and episodic memory with automatic persistence"""
    
    def __init__(self):
        self.short_term_memory: Dict[str, Any] = {}
        self.long_term_memory: Dict[str, Any] = {}
        self.episodic_memory: List[Dict] = []
        self.working_memory: Dict[str, Any] = {}
        
        self.memory_file = config.MEMORY_DIR / "memory_state.json"
        self.episodic_file = config.MEMORY_DIR / "episodic_memory.json"
        
        self.load_memory()
        logger.info("🧠 Memory Manager initialized")
    
    def load_memory(self):
        """Load memory from persistent storage"""
        try:
            if self.memory_file.exists():
                with open(self.memory_file, 'r') as f:
                    data = json.load(f)
                    self.long_term_memory = data.get("long_term", {})
                    self.short_term_memory = data.get("short_term", {})
                logger.info(f"📚 Loaded memory: {len(self.long_term_memory)} long-term entries")
            
            if self.episodic_file.exists():
                with open(self.episodic_file, 'r') as f:
                    self.episodic_memory = json.load(f)
                logger.info(f"📖 Loaded {len(self.episodic_memory)} episodic memories")
        except Exception as e:
            logger.error(f"Error loading memory: {e}")
    
    def save_memory(self):
        """Save memory to persistent storage"""
        try:
            config.MEMORY_DIR.mkdir(parents=True, exist_ok=True)
            
            # Clean expired short-term memories
            self._cleanup_short_term()
            
            memory_data = {
                "long_term": self.long_term_memory,
                "short_term": self.short_term_memory,
                "saved_at": datetime.now().isoformat()
            }
            
            with open(self.memory_file, 'w') as f:
                json.dump(memory_data, f, indent=2)
            
            with open(self.episodic_file, 'w') as f:
                json.dump(self.episodic_memory, f, indent=2)
            
            logger.debug("💾 Memory saved to disk")
        except Exception as e:
            logger.error(f"Error saving memory: {e}")
    
    def store_short_term(self, key: str, value: Any, ttl_seconds: int = 3600):
        """Store in short-term memory with expiration"""
        self.short_term_memory[key] = {
            "value": value,
            "stored_at": datetime.now().isoformat(),
            "expires_at": (datetime.now() + timedelta(seconds=ttl_seconds)).isoformat()
        }
        logger.debug(f"📝 Short-term memory: {key}")
    
    def store_long_term(self, key: str, value: Any, importance: float = 0.5):
        """Store in long-term memory with importance weighting"""
        self.long_term_memory[key] = {
            "value": value,
            "stored_at": datetime.now().isoformat(),
            "importance": min(max(importance, 0), 1.0),
            "access_count": 0
        }
        logger.debug(f"💾 Long-term memory: {key}")
    
    def retrieve_short_term(self, key: str) -> Any:
        """Retrieve from short-term memory"""
        if key in self.short_term_memory:
            entry = self.short_term_memory[key]
            if datetime.fromisoformat(entry["expires_at"]) > datetime.now():
                logger.debug(f"✅ Retrieved short-term: {key}")
                return entry["value"]
            else:
                del self.short_term_memory[key]
                logger.debug(f"⏰ Short-term memory expired: {key}")
        return None
    
    def retrieve_long_term(self, key: str) -> Any:
        """Retrieve from long-term memory"""
        if key in self.long_term_memory:
            entry = self.long_term_memory[key]
            entry["access_count"] += 1
            logger.debug(f"✅ Retrieved long-term: {key}")
            return entry["value"]
        return None
    
    def store_episode(self, description: str, actions: List[str], 
                     outcomes: List[str], importance: float = 0.5):
        """Record an episodic memory (experience)"""
        episode = {
            "id": len(self.episodic_memory),
            "timestamp": datetime.now().isoformat(),
            "description": description,
            "actions": actions,
            "outcomes": outcomes,
            "importance": min(max(importance, 0), 1.0),
            "review_count": 0
        }
        self.episodic_memory.append(episode)
        logger.info(f"📺 Stored episode: {description}")
        return episode["id"]
    
    def _cleanup_short_term(self):
        """Remove expired short-term memories"""
        now = datetime.now()
        expired_keys = []
        
        for key, entry in self.short_term_memory.items():
            if datetime.fromisoformat(entry["expires_at"]) < now:
                expired_keys.append(key)
        
        for key in expired_keys:
            del self.short_term_memory[key]
        
        if expired_keys:
            logger.debug(f"🗑️ Cleaned up {len(expired_keys)} expired short-term memories")
    
    def get_learning_insights(self) -> Dict:
        """Extract learning insights from episodic memory"""
        if not self.episodic_memory:
            return {"insights": [], "patterns": []}
        
        # Analyze outcomes to find patterns
        all_outcomes = []
        for episode in self.episodic_memory:
            all_outcomes.extend(episode["outcomes"])
        
        # Count outcome frequencies
        outcome_counts = {}
        for outcome in all_outcomes:
            outcome_counts[outcome] = outcome_counts.get(outcome, 0) + 1
        
        # Find most common positive outcomes
        patterns = sorted(outcome_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            "total_episodes": len(self.episodic_memory),
            "avg_importance": sum(e["importance"] for e in self.episodic_memory) / len(self.episodic_memory),
            "patterns": [{"outcome": p[0], "frequency": p[1]} for p in patterns],
            "long_term_keys": list(self.long_term_memory.keys())[:10]
        }
    
    def get_memory_statistics(self) -> Dict:
        """Get memory usage statistics"""
        return {
            "short_term_entries": len(self.short_term_memory),
            "long_term_entries": len(self.long_term_memory),
            "episodic_entries": len(self.episodic_memory),
            "working_memory_size": len(self.working_memory),
            "avg_long_term_importance": np.mean([e.get("importance", 0.5) 
                                                 for e in self.long_term_memory.values()]) if self.long_term_memory else 0
        }
