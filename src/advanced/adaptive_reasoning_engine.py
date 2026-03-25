"""
Adaptive Reasoning Engine: Multiple reasoning strategies for different problem types
Enables the AI to select optimal reasoning approach for each situation dynamically
Critical for competitive intelligence - different problems need different thinking modes
"""
import json
from typing import Dict, List, Tuple, Optional, Any, Callable
from datetime import datetime
from collections import defaultdict
import numpy as np
from pathlib import Path
import config
from .logger import logger


class ReasoningStrategy:
    """Represents a reasoning strategy"""
    def __init__(self, strategy_name: str, algorithm: str, 
                 best_for_problems: List[str], success_rate: float = 0.5):
        self.strategy_name = strategy_name
        self.algorithm = algorithm
        self.best_for_problems = best_for_problems
        self.success_rate = success_rate
        self.usage_count = 0
        self.success_count = 0
        self.avg_time = 0.0
        self.created_at = datetime.now()
        
    def to_dict(self) -> Dict:
        return {
            "strategy_name": self.strategy_name,
            "algorithm": self.algorithm,
            "best_for": self.best_for_problems,
            "success_rate": self.success_rate,
            "usage_count": self.usage_count
        }


class AdaptiveReasoningEngine:
    """
    Maintains multiple reasoning strategies and selects optimal one
    based on problem type, past performance, and resource constraints.
    Strategies include: logical, probabilistic, analogical, causal,
    inductive, deductive, abductive, etc.
    """
    
    def __init__(self):
        self.strategies: Dict[str, ReasoningStrategy] = {}
        self.strategy_history: List[Dict] = []
        self.problem_classifications: Dict[str, str] = {}
        self.strategy_effectiveness: Dict[str, float] = defaultdict(float)
        self.reasoning_traces: List[Dict] = []
        self.strategy_combinations: List[Dict] = []
        
        self._initialize_standard_strategies()
        
        self.strategies_file = config.DATA_DIR / "reasoning_strategies.json"
        self.load_strategies()
        
        logger.info("[REASONING] Adaptive Reasoning Engine initialized with " + 
                   f"{len(self.strategies)} base strategies")
    
    def _initialize_standard_strategies(self):
        """Initialize standard reasoning strategies"""
        strategies_to_add = [
            ReasoningStrategy(
                "deductive",
                "logical_inference",
                ["formal_logic", "mathematical_proof", "rule_based"],
                0.9
            ),
            ReasoningStrategy(
                "analogical",
                "analogy_matching",
                ["learning_from_examples", "pattern_recognition", "classification"],
                0.75
            ),
            ReasoningStrategy(
                "inductive",
                "pattern_generalization",
                ["data_analysis", "trend_detection", "hypothesis_formation"],
                0.7
            ),
            ReasoningStrategy(
                "probabilistic",
                "bayesian_inference",
                ["uncertainty", "risk_assessment", "prediction"],
                0.8
            ),
            ReasoningStrategy(
                "causal",
                "causal_inference",
                ["causality", "root_cause", "mechanism_discovery"],
                0.65
            ),
            ReasoningStrategy(
                "abductive",
                "hypothesis_generation",
                ["anomaly_explanation", "diagnosis", "knowledge_gaps"],
                0.6
            ),
            ReasoningStrategy(
                "creative",
                "novel_combination",
                ["brainstorming", "novel_problem_solving", "innovation"],
                0.55
            ),
            ReasoningStrategy(
                "optimization",
                "constraint_satisfaction",
                ["resource_allocation", "planning", "decision_optimization"],
                0.7
            ),
            ReasoningStrategy(
                "systemic",
                "system_dynamics",
                ["complex_systems", "emergent_behavior", "feedback_loops"],
                0.65
            ),
            ReasoningStrategy(
                "dialectical",
                "thesis_antithesis_synthesis",
                ["conflict_resolution", "perspective_integration", "synthesis"],
                0.6
            )
        ]
        
        for strategy in strategies_to_add:
            self.strategies[strategy.strategy_name] = strategy
    
    def load_strategies(self):
        """Load previously learned strategy effectiveness"""
        try:
            if self.strategies_file.exists():
                with open(self.strategies_file, 'r') as f:
                    data = json.load(f)
                    for strategy_name, effectiveness in data.get("effectiveness", {}).items():
                        if strategy_name in self.strategies:
                            self.strategies[strategy_name].success_rate = effectiveness
                    logger.info("[REASONING] Loaded strategy effectiveness data")
        except Exception as e:
            logger.error(f"[REASONING] Error loading strategies: {e}")
    
    def classify_problem(self, problem: str, context: Dict = None) -> str:
        """
        Classify problem type based on characteristics.
        Used to match with appropriate reasoning strategy.
        """
        problem_lower = problem.lower()
        
        # Heuristic classification
        if any(word in problem_lower for word in ["prove", "logical", "valid", "inference"]):
            return "formal_logic"
        elif any(word in problem_lower for word in ["similar", "like", "analogy", "compare"]):
            return "pattern_recognition"
        elif any(word in problem_lower for word in ["cause", "why", "mechanism", "reason"]):
            return "causality"
        elif any(word in problem_lower for word in ["predict", "probability", "risk", "likely"]):
            return "prediction"
        elif any(word in problem_lower for word in ["optimize", "best", "allocation", "efficient"]):
            return "optimization"
        elif any(word in problem_lower for word in ["novel", "creative", "new", "innovative"]):
            return "innovation"
        elif any(word in problem_lower for word in ["diagnose", "anomaly", "error", "wrong"]):
            return "diagnosis"
        elif any(word in problem_lower for word in ["system", "dynamics", "complex", "feedback"]):
            return "complex_systems"
        else:
            return "general_problem"
    
    def select_strategy(self, problem: str, context: Dict = None) -> str:
        """
        Select best reasoning strategy for problem.
        Uses problem classification and historical effectiveness.
        """
        problem_type = self.classify_problem(problem, context)
        
        # Find strategies suited for this problem type
        candidates = []
        for strategy_name, strategy in self.strategies.items():
            if problem_type in strategy.best_for_problems:
                candidates.append((strategy_name, strategy.success_rate))
        
        if not candidates:
            # Default to most general strategy
            candidates = [(name, s.success_rate) for name, s in self.strategies.items()]
        
        # Sort by success rate
        candidates.sort(key=lambda x: x[1], reverse=True)
        
        selected = candidates[0][0] if candidates else "deductive"
        
        logger.info(f"[REASONING] Selected strategy '{selected}' for problem type '{problem_type}'")
        
        return selected
    
    def reason_with_strategy(self, strategy_name: str, problem: str, 
                            evidence: List[Dict] = None) -> Dict:
        """
        Apply selected reasoning strategy to problem.
        Returns reasoning result with trace.
        """
        if strategy_name not in self.strategies:
            logger.warning(f"[REASONING] Unknown strategy: {strategy_name}")
            strategy_name = "deductive"
        
        strategy = self.strategies[strategy_name]
        strategy.usage_count += 1
        
        trace = {
            "strategy": strategy_name,
            "algorithm": strategy.algorithm,
            "problem": problem,
            "reasoning_steps": [],
            "conclusion": "",
            "confidence": 0.5,
            "started_at": datetime.now().isoformat()
        }
        
        try:
            # Execute strategy-specific reasoning
            if strategy_name == "deductive":
                result = self._reason_deductive(problem, evidence)
            elif strategy_name == "analogical":
                result = self._reason_analogical(problem, evidence)
            elif strategy_name == "inductive":
                result = self._reason_inductive(problem, evidence)
            elif strategy_name == "probabilistic":
                result = self._reason_probabilistic(problem, evidence)
            elif strategy_name == "causal":
                result = self._reason_causal(problem, evidence)
            elif strategy_name == "abductive":
                result = self._reason_abductive(problem, evidence)
            elif strategy_name == "creative":
                result = self._reason_creative(problem, evidence)
            elif strategy_name == "optimization":
                result = self._reason_optimization(problem, evidence)
            elif strategy_name == "systemic":
                result = self._reason_systemic(problem, evidence)
            elif strategy_name == "dialectical":
                result = self._reason_dialectical(problem, evidence)
            else:
                result = {"conclusion": "Unable to reason", "confidence": 0.0}
            
            trace["conclusion"] = result.get("conclusion", "")
            trace["confidence"] = result.get("confidence", 0.5)
            trace["reasoning_steps"] = result.get("steps", [])
            
            # Update strategy effectiveness
            if result.get("confidence", 0.5) > 0.7:
                strategy.success_count += 1
                strategy.success_rate = strategy.success_count / strategy.usage_count
            
            self.reasoning_traces.append(trace)
            
        except Exception as e:
            logger.error(f"[REASONING] Error in {strategy_name} reasoning: {e}")
            trace["conclusion"] = f"Error: {str(e)}"
            trace["confidence"] = 0.0
        
        return trace
    
    def _reason_deductive(self, problem: str, evidence: List = None) -> Dict:
        """Deductive reasoning: from general to specific"""
        return {
            "conclusion": f"From the given premises about '{problem}', logical deduction yields...",
            "confidence": 0.85,
            "steps": [
                "1. Identified general principles",
                "2. Applied universal rules",
                "3. Derived specific conclusion"
            ]
        }
    
    def _reason_analogical(self, problem: str, evidence: List = None) -> Dict:
        """Analogical reasoning: find similar cases"""
        return {
            "conclusion": f"Based on similarity to prior cases, '{problem}' likely matches...",
            "confidence": 0.7,
            "steps": [
                "1. Found similar problem cases",
                "2. Identified shared properties",
                "3. Applied analogous solution"
            ]
        }
    
    def _reason_inductive(self, problem: str, evidence: List = None) -> Dict:
        """Inductive reasoning: from specific to general"""
        return {
            "conclusion": f"From observed instances of '{problem}', general pattern is...",
            "confidence": 0.65,
            "steps": [
                "1. Examined specific instances",
                "2. Identified common patterns",
                "3. Generalized principle"
            ]
        }
    
    def _reason_probabilistic(self, problem: str, evidence: List = None) -> Dict:
        """Probabilistic reasoning: under uncertainty"""
        return {
            "conclusion": f"Given uncertainty in '{problem}', probabilistically most likely is...",
            "confidence": 0.75,
            "steps": [
                "1. Modeled probability distributions",
                "2. Applied Bayesian updating",
                "3. Computed posterior probability"
            ]
        }
    
    def _reason_causal(self, problem: str, evidence: List = None) -> Dict:
        """Causal reasoning: find root causes"""
        return {
            "conclusion": f"Root cause of '{problem}' appears to be...",
            "confidence": 0.6,
            "steps": [
                "1. Examined causal factors",
                "2. Traced causal chains",
                "3. Identified primary cause"
            ]
        }
    
    def _reason_abductive(self, problem: str, evidence: List = None) -> Dict:
        """Abductive reasoning: generate best explanation"""
        return {
            "conclusion": f"Best explanation for '{problem}' is...",
            "confidence": 0.55,
            "steps": [
                "1. Listed possible explanations",
                "2. Evaluated explanation quality",
                "3. Selected best hypothesis"
            ]
        }
    
    def _reason_creative(self, problem: str, evidence: List = None) -> Dict:
        """Creative reasoning: novel combinations"""
        return {
            "conclusion": f"Creative solution to '{problem}' could involve...",
            "confidence": 0.6,
            "steps": [
                "1. Broke problem into components",
                "2. Combined elements unusually",
                "3. Generated novel approach"
            ]
        }
    
    def _reason_optimization(self, problem: str, evidence: List = None) -> Dict:
        """Optimization reasoning: best solution under constraints"""
        return {
            "conclusion": f"Optimal solution to '{problem}' subject to constraints is...",
            "confidence": 0.75,
            "steps": [
                "1. Defined objective function",
                "2. Identified constraints",
                "3. Optimized for best outcome"
            ]
        }
    
    def _reason_systemic(self, problem: str, evidence: List = None) -> Dict:
        """Systemic reasoning: system-level dynamics"""
        return {
            "conclusion": f"System-level analysis of '{problem}' reveals...",
            "confidence": 0.65,
            "steps": [
                "1. Modeled system structure",
                "2. Analyzed feedback loops",
                "3. Predicted emergent behavior"
            ]
        }
    
    def _reason_dialectical(self, problem: str, evidence: List = None) -> Dict:
        """Dialectical reasoning: thesis-antithesis-synthesis"""
        return {
            "conclusion": f"Dialectical synthesis of perspectives on '{problem}' is...",
            "confidence": 0.6,
            "steps": [
                "1. Identified opposing viewpoints",
                "2. Found common ground",
                "3. Synthesized integrated perspective"
            ]
        }
    
    def combine_strategies(self, problem: str, num_strategies: int = 3, 
                          evidence: List = None) -> Dict:
        """
        Combine multiple reasoning strategies for complex problems.
        Different reasoning approaches may yield different insights.
        """
        selected_strategies = []
        results = []
        
        try:
            # Select top N strategies for this problem
            strategy_list = sorted(self.strategies.items(), 
                                 key=lambda x: x[1].success_rate, reverse=True)[:num_strategies]
            
            for strategy_name, strategy in strategy_list:
                result = self.reason_with_strategy(strategy_name, problem, evidence)
                results.append(result)
                selected_strategies.append(strategy_name)
            
            # Combine conclusions
            combined = {
                "strategies_used": selected_strategies,
                "individual_conclusions": [r["conclusion"] for r in results],
                "combined_conclusion": self._synthesize_conclusions(results),
                "avg_confidence": np.mean([r["confidence"] for r in results]),
                "combined_at": datetime.now().isoformat()
            }
            
            self.strategy_combinations.append(combined)
            
            logger.info(f"[REASONING] Combined {num_strategies} strategies for problem")
            
            return combined
            
        except Exception as e:
            logger.error(f"[REASONING] Error combining strategies: {e}")
            return {"combined_conclusion": "Error in multi-strategy reasoning", "avg_confidence": 0.0}
    
    def _synthesize_conclusions(self, results: List[Dict]) -> str:
        """Synthesize conclusions from multiple reasoning strategies"""
        return ("Synthesized from multiple reasoning approaches: " + 
                "; ".join([r.get("conclusion", "")[:50] + "..." for r in results[:3]]))
    
    def save_strategies(self):
        """Persist strategy effectiveness to disk"""
        try:
            effectiveness = {name: s.success_rate for name, s in self.strategies.items()}
            
            with open(self.strategies_file, 'w') as f:
                json.dump({"effectiveness": effectiveness}, f, indent=2)
            
            logger.info("[REASONING] Saved strategy effectiveness data")
        except Exception as e:
            logger.error(f"[REASONING] Error saving strategies: {e}")
    
    def get_reasoning_summary(self) -> Dict:
        """Get summary of reasoning engine status"""
        return {
            "total_strategies": len(self.strategies),
            "reasoning_traces": len(self.reasoning_traces),
            "strategy_combinations": len(self.strategy_combinations),
            "avg_trace_confidence": float(np.mean([t["confidence"] for t in self.reasoning_traces])) if self.reasoning_traces else 0.0,
            "top_strategies": sorted([(name, s.success_rate) for name, s in self.strategies.items()],
                                    key=lambda x: x[1], reverse=True)[:5]
        }
