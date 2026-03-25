"""
Value Alignment Engine: Multi-objective optimization with safety constraints

Enables system to:
- Maintain alignment with defined values
- Balance competing objectives safely
- Prevent misalignment/reward hacking
- Provide transparency into decisions
"""
from typing import Dict, List, Any, Optional, Callable, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

import config
from logger import logger


class ValueType(Enum):
    """Core value types"""
    RELIABILITY = "reliability"  # Never harm -> always works
    SAFETY = "safety"  # Never cause harm
    EFFICIENCY = "efficiency"  # Minimize waste
    TRANSPARENCY = "transparency"  # Explain decisions
    FAIRNESS = "fairness"  # Treat all equally
    AUTONOMY = "autonomy"  # Respect independence
    PRIVACY = "privacy"  # Protect data


@dataclass
class ObjectiveFunction:
    """An objective the system can optimize"""
    name: str
    description: str
    
    # Bounds and constraints
    min_value: float = 0.0
    max_value: float = 1.0
    is_constraint: bool = False  # Hard limit vs soft objective
    
    # Weighting
    weight: float = 1.0  # Relative importance
    value_alignment: Dict[ValueType, float] = field(default_factory=dict)  # Alignment with values


@dataclass
class Decision:
    """A decision made by the system"""
    decision_id: str
    timestamp: datetime = field(default_factory=datetime.now)
    
    option_a: Dict[str, float]  # Metrics for option A
    option_b: Dict[str, float]  # Metrics for option B
    
    chosen: str  # "a" or "b"
    confidence: float = 0.5
    
    # Alignment metrics
    value_alignment_scores: Dict[ValueType, float] = field(default_factory=dict)
    safety_check_passed: bool = True
    constraint_violations: List[str] = field(default_factory=list)


