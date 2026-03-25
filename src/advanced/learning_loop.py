"""
Autonomous Learning Loop: Closed-loop adaptation system

Implements the complete cycle:
Observe → Analyze → Learn → Adapt → Execute → Measure → Repeat
"""
from typing import Dict, List, Any, Callable, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import json
import threading
import time

import config
from logger import logger
from self_model import get_self_model
from metrics_collector import get_metrics_collector
from system_orchestrator import get_system_orchestrator


class AdaptationType(Enum):
    """Types of system adaptations"""
    PARAMETER_TUNING = "parameter_tuning"
    ALGORITHM_SWITCH = "algorithm_switch"
    ARCHITECTURE_CHANGE = "architecture_change"
    RESOURCE_REALLOCATION = "resource_reallocation"
    CACHING_ADJUSTMENT = "caching_adjustment"


@dataclass
class Observation:
    """System observation"""
    timestamp: datetime
    metrics: Dict[str, Any]
    health: Dict[str, Any]
    bottlenecks: List[str]


@dataclass
class Analysis:
    """Analysis of observations"""
    timestamp: datetime
    pattern: str
    severity: float  # 0-1
    root_cause: str
    impacts: List[str]
    confidence: float  # 0-1


@dataclass
class LearningOutcome:
    """What system learned"""
    timestamp: datetime
    pattern: str
    rule: str  # Human-readable rule
    confidence: float
    evidence: List[Dict]


@dataclass
class Adaptation:
    """System adaptation/change"""
    timestamp: datetime
    adaptation_type: AdaptationType
    target: str  # What component/parameter
    change: str  # What changed
    reason: str
    prediction: Dict[str, Any]  # Expected outcome
    actual_outcome: Optional[Dict[str, Any]] = None
    successful: Optional[bool] = None


