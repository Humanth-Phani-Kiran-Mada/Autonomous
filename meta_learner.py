"""
Meta-Learning Engine: Learn how to learn better
Enables the AI to improve its own learning strategies and adapt to new domains
"""
import json
from typing import Dict, List, Callable, Tuple
from datetime import datetime
import numpy as np
from pathlib import Path
import config
from src.logger import logger


class MetaLearner:
    """
    Meta-learning system that learns to improve learning itself.
    Adapts learning strategies based on domain, tracks strategy effectiveness,
    and automatically improves its approach over time.
    """
    
    def __init__(self, learning_engine, self_model):
        self.learning_engine = learning_engine
        self.self_model = self_model
        
        self.learning_strategies: Dict[str, Dict] = {}
        self.strategy_history: List[Dict] = []
        self.domain_experts: Dict[str, Dict] = {}
        self.adaptation_history: List[Dict] = []
        self.meta_metrics: Dict[str, List[float]] = {}
        
        self.strategies_file = config.DATA_DIR / "learning_strategies.json"
        self.meta_metrics_file = config.DATA_DIR / "meta_metrics.json"
        
        self._initialize_strategies()
        self.load_meta_learning_state()
        logger.info("🧠 Meta-Learning Engine initialized")
    
    def _initialize_strategies(self):
        """Initialize default learning strategies"""
        self.learning_strategies = {
            "deep_learning": {
                "name": "Deep Learning",
                "domain": "ml_ai",
                "effectiveness": 0.5,
                "parameters": {"learning_rate": 0.001, "batch_size": 32, "epochs": 100},
                "usage_count": 0,
                "success_rate": 0.0
            },
            "reinforcement_learning": {
                "name": "Reinforcement Learning",
                "domain": "decision_making",
                "effectiveness": 0.5,
                "parameters": {"exploration_rate": 0.2, "discount_factor": 0.99, "update_rate": 0.1},
                "usage_count": 0,
                "success_rate": 0.0
            },
            "transfer_learning": {
                "name": "Transfer Learning",
                "domain": "knowledge_transfer",
                "effectiveness": 0.5,
                "parameters": {"similarity_threshold": 0.7, "adaptation_rate": 0.1},
                "usage_count": 0,
                "success_rate": 0.0
            },
            "curriculum_learning": {
                "name": "Curriculum Learning",
                "domain": "progressive_learning",
                "effectiveness": 0.5,
                "parameters": {"difficulty_increase": 0.1, "task_batch_size": 10},
                "usage_count": 0,
                "success_rate": 0.0
            },
            "active_learning": {
                "name": "Active Learning",
                "domain": "selective_sampling",
                "effectiveness": 0.5,
                "parameters": {"uncertainty_threshold": 0.5, "sample_ratio": 0.2},
                "usage_count": 0,
                "success_rate": 0.0
            },
            "few_shot_learning": {
                "name": "Few-Shot Learning",
                "domain": "quick_adaptation",
                "effectiveness": 0.5,
                "parameters": {"examples_needed": 5, "similarity_learning": 0.1},
                "usage_count": 0,
                "success_rate": 0.0
            }
        }
    
    def load_meta_learning_state(self):
        """Load meta-learning state from disk"""
        try:
            if self.strategies_file.exists():
                with open(self.strategies_file, 'r') as f:
                    data = json.load(f)
                    self.learning_strategies.update(data.get("strategies", {}))
            
            if self.meta_metrics_file.exists():
                with open(self.meta_metrics_file, 'r') as f:
                    self.meta_metrics = json.load(f)
            
            logger.info("📂 Meta-learning state loaded")
        except Exception as e:
            logger.error(f"Error loading meta-learning state: {e}")
    
    def save_meta_learning_state(self):
        """Persist meta-learning state"""
        try:
            with open(self.strategies_file, 'w') as f:
                json.dump({"strategies": self.learning_strategies}, f, indent=2)
            
            with open(self.meta_metrics_file, 'w') as f:
                json.dump(self.meta_metrics, f, indent=2)
            
            logger.debug("💾 Meta-learning state saved")
        except Exception as e:
            logger.error(f"Error saving meta-learning state: {e}")
    
    def select_strategy(self, domain: str, task_type: str = "general") -> Tuple[str, Dict]:
        """Select the best learning strategy for a given domain and task"""
        # Find strategies matching domain
        matching_strategies = [
            (name, strategy) for name, strategy in self.learning_strategies.items()
            if domain in strategy.get("domain", "") or task_type in strategy.get("domain", "")
        ]
        
        if not matching_strategies:
            matching_strategies = list(self.learning_strategies.items())
        
        # Select based on effectiveness and success rate
        best_strategy = max(matching_strategies, 
                          key=lambda x: x[1]["effectiveness"] * 0.6 + x[1]["success_rate"] * 0.4)
        
        strategy_name, strategy_config = best_strategy
        
        logger.info(f"📋 Selected strategy: {strategy_name} for domain: {domain}")
        return strategy_name, strategy_config
    
    def execute_with_strategy(self, strategy_name: str, task: Callable, 
                             task_args: Dict = None, domain: str = "general") -> Dict:
        """Execute a learning task using a specific strategy"""
        if strategy_name not in self.learning_strategies:
            logger.warning(f"Unknown strategy: {strategy_name}")
            return {"status": "error", "error": "Unknown strategy"}
        
        strategy = self.learning_strategies[strategy_name]
        params = strategy["parameters"].copy()
        
        execution_record = {
            "strategy": strategy_name,
            "domain": domain,
            "timestamp": datetime.now().isoformat(),
            "parameters": params
        }
        
        try:
            # Execute task with strategy parameters
            result = task(**(task_args or {}), **params)
            
            execution_record["status"] = "success"
            execution_record["result"] = result
            execution_record["success"] = True
            
            # Update strategy effectiveness
            self._update_strategy_effectiveness(strategy_name, True, result.get("performance", 0.5))
            
            logger.info(f"✅ Strategy executed: {strategy_name}")
        
        except Exception as e:
            execution_record["status"] = "error"
            execution_record["error"] = str(e)
            execution_record["success"] = False
            
            # Update strategy effectiveness
            self._update_strategy_effectiveness(strategy_name, False, 0.0)
            
            logger.error(f"❌ Strategy execution failed: {e}")
        
        self.strategy_history.append(execution_record)
        return execution_record
    
    def _update_strategy_effectiveness(self, strategy_name: str, success: bool, performance: float = 0.5):
        """Update strategy effectiveness based on results"""
        strategy = self.learning_strategies[strategy_name]
        strategy["usage_count"] += 1
        
        if success:
            strategy["success_rate"] = (strategy["success_rate"] * (strategy["usage_count"] - 1) + 1) / strategy["usage_count"]
            improvement = performance * config.LEARNING_RATE
            strategy["effectiveness"] = min(strategy["effectiveness"] + improvement, 1.0)
        else:
            strategy["success_rate"] = (strategy["success_rate"] * (strategy["usage_count"] - 1)) / strategy["usage_count"]
            strategy["effectiveness"] = max(strategy["effectiveness"] - 0.05, 0.0)
        
        logger.debug(f"📊 Updated {strategy_name}: effectiveness={strategy['effectiveness']:.2%}, success_rate={strategy['success_rate']:.2%}")
    
    def adapt_learning_parameters(self, strategy_name: str, domain: str, 
                                  performance_feedback: float):
        """Adaptively adjust learning parameters based on performance"""
        if strategy_name not in self.learning_strategies:
            return
        
        strategy = self.learning_strategies[strategy_name]
        params = strategy["parameters"]
        
        adaptation = {
            "strategy": strategy_name,
            "domain": domain,
            "timestamp": datetime.now().isoformat(),
            "feedback": performance_feedback,
            "changes": {}
        }
        
        # Adapt parameters based on feedback
        if performance_feedback < 0.3:
            # Poor performance - increase exploration
            if "exploration_rate" in params:
                params["exploration_rate"] = min(params["exploration_rate"] + 0.05, 0.5)
                adaptation["changes"]["exploration_rate"] = f"↑ {params['exploration_rate']}"
            
            if "learning_rate" in params:
                params["learning_rate"] = params["learning_rate"] * 1.5
                adaptation["changes"]["learning_rate"] = f"↑ {params['learning_rate']}"
        
        elif performance_feedback > 0.8:
            # Good performance - increase exploitation
            if "exploration_rate" in params:
                params["exploration_rate"] = max(params["exploration_rate"] - 0.02, 0.05)
                adaptation["changes"]["exploration_rate"] = f"↓ {params['exploration_rate']}"
            
            if "learning_rate" in params:
                params["learning_rate"] = params["learning_rate"] * 0.9
                adaptation["changes"]["learning_rate"] = f"↓ {params['learning_rate']}"
        
        self.adaptation_history.append(adaptation)
        logger.info(f"🔧 Adapted parameters for {strategy_name}: {adaptation['changes']}")
    
    def register_domain_expert(self, domain: str, expert_knowledge: Dict):
        """Register domain-specific learning expertise"""
        self.domain_experts[domain] = {
            "domain": domain,
            "knowledge": expert_knowledge,
            "effectiveness": 0.5,
            "registered_at": datetime.now().isoformat(),
            "applications": 0,
            "success_count": 0
        }
        logger.info(f"🏆 Registered domain expert: {domain}")
    
    def get_domain_specific_strategy(self, domain: str) -> Dict:
        """Get domain-specific learning strategy"""
        if domain in self.domain_experts:
            expert = self.domain_experts[domain]
            logger.info(f"🎯 Using domain expert knowledge for: {domain}")
            return expert["knowledge"]
        else:
            # Generate generic strategy
            return self._generate_generic_strategy(domain)
    
    def _generate_generic_strategy(self, domain: str) -> Dict:
        """Generate a generic strategy for unknown domains"""
        return {
            "domain": domain,
            "learning_rate": 0.01,
            "exploration_rate": 0.15,
            "batch_processing": True,
            "adaptive": True
        }
    
    def learn_from_failure(self, failed_task: Dict, failure_context: Dict) -> Dict:
        """Learn from failures and adjust strategy"""
        logger.info(f"🔍 Analyzing failure: {failed_task.get('task_name', 'unknown')}")
        
        failure_analysis = {
            "timestamp": datetime.now().isoformat(),
            "failed_task": failed_task,
            "context": failure_context,
            "root_causes": [],
            "recommended_changes": []
        }
        
        # Analyze failure root causes
        if failed_task.get("error_type") == "performance":
            failure_analysis["root_causes"].append("Suboptimal strategy parameters")
            failure_analysis["recommended_changes"].append("Adapt learning rate and exploration")
        
        if failed_task.get("error_type") == "timeout":
            failure_analysis["root_causes"].append("Computational complexity exceeded")
            failure_analysis["recommended_changes"].append("Use simpler model or reduce data size")
        
        if failed_task.get("error_type") == "convergence":
            failure_analysis["root_causes"].append("Goals are unrealistic for current capabilities")
            failure_analysis["recommended_changes"].append("Decompose into simpler sub-tasks")
        
        # Update self-model with failure
        self.self_model.analyze_error_patterns(
            error_type=failed_task.get("error_type", "unknown"),
            context=failure_context,
            capability=failed_task.get("capability", "learning")
        )
        
        logger.info(f"📋 Analysis complete: {len(failure_analysis['recommended_changes'])} recommendations")
        return failure_analysis
    
    def get_meta_learning_summary(self) -> Dict:
        """Get comprehensive meta-learning summary"""
        strategy_stats = {}
        for name, strategy in self.learning_strategies.items():
            strategy_stats[name] = {
                "effectiveness": strategy["effectiveness"],
                "success_rate": strategy["success_rate"],
                "usage_count": strategy["usage_count"]
            }
        
        return {
            "strategies_count": len(self.learning_strategies),
            "domain_experts": len(self.domain_experts),
            "strategy_history_size": len(self.strategy_history),
            "adaptations_made": len(self.adaptation_history),
            "strategy_stats": strategy_stats,
            "top_strategy": max(strategy_stats.items(), key=lambda x: x[1]["effectiveness"])[0] if strategy_stats else None
        }
    
    def recommend_learning_path(self, goal: str, current_capabilities: Dict) -> List[Dict]:
        """Recommend optimal learning path to achieve a goal"""
        logger.info(f"🗺️ Planning learning path for: {goal}")
        
        path = []
        gap_analysis = {goal: {"target": 1.0, "current": current_capabilities.get(goal, 0.0)}}
        
        # Identify capability gaps
        gaps = sorted(gap_analysis.items(), key=lambda x: x[1]["current"] - x[1]["target"])
        
        for capability, levels in gaps:
            gap_size = levels["target"] - levels["current"]
            
            # Recommend strategies based on gap size
            if gap_size > 0.5:
                strategy_recommendation = "Use curriculum learning: start with simple tasks"
            elif gap_size > 0.2:
                strategy_recommendation = "Use transfer learning from similar domains"
            else:
                strategy_recommendation = "Use reinforcement learning for fine-tuning"
            
            path.append({
                "capability": capability,
                "current_level": levels["current"],
                "target_level": levels["target"],
                "gap": gap_size,
                "recommended_strategy": strategy_recommendation,
                "estimated_time": gap_size * 100  # Iterations
            })
        
        return path
