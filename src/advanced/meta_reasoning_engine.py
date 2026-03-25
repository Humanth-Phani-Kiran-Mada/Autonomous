"""
Meta-Reasoning Engine: Self-directed optimization of reasoning processes

Enables system to:
- Analyze its own reasoning patterns
- Identify inefficient thinking
- Optimize decision-making strategies
- Learn better inference strategies
"""
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import time

import config
from logger import logger


class ReasoningStyle(Enum):
    """Reasoning styles to switch between"""
    DEPTH_FIRST = "depth_first"  # Deep analysis
    BREADTH_FIRST = "breadth_first"  # Explore many options
    HEURISTIC = "heuristic"  # Use patterns/rules
    ANALYTICAL = "analytical"  # Data-driven
    SYNTHESIS = "synthesis"  # Combine approaches


@dataclass
class ReasoningTrace:
    """Record of a reasoning process"""
    trace_id: str
    task: str
    style: ReasoningStyle
    
    # Execution
    start_time: datetime = field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    duration: float = 0.0
    
    # Quality metrics
    steps: int = 0  # Number of reasoning steps
    branches_explored: int = 0
    dead_ends: int = 0
    optimal: bool = False  # Did it find optimal solution?
    confidence: float = 0.5  # Confidence in answer
    
    # Outcome
    result: Optional[str] = None
    success: bool = False
    quality_score: float = 0.5
    
    # Analysis
    efficiency: float = 0.0  # Quality / duration
    effectiveness: float = 0.0  # Quality / steps


@dataclass
class ReasoningStrategy:
    """A strategy for approaching reasoning tasks"""
    name: str
    style: ReasoningStyle
    
    # Parameters
    max_depth: int = 5  # Max analysis depth
    max_breadth: int = 10  # Max options to explore
    timeout: float = 5.0  # Max time budget
    heuristic_threshold: float = 0.8  # Use heuristics if confidence high
    
    # Performance
    total_uses: int = 0
    successful_uses: int = 0
    total_time: float = 0.0
    total_efficiency: float = 0.0
    
    @property
    def success_rate(self) -> float:
        return self.successful_uses / max(self.total_uses, 1)
    
    @property
    def avg_efficiency(self) -> float:
        return self.total_efficiency / max(self.total_uses, 1)


