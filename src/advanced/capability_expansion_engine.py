"""
Capability Expansion Engine: Dynamically create entirely new capabilities
by composing existing skills and discovering emergent abilities.
Enables continuous self-improvement and acquisition of novel skills.
"""
import json
from typing import Dict, List, Tuple, Optional, Any, Callable
from datetime import datetime
from collections import defaultdict
import numpy as np
from pathlib import Path
import config
from .logger import logger


class CapabilityComposition:
    """Represents a capability created by composing existing ones"""
    def __init__(self, capability_id: str, name: str, description: str,
                 base_capabilities: List[str]):
        self.capability_id = capability_id
        self.name = name
        self.description = description
        self.base_capabilities = base_capabilities
        self.proficiency = 0.0
        self.effectiveness = 0.0
        self.successful_uses = 0
        self.failed_uses = 0
        self.created_at = datetime.now()
        self.applications = []
        self.improvement_potential = 1.0
        
    def to_dict(self) -> Dict:
        return {
            "capability_id": self.capability_id,
            "name": self.name,
            "description": self.description,
            "base_capabilities": self.base_capabilities,
            "proficiency": self.proficiency,
            "effectiveness": self.effectiveness,
            "total_uses": self.successful_uses + self.failed_uses
        }


class CapabilityExpansionEngine:
    """
    Dynamically discovers and creates new capabilities by combining
    existing skills in novel ways. Key mechanism for continuous improvement
    and reaching capabilities beyond initial design.
    """
    
    def __init__(self):
        self.base_capabilities: Dict[str, Dict] = {}
        self.composed_capabilities: Dict[str, CapabilityComposition] = {}
        self.capability_interactions: List[Dict] = []
        self.expansion_history: List[Dict] = []
        self.novelty_database: List[Dict] = []
        self.skill_combinations: List[Dict] = []
        self.emergence_events: List[Dict] = []
        
        self.capabilities_file = config.DATA_DIR / "capabilities.json"
        self.load_capabilities()
        
        logger.info("[EXPANSION] Capability Expansion Engine initialized")
    
    def load_capabilities(self):
        """Load previously discovered capabilities"""
        try:
            if self.capabilities_file.exists():
                with open(self.capabilities_file, 'r') as f:
                    data = json.load(f)
                    self.base_capabilities = data.get("base", {})
                    logger.info(f"[EXPANSION] Loaded {len(self.base_capabilities)} base capabilities")
        except Exception as e:
            logger.error(f"[EXPANSION] Error loading capabilities: {e}")
    
    def register_base_capability(self, capability_name: str, description: str,
                                 performance_level: float = 0.5, 
                                 domains: List[str] = None):
        """Register a base capability available to the system"""
        self.base_capabilities[capability_name] = {
            "name": capability_name,
            "description": description,
            "performance_level": performance_level,
            "domains": domains or [],
            "registered_at": datetime.now().isoformat(),
            "use_count": 0,
            "success_rate": 0.5
        }
        
        logger.info(f"[EXPANSION] Registered base capability: {capability_name}")
    
    def discover_capability_combinations(self) -> List[Dict]:
        """
        Systematically search for interesting combinations of base capabilities.
        Some combinations may create emergent new abilities.
        """
        combinations = []
        
        try:
            capability_names = list(self.base_capabilities.keys())
            
            # Try all pairs and some triples
            for i, cap1 in enumerate(capability_names):
                for cap2 in capability_names[i+1:]:
                    # Check if this pair creates synergy
                    synergy = self._evaluate_combination_synergy(cap1, cap2)
                    
                    if synergy > 0.6:
                        combination = {
                            "capability_1": cap1,
                            "capability_2": cap2,
                            "synergy": synergy,
                            "potential_emergent_ability": self._name_combination(cap1, cap2),
                            "discovered_at": datetime.now().isoformat()
                        }
                        combinations.append(combination)
                        self.capability_interactions.append(combination)
            
            logger.info(f"[EXPANSION] Discovered {len(combinations)} capability combinations with synergy")
            
        except Exception as e:
            logger.error(f"[EXPANSION] Error discovering combinations: {e}")
        
        return combinations
    
    def _evaluate_combination_synergy(self, cap1: str, cap2: str) -> float:
        """
        Evaluate how well two capabilities work together.
        High synergy means the combination creates emergent ability.
        """
        synergy = 0.0
        
        try:
            base1 = self.base_capabilities.get(cap1, {})
            base2 = self.base_capabilities.get(cap2, {})
            
            # Metric 1: Domain overlap
            domains1 = set(base1.get("domains", []))
            domains2 = set(base2.get("domains", []))
            
            if domains1 and domains2:
                overlap = len(domains1.intersection(domains2))
                union = len(domains1.union(domains2))
                domain_synergy = overlap / union if union > 0 else 0.3
                synergy += domain_synergy * 0.4
            
            # Metric 2: Complementary capabilities
            # Different capabilities that work together are high synergy
            if not domains1 or not domains2:
                synergy += 0.2  # Likely complementary
            
            # Metric 3: Performance compatibility
            perf1 = base1.get("performance_level", 0.5)
            perf2 = base2.get("performance_level", 0.5)
            
            # Similar performance levels can work well together
            perf_synergy = 1.0 - abs(perf1 - perf2)
            synergy += perf_synergy * 0.3
            
            # Metric 4: Combined use count (used together = good combination)
            use1 = base1.get("use_count", 0)
            use2 = base2.get("use_count", 0)
            combined_use = min(use1, use2)
            combined_synergy = min(1.0, combined_use / 10.0)
            synergy += combined_synergy * 0.3
            
            synergy = min(1.0, synergy)
            
        except Exception as e:
            logger.error(f"[EXPANSION] Error evaluating synergy: {e}")
        
        return synergy
    
    def _name_combination(self, cap1: str, cap2: str) -> str:
        """Generate name for composite capability"""
        return f"Combined_{cap1}_{cap2}".replace(" ", "_")
    
    def create_composite_capability(self, name: str, description: str,
                                   base_caps: List[str]) -> CapabilityComposition:
        """
        Create a new capability by composing existing base capabilities.
        """
        cap_id = f"comp_{datetime.now().timestamp()}"
        composition = CapabilityComposition(cap_id, name, description, base_caps)
        
        # Initialize proficiency based on base capability levels
        base_proficiencies = []
        for base_cap in base_caps:
            if base_cap in self.base_capabilities:
                perf = self.base_capabilities[base_cap].get("performance_level", 0.5)
                base_proficiencies.append(perf)
        
        if base_proficiencies:
            # Composition proficiency is average of base capabilities (can improve with use)
            composition.proficiency = np.mean(base_proficiencies) * 0.9  # 90% initially
        
        self.composed_capabilities[cap_id] = composition
        
        expansion_record = {
            "capability_id": cap_id,
            "name": name,
            "base_capabilities": base_caps,
            "initial_proficiency": composition.proficiency,
            "created_at": datetime.now().isoformat()
        }
        self.expansion_history.append(expansion_record)
        
        logger.info(f"[EXPANSION] Created composite capability: {name}")
        
        return composition
    
    def detect_emergent_capability(self, observed_behavior: str,
                                  required_bases: List[str]) -> Optional[Dict]:
        """
        Detect when a new capability emerges from combination of others.
        Emergence happens when combined ability > sum of parts.
        """
        # Check if this emergent behavior exceeds what base capabilities could do
        base_combined_performance = []
        for base_cap in required_bases:
            if base_cap in self.base_capabilities:
                perf = self.base_capabilities[base_cap].get("performance_level", 0.5)
                base_combined_performance.append(perf)
        
        expected_performance = np.mean(base_combined_performance) if base_combined_performance else 0.5
        
        # If observed behavior performs better than expected, it's emergent
        if 0.8 > expected_performance:  # Arbitrary threshold
            emergence = {
                "emergent_behavior": observed_behavior,
                "required_bases": required_bases,
                "emergence_strength": 0.8 - expected_performance,
                "discovered_at": datetime.now().isoformat()
            }
            self.emergence_events.append(emergence)
            
            logger.info(f"[EXPANSION] Detected emergent capability: {observed_behavior}")
            
            return emergence
        
        return None
    
    def expand_capability(self, capability_id: str, improvement_factor: float = 1.1) -> float:
        """
        Expand existing capability through practice and optimization.
        Returns new proficiency level.
        """
        if capability_id not in self.composed_capabilities:
            return 0.0
        
        capability = self.composed_capabilities[capability_id]
        
        # Proficiency improvement with diminishing returns
        old_proficiency = capability.proficiency
        new_proficiency = min(1.0, old_proficiency + (1.0 - old_proficiency) * 0.1 * improvement_factor)
        
        capability.proficiency = new_proficiency
        capability.improvement_potential *= 0.95  # Diminishing returns
        
        logger.info(f"[EXPANSION] Expanded capability {capability_id}: " +
                   f"{old_proficiency:.2f} -> {new_proficiency:.2f}")
        
        return new_proficiency
    
    def record_capability_use(self, capability_id: str, success: bool,
                             performance_score: float = 0.5):
        """Record use of a capability, update statistics"""
        if capability_id not in self.composed_capabilities:
            return
        
        capability = self.composed_capabilities[capability_id]
        
        if success:
            capability.successful_uses += 1
        else:
            capability.failed_uses += 1
        
        total_uses = capability.successful_uses + capability.failed_uses
        capability.effectiveness = capability.successful_uses / total_uses if total_uses > 0 else 0.0
        
        capability.applications.append({
            "success": success,
            "performance": performance_score,
            "timestamp": datetime.now().isoformat()
        })
        
        logger.debug(f"[EXPANSION] Recorded use of {capability_id}: "
                    f"effectiveness now {capability.effectiveness:.2f}")
    
    def find_capability_gaps(self, goals: List[str], 
                            existing_capabilities: List[str]) -> List[Dict]:
        """
        Identify what new capabilities would help achieve goals.
        Suggests which base capabilities to combine.
        """
        gaps = []
        
        try:
            # For each goal, check if existing capabilities are sufficient
            for goal in goals:
                gap = {
                    "goal": goal,
                    "existing_capabilities": existing_capabilities,
                    "suggested_new_capability": self._suggest_capability(goal),
                    "reason": "Needed for goal achievement",
                    "identified_at": datetime.now().isoformat()
                }
                gaps.append(gap)
            
            logger.info(f"[EXPANSION] Found {len(gaps)} capability gaps")
            
        except Exception as e:
            logger.error(f"[EXPANSION] Error finding gaps: {e}")
        
        return gaps
    
    def _suggest_capability(self, goal: str) -> str:
        """Suggest a new capability that would help achieve goal"""
        return f"Capability_for_{goal.replace(' ', '_')}"
    
    def explore_capability_space(self) -> List[Dict]:
        """
        Systematically explore the space of possible capabilities.
        Generates suggestions for new capabilities to acquire.
        """
        exploration_results = []
        
        try:
            # Strategy 1: Combine high-performing capabilities
            high_performers = [
                (name, cap["performance_level"]) 
                for name, cap in self.base_capabilities.items()
                if cap.get("performance_level", 0) > 0.7
            ]
            
            for i, (cap1_name, _) in enumerate(high_performers):
                for cap2_name, _ in high_performers[i+1:]:
                    exploration_results.append({
                        "exploration_type": "combine_strong",
                        "capability_1": cap1_name,
                        "capability_2": cap2_name,
                        "expected_value": "high"
                    })
            
            # Strategy 2: Combine weak capability with strong one (to improve weak)
            weak_performers = [name for name, cap in self.base_capabilities.items()
                             if cap.get("performance_level", 0) < 0.5]
            
            for weak_cap in weak_performers:
                best_strong = sorted(
                    [(name, cap["performance_level"]) 
                     for name, cap in self.base_capabilities.items()
                     if cap.get("performance_level", 0) > 0.7],
                    key=lambda x: x[1], reverse=True
                )
                
                if best_strong:
                    exploration_results.append({
                        "exploration_type": "improve_weak",
                        "weak_capability": weak_cap,
                        "strong_capability": best_strong[0][0],
                        "expected_value": "medium"
                    })
            
            logger.info(f"[EXPANSION] Explored capability space: {len(exploration_results)} candidates")
            
        except Exception as e:
            logger.error(f"[EXPANSION] Error exploring capability space: {e}")
        
        return exploration_results
    
    def save_capabilities(self):
        """Persist capabilities to disk"""
        try:
            data = {
                "base": self.base_capabilities,
                "composed": {cid: cap.to_dict() for cid, cap in self.composed_capabilities.items()}
            }
            
            with open(self.capabilities_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            logger.info(f"[EXPANSION] Saved {len(self.base_capabilities)} base + " +
                       f"{len(self.composed_capabilities)} composed capabilities")
        except Exception as e:
            logger.error(f"[EXPANSION] Error saving capabilities: {e}")
    
    def get_expansion_summary(self) -> Dict:
        """Get summary of capability expansion system"""
        return {
            "base_capabilities": len(self.base_capabilities),
            "composed_capabilities": len(self.composed_capabilities),
            "capability_interactions": len(self.capability_interactions),
            "emergence_events": len(self.emergence_events),
            "expansion_history_size": len(self.expansion_history),
            "avg_composed_proficiency": float(np.mean([c.proficiency for c in self.composed_capabilities.values()])) if self.composed_capabilities else 0.0
        }
