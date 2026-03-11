"""
Curriculum Learning System: Self-generates optimal learning paths dynamically
Avoids catastrophic forgetting by ordering learning from simple to complex.
Enables rapid skill acquisition while maintaining knowledge integrity.
"""
import json
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime
from collections import defaultdict
import numpy as np
from pathlib import Path
import config
from .logger import logger


class LearningUnit:
    """Represents an atomic unit of learning"""
    def __init__(self, unit_id: str, topic: str, difficulty: float, 
                 prerequisites: List[str] = None):
        self.unit_id = unit_id
        self.topic = topic
        self.difficulty = difficulty  # 0-1, where 1 is most difficult
        self.prerequisites = prerequisites or []
        self.completion_status = False
        self.mastery_level = 0.0  # 0-1
        self.practice_count = 0
        self.last_practiced = None
        self.estimated_time = 0.0
        
    def to_dict(self) -> Dict:
        return {
            "unit_id": self.unit_id,
            "topic": self.topic,
            "difficulty": self.difficulty,
            "prerequisites": self.prerequisites,
            "mastery_level": self.mastery_level,
            "completion_status": self.completion_status,
            "practice_count": self.practice_count
        }


class Curriculum:
    """A complete learning curriculum"""
    def __init__(self, curriculum_id: str, learning_goal: str, domain: str):
        self.curriculum_id = curriculum_id
        self.learning_goal = learning_goal
        self.domain = domain
        self.units: Dict[str, LearningUnit] = {}
        self.current_unit_index = 0
        self.created_at = datetime.now()
        self.completion_status = False
        self.learning_efficiency = 0.0
        
    def add_unit(self, unit: LearningUnit):
        """Add learning unit to curriculum"""
        self.units[unit.unit_id] = unit
    
    def get_next_unit(self) -> Optional[LearningUnit]:
        """Get next appropriate learning unit"""
        units_list = list(self.units.values())
        if self.current_unit_index < len(units_list):
            return units_list[self.current_unit_index]
        return None
    
    def complete_unit(self, unit_id: str, mastery_level: float):
        """Mark unit as completed"""
        if unit_id in self.units:
            self.units[unit_id].completion_status = True
            self.units[unit_id].mastery_level = mastery_level
            self.current_unit_index += 1


