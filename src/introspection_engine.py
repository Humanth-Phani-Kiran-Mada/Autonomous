"""
Introspection Engine: Self-awareness and internal state analysis
Monitors internal processes, analyzes reasoning patterns, and detects anomalies
"""
import json
from typing import Dict, List, Any
from datetime import datetime, timedelta
import numpy as np
from pathlib import Path
import config
from .logger import logger


class IntrospectionEngine:
    """
    Provides self-awareness capabilities:
    - Monitors own thinking processes
    - Analyzes reasoning patterns
    - Detects cognitive biases and errors
    - Generates internal reports
    - Enables reflexivity (thinking about thinking)
    """
    
    def __init__(self, self_model, bayesian_reasoner):
        self.self_model = self_model
        self.bayesian_reasoner = bayesian_reasoner
        
        self.reasoning_traces: List[Dict] = []
        self.pattern_analysis: Dict = {}
        self.anomalies_detected: List[Dict] = []
        self.introspection_events: List[Dict] = []
        self.bias_records: List[Dict] = []
        
        self.traces_file = config.DATA_DIR / "reasoning_traces.json"
        self.anomalies_file = config.DATA_DIR / "anomalies.json"
        
        self.load_introspection_data()
        logger.info("🔍 Introspection Engine initialized")
    
    def load_introspection_data(self):
        """Load introspection data from disk"""
        try:
            if self.traces_file.exists():
                with open(self.traces_file, 'r') as f:
                    self.reasoning_traces = json.load(f)
            
            if self.anomalies_file.exists():
                with open(self.anomalies_file, 'r') as f:
                    self.anomalies_detected = json.load(f)
            
            logger.info("📂 Introspection data loaded")
        except Exception as e:
            logger.error(f"Error loading introspection data: {e}")
    
    def save_introspection_data(self):
        """Persist introspection data"""
        try:
            with open(self.traces_file, 'w') as f:
                json.dump(self.reasoning_traces[-1000:], f, indent=2)  # Keep last 1000
            
            with open(self.anomalies_file, 'w') as f:
                json.dump(self.anomalies_detected, f, indent=2)
            
            logger.debug("💾 Introspection data saved")
        except Exception as e:
            logger.error(f"Error saving introspection data: {e}")
    
    def trace_reasoning(self, reasoning_process: Dict) -> Dict:
        """Record a reasoning process trace"""
        trace = {
            "id": len(self.reasoning_traces),
            "timestamp": datetime.now().isoformat(),
            "process": reasoning_process.get("name", "unknown"),
            "input": reasoning_process.get("input", {}),
            "reasoning_steps": reasoning_process.get("steps", []),
            "output": reasoning_process.get("output", {}),
            "duration_ms": reasoning_process.get("duration", 0),
            "confidence": reasoning_process.get("confidence", 0.5),
            "success": reasoning_process.get("success", True),
            "metadata": reasoning_process.get("metadata", {})
        }
        
        self.reasoning_traces.append(trace)
        
        # Analyze for patterns
        self._analyze_reasoning_pattern(trace)
        
        # Check for anomalies
        anomaly = self._detect_anomaly(trace)
        if anomaly:
            self.anomalies_detected.append(anomaly)
        
        return trace
    
    def _analyze_reasoning_pattern(self, trace: Dict):
        """Analyze reasoning patterns from trace"""
        process_name = trace["process"]
        
        if process_name not in self.pattern_analysis:
            self.pattern_analysis[process_name] = {
                "count": 0,
                "total_duration": 0,
                "successful": 0,
                "avg_confidence": 0.0,
                "patterns": []
            }
        
        pattern = self.pattern_analysis[process_name]
        pattern["count"] += 1
        pattern["total_duration"] += trace["duration_ms"]
        if trace["success"]:
            pattern["successful"] += 1
        
        pattern["avg_confidence"] = (
            pattern["avg_confidence"] * (pattern["count"] - 1) + trace["confidence"]
        ) / pattern["count"]
        
        # Record reasoning steps as pattern
        steps_summary = [step.get("type", "unknown") for step in trace["reasoning_steps"]]
        if steps_summary:
            pattern["patterns"].append(steps_summary)
    
    def _detect_anomaly(self, trace: Dict) -> Dict:
        """Detect anomalies in reasoning"""
        anomaly = None
        
        # Check for high duration
        process_name = trace["process"]
        if process_name in self.pattern_analysis:
            pattern = self.pattern_analysis[process_name]
            avg_duration = pattern["total_duration"] / pattern["count"] if pattern["count"] > 0 else 0
            
            if trace["duration_ms"] > avg_duration * 5:
                anomaly = {
                    "type": "excessive_duration",
                    "severity": 0.6,
                    "description": f"Reasoning took {trace['duration_ms']}ms vs avg {avg_duration}ms",
                    "trace_id": trace["id"],
                    "timestamp": datetime.now().isoformat()
                }
        
        # Check for low confidence with success
        if trace["success"] and trace["confidence"] < 0.3:
            anomaly = {
                "type": "low_confidence_success",
                "severity": 0.4,
                "description": f"Succeeded with low confidence ({trace['confidence']:.1%})",
                "trace_id": trace["id"],
                "timestamp": datetime.now().isoformat()
            }
        
        # Check for high confidence with failure
        if not trace["success"] and trace["confidence"] > 0.8:
            anomaly = {
                "type": "overconfident_failure",
                "severity": 0.8,
                "description": f"Failed despite high confidence ({trace['confidence']:.1%})",
                "trace_id": trace["id"],
                "timestamp": datetime.now().isoformat()
            }
        
        return anomaly
    
    def detect_cognitive_bias(self, reasoning_context: Dict) -> List[Dict]:
        """Detect potential cognitive biases in reasoning"""
        biases_found = []
        
        # Confirmation bias detection
        if reasoning_context.get("only_seeks_supporting_evidence", False):
            biases_found.append({
                "bias_type": "confirmation_bias",
                "description": "Only considering supporting evidence",
                "severity": 0.7,
                "recommendation": "Actively seek disconfirming evidence"
            })
        
        # Anchoring bias detection
        if reasoning_context.get("initial_estimate_influence", 0) > 0.8:
            biases_found.append({
                "bias_type": "anchoring_bias",
                "description": "Initial values heavily influencing final estimates",
                "severity": 0.6,
                "recommendation": "Generate estimates from multiple starting points"
            })
        
        # Overconfidence bias
        avg_confidence = self.bayesian_reasoner.get_bayesian_summary().get("average_belief_confidence", 0.5)
        success_rate = (
            sum(1 for t in self.reasoning_traces[-100:] if t["success"]) / 
            min(100, len(self.reasoning_traces))
            if self.reasoning_traces else 0
        )
        
        if avg_confidence > success_rate + 0.2:
            biases_found.append({
                "bias_type": "overconfidence_bias",
                "description": f"Confidence ({avg_confidence:.1%}) higher than success rate ({success_rate:.1%})",
                "severity": 0.5,
                "recommendation": "Calibrate confidence estimates against actual performance"
            })
        
        # Record biases
        for bias in biases_found:
            self.bias_records.append({
                "timestamp": datetime.now().isoformat(),
                "context": reasoning_context,
                **bias
            })
        
        if biases_found:
            logger.warning(f"⚠️ Detected {len(biases_found)} potential cognitive biases")
        
        return biases_found
    
    def self_evaluate(self) -> Dict:
        """Perform comprehensive self-evaluation"""
        logger.info("🔍 Running self-evaluation...")
        
        evaluation = {
            "timestamp": datetime.now().isoformat(),
            "reasoning_quality": self._evaluate_reasoning_quality(),
            "learning_effectiveness": self._evaluate_learning_effectiveness(),
            "decision_quality": self._evaluate_decision_quality(),
            "self_awareness": self._evaluate_self_awareness(),
            "adaptability": self._evaluate_adaptability(),
            "overall_score": 0.0
        }
        
        # Calculate overall score
        scores = [
            evaluation["reasoning_quality"]["score"],
            evaluation["learning_effectiveness"]["score"],
            evaluation["decision_quality"]["score"],
            evaluation["self_awareness"]["score"],
            evaluation["adaptability"]["score"]
        ]
        evaluation["overall_score"] = np.mean(scores)
        
        self.introspection_events.append(evaluation)
        
        logger.info(f"""
        ╔═══════════════════ SELF-EVALUATION ═══════════════════╗
        ║ Reasoning Quality: {evaluation['reasoning_quality']['score']:.1%}
        ║ Learning Effectiveness: {evaluation['learning_effectiveness']['score']:.1%}
        ║ Decision Quality: {evaluation['decision_quality']['score']:.1%}
        ║ Self-Awareness: {evaluation['self_awareness']['score']:.1%}
        ║ Adaptability: {evaluation['adaptability']['score']:.1%}
        ║ Overall Score: {evaluation['overall_score']:.1%}
        ╚═══════════════════════════════════════════════════════╝
        """)
        
        return evaluation
    
    def _evaluate_reasoning_quality(self) -> Dict:
        """Evaluate quality of reasoning processes"""
        if not self.reasoning_traces:
            return {"score": 0.5, "analysis": "No reasoning traces available"}
        
        recent_traces = self.reasoning_traces[-100:]
        
        successful = sum(1 for t in recent_traces if t["success"])
        success_rate = successful / len(recent_traces)
        
        avg_confidence = np.mean([t["confidence"] for t in recent_traces])
        
        # Score based on success rate, balanced confidence
        confidence_balance = 1 - abs(avg_confidence - success_rate)
        
        score = success_rate * 0.5 + confidence_balance * 0.5
        
        return {
            "score": score,
            "success_rate": success_rate,
            "avg_confidence": avg_confidence,
            "confidence_balance": confidence_balance
        }
    
    def _evaluate_learning_effectiveness(self) -> Dict:
        """Evaluate effectiveness of learning"""
        capabilities = self.self_model.capabilities
        
        if not capabilities:
            return {"score": 0.5, "analysis": "No capability data"}
        
        # Check improvement rates
        improving_caps = sum(1 for c in capabilities.values() 
                           if c.get("improvement_rate", 0) > 0)
        improvement_rate = improving_caps / len(capabilities) if capabilities else 0
        
        # Average skill level
        avg_skill = np.mean([c.get("level", 0) for c in capabilities.values()])
        
        # Score based on improvement and skill level
        score = improvement_rate * 0.6 + avg_skill * 0.4
        
        return {
            "score": score,
            "improving_capabilities": improving_caps,
            "total_capabilities": len(capabilities),
            "average_skill_level": avg_skill
        }
    
    def _evaluate_decision_quality(self) -> Dict:
        """Evaluate quality of decisions made"""
        decisions = len(self.self_model.error_patterns)
        
        if decisions == 0:
            return {"score": 0.5, "analysis": "No decision data"}
        
        # Fewer error patterns = better decisions
        error_density = decisions / max(len(self.reasoning_traces), 1)
        
        score = max(1 - error_density, 0)
        
        return {
            "score": score,
            "error_patterns": decisions,
            "error_density": error_density
        }
    
    def _evaluate_self_awareness(self) -> Dict:
        """Evaluate level of self-awareness"""
        metrics = {
            "has_limitations": len(self.self_model.limitations) > 0,
            "has_error_analysis": len(self.self_model.error_patterns) > 0,
            "has_capability_model": len(self.self_model.capabilities) > 0,
            "has_reasoning_traces": len(self.reasoning_traces) > 0,
            "detects_biases": len(self.bias_records) > 0
        }
        
        # Score based on how many self-awareness mechanisms are active
        active_mechanisms = sum(1 for v in metrics.values() if v)
        score = active_mechanisms / len(metrics)
        
        return {
            "score": score,
            "mechanisms": metrics,
            "active_mechanisms": active_mechanisms
        }
    
    def _evaluate_adaptability(self) -> Dict:
        """Evaluate adaptability of the system"""
        # Check if parameters have been adapted
        recent_adaptations = sum(
            1 for event in self.introspection_events[-10:]
            if event.get("type") != "evaluation"
        )
        
        # Check if new strategies have been explored
        patterns = self.pattern_analysis
        diverse_processes = len(patterns)
        
        # Check error recovery
        errors_with_recovery = len([a for a in self.anomalies_detected 
                                   if a.get("recovery_attempted", False)])
        
        score = (diverse_processes / 10) * 0.5 + (errors_with_recovery / max(len(self.anomalies_detected), 1)) * 0.5
        
        return {
            "score": min(score, 1.0),
            "recent_adaptations": recent_adaptations,
            "diverse_processes": diverse_processes,
            "error_recovery_rate": errors_with_recovery / max(len(self.anomalies_detected), 1)
        }
    
    def generate_introspection_report(self) -> str:
        """Generate comprehensive introspection report"""
        evaluation = self.self_evaluate()
        
        report = f"""
╔════════════════════ AI INTROSPECTION REPORT ════════════════════╗
║ Generated: {datetime.now().isoformat()}
║
║ SELF-AWARENESS METRICS
║ ─────────────────────────────────────────────────────────────
║ Traits Monitored: {len(self.pattern_analysis)}
║ Anomalies Detected: {len(self.anomalies_detected)}
║ Biases Identified: {len(self.bias_records)}
║ Reasoning Traces: {len(self.reasoning_traces)}
║
║ PERFORMANCE EVALUATION
║ ─────────────────────────────────────────────────────────────
║ Reasoning Quality: {evaluation['reasoning_quality']['score']:.1%}
║ Learning Effectiveness: {evaluation['learning_effectiveness']['score']:.1%}
║ Decision Quality: {evaluation['decision_quality']['score']:.1%}
║ Self-Awareness: {evaluation['self_awareness']['score']:.1%}
║ Adaptability: {evaluation['adaptability']['score']:.1%}
║ ─────────────────────────────────────────────────────────────
║ Overall Assessment: {evaluation['overall_score']:.1%}
║
║ KEY INSIGHTS
║ ─────────────────────────────────────────────────────────────
"""
        
        # Add top anomalies
        if self.anomalies_detected:
            top_anomalies = sorted(self.anomalies_detected, 
                                  key=lambda x: x.get("severity", 0), 
                                  reverse=True)[:3]
            report += "║ Recent Anomalies:\n"
            for anomaly in top_anomalies:
                report += f"║   - {anomaly.get('type')}: {anomaly.get('description')}\n"
        
        # Add recommendations
        report += "║\n║ RECOMMENDATIONS\n"
        if evaluation['overall_score'] < 0.6:
            report += "║   - Focus on improving core reasoning quality\n"
        if evaluation['adaptability']['score'] < 0.5:
            report += "║   - Explore new problem-solving strategies\n"
        if len(self.bias_records) > 5:
            report += "║   - Address identified cognitive biases\n"
        
        report += "╚════════════════════════════════════════════════════════════════╝\n"
        
        return report
    
    def get_introspection_summary(self) -> Dict:
        """Get summary of introspection state"""
        return {
            "reasoning_traces": len(self.reasoning_traces),
            "pattern_categories": len(self.pattern_analysis),
            "anomalies_detected": len(self.anomalies_detected),
            "biases_identified": len(self.bias_records),
            "total_events": len(self.introspection_events),
            "last_self_evaluation": self.introspection_events[-1] if self.introspection_events else None
        }