class MetaReasoningEngine:
    """
    Self-optimizing reasoning processor
    
    Features:
    - Track reasoning processes
    - Measure reasoning efficiency
    - Adapt reasoning strategies
    - Learn optimal approaches
    """
    
    def __init__(self):
        self.strategies: Dict[str, ReasoningStrategy] = {}
        self.traces: List[ReasoningTrace] = []
        self.current_trace: Optional[ReasoningTrace] = None
        
        # Initialize standard strategies
        self._initialize_strategies()
        
        logger.info("✓ Meta-Reasoning Engine initialized")
    
    def _initialize_strategies(self) -> None:
        """Initialize standard reasoning strategies"""
        
        strategies = [
            ReasoningStrategy(
                name="careful",
                style=ReasoningStyle.ANALYTICAL,
                max_depth=10,
                max_breadth=5,
                timeout=10.0
            ),
            ReasoningStrategy(
                name="fast",
                style=ReasoningStyle.HEURISTIC,
                max_depth=3,
                max_breadth=3,
                timeout=1.0
            ),
            ReasoningStrategy(
                name="thorough",
                style=ReasoningStyle.DEPTH_FIRST,
                max_depth=15,
                max_breadth=10,
                timeout=30.0
            ),
            ReasoningStrategy(
                name="broad",
                style=ReasoningStyle.BREADTH_FIRST,
                max_depth=3,
                max_breadth=20,
                timeout=5.0
            ),
        ]
        
        for strategy in strategies:
            self.strategies[strategy.name] = strategy
    
    def begin_reasoning(
        self,
        task: str,
        strategy_name: str = "careful"
    ) -> str:
        """Begin a reasoning process with specified strategy"""
        
        strategy = self.strategies.get(strategy_name)
        if not strategy:
            logger.warning(f"Strategy not found: {strategy_name}, using 'fast'")
            strategy = self.strategies["fast"]
        
        trace_id = f"trace_{int(time.time()*1000000) % 1000000}"
        
        self.current_trace = ReasoningTrace(
            trace_id=trace_id,
            task=task,
            style=strategy.style
        )
        
        logger.debug(f"Beginning reasoning: {task} ({strategy.name})")
        
        return trace_id
    
    def record_reasoning_step(
        self,
        step_description: str,
        branch_count: int = 1,
        dead_end: bool = False
    ) -> None:
        """Record a step in reasoning process"""
        
        if not self.current_trace:
            return
        
        self.current_trace.steps += 1
        self.current_trace.branches_explored += branch_count
        if dead_end:
            self.current_trace.dead_ends += 1
        
        logger.debug(f"Reasoning step {self.current_trace.steps}: {step_description}")
    
    def conclude_reasoning(
        self,
        result: str,
        success: bool = True,
        quality_score: float = 0.5,
        is_optimal: bool = False,
        confidence: float = 0.5
    ) -> ReasoningTrace:
        """Conclude reasoning process and return trace"""
        
        if not self.current_trace:
            raise RuntimeError("No active reasoning trace")
        
        self.current_trace.end_time = datetime.now()
        self.current_trace.duration = (
            self.current_trace.end_time - self.current_trace.start_time
        ).total_seconds()
        
        self.current_trace.result = result
        self.current_trace.success = success
        self.current_trace.quality_score = quality_score
        self.current_trace.optimal = is_optimal
        self.current_trace.confidence = confidence
        
        # Calculate efficiency
        if self.current_trace.duration > 0:
            self.current_trace.efficiency = quality_score / self.current_trace.duration
        
        if self.current_trace.steps > 0:
            self.current_trace.effectiveness = quality_score / self.current_trace.steps
        
        # Update strategy metrics
        strategy = self.strategies[self.current_trace.style.value] if self.current_trace.style else None
        # Actually get the strategy that was used
        for strat in self.strategies.values():
            if strat.style == self.current_trace.style:
                strat.total_uses += 1
                if success:
                    strat.successful_uses += 1
                strat.total_time += self.current_trace.duration
                strat.total_efficiency += self.current_trace.efficiency
                break
        
        # Store trace
        self.traces.append(self.current_trace)
        trace = self.current_trace
        self.current_trace = None
        
        logger.debug(f"✓ Concluded reasoning: {result} ({quality_score:.2f} quality)")
        logger.debug(f"  Steps: {trace.steps}, Duration: {trace.duration:.3f}s, " +
                    f"Efficiency: {trace.efficiency:.2f}")
        
        return trace
    
    def get_best_strategy(self) -> ReasoningStrategy:
        """Get best-performing strategy based on recent traces"""
        
        # Calculate performance score for each strategy
        strategy_scores = {}
        
        for name, strategy in self.strategies.items():
            if strategy.total_uses == 0:
                strategy_scores[name] = 0
            else:
                # Score = success_rate * efficiency
                score = (
                    strategy.success_rate * 0.6 +
                    min(strategy.avg_efficiency, 1.0) * 0.4
                )
                strategy_scores[name] = score
        
        best_name = max(strategy_scores, key=strategy_scores.get)
        return self.strategies[best_name]
    
    def recommend_strategy(self, task_complexity: float) -> str:
        """
        Recommend strategy based on task complexity
        
        complexity: 0-1 scale
        """
        
        if task_complexity < 0.3:
            return "fast"
        elif task_complexity < 0.6:
            return "careful"
        else:
            return "thorough"
    
    def optimize_reasoning(self) -> Dict[str, Any]:
        """Analyze reasoning patterns and suggest optimizations"""
        
        if len(self.traces) < 10:
            return {"status": "insufficient_data"}
        
        # Analyze recent traces
        recent = self.traces[-50:]  # Last 50
        
        # Find patterns
        efficient_traces = [t for t in recent if t.efficiency > 0.5]
        inefficient_traces = [t for t in recent if t.efficiency < 0.2]
        
        avg_steps = sum(t.steps for t in recent) / len(recent)
        avg_duration = sum(t.duration for t in recent) / len(recent)
        success_rate = sum(1 for t in recent if t.success) / len(recent)
        
        optimizations = []
        
        # Suggest optimizations
        if avg_steps > 20:
            optimizations.append({
                "issue": "excessive_reasoning_steps",
                "suggestion": "Use heuristics to reduce steps",
                "potential_improvement": "30% faster"
            })
        
        if avg_duration > 5.0:
            optimizations.append({
                "issue": "slow_reasoning",
                "suggestion": "Switch to faster strategies or reduce depth",
                "potential_improvement": "50% faster"
            })
        
        if success_rate < 0.7:
            optimizations.append({
                "issue": "low_success_rate",
                "suggestion": "Increase thoroughness or use different approach",
                "potential_improvement": "15% higher success"
            })
        
        logger.info("Meta-Reasoning Optimization Analysis:")
        logger.info(f"  Traces analyzed: {len(recent)}")
        logger.info(f"  Avg steps/trace: {avg_steps:.1f}")
        logger.info(f"  Avg duration: {avg_duration:.3f}s")
        logger.info(f"  Success rate: {success_rate:.1%}")
        
        if optimizations:
            logger.info("\n  Suggested optimizations:")
            for opt in optimizations:
                logger.info(f"    - {opt['issue']}: {opt['suggestion']}")
                logger.info(f"      Potential: {opt['potential_improvement']}")
        
        return {
            "status": "analysis_complete",
            "traces_analyzed": len(recent),
            "avg_steps": avg_steps,
            "avg_duration": avg_duration,
            "success_rate": success_rate,
            "optimizations": optimizations,
            "best_strategy": self.get_best_strategy().name
        }
    
    def get_reasoning_stats(self) -> Dict[str, Any]:
        """Get comprehensive reasoning statistics"""
        
        if not self.traces:
            return {"status": "no_traces"}
        
        total_traces = len(self.traces)
        successful = sum(1 for t in self.traces if t.success)
        
        strategy_stats = {}
        for name, strategy in self.strategies.items():
            if strategy.total_uses > 0:
                strategy_stats[name] = {
                    "uses": strategy.total_uses,
                    "success_rate": f"{strategy.success_rate:.1%}",
                    "avg_efficiency": f"{strategy.avg_efficiency:.3f}",
                    "avg_time": f"{strategy.total_time/strategy.total_uses:.3f}s"
                }
        
        return {
            "total_reasoning_traces": total_traces,
            "successful": successful,
            "success_rate": f"{successful/total_traces:.1%}",
            "avg_trace_duration": f"{sum(t.duration for t in self.traces)/total_traces:.3f}s",
            "avg_trace_steps": f"{sum(t.steps for t in self.traces)/total_traces:.1f}",
            "total_reasoning_time": f"{sum(t.duration for t in self.traces):.1f}s",
            "strategy_performance": strategy_stats
        }


# Global instance
_engine: Optional[MetaReasoningEngine] = None


def get_meta_reasoning_engine() -> MetaReasoningEngine:
    """Get or create meta-reasoning engine"""
    global _engine
    if _engine is None:
        _engine = MetaReasoningEngine()
    return _engine
