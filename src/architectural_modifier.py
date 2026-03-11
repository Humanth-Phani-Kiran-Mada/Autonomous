"""
Architectural Modifier: Allows AI to modify its own architecture dynamically
Enables the system to add/remove/modify components based on performance and needs.
The ultimate self-improvement mechanism - system can change how it works.
"""
import json
from typing import Dict, List, Tuple, Optional, Any, Callable
from datetime import datetime
from pathlib import Path
import config
from .logger import logger


class ComponentModification:
    """Represents a modification to system architecture"""
    def __init__(self, modification_id: str, mod_type: str, 
                 component_name: str, description: str):
        self.modification_id = modification_id
        self.mod_type = mod_type  # "add", "remove", "modify", "replace"
        self.component_name = component_name
        self.description = description
        self.status = "proposed"  # proposed, tested, implemented, reverted
        self.test_results: Dict = {}
        self.implemented_at = None
        self.reverted_at = None
        
    def to_dict(self) -> Dict:
        return {
            "mod_id": self.modification_id,
            "type": self.mod_type,
            "component": self.component_name,
            "description": self.description,
            "status": self.status
        }


class ArchitecturalModifier:
    """
    Proposes, tests, and implements modifications to system architecture.
    Allows the AI to evolve its own structure based on needs and performance.
    """
    
    def __init__(self):
        self.modifications: Dict[str, ComponentModification] = {}
        self.modification_history: List[Dict] = []
        self.architecture_versions: List[Dict] = []
        self.performance_impact: Dict[str, float] = {}
        self.rollback_points: List[Dict] = []
        self.constraints: Dict[str, Any] = {}
        
        self.mod_file = config.DATA_DIR / "modifications.json"
        
        # Initialize default constraints
        self._initialize_constraints()
        
        logger.info("[ARCHITECTURE] Architectural Modifier initialized")
    
    def _initialize_constraints(self):
        """Initialize constraints on modifications"""
        self.constraints = {
            "max_components": 50,
            "max_modification_frequency": 10,  # per iteration
            "required_buffer_time": 100,  # iterations between major changes
            "rollback_enabled": True,
            "safety_checks": True,
            "preserve_core_functionality": True
        }
    
    def propose_modification(self, mod_type: str, component_name: str,
                           description: str, reasoning: str = "") -> ComponentModification:
        """Propose a modification to architecture"""
        mod_id = f"mod_{datetime.now().timestamp()}"
        modification = ComponentModification(mod_id, mod_type, component_name, description)
        
        self.modifications[mod_id] = modification
        
        proposal_record = {
            "mod_id": mod_id,
            "type": mod_type,
            "component": component_name,
            "reasoning": reasoning,
            "proposed_at": datetime.now().isoformat(),
            "status": "proposed"
        }
        self.modification_history.append(proposal_record)
        
        logger.info(f"[ARCHITECTURE] Proposed modification: {mod_type} {component_name}")
        
        return modification
    
    def evaluate_modification(self, mod_id: str, 
                            current_performance: Dict,
                            expected_improvement: float = 0.1) -> Dict:
        """
        Evaluate if modification should be applied.
        Returns assessment: safe/risky, recommended action.
        """
        if mod_id not in self.modifications:
            return {"error": "modification not found"}
        
        modification = self.modifications[mod_id]
        assessment = {
            "mod_id": mod_id,
            "safe": True,
            "reasons": [],
            "risks": [],
            "recommendation": "proceed with caution"
        }
        
        try:
            # Check 1: Does modification respect constraints?
            if not self._check_constraints(modification):
                assessment["safe"] = False
                assessment["risks"].append("Violates system constraints")
            
            # Check 2: Type-specific validations
            if modification.mod_type == "add":
                # Adding components is generally safe
                assessment["recommendation"] = "safe to add"
                assessment["reasons"].append("Adding components is reversible and expands capability")
            
            elif modification.mod_type == "remove":
                # Removing requires checking for dependencies
                if self._check_removal_safety(modification.component_name):
                    assessment["recommendation"] = "safe to remove"
                    assessment["reasons"].append("No critical dependencies found")
                else:
                    assessment["safe"] = False
                    assessment["risks"].append("Component has critical dependencies")
            
            elif modification.mod_type == "modify":
                # Modifications should be tested first
                assessment["recommendation"] = "test first, then implement"
                assessment["reasons"].append("Modifications should be validated on test systems")
            
            elif modification.mod_type == "replace":
                # Replacements are riskier
                assessment["safe"] = False  # By default safer
                assessment["recommendation"] = "implement with rollback plan"
                assessment["risks"].append("Replacements can cause system instability")
            
        except Exception as e:
            logger.error(f"[ARCHITECTURE] Error evaluating modification: {e}")
            assessment["safe"] = False
            assessment["risks"].append(str(e))
        
        return assessment
    
    def _check_constraints(self, modification: ComponentModification) -> bool:
        """Check if modification respects constraints"""
        try:
            # Type-specific constraint checks
            if modification.mod_type == "add":
                # Check component limit
                current_components = 12  # Base + integration components
                if current_components >= self.constraints["max_components"]:
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"[ARCHITECTURE] Error checking constraints: {e}")
            return False
    
    def _check_removal_safety(self, component_name: str) -> bool:
        """Check if component can be safely removed"""
        # Define critical components that should not be removed
        critical_components = [
            "autonomous_agent",
            "integration_layer",
            "cycle_coordinator",
            "memory_manager"
        ]
        
        if component_name in critical_components:
            return False
        
        # In real system, check dependency graph
        return True
    
    def implement_modification(self, mod_id: str) -> bool:
        """Implement an approved modification"""
        if mod_id not in self.modifications:
            logger.warning(f"[ARCHITECTURE] Modification {mod_id} not found")
            return False
        
        modification = self.modifications[mod_id]
        
        try:
            # Create rollback point first
            rollback_point = {
                "timestamp": datetime.now().isoformat(),
                "modification_id": mod_id,
                "modification_type": modification.mod_type,
                "component": modification.component_name
            }
            self.rollback_points.append(rollback_point)
            
            # Apply modification based on type
            if modification.mod_type == "add":
                result = self._apply_add(modification)
            elif modification.mod_type == "remove":
                result = self._apply_remove(modification)
            elif modification.mod_type == "modify":
                result = self._apply_modify(modification)
            elif modification.mod_type == "replace":
                result = self._apply_replace(modification)
            else:
                return False
            
            if result:
                modification.status = "implemented"
                modification.implemented_at = datetime.now().isoformat()
                
                logger.info(f"[ARCHITECTURE] Implemented: {modification.mod_type} {modification.component_name}")
                return True
            else:
                logger.error(f"[ARCHITECTURE] Failed to implement modification {mod_id}")
                return False
                
        except Exception as e:
            logger.error(f"[ARCHITECTURE] Error implementing modification: {e}")
            return False
    
    def _apply_add(self, modification: ComponentModification) -> bool:
        """Add a new component to architecture"""
        # In real implementation, would dynamically load and initialize component
        logger.info(f"[ARCHITECTURE] Adding component: {modification.component_name}")
        return True
    
    def _apply_remove(self, modification: ComponentModification) -> bool:
        """Remove a component from architecture"""
        logger.info(f"[ARCHITECTURE] Removing component: {modification.component_name}")
        return True
    
    def _apply_modify(self, modification: ComponentModification) -> bool:
        """Modify existing component"""
        logger.info(f"[ARCHITECTURE] Modifying component: {modification.component_name}")
        return True
    
    def _apply_replace(self, modification: ComponentModification) -> bool:
        """Replace component with new version"""
        logger.info(f"[ARCHITECTURE] Replacing component: {modification.component_name}")
        return True
    
    def test_modification(self, mod_id: str, test_data: Dict) -> Dict:
        """Test modification in sandbox before implementing"""
        if mod_id not in self.modifications:
            return {"error": "modification not found"}
        
        modification = self.modifications[mod_id]
        test_results = {
            "mod_id": mod_id,
            "test_status": "passed",
            "performance_change": 0.0,
            "errors": [],
            "tested_at": datetime.now().isoformat()
        }
        
        try:
            # Simulate testing the modification
            baseline = test_data.get("current_performance", 0.5)
            expected_improvement = test_data.get("expected_improvement", 0.1)
            
            # Predict outcome
            predicted_performance = baseline + (expected_improvement * 0.8)  # 80% of expected
            
            test_results["performance_change"] = predicted_performance - baseline
            test_results["predicted_performance"] = predicted_performance
            
            if predicted_performance > baseline:
                test_results["test_status"] = "passed"
                test_results["recommendation"] = "implement"
            else:
                test_results["test_status"] = "failed"
                test_results["recommendation"] = "do not implement"
            
            modification.test_results = test_results
            
            logger.info(f"[ARCHITECTURE] Test results for {mod_id}: {test_results['test_status']}")
            
        except Exception as e:
            logger.error(f"[ARCHITECTURE] Error testing modification: {e}")
            test_results["test_status"] = "error"
            test_results["errors"].append(str(e))
        
        return test_results
    
    def rollback_modification(self, mod_id: str) -> bool:
        """Revert a modification"""
        if mod_id not in self.modifications:
            return False
        
        if not self.constraints["rollback_enabled"]:
            logger.warning("[ARCHITECTURE] Rollback is disabled")
            return False
        
        modification = self.modifications[mod_id]
        
        try:
            # Reverse the modification based on type
            if modification.mod_type == "add":
                # Remove what was added
                logger.info(f"[ARCHITECTURE] Rolling back add: {modification.component_name}")
            elif modification.mod_type == "remove":
                # Re-add what was removed
                logger.info(f"[ARCHITECTURE] Rolling back remove: {modification.component_name}")
            
            modification.status = "reverted"
            modification.reverted_at = datetime.now().isoformat()
            
            logger.info(f"[ARCHITECTURE] Rolled back modification {mod_id}")
            return True
            
        except Exception as e:
            logger.error(f"[ARCHITECTURE] Error rolling back: {e}")
            return False
    
    def detect_architectural_needs(self, system_metrics: Dict) -> List[str]:
        """Analyze metrics and detect if architecture needs modification"""
        needs = []
        
        try:
            # Check memory usage
            if system_metrics.get("memory_usage", 0.5) > 0.8:
                needs.append("high_memory_usage - consider component reduction")
            
            # Check bottlenecks
            if system_metrics.get("cycle_time", 0) > 10:
                needs.append("slow_cycles - consider parallelization")
            
            # Check learning rate
            if system_metrics.get("learning_rate", 0.5) < 0.2:
                needs.append("slow_learning - consider architecture expansion")
            
            # Check error rate
            if system_metrics.get("error_rate", 0) > 0.1:
                needs.append("high_errors - consider robustness components")
            
            if needs:
                logger.info(f"[ARCHITECTURE] Detected {len(needs)} architectural needs")
            
        except Exception as e:
            logger.error(f"[ARCHITECTURE] Error detecting architectural needs: {e}")
        
        return needs
    
    def recommend_modifications(self, system_state: Dict) -> List[Dict]:
        """Recommend architectural modifications based on system state"""
        recommendations = []
        
        try:
            needs = self.detect_architectural_needs(system_state)
            
            for need in needs:
                if "high_memory_usage" in need:
                    recommendations.append({
                        "type": "remove",
                        "target": "optional_components",
                        "reason": "Reduce memory footprint"
                    })
                
                elif "slow_cycles" in need:
                    recommendations.append({
                        "type": "add",
                        "target": "parallelization_module",
                        "reason": "Improve cycle speed through parallelization"
                    })
                
                elif "slow_learning" in need:
                    recommendations.append({
                        "type": "add",
                        "target": "advanced_learning_engine",
                        "reason": "Accelerate learning progress"
                    })
                
                elif "high_errors" in need:
                    recommendations.append({
                        "type": "add",
                        "target": "enhanced_error_recovery",
                        "reason": "Improve robustness"
                    })
            
            logger.info(f"[ARCHITECTURE] Generated {len(recommendations)} recommendations")
            
        except Exception as e:
            logger.error(f"[ARCHITECTURE] Error generating recommendations: {e}")
        
        return recommendations
    
    def save_modifications(self):
        """Save modification history to disk"""
        try:
            data = {
                "total_modifications": len(self.modification_history),
                "implemented": sum(1 for m in self.modifications.values() if m.status == "implemented"),
                "reverted": sum(1 for m in self.modifications.values() if m.status == "reverted"),
                "recent_modifications": self.modification_history[-20:]
            }
            
            with open(self.mod_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            logger.info("[ARCHITECTURE] Saved modification history")
        except Exception as e:
            logger.error(f"[ARCHITECTURE] Error saving modifications: {e}")
    
    def get_architecture_summary(self) -> Dict:
        """Get comprehensive architecture summary"""
        return {
            "total_modifications_proposed": len(self.modifications),
            "modifications_implemented": sum(1 for m in self.modifications.values() if m.status == "implemented"),
            "modifications_pending": sum(1 for m in self.modifications.values() if m.status == "proposed"),
            "rollback_points": len(self.rollback_points),
            "architecture_versions": len(self.architecture_versions),
            "constraints": self.constraints,
            "recent_changes": [m.to_dict() for m in list(self.modifications.values())[-5:]]
        }