class CurriculumLearningSystem:
    """
    Generates and manages self-optimized learning curricula.
    Orders learning from simple to complex, avoiding catastrophic forgetting,
    and maximizing knowledge retention through strategic sequencing.
    """
    
    def __init__(self):
        self.curricula: Dict[str, Curriculum] = {}
        self.learning_units: Dict[str, LearningUnit] = {}
        self.completion_history: List[Dict] = []
        self.domain_complexity: Dict[str, float] = {}
        self.prerequisite_graph: Dict[str, List[str]] = defaultdict(list)
        self.learning_effectiveness: Dict[str, float] = {}
        
        self.curricula_file = config.DATA_DIR / "curricula.json"
        self.load_curricula()
        
        logger.info("[CURRICULUM] Curriculum Learning System initialized")
    
    def load_curricula(self):
        """Load previously generated curricula"""
        try:
            if self.curricula_file.exists():
                with open(self.curricula_file, 'r') as f:
                    curricula_data = json.load(f)
                    logger.info(f"[CURRICULUM] Loaded {len(curricula_data)} curricula")
        except Exception as e:
            logger.error(f"[CURRICULUM] Error loading curricula: {e}")
    
    def generate_curriculum(self, goal: str, domain: str, 
                          available_topics: List[str]) -> Curriculum:
        """
        Generate a self-optimized curriculum for learning.
        Orders topics from simpler to more complex, respecting prerequisites.
        """
        curriculum_id = f"curriculum_{domain}_{datetime.now().timestamp()}"
        curriculum = Curriculum(curriculum_id, goal, domain)
        
        try:
            # Step 1: Classify topics by difficulty
            topic_difficulty = self._estimate_topic_difficulty(available_topics)
            
            # Step 2: Build prerequisite graph
            prereq_graph = self._build_prerequisite_graph(available_topics)
            
            # Step 3: Generate learning sequence
            sequence = self._topological_sort_by_difficulty(
                available_topics, 
                topic_difficulty, 
                prereq_graph
            )
            
            # Step 4: Create learning units and add to curriculum
            unit_index = 0
            for topic in sequence:
                unit_id = f"{curriculum_id}_unit_{unit_index}"
                difficulty = topic_difficulty.get(topic, 0.5)
                prerequisites = prereq_graph.get(topic, [])
                
                unit = LearningUnit(unit_id, topic, difficulty, prerequisites)
                curriculum.add_unit(unit)
                self.learning_units[unit_id] = unit
                unit_index += 1
            
            self.curricula[curriculum_id] = curriculum
            
            logger.info(f"[CURRICULUM] Generated curriculum '{goal}' with {len(sequence)} units for {domain}")
            
        except Exception as e:
            logger.error(f"[CURRICULUM] Error generating curriculum: {e}")
        
        return curriculum
    
    def _estimate_topic_difficulty(self, topics: List[str]) -> Dict[str, float]:
        """
        Estimate difficulty of each topic.
        More complex heuristics can be added based on domain knowledge.
        """
        difficulty_map = {}
        
        try:
            for topic in topics:
                # Estimate based on topic characteristics
                difficulty = 0.5  # Default medium difficulty
                
                # Heuristic 1: Topics with math/algorithms are harder
                hard_keywords = ["algorithm", "matrix", "optimization", "calculus", "theorem"]
                for keyword in hard_keywords:
                    if keyword.lower() in topic.lower():
                        difficulty += 0.2
                
                # Heuristic 2: Foundational topics are easier
                easy_keywords = ["intro", "basics", "overview", "definition", "concept"]
                for keyword in easy_keywords:
                    if keyword.lower() in topic.lower():
                        difficulty -= 0.2
                
                # Heuristic 3: Topic length proxy for complexity
                difficulty += len(topic.split()) * 0.05
                
                # Clamp to [0, 1]
                difficulty = max(0.0, min(1.0, difficulty))
                difficulty_map[topic] = difficulty
                
        except Exception as e:
            logger.error(f"[CURRICULUM] Error estimating difficulty: {e}")
        
        return difficulty_map
    
    def _build_prerequisite_graph(self, topics: List[str]) -> Dict[str, List[str]]:
        """
        Build prerequisite relationships between topics.
        Using heuristics to infer prerequisites.
        """
        prereq_map = {}
        
        try:
            for topic in topics:
                prerequisites = []
                
                # Heuristic: Look for logical prerequisites
                for other_topic in topics:
                    if other_topic == topic:
                        continue
                    
                    # If other_topic is "foundations" or "basics", it's a prerequisite
                    if any(word in other_topic.lower() for word in ["foundation", "basic", "intro"]):
                        if not any(word in topic.lower() for word in ["foundation", "basic", "intro"]):
                            prerequisites.append(other_topic)
                
                prereq_map[topic] = prerequisites
                
        except Exception as e:
            logger.error(f"[CURRICULUM] Error building prerequisite graph: {e}")
        
        return prereq_map
    
    def _topological_sort_by_difficulty(self, topics: List[str],
                                       difficulty_map: Dict[str, float],
                                       prereq_graph: Dict[str, List[str]]) -> List[str]:
        """
        Order topics respecting prerequisites and difficulty.
        Topics with fewer/met prerequisites should come first.
        Among same-level topics, easier ones come first.
        """
        sorted_topics = []
        remaining = set(topics)
        met_prerequisites = set()
        
        try:
            while remaining:
                # Find topics whose prerequisites are met
                available = []
                for topic in remaining:
                    prereqs = prereq_graph.get(topic, [])
                    if all(p in met_prerequisites for p in prereqs):
                        available.append(topic)
                
                if not available:
                    # No prerequisites satisfied, just take easiest
                    available = list(remaining)
                
                # Sort available by difficulty (easiest first)
                available.sort(key=lambda t: difficulty_map.get(t, 0.5))
                
                # Take the easiest one
                chosen = available[0]
                sorted_topics.append(chosen)
                remaining.remove(chosen)
                met_prerequisites.add(chosen)
            
        except Exception as e:
            logger.error(f"[CURRICULUM] Error in topological sort: {e}")
            sorted_topics = list(topics)  # Fallback
        
        return sorted_topics
    
    def adapt_curriculum(self, curriculum_id: str, performance_data: Dict):
        """
        Dynamically adapt curriculum based on learner performance.
        If struggling, insert easier review units.
        If excelling, increase difficulty or skip units.
        """
        if curriculum_id not in self.curricula:
            return
        
        curriculum = self.curricula[curriculum_id]
        current_mastery = performance_data.get("mastery_level", 0.5)
        time_taken = performance_data.get("time_taken", 1.0)
        errors = performance_data.get("errors", 0)
        
        try:
            if current_mastery < 0.6:
                # Struggling: insert review unit or repeat current
                logger.info(f"[CURRICULUM] Student struggling in {curriculum_id}, adapting...")
                # Could insert additional practice units here
            
            elif current_mastery > 0.9 and time_taken < 0.5:
                # Excelling: can skip ahead or increase difficulty
                logger.info(f"[CURRICULUM] Student excelling in {curriculum_id}, accelerating...")
                curriculum.current_unit_index += 1
            
            # Update learning efficiency
            efficiency = current_mastery / max(0.1, time_taken)
            curriculum.learning_efficiency = efficiency
            
        except Exception as e:
            logger.error(f"[CURRICULUM] Error adapting curriculum: {e}")
    
    def get_next_learning_target(self, curriculum_id: str) -> Optional[LearningUnit]:
        """Get the next unit the AI should learn"""
        if curriculum_id not in self.curricula:
            return None
        
        curriculum = self.curricula[curriculum_id]
        return curriculum.get_next_unit()
    
    def record_unit_completion(self, curriculum_id: str, unit_id: str, 
                              mastery_level: float, time_taken: float):
        """Record completion of a learning unit"""
        if curriculum_id not in self.curricula:
            return
        
        curriculum = self.curricula[curriculum_id]
        
        try:
            if unit_id in curriculum.units:
                unit = curriculum.units[unit_id]
                unit.completion_status = True
                unit.mastery_level = mastery_level
                unit.practice_count += 1
                unit.last_practiced = datetime.now().isoformat()
                
                # Record in completion history
                completion_record = {
                    "curriculum_id": curriculum_id,
                    "unit_id": unit_id,
                    "topic": unit.topic,
                    "mastery_level": mastery_level,
                    "time_taken": time_taken,
                    "completed_at": datetime.now().isoformat()
                }
                self.completion_history.append(completion_record)
                
                # Move to next unit
                curriculum.current_unit_index += 1
                
                logger.info(f"[CURRICULUM] Completed unit {unit_id} with mastery {mastery_level:.2f}")
                
        except Exception as e:
            logger.error(f"[CURRICULUM] Error recording unit completion: {e}")
    
    def create_spaced_review_schedule(self, curriculum_id: str, days_lookahead: int = 30) -> List[Dict]:
        """
        Create spaced repetition schedule for review.
        Reviews are scheduled based on Ebbinghaus forgetting curve.
        """
        schedule = []
        
        try:
            if curriculum_id not in self.curricula:
                return schedule
            
            curriculum = self.curricula[curriculum_id]
            
            for unit in curriculum.units.values():
                if unit.completion_status and unit.mastery_level < 1.0:
                    # Schedule reviews at increasing intervals
                    intervals = [1, 3, 7, 14, 30]  # Days
                    
                    for interval in intervals:
                        review = {
                            "unit_id": unit.unit_id,
                            "topic": unit.topic,
                            "days_until_review": interval,
                            "reason": "spaced_repetition",
                            "estimated_time": unit.estimated_time * 0.5
                        }
                        schedule.append(review)
            
            logger.info(f"[CURRICULUM] Created spaced review schedule with {len(schedule)} reviews")
            
        except Exception as e:
            logger.error(f"[CURRICULUM] Error creating review schedule: {e}")
        
        return schedule
    
    def get_curriculum_progress(self, curriculum_id: str) -> Dict:
        """Get detailed progress on curriculum"""
        if curriculum_id not in self.curricula:
            return {}
        
        curriculum = self.curricula[curriculum_id]
        total_units = len(curriculum.units)
        completed_units = sum(1 for u in curriculum.units.values() if u.completion_status)
        avg_mastery = np.mean([u.mastery_level for u in curriculum.units.values()]) if total_units > 0 else 0.0
        
        return {
            "curriculum_id": curriculum_id,
            "goal": curriculum.learning_goal,
            "domain": curriculum.domain,
            "total_units": total_units,
            "completed_units": completed_units,
            "completion_percentage": (completed_units / total_units * 100) if total_units > 0 else 0,
            "average_mastery": float(avg_mastery),
            "learning_efficiency": curriculum.learning_efficiency,
            "status": "completed" if curriculum.completion_status else "in_progress"
        }
    
    def save_curricula(self):
        """Persist curricula to disk"""
        try:
            curricula_data = {}
            for curr_id, curriculum in self.curricula.items():
                curricula_data[curr_id] = {
                    "goal": curriculum.learning_goal,
                    "domain": curriculum.domain,
                    "units_count": len(curriculum.units),
                    "completion_status": curriculum.completion_status
                }
            
            with open(self.curricula_file, 'w') as f:
                json.dump(curricula_data, f, indent=2)
            
            logger.info(f"[CURRICULUM] Saved {len(self.curricula)} curricula")
        except Exception as e:
            logger.error(f"[CURRICULUM] Error saving curricula: {e}")
    
    def get_system_summary(self) -> Dict:
        """Get summary of curriculum system status"""
        total_units = len(self.learning_units)
        completed_units = sum(1 for u in self.learning_units.values() if u.completion_status)
        
        return {
            "total_curricula": len(self.curricula),
            "total_units": total_units,
            "completed_units": completed_units,
            "completion_history_size": len(self.completion_history),
            "domains": list(self.domain_complexity.keys())
        }
