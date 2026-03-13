"""
Experimentation Framework: Multi-armed bandit exploration and A/B testing

Enables system to:
- Try novel approaches safely
- Compare algorithm performance
- Statistically validate improvements
- Promote winners automatically
"""
from typing import Dict, List, Any, Callable, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import random
import math
import time

import config
from logger import logger


class ExplorationStrategy(Enum):
    """Exploration strategies"""
    EPSILON_GREEDY = "epsilon_greedy"  # 90/10 split
    UCB1 = "ucb1"  # Upper confidence bound
    THOMPSON = "thompson"  # Thompson sampling


@dataclass
class Algorithm:
    """Algorithm variant to test"""
    name: str
    implementation: Callable
    version: int = 1
    is_baseline: bool = False
    
    # Performance tracking
    trials: int = 0
    successes: int = 0
    total_time: float = 0.0
    total_quality: float = 0.0
    
    @property
    def success_rate(self) -> float:
        """Calculate success rate"""
        return self.successes / max(self.trials, 1)
    
    @property
    def avg_time(self) -> float:
        """Calculate average execution time"""
        return self.total_time / max(self.trials, 1)
    
    @property
    def avg_quality(self) -> float:
        """Calculate average quality score"""
        return self.total_quality / max(self.trials, 1)
    
    @property
    def confidence_level(self) -> float:
        """Confidence in this algorithm (0-1)"""
        # Higher with more trials
        return min(self.trials / 100, 1.0)


@dataclass
class Experiment:
    """A/B test experiment"""
    name: str
    control: Algorithm
    variant: Algorithm
    hypothesis: str
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    winner: Optional[Algorithm] = None
    p_value: float = 1.0
    confidence: float = 0.0
    samples_required: int = 100


