"""
Advanced Memory Consolidation: Prevent catastrophic forgetting
Implements memory stability, spaced repetition, and consolidation mechanisms
"""
import json
from typing import Dict, List, Any, Tuple
from datetime import datetime, timedelta
import numpy as np
from pathlib import Path
import config
from src.logger import logger


class MemoryConsolidation:
    """
    Prevents catastrophic forgetting by:
    - Consolidating important memories
    - Implementing rehearsal schedules
    - Maintaining memory stability
    - Balancing plasticity-stability tradeoff
    """
    
    def __init__(self, memory_manager):
        self.memory_manager = memory_manager
        
        self.consolidation_schedule: List[Dict] = []
        self.rehearsal_history: List[Dict] = []
        self.memory_stability: Dict[str, float] = {}
        self.forgetting_curves: Dict[str, List[float]] = {}
        
        self.consolidation_file = config.DATA_DIR / "memory_consolidation.json"
        self.load_consolidation_state()
        logger.info("🧠 Memory Consolidation Engine initialized")
    
    def load_consolidation_state(self):
        """Load consolidation state from disk"""
        try:
            if self.consolidation_file.exists():
                with open(self.consolidation_file, 'r') as f:
                    data = json.load(f)
                    self.consolidation_schedule = data.get("schedule", [])
                    self.memory_stability = data.get("stability", {})
        except Exception as e:
            logger.error(f"Error loading consolidation state: {e}")
    
    def save_consolidation_state(self):
        """Persist consolidation state"""
        try:
            data = {
                "schedule": self.consolidation_schedule,
                "stability": self.memory_stability,
                "saved_at": datetime.now().isoformat()
            }
            with open(self.consolidation_file, 'w') as f:
                json.dump(data, f, indent=2)
            logger.debug("💾 Memory consolidation state saved")
        except Exception as e:
            logger.error(f"Error saving consolidation state: {e}")
    
    def consolidate_memory(self, memory_key: str, memory_content: Any, importance: float = 0.5):
        """Schedule memory for consolidation using spaced repetition"""
        consolidation_entry = {
            "memory_key": memory_key,
            "original_content": memory_content,
            "importance": importance,
            "created_at": datetime.now().isoformat(),
            "consolidation_level": 0,
            "rehearsals": 0,
            "stability": 0.3,
            "schedule": self._generate_rehearsal_schedule(importance)
        }
        
        self.consolidation_schedule.append(consolidation_entry)
        self.memory_stability[memory_key] = 0.3
        
        logger.info(f"📌 Memory consolidated: {memory_key} (importance={importance:.1%})")
    
    def _generate_rehearsal_schedule(self, importance: float) -> List[Dict]:
        """Generate spacing-based rehearsal schedule (Ebbinghaus spacing effect)"""
        now = datetime.now()
        
        # Intervals based on importance (more important = more frequent rehearsal)
        base_intervals = [
            1,      # 1 day
            3,      # 3 days
            7,      # 1 week
            14,     # 2 weeks
            30      # 1 month
        ]
        
        # Scale intervals based on importance
        scaled_intervals = [max(1, int(interval / (importance + 0.5))) for interval in base_intervals]
        
        schedule = []
        for i, interval in enumerate(scaled_intervals):
            schedule.append({
                "rehearsal_number": i + 1,
                "scheduled_at": (now + timedelta(days=interval)).isoformat(),
                "completed": False,
                "effectiveness": 0.0
            })
        
        return schedule
    
    def get_rehearsal_tasks(self, due_within_days: int = 7) -> List[Dict]:
        """Get memories that are due for rehearsal"""
        due_tasks = []
        now = datetime.now()
        cutoff = now + timedelta(days=due_within_days)
        
        for memory_entry in self.consolidation_schedule:
            schedule = memory_entry.get("schedule", [])
            
            for rehearsal in schedule:
                if not rehearsal.get("completed", False):
                    scheduled_time = datetime.fromisoformat(rehearsal["scheduled_at"])
                    
                    if scheduled_time <= cutoff:
                        due_tasks.append({
                            "memory_key": memory_entry["memory_key"],
                            "scheduled_at": rehearsal["scheduled_at"],
                            "rehearsal_number": rehearsal["rehearsal_number"],
                            "importance": memory_entry["importance"]
                        })
        
        return sorted(due_tasks, key=lambda x: x["scheduled_at"])
    
    def perform_rehearsal(self, memory_key: str, rehearsal_number: int = 1) -> Dict:
        """Perform memory rehearsal and track effectiveness"""
        logger.info(f"🔄 Rehearsing memory: {memory_key}")
        
        # Find the memory entry
        for memory_entry in self.consolidation_schedule:
            if memory_entry["memory_key"] == memory_key:
                schedule = memory_entry.get("schedule", [])
                
                # Mark rehearsal as completed
                if rehearsal_number <= len(schedule):
                    schedule[rehearsal_number - 1]["completed"] = True
                    
                    # Calculate effectiveness (based on memory retrieval)
                    retrieval_success = True
                    
                    try:
                        retrieved = self.memory_manager.retrieve_long_term(memory_key)
                        retrieval_success = retrieved is not None
                    except:
                        retrieval_success = False
                    
                    effectiveness = 1.0 if retrieval_success else 0.5
                    schedule[rehearsal_number - 1]["effectiveness"] = effectiveness
                    
                    # Update stability
                    old_stability = memory_entry["stability"]
                    memory_entry["stability"] = min(old_stability + (effectiveness * 0.2), 1.0)
                    memory_entry["rehearsals"] += 1
                    memory_entry["consolidation_level"] = min(
                        memory_entry["consolidation_level"] + 1, len(schedule)
                    )
                    
                    self.memory_stability[memory_key] = memory_entry["stability"]
                    
                    rehearsal_record = {
                        "memory_key": memory_key,
                        "rehearsal_number": rehearsal_number,
                        "timestamp": datetime.now().isoformat(),
                        "effectiveness": effectiveness,
                        "stability_after": memory_entry["stability"],
                        "consolidation_level": memory_entry["consolidation_level"]
                    }
                    
                    self.rehearsal_history.append(rehearsal_record)
                    
                    logger.info(f"✅ Rehearsal complete: stability={memory_entry['stability']:.1%}")
                    
                    return rehearsal_record
        
        return {"status": "memory_not_found"}
    
    def prevent_catastrophic_forgetting(self, new_learning: Dict, old_learning_sample: List[Dict] = None):
        """
        Prevent catastrophic forgetting by rehearsing important old memories
        when new learning occurs
        """
        logger.info("🛡️ Preventing catastrophic forgetting...")
        
        # Get important old memories
        important_old = sorted(
            self.consolidation_schedule,
            key=lambda x: x["importance"],
            reverse=True
        )[:5]
        
        # Rehearse subset of old memories
        rehearsals_performed = 0
        
        for memory_entry in important_old:
            if memory_entry["stability"] < 0.8:
                # Find first incomplete rehearsal
                for rehearsal in memory_entry.get("schedule", []):
                    if not rehearsal.get("completed", False):
                        self.perform_rehearsal(memory_entry["memory_key"])
                        rehearsals_performed += 1
                        break
        
        logger.info(f"✅ Catastrophic forgetting prevention: {rehearsals_performed} memories rehearsed")
        
        return {"rehearsals_performed": rehearsals_performed}
    
    def estimate_retention(self, memory_key: str) -> Dict:
        """Estimate retention probability using Ebbinghaus forgetting curve"""
        if memory_key not in self.memory_stability:
            return {"retention_probability": 0.5, "status": "unknown"}
        
        # Find memory entry
        for memory_entry in self.consolidation_schedule:
            if memory_entry["memory_key"] == memory_key:
                
                # Calculate days since creation
                created = datetime.fromisoformat(memory_entry["created_at"])
                days_elapsed = (datetime.now() - created).days
                
                # Estimate retention using forgetting curve model
                # R(t) = e^(-t/S) where S is stability strength
                stability = memory_entry["stability"]
                
                retention_prob = np.exp(-days_elapsed / (stability * 30 + 1))
                
                return {
                    "memory_key": memory_key,
                    "retention_probability": max(retention_prob, 0),
                    "days_elapsed": days_elapsed,
                    "stability": stability,
                    "consolidation_level": memory_entry["consolidation_level"],
                    "total_rehearsals": memory_entry["rehearsals"]
                }
        
        return {"status": "memory_not_found"}
    
    def optimize_consolidation_strategy(self) -> Dict:
        """Adapt consolidation strategy based on effectiveness"""
        logger.info("🔧 Optimizing memory consolidation strategy...")
        
        if not self.rehearsal_history:
            return {"status": "no_data"}
        
        # Analyze rehearsal effectiveness
        recent_rehearsals = self.rehearsal_history[-50:]
        
        effectiveness_by_schedule_level = {}
        for rehearsal in recent_rehearsals:
            level = rehearsal.get("consolidation_level", 1)
            effectiveness = rehearsal.get("effectiveness", 0)
            
            if level not in effectiveness_by_schedule_level:
                effectiveness_by_schedule_level[level] = []
            
            effectiveness_by_schedule_level[level].append(effectiveness)
        
        # Calculate average effectiveness at each level
        avg_effectiveness = {
            level: np.mean(effs) for level, effs in effectiveness_by_schedule_level.items()
        }
        
        # Identify bottlenecks
        bottlenecks = [
            (level, eff) for level, eff in avg_effectiveness.items() if eff < 0.7
        ]
        
        optimization = {
            "total_rehearsals": len(self.rehearsal_history),
            "average_effectiveness": np.mean([r.get("effectiveness", 0) for r in recent_rehearsals]),
            "consolidation_levels": len(avg_effectiveness),
            "bottlenecks": bottlenecks,
            "recommendations": []
        }
        
        if bottlenecks:
            worst_level = max(bottlenecks, key=lambda x: x[0])[0]
            optimization["recommendations"].append(
                f"Improve rehearsal effectiveness at consolidation level {worst_level}"
            )
        
        if optimization["average_effectiveness"] < 0.7:
            optimization["recommendations"].append("Consider more frequent rehearsals")
        
        return optimization
    
    def get_consolidation_summary(self) -> Dict:
        """Get comprehensive consolidation summary"""
        return {
            "memories_in_consolidation": len(self.consolidation_schedule),
            "average_stability": np.mean(list(self.memory_stability.values())) if self.memory_stability else 0,
            "high_stability_memories": sum(1 for s in self.memory_stability.values() if s > 0.8),
            "rehearsals_performed": len(self.rehearsal_history),
            "average_rehearsal_effectiveness": np.mean([r.get("effectiveness", 0) for r in self.rehearsal_history]) if self.rehearsal_history else 0,
            "pending_rehearsals": len(self.get_rehearsal_tasks(due_within_days=7))
        }
