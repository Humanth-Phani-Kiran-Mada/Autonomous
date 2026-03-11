"""
Autonomous Goal Generation: Self-motivated goal creation and refinement
The AI autonomously generates meaningful goals based on its state and aspirations
"""
import json
from typing import Dict, List, Tuple
from datetime import datetime, timedelta
import numpy as np
from pathlib import Path
import config
from .logger import logger


class AutonomousGoalGenerator:
    """
    Generates goals autonomously based on:
    - Capability gaps (what it can't do well)
    - Knowledge gaps (what it doesn't know)
    - Performance plateaus (where it's stuck)
    - New opportunities (what it could learn)
    - Intrinsic motivation (curiosity-driven learning)
    """
    
    def __init__(self, self_model, learning_engine):
        self.self_model = self_model
        self.learning_engine = learning_engine
        
        self.generated_goals: List[Dict] = []
        self.goal_derivations: List[Dict] = []
        self.fulfilled_goals: List[Dict] = []
        self.motivation_sources: Dict[str, float] = {}
        
        self.goals_file = config.DATA_DIR / "autonomous_goals.json"
        self.motivations_file = config.DATA_DIR / "motivations.json"
        
        self._initialize_motivation_sources()
        self.load_generated_goals()
        logger.info("🎯 Autonomous Goal Generator initialized")
    
    def _initialize_motivation_sources(self):
        """Initialize sources of intrinsic motivation"""
        self.motivation_sources = {
            "curiosity": 0.3,  # Interest in new knowledge
            "competence": 0.3,  # Drive to improve capabilities
            "autonomy": 0.2,   # Drive to act independently
            "mastery": 0.2    # Drive to achieve excellence
        }
    
    def load_generated_goals(self):
        """Load previously generated goals"""
        try:
            if self.goals_file.exists():
                with open(self.goals_file, 'r') as f:
                    data = json.load(f)
                    self.generated_goals = data.get("goals", [])
                    self.fulfilled_goals = data.get("fulfilled", [])
            logger.info(f"📂 Loaded {len(self.generated_goals)} autonomous goals")
        except Exception as e:
            logger.error(f"Error loading goals: {e}")
    
    def save_generated_goals(self):
        """Persist generated goals"""
        try:
            goals_data = {
                "goals": self.generated_goals,
                "fulfilled": self.fulfilled_goals,
                "saved_at": datetime.now().isoformat()
            }
            with open(self.goals_file, 'w') as f:
                json.dump(goals_data, f, indent=2)
            logger.debug("💾 Autonomous goals saved")
        except Exception as e:
            logger.error(f"Error saving goals: {e}")
    
    def generate_goals_autonomously(self) -> List[Dict]:
        """Generate goals based on current state and motivations"""
        logger.info("🧠 Generating autonomous goals...")
        
        new_goals = []
        
        # Goal 1: Fill capability gaps
        capability_gap_goals = self._generate_capability_gap_goals()
        new_goals.extend(capability_gap_goals)
        
        # Goal 2: Explore knowledge gaps
        knowledge_gap_goals = self._generate_knowledge_gap_goals()
        new_goals.extend(knowledge_gap_goals)
        
        # Goal 3: Break performance plateaus
        plateau_goals = self._generate_plateau_breaking_goals()
        new_goals.extend(plateau_goals)
        
        # Goal 4: Curiosity-driven exploration
        curiosity_goals = self._generate_curiosity_driven_goals()
        new_goals.extend(curiosity_goals)
        
        # Goal 5: Meta-improvement goals
        meta_goals = self._generate_meta_improvement_goals()
        new_goals.extend(meta_goals)
        
        # Register new goals
        for goal in new_goals:
            self._register_goal(goal)
        
        logger.info(f"✅ Generated {len(new_goals)} autonomous goals")
        return new_goals
    
    def _generate_capability_gap_goals(self) -> List[Dict]:
        """Generate goals to fill capability gaps"""
        goals = []
        
        capabilities = self.self_model.capabilities
        weak_capabilities = [
            (name, cap) for name, cap in capabilities.items()
            if cap.get("level", 0) < 0.5
        ]
        
        for cap_name, cap_info in sorted(weak_capabilities, 
                                         key=lambda x: x[1].get("level", 0))[:3]:
            gap_size = 0.5 - cap_info.get("level", 0)
            
            goal = {
                "id": len(self.generated_goals) + len(goals),
                "type": "capability_improvement",
                "derived_from": "capability_gaps",
                "name": f"Improve {cap_name}",
                "description": f"Increase {cap_name} capability from {cap_info.get('level', 0):.1%} to 75%",
                "target_capability": cap_name,
                "current_level": cap_info.get("level", 0),
                "target_level": 0.75,
                "priority": 0.8 + (gap_size * 0.2),  # Higher priority for bigger gaps
                "motivation_source": "competence",
                "generated_at": datetime.now().isoformat(),
                "deadline": (datetime.now() + timedelta(days=30)).isoformat(),
                "status": "active"
            }
            
            goals.append(goal)
            
            derivation = {
                "goal_id": goal["id"],
                "source_type": "capability_gaps",
                "reasoning": f"Capability '{cap_name}' at {cap_info.get('level', 0):.1%}, gap of {gap_size:.1%}",
                "timestamp": datetime.now().isoformat()
            }
            self.goal_derivations.append(derivation)
        
        return goals
    
    def _generate_knowledge_gap_goals(self) -> List[Dict]:
        """Generate goals for knowledge acquisition in gaps"""
        goals = []
        
        # Get learning domains summary
        learning_summary = self.learning_engine.get_learning_summary()
        learned_domains = set(d[0] if isinstance(d, tuple) else d 
                            for d in learning_summary.get("most_learned_domains", []))
        
        # Define important domains
        important_domains = ["ai_ml", "programming", "data_science", "reasoning", "optimization"]
        
        # Find gaps
        domain_gaps = [d for d in important_domains if d not in learned_domains]
        
        for domain in domain_gaps[:3]:
            goal = {
                "id": len(self.generated_goals) + len(goals),
                "type": "knowledge_acquisition",
                "derived_from": "knowledge_gaps",
                "name": f"Master {domain}",
                "description": f"Acquire comprehensive knowledge in {domain} domain",
                "target_domain": domain,
                "priority": 0.7,
                "motivation_source": "curiosity",
                "generated_at": datetime.now().isoformat(),
                "deadline": (datetime.now() + timedelta(days=60)).isoformat(),
                "status": "active"
            }
            
            goals.append(goal)
            
            self.goal_derivations.append({
                "goal_id": goal["id"],
                "source_type": "knowledge_gaps",
                "reasoning": f"'{domain}' domain not yet explored, important for AI development",
                "timestamp": datetime.now().isoformat()
            })
        
        return goals
    
    def _generate_plateau_breaking_goals(self) -> List[Dict]:
        """Generate goals to break through performance plateaus"""
        goals = []
        
        # Find capabilities that haven't improved recently
        current_time = datetime.now()
        
        for cap_name, cap_info in self.self_model.capabilities.items():
            last_update = datetime.fromisoformat(cap_info.get("last_updated", datetime.now().isoformat()))
            days_since_update = (current_time - last_update).days
            
            if days_since_update > 7 and cap_info.get("improvement_rate", 0) < 0.01:
                goal = {
                    "id": len(self.generated_goals) + len(goals),
                    "type": "plateau_breakthrough",
                    "derived_from": "performance_plateaus",
                    "name": f"Break plateau in {cap_name}",
                    "description": f"Achieve breakthrough improvement in stagnant {cap_name} capability",
                    "target_capability": cap_name,
                    "priority": 0.65,
                    "motivation_source": "autonomy",
                    "generated_at": datetime.now().isoformat(),
                    "deadline": (datetime.now() + timedelta(days=14)).isoformat(),
                    "status": "active"
                }
                
                goals.append(goal)
                
                self.goal_derivations.append({
                    "goal_id": goal["id"],
                    "source_type": "performance_plateaus",
                    "reasoning": f"'{cap_name}' plateaued for {days_since_update} days, improvement_rate={cap_info.get('improvement_rate', 0):.3f}",
                    "timestamp": datetime.now().isoformat()
                })
        
        return goals[:2]  # Limit to 2
    
    def _generate_curiosity_driven_goals(self) -> List[Dict]:
        """Generate goals driven by curiosity and exploration"""
        goals = []
        
        exploration_topics = [
            {"topic": "Emergent Behavior", "reason": "How complex behavior emerges from simple rules"},
            {"topic": "Self-Organization", "reason": "Understanding self-organizing systems"},
            {"topic": "Optimization Algorithms", "reason": "Novel approach to capability improvement"},
            {"topic": "Reasoning about Uncertainty", "reason": "Better decision-making under uncertainty"}
        ]
        
        for item in exploration_topics[:2]:
            goal = {
                "id": len(self.generated_goals) + len(goals),
                "type": "curiosity_exploration",
                "derived_from": "intrinsic_motivation",
                "name": f"Explore {item['topic']}",
                "description": f"Investigate {item['topic']}: {item['reason']}",
                "topic": item["topic"],
                "priority": 0.5,
                "motivation_source": "curiosity",
                "generated_at": datetime.now().isoformat(),
                "deadline": (datetime.now() + timedelta(days=45)).isoformat(),
                "status": "active"
            }
            
            goals.append(goal)
            
            self.goal_derivations.append({
                "goal_id": goal["id"],
                "source_type": "curiosity",
                "reasoning": f"Intrinsic motivation to understand: {item['reason']}",
                "timestamp": datetime.now().isoformat()
            })
        
        return goals
    
    def _generate_meta_improvement_goals(self) -> List[Dict]:
        """Generate meta-level goals for improving improvement processes"""
        goals = []
        
        goal = {
            "id": len(self.generated_goals) + len(goals),
            "type": "meta_improvement",
            "derived_from": "self_reflection",
            "name": "Optimize learning processes",
            "description": "Analyze and improve own learning strategies, adaptation mechanisms, and goal generation",
            "priority": 0.75,
            "motivation_source": "mastery",
            "generated_at": datetime.now().isoformat(),
            "deadline": (datetime.now() + timedelta(days=30)).isoformat(),
            "status": "active",
            "subitems": [
                "Analyze meta-learning strategy effectiveness",
                "Improve goal generation accuracy",
                "Optimize resource allocation"
            ]
        }
        
        goals.append(goal)
        
        return goals
    
    def _register_goal(self, goal: Dict):
        """Register a new goal"""
        # Check if goal already exists
        for existing in self.generated_goals:
            if (existing["name"] == goal["name"] and 
                existing["status"] != "completed"):
                logger.info(f"📌 Goal already exists: {goal['name']}")
                return
        
        self.generated_goals.append(goal)
        logger.info(f"✅ Registered goal: {goal['name']} (priority={goal.get('priority', 0):.1%})")
    
    def mark_goal_fulfilled(self, goal_id: int) -> bool:
        """Mark a goal as fulfilled"""
        for goal in self.generated_goals:
            if goal["id"] == goal_id:
                goal["status"] = "completed"
                goal["completed_at"] = datetime.now().isoformat()
                
                # Move to fulfilled
                self.fulfilled_goals.append(goal)
                self.generated_goals.remove(goal)
                
                logger.info(f"✅ Goal completed: {goal['name']}")
                
                # Generate follow-up goals
                self._generate_follow_up_goals(goal)
                
                return True
        
        return False
    
    def _generate_follow_up_goals(self, completed_goal: Dict):
        """Generate follow-up goals based on completion"""
        if completed_goal["type"] == "capability_improvement":
            # Create advanced goal to further improve
            follow_up = {
                "id": len(self.generated_goals),
                "type": "advanced_capability",
                "derived_from": "goal_completion",
                "name": f"Master {completed_goal.get('target_capability')}",
                "description": f"Achieve 90%+ proficiency in {completed_goal.get('target_capability')}",
                "target_capability": completed_goal.get("target_capability"),
                "priority": 0.6,
                "generated_at": datetime.now().isoformat(),
                "status": "active"
            }
            self._register_goal(follow_up)
    
    def evaluate_goal_progress(self, goal_id: int) -> Dict:
        """Evaluate progress towards a goal"""
        for goal in self.generated_goals:
            if goal["id"] == goal_id:
                progress = {
                    "goal_id": goal_id,
                    "goal_name": goal["name"],
                    "current_status": goal["status"],
                    "progress_percentage": 0.0,
                    "evaluation_at": datetime.now().isoformat()
                }
                
                # Evaluate based on goal type
                if goal["type"] == "capability_improvement":
                    target_cap = goal.get("target_capability")
                    if target_cap in self.self_model.capabilities:
                        cap = self.self_model.capabilities[target_cap]
                        current = cap.get("level", 0)
                        target = goal.get("target_level", 0.75)
                        initial = goal.get("current_level", 0)
                        
                        progress_range = target - initial
                        current_progress = current - initial
                        progress["progress_percentage"] = (current_progress / progress_range) if progress_range > 0 else 0
                
                return progress
        
        return None
    
    def get_active_goals(self) -> List[Dict]:
        """Get all active goals sorted by priority"""
        active = [g for g in self.generated_goals if g["status"] == "active"]
        return sorted(active, key=lambda x: x.get("priority", 0), reverse=True)
    
    def get_goal_generation_summary(self) -> Dict:
        """Get summary of goal generation state"""
        active_goals = self.get_active_goals()
        
        return {
            "total_generated": len(self.generated_goals) + len(self.fulfilled_goals),
            "active_goals": len(active_goals),
            "completed_goals": len(self.fulfilled_goals),
            "motivation_distribution": self.motivation_sources,
            "top_active_goals": [
                {"name": g["name"], "priority": g.get("priority", 0)}
                for g in active_goals[:3]
            ],
            "goal_types_distribution": self._count_goal_types(),
            "autonomous_motivation_level": sum(self.motivation_sources.values())
        }
    
    def _count_goal_types(self) -> Dict:
        """Count goals by type"""
        type_counts = {}
        for goal in self.generated_goals + self.fulfilled_goals:
            goal_type = goal.get("type", "unknown")
            type_counts[goal_type] = type_counts.get(goal_type, 0) + 1
        return type_counts