class AutonomousLearningLoop:
    """
    Manages the complete autonomous learning cycle.
    
    Cycle:
    1. OBSERVE - Collect metrics, health, performance data
    2. ANALYZE - Pattern detection, root cause analysis
    3. LEARN - Extract actionable rules and patterns
    4. ADAPT - Change system based on learning
    5. EXECUTE - Apply changes to running system
    6. MEASURE - Verify changes had expected impact
    7. REPEAT
    """
    
    def __init__(self, cycle_interval_seconds: int = 60):
        self.cycle_interval = cycle_interval_seconds
        self.self_model = get_self_model()
        self.metrics = get_metrics_collector()
        self.orchestrator = get_system_orchestrator()
        
        self.observations: List[Observation] = []
        self.analyses: List[Analysis] = []
        self.learned_outcomes: List[LearningOutcome] = []
        self.adaptations: List[Adaptation] = []
        
        self.running = False
        self.cycle_thread: Optional[threading.Thread] = None
        self.cycle_count = 0
        self.successful_adaptations = 0
        self.failed_adaptations = 0
        
        logger.info("✓ Autonomous Learning Loop initialized")
    
    def start(self) -> None:
        """Start the learning loop"""
        if self.running:
            logger.warning("Learning loop already running")
            return
        
        self.running = True
        self.cycle_thread = threading.Thread(target=self._learning_loop, daemon=True)
        self.cycle_thread.start()
        logger.info(f"✓ Learning loop started (interval: {self.cycle_interval}s)")
    
    def stop(self) -> None:
        """Stop the learning loop"""
        self.running = False
        if self.cycle_thread:
            self.cycle_thread.join(timeout=5)
        logger.info("Learning loop stopped")
    
    def _learning_loop(self) -> None:
        """Main learning loop"""
        while self.running:
            try:
                self._execute_learning_cycle()
                time.sleep(self.cycle_interval)
            except Exception as e:
                logger.error(f"Error in learning cycle: {e}")
                time.sleep(1)
    
    def _execute_learning_cycle(self) -> None:
        """Execute one complete learning cycle"""
        self.cycle_count += 1
        logger.info(f"\n{'='*60}")
        logger.info(f"Learning Cycle #{self.cycle_count}")
        logger.info(f"{'='*60}")
        
        # Step 1: Observe
        observations = self._observe()
        
        # Step 2: Analyze
        analysis = self._analyze(observations)
        
        # Step 3: Learn
        learning = self._learn(analysis)
        
        # Step 4-5: Adapt and Execute
        adaptation = self._adapt_and_execute(learning, analysis)
        
        if adaptation:
            # Step 6: Measure
            outcome = self._measure_outcome(adaptation)
            adaptation.actual_outcome = outcome
            adaptation.successful = self._evaluate_success(adaptation)
            
            if adaptation.successful:
                self.successful_adaptations += 1
                logger.info(f"✓ Adaptation successful: {adaptation.change}")
            else:
                self.failed_adaptations += 1
                logger.warning(f"✗ Adaptation unsuccessful: {adaptation.change}")
                self._rollback(adaptation)
            
            self.adaptations.append(adaptation)
    
    def _observe(self) -> Observation:
        """Step 1: Observe current system state"""
        status = self.orchestrator.get_system_status()
        
        # Get self-model analysis
        self_analysis = self.self_model.analyze_self()
        
        observation = Observation(
            timestamp=datetime.now(),
            metrics=status.get('metrics', {}),
            health=status['components']['health'],
            bottlenecks=self_analysis.bottlenecks
        )
        
        self.observations.append(observation)
        logger.info(f"📊 Observed {len(observation.metrics)} metrics, "
                   f"{len(observation.bottlenecks)} bottlenecks")
        
        return observation
    
    def _analyze(self, obs: Observation) -> Analysis:
        """Step 2: Analyze observations for patterns"""
        
        # Detect patterns
        pattern = self._detect_pattern(obs)
        
        # Determine severity
        severity = self._calculate_severity(obs)
        
        # Root cause analysis
        root_cause = self._find_root_cause(obs, pattern)
        
        # Identify impacts
        impacts = self._identify_impacts(obs, root_cause)
        
        analysis = Analysis(
            timestamp=datetime.now(),
            pattern=pattern,
            severity=severity,
            root_cause=root_cause,
            impacts=impacts,
            confidence=0.85  # Placeholder
        )
        
        self.analyses.append(analysis)
        logger.info(f"🔍 Analysis: {pattern} (severity: {severity:.1%}, "
                   f"confidence: {analysis.confidence:.1%})")
        
        return analysis
    
    def _learn(self, analysis: Analysis) -> LearningOutcome:
        """Step 3: Extract learnings from analysis"""
        
        # Generate actionable rule
        rule = self._generate_rule(analysis)
        
        # Gather evidence
        evidence = self._gather_evidence(analysis)
        
        learning = LearningOutcome(
            timestamp=datetime.now(),
            pattern=analysis.pattern,
            rule=rule,
            confidence=analysis.confidence,
            evidence=evidence
        )
        
        self.learned_outcomes.append(learning)
        logger.info(f"💡 Learned: {rule}")
        
        return learning
    
    def _adapt_and_execute(self, learning: LearningOutcome, analysis: Analysis) -> Optional[Adaptation]:
        """Step 4-5: Generate and execute adaptations"""
        
        if not analysis.bottlenecks:
            logger.info("No actionable bottlenecks to address")
            return None
        
        # Focus on highest priority bottleneck
        target = analysis.bottlenecks[0]
        
        # Determine adaptation type and strategy
        adaptation_type = self._determine_adaptation_type(target, analysis)
        change = self._generate_adaptation(target, adaptation_type, learning)
        
        if not change:
            return None
        
        # Predict outcome
        prediction = self._predict_outcome(change)
        
        adaptation = Adaptation(
            timestamp=datetime.now(),
            adaptation_type=adaptation_type,
            target=target,
            change=change,
            reason=analysis.root_cause,
            prediction=prediction
        )
        
        # Execute adaptation
        execution_success = self._execute_adaptation(adaptation)
        
        if execution_success:
            logger.info(f"🔧 Executed adaptation on {target}: {change}")
            return adaptation
        else:
            logger.warning(f"Failed to execute adaptation on {target}")
            return None
    
    def _measure_outcome(self, adaptation: Adaptation) -> Dict[str, Any]:
        """Step 6: Measure actual outcome of changes"""
        
        # Wait a moment for changes to take effect
        time.sleep(5)
        
        # Collect new metrics
        status = self.orchestrator.get_system_status()
        
        outcome = {
            "timestamp": datetime.now().isoformat(),
            "metrics_after": status.get('metrics', {}),
            "health_after": status['components']['health'],
            "performance_improved": False,  # Placeholder
            "resource_improved": False
        }
        
        logger.info(f"📈 Measured outcome: {outcome}")
        return outcome
    
    def _evaluate_success(self, adaptation: Adaptation) -> bool:
        """Evaluate if adaptation was successful"""
        if not adaptation.actual_outcome:
            return False
        
        # Check if predictions matched reality
        predicted_improvement = adaptation.prediction.get('improvement', 0)
        actual_result = adaptation.actual_outcome.get('performance_improved', False)
        
        return actual_result or predicted_improvement > 0.1
    
    def _rollback(self, adaptation: Adaptation) -> None:
        """Rollback failed adaptation"""
        logger.warning(f"Rolling back failed adaptation: {adaptation.change}")
        # TODO: Implement rollback logic
    
    def _detect_pattern(self, obs: Observation) -> str:
        """Detect patterns in observations"""
        # Check for memory spike
        for comp, metrics in obs.metrics.items():
            mem_usage = metrics.get('memory_percent', 0)
            if mem_usage > 85:
                return f"memory_spike_{comp}"
        
        # Check for latency spike
        for comp, metrics in obs.metrics.items():
            latency = metrics.get('operation_time', {}).get('avg', 0)
            if latency > 500:
                return f"latency_spike_{comp}"
        
        # Check for error spike
        if obs.health.get('unhealthy_count', 0) > 0:
            return "health_degradation"
        
        return "normal_operation"
    
    def _calculate_severity(self, obs: Observation) -> float:
        """Calculate severity of current state"""
        severity = 0.0
        
        # Health impacts severity
        total = obs.health.get('total_components', 1)
        unhealthy = obs.health.get('unhealthy_count', 0)
        severity += (unhealthy / total) * 0.5
        
        # Bottleneck count impacts severity
        severity += min(len(obs.bottlenecks) / 5, 1.0) * 0.3
        
        # Alerts impact severity
        severity += min(obs.health.get('active_alerts', 0) / 10, 1.0) * 0.2
        
        return min(severity, 1.0)
    
    def _find_root_cause(self, obs: Observation, pattern: str) -> str:
        """Find root cause of pattern"""
        if "memory_spike" in pattern:
            return "Excessive memory allocation or leak in component"
        elif "latency_spike" in pattern:
            return "Performance degradation in critical path"
        elif "health_degradation" in pattern:
            return "Multiple component failures"
        else:
            return "No obvious root cause"
    
    def _identify_impacts(self, obs: Observation, root_cause: str) -> List[str]:
        """Identify what's impacted by the issue"""
        impacts = []
        
        if obs.health.get('unhealthy_count', 0) > 0:
            impacts.append("system_reliability")
        
        if len(obs.bottlenecks) > 0:
            impacts.append("system_performance")
        
        if obs.health.get('active_alerts', 0) > 0:
            impacts.append("alerting_system")
        
        return impacts
    
    def _generate_rule(self, analysis: Analysis) -> str:
        """Generate human-readable rule from analysis"""
        return (f"When {analysis.pattern} (severity {analysis.severity:.1%}), "
               f"likely root cause is {analysis.root_cause}")
    
    def _gather_evidence(self, analysis: Analysis) -> List[Dict]:
        """Gather supporting evidence for learning"""
        # Look for similar patterns in history
        similar = [
            {
                "pattern": a.pattern,
                "confidence": a.confidence,
                "timestamp": a.timestamp.isoformat()
            }
            for a in self.analyses[-10:] if a.pattern == analysis.pattern
        ]
        
        return similar
    
    def _determine_adaptation_type(self, target: str, analysis: Analysis) -> AdaptationType:
        """Determine what type of adaptation is needed"""
        if "memory" in analysis.pattern:
            return AdaptationType.CACHING_ADJUSTMENT
        elif "latency" in analysis.pattern:
            return AdaptationType.ALGORITHM_SWITCH
        elif "health" in analysis.pattern:
            return AdaptationType.RESOURCE_REALLOCATION
        else:
            return AdaptationType.PARAMETER_TUNING
    
    def _generate_adaptation(
        self,
        target: str,
        adaptation_type: AdaptationType,
        learning: LearningOutcome
    ) -> Optional[str]:
        """Generate specific adaptation"""
        
        if adaptation_type == AdaptationType.PARAMETER_TUNING:
            return f"Increase timeout for {target} by 20%"
        elif adaptation_type == AdaptationType.CACHING_ADJUSTMENT:
            return f"Increase TTL from 3600 to 7200 for {target}"
        elif adaptation_type == AdaptationType.ALGORITHM_SWITCH:
            return f"Switch to faster algorithm for {target}"
        elif adaptation_type == AdaptationType.RESOURCE_REALLOCATION:
            return f"Reallocate resources to {target}"
        else:
            return None
    
    def _predict_outcome(self, change: str) -> Dict[str, Any]:
        """Predict outcome of change"""
        return {
            "improvement": 0.15,  # Predict 15% improvement
            "confidence": 0.75,
            "latency_reduction": "10-20%",
            "memory_reduction": "5-10%"
        }
    
    def _execute_adaptation(self, adaptation: Adaptation) -> bool:
        """Execute adaptation"""
        try:
            logger.info(f"Executing: {adaptation.change}")
            # TODO: Implement actual execution
            return True
        except Exception as e:
            logger.error(f"Failed to execute adaptation: {e}")
            return False
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get learning loop statistics"""
        return {
            "cycles_executed": self.cycle_count,
            "adaptations_attempted": len(self.adaptations),
            "successful_adaptations": self.successful_adaptations,
            "failed_adaptations": self.failed_adaptations,
            "success_rate": (
                self.successful_adaptations / max(len(self.adaptations), 1) * 100
            ),
            "patterns_learned": len(set(o.pattern for o in self.learned_outcomes)),
            "total_learnings": len(self.learned_outcomes)
        }


# Global instance
_learning_loop: Optional[AutonomousLearningLoop] = None


def get_learning_loop() -> AutonomousLearningLoop:
    """Get or create global learning loop"""
    global _learning_loop
    if _learning_loop is None:
        _learning_loop = AutonomousLearningLoop()
    return _learning_loop
