"""
Self-Model Engine: AI understanding of its own capabilities and limitations
Enables introspection, self-diagnosis, and adaptive behavior
"""
import json
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta
import numpy as np
from pathlib import Path
import config
from .logger import logger


class SelfModel:
    """
    Maintains a comprehensive model of the AI's own capabilities, limitations,
    and performance characteristics. Enables true self-awareness and adaptation.
    """
    
    def __init__(self):
        self.capabilities: Dict[str, Dict] = {}
        self.performance_history: List[Dict] = []
        self.limitations: List[Dict] = []
        self.confidence_intervals: Dict[str, Tuple[float, float]] = {}
        self.error_patterns: List[Dict] = []
        self.learning_curves: Dict[str, List[float]] = {}
        self.resource_usage: Dict[str, float] = {}
        self.self_diagnostics: Dict[str, any] = {}
        
        self.model_file = config.DATA_DIR / "self_model.json"
        self.diagnostics_file = config.DATA_DIR / "diagnostics.json"
        
        self.load_self_model()
        logger.info(" Self-Model Engine initialized")
    
    def load_self_model(self):
        """Load self-model from persistent storage"""
        try:
            if self.model_file.exists():
                with open(self.model_file, 'r') as f:
                    data = json.load(f)
                    self.capabilities = data.get("capabilities", {})
                    self.limitations = data.get("limitations", [])
                    self.learning_curves = data.get("learning_curves", {})
                logger.info(" Self-model loaded from disk")
        except Exception as e:
            logger.error(f"Error loading self-model: {e}")
    
    def save_self_model(self):
        """Persist self-model to disk"""
        try:
            model_data = {
                "capabilities": self.capabilities,
                "limitations": self.limitations,
                "learning_curves": self.learning_curves,
                "confidence_intervals": self.confidence_intervals,
                "saved_at": datetime.now().isoformat()
            }
            with open(self.model_file, 'w') as f:
                json.dump(model_data, f, indent=2)
            logger.debug(" Self-model saved")
        except Exception as e:
            logger.error(f"Error saving self-model: {e}")
    
    def register_capability(self, capability_name: str, initial_level: float = 0.0,
                           domain: str = "general", description: str = ""):
        """Register a new capability in the self-model"""
        self.capabilities[capability_name] = {
            "name": capability_name,
            "domain": domain,
            "description": description,
            "level": initial_level,
            "last_updated": datetime.now().isoformat(),
            "improvement_rate": 0.0,
            "usage_count": 0,
            "success_count": 0,
            "failure_count": 0,
            "confidence": 0.5
        }
        
        # Initialize learning curve
        self.learning_curves[capability_name] = [initial_level]
        
        logger.info(f" Registered capability: {capability_name} ({domain})")
    
    def update_capability_performance(self, capability_name: str, 
                                     success: bool, confidence: float = 0.5,
                                     performance_metric: float = 0.5):
        """Update capability performance based on execution results"""
        if capability_name not in self.capabilities:
            self.register_capability(capability_name)
        
        cap = self.capabilities[capability_name]
        cap["usage_count"] += 1
        
        if success:
            cap["success_count"] += 1
            improvement = performance_metric * config.LEARNING_RATE
            cap["level"] = min(cap["level"] + improvement, 1.0)
        else:
            cap["failure_count"] += 1
            cap["level"] = max(cap["level"] - (1 - performance_metric) * 0.01, 0.0)
        
        # Update confidence using Bayesian approach
        success_rate = cap["success_count"] / cap["usage_count"] if cap["usage_count"] > 0 else 0
        cap["confidence"] = success_rate * 0.7 + confidence * 0.3
        
        # Update learning curve
        self.learning_curves.setdefault(capability_name, []).append(cap["level"])
        
        # Calculate improvement rate
        if len(self.learning_curves[capability_name]) > 5:
            recent_curve = self.learning_curves[capability_name][-5:]
            cap["improvement_rate"] = (recent_curve[-1] - recent_curve[0]) / 4
        
        cap["last_updated"] = datetime.now().isoformat()
        
        logger.debug(f" Updated {capability_name}: level={cap['level']:.2%}, confidence={cap['confidence']:.2%}")
    
    def detect_limitation(self, limitation_type: str, description: str,
                         severity: float = 0.5, affected_capability: str = "general"):
        """Detect and record a limitation or constraint"""
        limitation = {
            "id": len(self.limitations),
            "type": limitation_type,
            "description": description,
            "severity": min(max(severity, 0), 1.0),
            "affected_capability": affected_capability,
            "detected_at": datetime.now().isoformat(),
            "detection_count": 1,
            "mitigation_strategies": []
        }
        
        # Check if similar limitation exists
        for existing in self.limitations:
            if existing["type"] == limitation_type and existing["affected_capability"] == affected_capability:
                existing["detection_count"] += 1
                existing["severity"] = max(existing["severity"], severity)
                logger.info(f"⚠ Limitation reinforced: {limitation_type}")
                return existing
        
        self.limitations.append(limitation)
        logger.warning(f"⚠ New limitation detected: {limitation_type} (severity={severity:.2%})")
        return limitation
    
    def add_mitigation_strategy(self, limitation_id: int, strategy: str):
        """Add workaround strategy for a detected limitation"""
        if 0 <= limitation_id < len(self.limitations):
            limitation = self.limitations[limitation_id]
            if strategy not in limitation["mitigation_strategies"]:
                limitation["mitigation_strategies"].append(strategy)
                logger.info(f" Added mitigation strategy for {limitation['type']}")
    
    def get_confidence_interval(self, capability_name: str, confidence_level: float = 0.95) -> Tuple[float, float]:
        """Calculate confidence interval for a capability estimate"""
        if capability_name not in self.capabilities:
            return (0.0, 1.0)
        
        cap = self.capabilities[capability_name]
        if cap["usage_count"] < 2:
            return (0.0, cap["level"])
        
        success_rate = cap["success_count"] / cap["usage_count"]
        std_error = np.sqrt(success_rate * (1 - success_rate) / cap["usage_count"])
        
        # Use t-distribution for small samples
        z_score = 1.96 if cap["usage_count"] > 30 else 2.576
        margin = z_score * std_error
        
        lower = max(success_rate - margin, 0)
        upper = min(success_rate + margin, 1)
        
        return (lower, upper)
    
    def analyze_error_patterns(self, error_type: str, context: Dict, 
                              capability: str = "general"):
        """Analyze and learn from error patterns"""
        error_record = {
            "timestamp": datetime.now().isoformat(),
            "error_type": error_type,
            "capability": capability,
            "context": context,
            "frequency": 1
        }
        
        # Check for similar errors
        for existing_error in self.error_patterns:
            if (existing_error["error_type"] == error_type and 
                existing_error["capability"] == capability):
                existing_error["frequency"] += 1
                logger.info(f" Error pattern reinforced: {error_type}")
                return existing_error
        
        self.error_patterns.append(error_record)
        logger.warning(f" New error pattern: {error_type} in {capability}")
        
        # Trigger recovery mechanism if frequency is high
        if self._is_repeating_error(error_type):
            self.detect_limitation("repeating_error", f"Repeating error: {error_type}", 
                                 severity=0.7, affected_capability=capability)
        
        return error_record
    
    def _is_repeating_error(self, error_type: str) -> bool:
        """Check if an error occurs repeatedly"""
        error_count = sum(1 for e in self.error_patterns if e["error_type"] == error_type)
        return error_count >= 3
    
    def run_self_diagnostics(self) -> Dict:
        """Run comprehensive self-diagnostics"""
        logger.info(" Running self-diagnostics...")
        
        diagnostics = {
            "timestamp": datetime.now().isoformat(),
            "total_capabilities": len(self.capabilities),
            "active_capabilities": sum(1 for c in self.capabilities.values() if c["usage_count"] > 0),
            "average_confidence": np.mean([c["confidence"] for c in self.capabilities.values()]) if self.capabilities else 0,
            "detected_limitations": len(self.limitations),
            "severe_limitations": sum(1 for l in self.limitations if l["severity"] > 0.7),
            "repeating_errors": len(self.error_patterns),
            "capability_health": self._assess_capability_health(),
            "learning_status": self._assess_learning_status(),
            "resource_health": self._assess_resource_health(),
            "recommendations": self._generate_recommendations()
        }
        
        self.self_diagnostics = diagnostics
        
        logger.info(f"""
        ╔════════════════════════ SELF-DIAGNOSTICS ════════════════════════╗
        ║ Capabilities: {diagnostics['total_capabilities']} registered, {diagnostics['active_capabilities']} active
        ║ Avg Confidence: {diagnostics['average_confidence']:.2%}
        ║ Limitations: {diagnostics['detected_limitations']} ({diagnostics['severe_limitations']} severe)
        ║ Error Patterns: {diagnostics['repeating_errors']} detected
        ║ Status: {diagnostics['capability_health']['status']}
        ║ Recommendations: {len(diagnostics['recommendations'])} actions suggested
        ╚══════════════════════════════════════════════════════════════════╝
        """)
        
        return diagnostics
    
    def _assess_capability_health(self) -> Dict:
        """Assess overall health of capabilities"""
        if not self.capabilities:
            return {"status": "UNKNOWN", "score": 0.0}
        
        scores = [c["confidence"] * c["level"] for c in self.capabilities.values()]
        avg_score = np.mean(scores)
        
        if avg_score > 0.8:
            status = "EXCELLENT"
        elif avg_score > 0.6:
            status = "GOOD"
        elif avg_score > 0.4:
            status = "FAIR"
        else:
            status = "POOR"
        
        return {"status": status, "score": avg_score}
    
    def _assess_learning_status(self) -> Dict:
        """Assess learning progress and trajectory"""
        if not self.learning_curves:
            return {"status": "IDLE", "improvement_rate": 0.0}
        
        total_improvement = 0
        for curve in self.learning_curves.values():
            if len(curve) > 1:
                total_improvement += curve[-1] - curve[0]
        
        avg_improvement = total_improvement / len(self.learning_curves) if self.learning_curves else 0
        
        if avg_improvement > 0.1:
            status = "RAPID_LEARNING"
        elif avg_improvement > 0.02:
            status = "STEADY_LEARNING"
        elif avg_improvement > -0.02:
            status = "STABLE"
        else:
            status = "DECLINING"
        
        return {"status": status, "improvement_rate": avg_improvement}
    
    def _assess_resource_health(self) -> Dict:
        """Assess resource utilization health"""
        # Check if resource usage is within acceptable limits
        memory_ok = self.resource_usage.get("memory_percent", 0) < 80
        cpu_ok = self.resource_usage.get("cpu_percent", 0) < 85
        
        status = "HEALTHY" if (memory_ok and cpu_ok) else "WARNING"
        
        return {
            "status": status,
            "memory": self.resource_usage.get("memory_percent", 0),
            "cpu": self.resource_usage.get("cpu_percent", 0)
        }
    
    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations for self-improvement"""
        recommendations = []
        
        # Recommend focusing on weak capabilities
        weak_caps = [c["name"] for c in self.capabilities.values() if c["level"] < 0.3]
        if weak_caps:
            recommendations.append(f"Improve weak capabilities: {', '.join(weak_caps[:3])}")
        
        # Recommend mitigating severe limitations
        severe_lims = [l for l in self.limitations if l["severity"] > 0.7]
        if severe_lims:
            recommendations.append(f"Address {len(severe_lims)} severe limitations")
        
        # Recommend learning from error patterns
        if self.error_patterns:
            top_errors = sorted(self.error_patterns, key=lambda x: x["frequency"], reverse=True)[:2]
            error_names = [e["error_type"] for e in top_errors]
            recommendations.append(f"Analyze error patterns: {', '.join(error_names)}")
        
        # Recommend exploring underutilized capabilities
        unused_caps = [c["name"] for c in self.capabilities.values() if c["usage_count"] == 0]
        if unused_caps:
            recommendations.append(f"Explore underutilized: {', '.join(unused_caps[:3])}")
        
        return recommendations
    
    def get_self_model_summary(self) -> Dict:
        """Get comprehensive self-model summary"""
        return {
            "capabilities_count": len(self.capabilities),
            "active_capabilities": sum(1 for c in self.capabilities.values() if c["usage_count"] > 0),
            "average_capability_level": np.mean([c["level"] for c in self.capabilities.values()]) if self.capabilities else 0,
            "average_confidence": np.mean([c["confidence"] for c in self.capabilities.values()]) if self.capabilities else 0,
            "limitations_count": len(self.limitations),
            "error_patterns": len(self.error_patterns),
            "diagnostics": self.self_diagnostics
        }
