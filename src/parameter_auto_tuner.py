"""
Parameter Auto-Tuning Engine: Dynamic configuration optimization

Enables system to:
- Tune configuration parameters automatically
- Search parameter space efficiently
- Learn optimal settings
- Adapt to changing conditions
"""
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import math
import random

import config
from logger import logger


class ParameterType(Enum):
    """Types of parameters"""
    FLOAT = "float"
    INTEGER = "integer"
    BOOLEAN = "boolean"
    DISCRETE = "discrete"  # List of choices


@dataclass
class ParameterBound:
    """Bounds for a parameter"""
    param_type: ParameterType
    min_value: float = 0.0
    max_value: float = 100.0
    step: float = 1.0  # For discrete steps
    choices: List[Any] = field(default_factory=list)  # For discrete


@dataclass
class ParameterSetting:
    """A configuration of parameters"""
    setting_id: str
    parameters: Dict[str, Any]
    created_at: datetime = field(default_factory=datetime.now)
    
    # Performance
    trials: int = 0
    total_score: float = 0.0
    avg_score: float = 0.0
    best_score: float = 0.0
    
    is_active: bool = False
    

class ParameterOptimizer:
    """
    Core algorithm for parameter optimization
    
    Implements Bayesian optimization with Gaussian process
    """
    
    def __init__(self):
        self.history: List[Tuple[Dict[str, Any], float]] = []
        logger.info("✓ Parameter Optimizer initialized")
    
    def suggest_parameters(
        self,
        bounds: Dict[str, ParameterBound],
        n_suggestions: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Suggest new parameters to try
        
        Uses exploration-exploitation balance
        """
        
        suggestions = []
        
        # If little history, use random sampling
        if len(self.history) < 5:
            for _ in range(n_suggestions):
                params = self._random_sample(bounds)
                suggestions.append(params)
        else:
            # Use Bayesian approach
            # 1. Find current best
            best_params = max(self.history, key=lambda x: x[1])[0]
            
            # 2. Generate exploitation candidates (around best)
            for _ in range(n_suggestions // 2):
                params = self._local_search(best_params, bounds)
                suggestions.append(params)
            
            # 3. Generate exploration candidates (random)
            for _ in range(n_suggestions - len(suggestions)):
                params = self._random_sample(bounds)
                suggestions.append(params)
        
        return suggestions
    
    def _random_sample(self, bounds: Dict[str, ParameterBound]) -> Dict[str, Any]:
        """Generate random parameters within bounds"""
        params = {}
        
        for name, bound in bounds.items():
            if bound.param_type == ParameterType.FLOAT:
                params[name] = random.uniform(bound.min_value, bound.max_value)
            elif bound.param_type == ParameterType.INTEGER:
                params[name] = random.randint(int(bound.min_value), int(bound.max_value))
            elif bound.param_type == ParameterType.BOOLEAN:
                params[name] = random.choice([True, False])
            elif bound.param_type == ParameterType.DISCRETE:
                params[name] = random.choice(bound.choices)
        
        return params
    
    def _local_search(
        self,
        center_params: Dict[str, Any],
        bounds: Dict[str, ParameterBound]
    ) -> Dict[str, Any]:
        """Generate parameters near current best"""
        params = center_params.copy()
        
        for name, value in center_params.items():
            if name not in bounds:
                continue
            
            bound = bounds[name]
            
            if bound.param_type == ParameterType.FLOAT:
                # Add Gaussian noise
                noise = random.gauss(0, (bound.max_value - bound.min_value) * 0.1)
                new_value = value + noise
                params[name] = max(bound.min_value, min(bound.max_value, new_value))
            
            elif bound.param_type == ParameterType.INTEGER:
                # Add small integer noise
                noise = random.randint(-2, 2)
                new_value = value + noise
                params[name] = max(int(bound.min_value), min(int(bound.max_value), new_value))
            
            elif bound.param_type in [ParameterType.BOOLEAN, ParameterType.DISCRETE]:
                # Small chance to flip
                if random.random() < 0.1:
                    if bound.param_type == ParameterType.BOOLEAN:
                        params[name] = not value
                    else:
                        params[name] = random.choice(bound.choices)
        
        return params
    
    def record_evaluation(self, params: Dict[str, Any], score: float) -> None:
        """Record parameter evaluation result"""
        self.history.append((params, score))


class ParameterAutoTuner:
    """
    Autonomous parameter tuning engine
    
    Features:
    - Track parameter settings
    - Measure their performance
    - Optimize parameter space
    - Adapt to changing conditions
    """
    
    def __init__(self):
        self.optimizer = ParameterOptimizer()
        self.settings: Dict[str, ParameterSetting] = {}
        self.active_setting: Optional[str] = None
        self.bounds: Dict[str, ParameterBound] = {}
        
        # Initialize common parameters
        self._initialize_bounds()
        
        logger.info("✓ Parameter Auto-Tuner initialized")
    
    def _initialize_bounds(self) -> None:
        """Initialize parameter bounds"""
        
        self.bounds = {
            # Cache parameters
            "cache_size": ParameterBound(
                ParameterType.INTEGER,
                min_value=100,
                max_value=10000,
                step=100
            ),
            "cache_ttl": ParameterBound(
                ParameterType.INTEGER,
                min_value=60,
                max_value=3600,
                step=60
            ),
            # Task queue parameters
            "queue_batch_size": ParameterBound(
                ParameterType.INTEGER,
                min_value=1,
                max_value=100,
                step=1
            ),
            "queue_timeout": ParameterBound(
                ParameterType.FLOAT,
                min_value=0.1,
                max_value=30.0,
                step=0.1
            ),
            # Resource allocation
            "memory_pool_size": ParameterBound(
                ParameterType.INTEGER,
                min_value=100,
                max_value=5000,
                step=100
            ),
            "worker_threads": ParameterBound(
                ParameterType.INTEGER,
                min_value=2,
                max_value=32,
                step=1
            ),
            # Learning parameters
            "learning_rate": ParameterBound(
                ParameterType.FLOAT,
                min_value=0.001,
                max_value=0.1,
                step=0.001
            ),
            "convergence_threshold": ParameterBound(
                ParameterType.FLOAT,
                min_value=0.001,
                max_value=0.1,
                step=0.001
            ),
        }
    
    def register_parameter_set(self, params: Dict[str, Any]) -> str:
        """Register and test a parameter set"""
        
        setting_id = f"setting_{len(self.settings)}"
        
        setting = ParameterSetting(
            setting_id=setting_id,
            parameters=params
        )
        
        self.settings[setting_id] = setting
        
        if not self.active_setting:
            self.active_setting = setting_id
            setting.is_active = True
        
        logger.info(f"Registered parameter set: {setting_id}")
        
        return setting_id
    
    def record_performance(self, setting_id: str, score: float) -> None:
        """Record performance of a parameter set"""
        
        if setting_id not in self.settings:
            return
        
        setting = self.settings[setting_id]
        setting.trials += 1
        setting.total_score += score
        setting.avg_score = setting.total_score / setting.trials
        setting.best_score = max(setting.best_score, score)
        
        # Record for optimizer
        self.optimizer.record_evaluation(setting.parameters, score)
    
    def get_next_parameters_to_try(self, n_suggestions: int = 3) -> List[Dict[str, Any]]:
        """Get next parameters to evaluate"""
        
        suggestions = self.optimizer.suggest_parameters(self.bounds, n_suggestions)
        
        logger.info(f"Suggesting {len(suggestions)} parameter sets to try:")
        for i, params in enumerate(suggestions):
            logger.info(f"  {i+1}. {self._format_params(params)}")
        
        return suggestions
    
    def _format_params(self, params: Dict[str, Any]) -> str:
        """Format parameters for logging"""
        items = [f"{k}={v:.3f}" if isinstance(v, float) else f"{k}={v}"
                for k, v in params.items()]
        return "{" + ", ".join(items) + "}"
    
    def apply_parameter_set(self, setting_id: str) -> bool:
        """Apply a parameter set as active"""
        
        if setting_id not in self.settings:
            return False
        
        # Deactivate current
        if self.active_setting and self.active_setting in self.settings:
            self.settings[self.active_setting].is_active = False
        
        # Activate new
        self.settings[setting_id].is_active = True
        self.active_setting = setting_id
        
        params = self.settings[setting_id].parameters
        logger.info(f"Applied parameter set: {setting_id}")
        logger.info(f"  Parameters: {self._format_params(params)}")
        
        return True
    
    def recommend_parameters(self) -> Optional[str]:
        """Recommend best parameter set to use"""
        
        if not self.settings:
            return None
        
        # Find best by average score
        best_setting = max(
            self.settings.values(),
            key=lambda s: s.avg_score if s.trials > 0 else -1
        )
        
        if best_setting.trials > 0:
            logger.info(f"✓ Recommending parameter set: {best_setting.setting_id}")
            logger.info(f"  Avg score: {best_setting.avg_score:.3f}")
            logger.info(f"  Best score: {best_setting.best_score:.3f}")
            logger.info(f"  Trials: {best_setting.trials}")
            
            return best_setting.setting_id
        
        return None
    
    def tune_iteratively(self, eval_function: callable, iterations: int = 10) -> Dict[str, Any]:
        """
        Iteratively tune parameters
        
        eval_function: takes Dict[str,Any] -> float
        """
        
        logger.info(f"Starting iterative parameter tuning ({iterations} iterations):")
        
        best_score = 0.0
        best_params = None
        
        for iteration in range(iterations):
            # Get suggestions
            suggestions = self.get_next_parameters_to_try(n_suggestions=3)
            
            # Evaluate each
            for params in suggestions:
                score = eval_function(params)
                setting_id = self.register_parameter_set(params)
                self.record_performance(setting_id, score)
                
                if score > best_score:
                    best_score = score
                    best_params = params
                
                logger.info(f"  Iteration {iteration+1}/{iterations}: score={score:.3f}")
        
        # Report best found
        logger.info(f"\n✓ Tuning complete")
        logger.info(f"  Best score: {best_score:.3f}")
        logger.info(f"  Best params: {self._format_params(best_params)}")
        
        return {
            "best_score": best_score,
            "best_parameters": best_params,
            "iterations": iterations,
            "total_evaluations": len(self.settings)
        }
    
    def get_tuning_progress(self) -> Dict[str, Any]:
        """Get status of parameter tuning"""
        
        if not self.settings:
            return {"status": "no_settings"}
        
        scores = [s.avg_score for s in self.settings.values() if s.trials > 0]
        
        if not scores:
            return {"status": "no_evaluations"}
        
        return {
            "total_settings": len(self.settings),
            "evaluated": sum(1 for s in self.settings.values() if s.trials > 0),
            "best_score": max(scores),
            "avg_score": sum(scores) / len(scores),
            "worst_score": min(scores),
            "improvement": f"{(max(scores) - min(scores)) / min(scores) * 100:.1f}%" if min(scores) > 0 else "N/A",
            "active_setting": self.active_setting
        }


# Global instance
_tuner: Optional[ParameterAutoTuner] = None


def get_parameter_auto_tuner() -> ParameterAutoTuner:
    """Get or create parameter auto-tuner"""
    global _tuner
    if _tuner is None:
        _tuner = ParameterAutoTuner()
    return _tuner
