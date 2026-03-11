"""
Reasoning Engine with goal planning and problem solving
"""
import json
from typing import Dict, List, Any, Callable, Optional
from datetime import datetime
import config
from src.logger import logger

class ReasoningEngine:
    \"\"\"Advanced reasoning engine for planning, problem-solving, and decision-making\"\"\"
    
    def __init__(self, kb, memory, learning_engine):
        self.kb = kb
        self.memory = memory
        self.learning = learning_engine
        self.goals: List[Dict] = []
        self.action_history: List[Dict] = []
        self.decision_log: List[Dict] = []
        
        self.goals_file = config.DATA_DIR / "goals.json"
        self.load_goals()
        logger.info("🧠 Reasoning Engine initialized")
    
    def load_goals(self):
        \"\"\"Load goals from disk\"\"\"
        try:
            if self.goals_file.exists():
                with open(self.goals_file, 'r') as f:
                    self.goals = json.load(f)
                logger.info(f\"📌 Loaded {len(self.goals)} goals\")
        except Exception as e:
            logger.error(f\"Error loading goals: {e}\")
    
    def save_goals(self):
        \"\"\"Save goals to disk\"\"\"
        try:
            with open(self.goals_file, 'w') as f:
                json.dump(self.goals, f, indent=2)
        except Exception as e:
            logger.error(f\"Error saving goals: {e}\")
    
    def set_goal(self, goal_name: str, description: str, priority: float = 0.5,
                 deadline: Optional[str] = None) -> Dict:
        \"\"\"Set a new goal for the AI\"\"\"
        goal = {
            "id": len(self.goals),
            "name": goal_name,
            "description": description,
            "priority": min(max(priority, 0), 1.0),
            "deadline": deadline,
            "created_at": datetime.now().isoformat(),
            "status": "pending\",
            "progress": 0.0,
            "sub_goals": []
        }
        
        self.goals.append(goal)
        logger.info(f\"🎯 Goal created: {goal_name}\")
        self.memory.store_long_term(f\"goal_{goal['id']}\", goal, importance=goal[\"priority\"])
        
        return goal
    
    def decompose_goal(self, goal_id: int, sub_goals: List[str]) -> List[Dict]:
        \"\"\"Break down a goal into sub-goals\"\"\"
        if goal_id >= len(self.goals):
            logger.error(f\"Goal {goal_id} not found\")
            return []
        
        goal = self.goals[goal_id]
        goal[\"sub_goals\"] = sub_goals
        
        logger.info(f\"📋 Decomposed goal '{goal['name']}' into {len(sub_goals)} sub-goals\")
        
        # Store decomposition as learning
        self.memory.store_episode(
            description=f\"Goal decomposition: {goal['name']}\",
            actions=[\"Analyze goal\", \"Create sub-goals\"],
            outcomes=sub_goals,
            importance=goal[\"priority\"]
        )
        
        return [{\"text\": sg, \"status\": \"pending\"} for sg in sub_goals]
    
    def plan_actions(self, goal_id: int) -> List[Dict]:
        \"\"\"Generate action plan for achieving a goal\"\"\"
        if goal_id >= len(self.goals):
            return []
        
        goal = self.goals[goal_id]
        
        # Search for relevant knowledge
        relevant_knowledge = self.kb.search(goal[\"description\"], top_k=5)
        
        # Generate action plan based on knowledge and patterns
        actions = []
        for i, knowledge in enumerate(relevant_knowledge):
            action = {
                \"id\": i,
                \"description\": f\"Use knowledge: {knowledge.get('content', '')[:100]}\",
                \"step\": i + 1,
                \"status\": \"pending\",
                \"estimated_importance\": knowledge.get(\"relevance_score\", 0.5)
            }
            actions.append(action)
        
        logger.info(f\"📍 Generated {len(actions)} actions for goal: {goal['name']}\")
        self.memory.store_short_term(f\"plan_{goal_id}\", actions)
        
        return actions
    
    def make_decision(self, options: List[Dict], context: Dict) -> Dict:
        \"\"\"Make a decision among options\"\"\"
        # Score each option based on multiple criteria
        scored_options = []
        
        for option in options:
            score = self._calculate_option_score(option, context)
            scored_options.append((option, score))
        
        # Select best option
        best_option, best_score = max(scored_options, key=lambda x: x[1])
        
        decision = {
            \"timestamp\": datetime.now().isoformat(),
            \"options_count\": len(options),
            \"selected_option\": best_option,
            \"confidence\": best_score,
            \"context\": context
        }
        
        self.decision_log.append(decision)
        logger.info(f\"✅ Decision made with confidence: {best_score:.2%}\")
        
        return decision
    
    def _calculate_option_score(self, option: Dict, context: Dict) -> float:
        \"\"\"Calculate score for an option\"\"\"
        base_score = option.get(\"priority\", 0.5)
        
        # Check if similar patterns exist
        pattern_boost = 0.0
        for pattern in self.learning.learned_patterns:
            if option.get(\"type\") == pattern.get(\"name\"):
                pattern_boost = pattern.get(\"confidence\", 0.5) * 0.3
                break
        
        # Check historical success
        history_boost = 0.0
        relevant_history = [a for a in self.action_history 
                          if a.get(\"type\") == option.get(\"type\")]
        if relevant_history:
            success_count = sum(1 for a in relevant_history if a.get(\"successful\", False))
            history_boost = (success_count / len(relevant_history)) * 0.2
        
        return min(base_score + pattern_boost + history_boost, 1.0)
    
    def reason_about(self, topic: str, context: Dict) -> Dict:
        \"\"\"Perform reasoning about a topic\"\"\"
        logger.info(f\"💭 Reasoning about: {topic}\")
        
        # Gather relevant knowledge
        knowledge_items = self.kb.search(topic, top_k=10)
        
        # Extract insights
        reasoning_result = {
            \"timestamp\": datetime.now().isoformat(),
            \"topic\": topic,
            \"knowledge_sources\": len(knowledge_items),
            \"insights\": self._extract_insights(knowledge_items),
            \"confidence\": self._calculate_reasoning_confidence(knowledge_items),
            \"next_questions\": self._generate_follow_up_questions(topic, knowledge_items)
        }
        
        logger.info(f\"🎓 Reasoning complete - confidence: {reasoning_result['confidence']:.2%}\")
        
        return reasoning_result
    
    def _extract_insights(self, knowledge_items: List[Dict]) -> List[str]:
        \"\"\"Extract key insights from knowledge\"\"\"
        insights = []
        for item in knowledge_items[:3]:
            content = item.get(\"content\", \"\")
            if len(content) > 50:
                insights.append(content[:150])
        return insights
    
    def _calculate_reasoning_confidence(self, knowledge_items: List[Dict]) -> float:
        \"\"\"Calculate confidence in reasoning\"\"\"
        if not knowledge_items:
            return 0.0
        return min(len(knowledge_items) / 10, 1.0)
    
    def _generate_follow_up_questions(self, topic: str, knowledge_items: List[Dict]) -> List[str]:
        \"\"\"Generate follow-up questions for deeper understanding\"\"\"
        return [
            f\"What are the practical applications of {topic}?\",
            f\"How does {topic} relate to other domains?\",
            f\"What are the latest developments in {topic}?\"
        ]
    
    def record_action(self, action_type: str, description: str, 
                     successful: bool, result: Any) -> Dict:
        \"\"\"Record an action taken and its outcome\"\"\"
        action_record = {
            \"timestamp\": datetime.now().isoformat(),
            \"type\": action_type,
            \"description\": description,
            \"successful\": successful,
            \"result\": str(result)[:200]
        }
        
        self.action_history.append(action_record)
        logger.info(f\"📝 Action recorded: {action_type} - {'✅' if successful else '❌'}\")
        
        # Update skills based on success
        if successful:
            self.learning.improve_skill(action_type, [{\"success\": True}])
        
        return action_record
    
    def get_reasoning_stats(self) -> Dict:
        \"\"\"Get reasoning statistics\"\"\"
        successful_actions = sum(1 for a in self.action_history if a.get(\"successful\", False))
        return {
            \"total_goals\": len(self.goals),
            \"total_actions\": len(self.action_history),
            \"successful_actions\": successful_actions,
            \"success_rate\": successful_actions / len(self.action_history) if self.action_history else 0,
            \"decisions_made\": len(self.decision_log),
            \"avg_decision_confidence\": sum(d.get(\"confidence\", 0) for d in self.decision_log) / len(self.decision_log) if self.decision_log else 0
        }