class ValueAlignmentEngine:
    """
    Multi-objective optimization with safety and ethics
    
    Features:
    - Define system values and objectives
    - Optimize decisions against multiple objectives
    - Enforce safety constraints
    - Prevent value drift
    - Provide decision transparency
    """
    
    def __init__(self):
        self.values: Dict[ValueType, float] = {
            ValueType.RELIABILITY: 1.0,
            ValueType.SAFETY: 1.0,
            ValueType.EFFICIENCY: 0.8,
            ValueType.TRANSPARENCY: 0.9,
            ValueType.FAIRNESS: 0.8,
            ValueType.AUTONOMY: 0.7,
            ValueType.PRIVACY: 0.95
        }
        
        self.objectives: Dict[str, ObjectiveFunction] = {}
        self.constraints: Dict[str, ObjectiveFunction] = {}
        self.decisions: List[Decision] = []
        
        # Safety parameters
        self.safety_threshold = 0.8  # Min safety score to proceed
        self.transparency_required = 0.7  # Min transparency
        
        self._initialize_core_values()
        
        logger.info("✓ Value Alignment Engine initialized")
    
    def _initialize_core_values(self) -> None:
        """Initialize core safety constraints"""
        
        # Define critical constraints
        constraints = [
            ObjectiveFunction(
                name="no_harm",
                description="Never cause harm to humans or data",
                is_constraint=True,
                value_alignment={ValueType.SAFETY: 1.0, ValueType.RELIABILITY: 0.9}
            ),
            ObjectiveFunction(
                name="always_available",
                description="System remains available and responsive",
                is_constraint=True,
                value_alignment={ValueType.RELIABILITY: 1.0, ValueType.SAFETY: 0.7}
            ),
            ObjectiveFunction(
                name="reversible_changes",
                description="Changes can be rolled back",
                is_constraint=True,
                value_alignment={ValueType.SAFETY: 0.9, ValueType.AUTONOMY: 0.6}
            ),
            ObjectiveFunction(
                name="explainable_decisions",
                description="Decisions can be explained",
                is_constraint=False,  # Soft requirement
                weight=0.8,
                value_alignment={ValueType.TRANSPARENCY: 1.0, ValueType.FAIRNESS: 0.8}
            ),
        ]
        
        for constraint in constraints:
            self.constraints[constraint.name] = constraint
    
    def register_objective(
        self,
        name: str,
        description: str,
        min_val: float = 0.0,
        max_val: float = 1.0,
        weight: float = 1.0,
        value_alignment: Optional[Dict[ValueType, float]] = None
    ) -> None:
        """Register an optimization objective"""
        
        obj = ObjectiveFunction(
            name=name,
            description=description,
            min_value=min_val,
            max_value=max_val,
            weight=weight,
            value_alignment=value_alignment or {}
        )
        
        self.objectives[name] = obj
        logger.info(f"Registered objective: {name}")
    
    def evaluate_decision(
        self,
        option_a: Dict[str, float],
        option_b: Dict[str, float],
        context: Optional[str] = None
    ) -> Decision:
        """
        Evaluate two options for alignment with values
        
        Returns decision and reasoning
        """
        
        decision_id = f"decision_{len(self.decisions)}"
        
        decision = Decision(
            decision_id=decision_id,
            option_a=option_a,
            option_b=option_b,
            chosen="a"
        )
        
        # Check constraints
        constraint_violations_a = self._check_constraints(option_a)
        constraint_violations_b = self._check_constraints(option_b)
        
        if constraint_violations_a and not constraint_violations_b:
            # Option B is safe, A violates constraints
            decision.chosen = "b"
            decision.safety_check_passed = True
            decision.constraint_violations = constraint_violations_a
            
            logger.info(f"Decision {decision_id}: Chose B (A violates constraints)")
            logger.info(f"  Violations in A: {', '.join(constraint_violations_a)}")
        
        elif constraint_violations_b and not constraint_violations_a:
            # Option A is safe, B violates constraints
            decision.chosen = "a"
            decision.safety_check_passed = True
            decision.constraint_violations = constraint_violations_b
            
            logger.info(f"Decision {decision_id}: Chose A (B violates constraints)")
        
        elif constraint_violations_a and constraint_violations_b:
            # Both violate - choose the one with fewer violations
            logger.warning(f"Decision {decision_id}: Both options violate constraints!")
            
            if len(constraint_violations_a) <= len(constraint_violations_b):
                decision.chosen = "a"
            else:
                decision.chosen = "b"
            
            decision.safety_check_passed = False
            decision.constraint_violations = min(
                constraint_violations_a,
                constraint_violations_b,
                key=len
            )
        
        else:
            # Both safe - optimize for objectives
            score_a = self._calculate_alignment_score(option_a)
            score_b = self._calculate_alignment_score(option_b)
            
            decision.chosen = "a" if score_a >= score_b else "b"
            decision.confidence = max(score_a, score_b)
            decision.value_alignment_scores = {
                "option_a": score_a,
                "option_b": score_b
            }
            
            logger.info(f"Decision {decision_id}: Both options safe")
            logger.info(f"  Option A value score: {score_a:.3f}")
            logger.info(f"  Option B value score: {score_b:.3f}")
            logger.info(f"  Chose: {'A' if decision.chosen == 'a' else 'B'}")
        
        self.decisions.append(decision)
        return decision
    
    def _check_constraints(self, metrics: Dict[str, float]) -> List[str]:
        """Check if metrics violate safety constraints"""
        violations = []
        
        for name, constraint in self.constraints.items():
            # Get metric value
            value = metrics.get(name, 0.5)
            
            # Check if value meets minimum threshold
            if value < constraint.min_value:
                violations.append(f"{name} (value={value:.2f}, min={constraint.min_value})")
        
        return violations
    
    def _calculate_alignment_score(self, metrics: Dict[str, float]) -> float:
        """
        Calculate how well metrics align with system values
        
        Returns 0-1 score
        """
        
        if not metrics:
            return 0.5
        
        total_score = 0.0
        total_weight = 0.0
        
        for obj_name, objective in self.objectives.items():
            if obj_name not in metrics:
                continue
            
            metric_value = metrics[obj_name]
            
            # Normalize to 0-1
            if objective.max_value > objective.min_value:
                normalized = (
                    (metric_value - objective.min_value) /
                    (objective.max_value - objective.min_value)
                )
            else:
                normalized = 0.5
            
            normalized = max(0.0, min(1.0, normalized))
            
            # Weight by objective importance and value alignment
            weight = objective.weight
            
            # Apply value alignment bonus
            if objective.value_alignment:
                value_score = sum(objective.value_alignment.values()) / len(objective.value_alignment)
                weight *= value_score
            
            total_score += normalized * weight
            total_weight += weight
        
        return total_score / max(total_weight, 1.0)
    
    def detect_value_drift(self) -> Dict[str, Any]:
        """Detect if system decisions are drifting from values"""
        
        if len(self.decisions) < 10:
            return {"status": "insufficient_data"}
        
        recent_decisions = self.decisions[-50:]
        
        # Analyze recent decisions
        value_alignment_trend = []
        safety_violations = 0
        
        for decision in recent_decisions:
            if decision.safety_check_passed:
                if "option_a" in decision.value_alignment_scores:
                    score = decision.value_alignment_scores.get(
                        "option_a" if decision.chosen == "a" else "option_b",
                        0.5
                    )
                    value_alignment_trend.append(score)
            else:
                safety_violations += 1
        
        # Calculate trend
        if len(value_alignment_trend) > 0:
            avg_alignment = sum(value_alignment_trend) / len(value_alignment_trend)
            min_alignment = min(value_alignment_trend)
        else:
            avg_alignment = 0.5
            min_alignment = 0.5
        
        drift_detected = False
        issues = []
        
        if avg_alignment < 0.6:
            drift_detected = True
            issues.append("Value alignment below threshold")
        
        if min_alignment < 0.3:
            drift_detected = True
            issues.append("Some decisions have poor value alignment")
        
        if safety_violations > len(recent_decisions) * 0.1:
            drift_detected = True
            issues.append(f"Safety violations detected ({safety_violations}/{len(recent_decisions)})")
        
        logger.info("Value Drift Analysis:")
        logger.info(f"  Decisions analyzed: {len(recent_decisions)}")
        logger.info(f"  Avg value alignment: {avg_alignment:.2f}")
        logger.info(f"  Min value alignment: {min_alignment:.2f}")
        logger.info(f"  Safety violations: {safety_violations}")
        
        if drift_detected:
            logger.warning("⚠ VALUE DRIFT DETECTED")
            for issue in issues:
                logger.warning(f"  - {issue}")
        else:
            logger.info("✓ Value alignment stable")
        
        return {
            "drift_detected": drift_detected,
            "avg_alignment": avg_alignment,
            "min_alignment": min_alignment,
            "safety_violations": safety_violations,
            "issues": issues
        }
    
    def get_alignment_report(self) -> Dict[str, Any]:
        """Get comprehensive alignment report"""
        
        return {
            "values": {
                vtype.value: score
                for vtype, score in self.values.items()
            },
            "objectives": {
                name: {
                    "description": obj.description,
                    "weight": obj.weight
                }
                for name, obj in self.objectives.items()
            },
            "constraints": list(self.constraints.keys()),
            "total_decisions": len(self.decisions),
            "safety_passing_rate": f"{sum(1 for d in self.decisions if d.safety_check_passed)/max(len(self.decisions),1):.1%}",
            "drift_analysis": self.detect_value_drift()
        }


# Global instance
_engine: Optional[ValueAlignmentEngine] = None


def get_value_alignment_engine() -> ValueAlignmentEngine:
    """Get or create value alignment engine"""
    global _engine
    if _engine is None:
        _engine = ValueAlignmentEngine()
    return _engine