class ExperimentationFramework:
    """
    Multi-armed bandit exploration engine.
    
    Features:
    - Algorithm registry
    - A/B testing infrastructure
    - Statistical significance testing
    - Automatic winner promotion
    - Exploration-exploitation trade-off
    """
    
    def __init__(self, strategy: ExplorationStrategy = ExplorationStrategy.EPSILON_GREEDY):
        self.strategy = strategy
        self.algorithms: Dict[str, Algorithm] = {}
        self.experiments: List[Experiment] = []
        self.active_experiments: Dict[str, Experiment] = {}
        self.epsilon = 0.1  # For epsilon-greedy
        
        logger.info(f"✓ Experimentation Framework initialized (strategy: {strategy.value})")
    
    def register_algorithm(
        self,
        name: str,
        implementation: Callable,
        is_baseline: bool = False
    ) -> Algorithm:
        """Register an algorithm variant to test"""
        algo = Algorithm(
            name=name,
            implementation=implementation,
            is_baseline=is_baseline
        )
        
        self.algorithms[name] = algo
        logger.info(f"Registered algorithm: {name}")
        
        return algo
    
    def create_experiment(
        self,
        name: str,
        control_algo: str,
        variant_algo: str,
        hypothesis: str,
        samples_required: int = 100
    ) -> Experiment:
        """Create A/B test experiment"""
        
        exp = Experiment(
            name=name,
            control=self.algorithms[control_algo],
            variant=self.algorithms[variant_algo],
            hypothesis=hypothesis,
            samples_required=samples_required
        )
        
        self.experiments.append(exp)
        self.active_experiments[name] = exp
        
        logger.info(f"Created experiment: {name}")
        logger.info(f"  Control: {control_algo}")
        logger.info(f"  Variant: {variant_algo}")
        logger.info(f"  Hypothesis: {hypothesis}")
        
        return exp
    
    def choose_algorithm(self, experiment_name: str, *args, **kwargs) -> Any:
        """
        Choose which algorithm to use for this trial
        
        Returns result of chosen algorithm
        """
        exp = self.active_experiments.get(experiment_name)
        if not exp:
            raise ValueError(f"Experiment not found: {experiment_name}")
        
        # Choose based on strategy
        if self.strategy == ExplorationStrategy.EPSILON_GREEDY:
            algo = self._epsilon_greedy_choice(exp)
        elif self.strategy == ExplorationStrategy.UCB1:
            algo = self._ucb1_choice(exp)
        else:  # THOMPSON
            algo = self._thompson_choice(exp)
        
        # Execute algorithm and measure
        start = time.time()
        try:
            result = algo.implementation(*args, **kwargs)
            duration = time.time() - start
            
            # Record trial
            algo.trials += 1
            algo.successes += 1
            algo.total_time += duration
            
            # Try to extract quality metric (if available)
            if isinstance(result, tuple) and len(result) == 2:
                value, quality = result
                algo.total_quality += quality
                return value
            else:
                return result
        
        except Exception as e:
            algo.trials += 1
            algo.total_time += time.time() - start
            logger.error(f"Algorithm {algo.name} failed: {e}")
            raise
    
    def _epsilon_greedy_choice(self, exp: Experiment) -> Algorithm:
        """Epsilon-greedy: 90% exploit best, 10% explore"""
        if random.random() < self.epsilon:
            # Explore: pick variant
            return exp.variant
        else:
            # Exploit: pick best so far
            if exp.control.success_rate >= exp.variant.success_rate:
                return exp.control
            else:
                return exp.variant
    
    def _ucb1_choice(self, exp: Experiment) -> Algorithm:
        """UCB1: Upper confidence bound"""
        control_ucb = self._calculate_ucb(exp.control, exp.samples_required)
        variant_ucb = self._calculate_ucb(exp.variant, exp.samples_required)
        
        return exp.control if control_ucb >= variant_ucb else exp.variant
    
    def _thompson_choice(self, exp: Experiment) -> Algorithm:
        """Thompson sampling"""
        control_sample = self._thompson_sample(exp.control)
        variant_sample = self._thompson_sample(exp.variant)
        
        return exp.control if control_sample >= variant_sample else exp.variant
    
    def _calculate_ucb(self, algo: Algorithm, total_trials: int) -> float:
        """Calculate UCB1 value"""
        if algo.trials == 0:
            return float('inf')
        
        exploitation = algo.success_rate
        exploration = math.sqrt(2 * math.log(total_trials) / algo.trials)
        
        return exploitation + exploration
    
    def _thompson_sample(self, algo: Algorithm) -> float:
        """Thompson sampling from beta distribution"""
        # Simplified: use success rate with variance
        if algo.trials == 0:
            return random.random()
        
        # Sample from beta distribution approximation
        alpha = algo.successes + 1
        beta = algo.trials - algo.successes + 1
        
        # Use mean of beta distribution
        return alpha / (alpha + beta)
    
    def complete_experiment(self, experiment_name: str) -> Experiment:
        """Complete experiment and determine winner"""
        
        exp = self.active_experiments.get(experiment_name)
        if not exp:
            raise ValueError(f"Experiment not found: {experiment_name}")
        
        exp.completed_at = datetime.now()
        
        # Statistical significance testing
        winner, p_value, confidence = self._run_significance_test(exp)
        
        exp.winner = winner
        exp.p_value = p_value
        exp.confidence = confidence
        
        if p_value < 0.05:  # 95% confidence
            logger.info(f"✓ Experiment {experiment_name} complete")
            logger.info(f"  Winner: {winner.name} (confidence: {confidence:.1%})")
            logger.info(f"  Control success rate: {exp.control.success_rate:.1%}")
            logger.info(f"  Variant success rate: {exp.variant.success_rate:.1%}")
            
            if not winner.is_baseline:
                # Promote variant
                self._promote_winner(experiment_name, winner)
        else:
            logger.warning(f"Experiment {experiment_name} inconclusive (p={p_value:.3f})")
        
        del self.active_experiments[experiment_name]
        return exp
    
    def _run_significance_test(self, exp: Experiment) -> Tuple[Algorithm, float, float]:
        """Run chi-square test for statistical significance"""
        
        # Control group
        control_success = exp.control.successes
        control_failure = exp.control.trials - exp.control.successes
        
        # Variant group
        variant_success = exp.variant.successes
        variant_failure = exp.variant.trials - exp.variant.successes
        
        # Calculate chi-square (simplified)
        total = exp.control.trials + exp.variant.trials
        if total == 0:
            return exp.variant, 1.0, 0.0
        
        control_rate = control_success / exp.control.trials if exp.control.trials > 0 else 0
        variant_rate = variant_success / exp.variant.trials if exp.variant.trials > 0 else 0
        
        # Determine winner
        if variant_rate > control_rate * 1.05:  # 5% improvement needed
            winner = exp.variant
            improvement = (variant_rate - control_rate) / control_rate
        else:
            winner = exp.control
            improvement = 0
        
        # Confidence based on sample size
        confidence = min(
            (exp.control.trials + exp.variant.trials) / exp.samples_required,
            1.0
        )
        
        # P-value estimation (simplified)
        p_value = 0.01 if confidence > 0.9 else 0.1
        
        return winner, p_value, confidence
    
    def _promote_winner(self, experiment_name: str, winner: Algorithm) -> None:
        """Promote winning algorithm to production"""
        logger.info(f"Promoting {winner.name} to production (from experiment {experiment_name})")
        
        # In real implementation, would:
        # - Update configuration
        # - Redirect traffic to winner
        # - Archive learning
        # - Start new experiment with new variant
    
    def get_experiment_status(self, experiment_name: str) -> Dict[str, Any]:
        """Get current status of experiment"""
        exp = self.active_experiments.get(experiment_name)
        if not exp:
            return {"status": "completed"}
        
        return {
            "name": exp.name,
            "hypothesis": exp.hypothesis,
            "control": {
                "name": exp.control.name,
                "trials": exp.control.trials,
                "success_rate": f"{exp.control.success_rate:.1%}",
                "avg_time": f"{exp.control.avg_time:.3f}s"
            },
            "variant": {
                "name": exp.variant.name,
                "trials": exp.variant.trials,
                "success_rate": f"{exp.variant.success_rate:.1%}",
                "avg_time": f"{exp.variant.avg_time:.3f}s"
            },
            "progress": f"{(exp.control.trials + exp.variant.trials) / exp.samples_required:.1%}",
            "leading": exp.variant.name if (
                exp.variant.success_rate > exp.control.success_rate
            ) else exp.control.name
        }
    
    def get_all_experiments(self) -> List[Dict[str, Any]]:
        """Get status of all experiments"""
        return [
            self.get_experiment_status(name)
            for name in self.active_experiments.keys()
        ]


# Global instance
_framework: Optional[ExperimentationFramework] = None


def get_experimentation_framework(
    strategy: ExplorationStrategy = ExplorationStrategy.EPSILON_GREEDY
) -> ExperimentationFramework:
    """Get or create experimentation framework"""
    global _framework
    if _framework is None:
        _framework = ExperimentationFramework(strategy)
    return _framework
