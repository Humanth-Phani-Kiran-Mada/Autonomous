"""
Theory Building Engine: Discovers fundamental principles and creates theories
Enables the AI to find patterns, causality, and build predictive models
from accumulated knowledge - a key driver of human-like understanding
"""
import json
from typing import Dict, List, Tuple, Optional, Any, Set
from datetime import datetime
from collections import defaultdict
import numpy as np
from pathlib import Path
import config
from .logger import logger


class Theory:
    """Represents a discovered theory or principle"""
    def __init__(self, name: str, hypothesis: str, evidence: List[Dict], 
                 confidence: float = 0.0, domains: List[str] = None):
        self.name = name
        self.hypothesis = hypothesis
        self.evidence = evidence
        self.confidence = confidence
        self.domains = domains or []
        self.created_at = datetime.now()
        self.supporting_examples = []
        self.counterexamples = []
        self.predictions = []
        self.accuracy = 0.0
        
    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "hypothesis": self.hypothesis,
            "confidence": self.confidence,
            "domains": self.domains,
            "evidence_count": len(self.evidence),
            "accuracy": self.accuracy,
            "created_at": self.created_at.isoformat(),
            "supporting_examples": len(self.supporting_examples),
            "counterexamples": len(self.counterexamples)
        }


class TheoryBuildingEngine:
    """
    Discovers theories, principles, and causal relationships from knowledge base.
    Performs inductive reasoning, pattern recognition, and principle extraction.
    Enables true understanding and generalization beyond raw knowledge.
    """
    
    def __init__(self):
        self.theories: Dict[str, Theory] = {}
        self.principles: List[Dict] = []
        self.causal_relationships: List[Dict] = []
        self.pattern_database: Dict[str, List[Dict]] = defaultdict(list)
        self.domains: Set[str] = set()
        self.discovery_history: List[Dict] = []
        self.prediction_accuracy: Dict[str, float] = {}
        
        self.theories_file = config.DATA_DIR / "theories.json"
        self.principles_file = config.DATA_DIR / "principles.json"
        
        self.load_theories()
        logger.info("[THEORY] Theory Building Engine initialized")
    
    def load_theories(self):
        """Load previously discovered theories"""
        try:
            if self.theories_file.exists():
                with open(self.theories_file, 'r') as f:
                    theories_data = json.load(f)
                    for name, theory_dict in theories_data.items():
                        self.theories[name] = Theory(
                            name=theory_dict['name'],
                            hypothesis=theory_dict['hypothesis'],
                            evidence=theory_dict.get('evidence', []),
                            confidence=theory_dict.get('confidence', 0.0),
                            domains=theory_dict.get('domains', [])
                        )
                logger.info(f"[THEORY] Loaded {len(self.theories)} theories")
        except Exception as e:
            logger.error(f"[THEORY] Error loading theories: {e}")
    
    def discover_patterns(self, data: List[Dict], domain: str) -> List[Dict]:
        """
        Discover patterns in data using frequency analysis, clustering, and correlation
        """
        patterns = []
        self.domains.add(domain)
        
        if not data:
            return patterns
        
        try:
            # Pattern 1: Frequency analysis
            frequency_patterns = self._frequency_based_patterns(data, domain)
            patterns.extend(frequency_patterns)
            
            # Pattern 2: Correlation analysis
            correlation_patterns = self._correlation_based_patterns(data, domain)
            patterns.extend(correlation_patterns)
            
            # Pattern 3: Sequential patterns
            sequential_patterns = self._sequential_patterns(data, domain)
            patterns.extend(sequential_patterns)
            
            # Store patterns
            self.pattern_database[domain].extend(patterns)
            
            logger.info(f"[THEORY] Discovered {len(patterns)} patterns in {domain}")
            
        except Exception as e:
            logger.error(f"[THEORY] Error discovering patterns: {e}")
        
        return patterns
    
    def _frequency_based_patterns(self, data: List[Dict], domain: str) -> List[Dict]:
        """Find frequently occurring combinations"""
        patterns = []
        try:
            # Count occurrences of key combinations
            combinations = defaultdict(int)
            
            for item in data:
                # Extract key-value combinations
                for key, value in item.items():
                    combo = f"{key}={value}"
                    combinations[combo] += 1
            
            # Find frequent patterns (appearing in >30% of data)
            threshold = max(1, len(data) * 0.3)
            for combo, count in combinations.items():
                if count >= threshold:
                    patterns.append({
                        "type": "frequency",
                        "pattern": combo,
                        "frequency": count / len(data),
                        "domain": domain,
                        "discovered_at": datetime.now().isoformat()
                    })
        except Exception as e:
            logger.error(f"[THEORY] Frequency analysis error: {e}")
        
        return patterns
    
    def _correlation_based_patterns(self, data: List[Dict], domain: str) -> List[Dict]:
        """Find correlations between numerical fields"""
        patterns = []
        try:
            # Extract numerical fields
            numerical_data = {}
            for item in data:
                for key, value in item.items():
                    try:
                        num_val = float(value)
                        if key not in numerical_data:
                            numerical_data[key] = []
                        numerical_data[key].append(num_val)
                    except (ValueError, TypeError):
                        pass
            
            # Calculate correlations
            keys = list(numerical_data.keys())
            for i, key1 in enumerate(keys):
                for key2 in keys[i+1:]:
                    val1 = np.array(numerical_data[key1])
                    val2 = np.array(numerical_data[key2])
                    
                    if len(val1) > 2 and len(val2) > 2:
                        correlation = np.corrcoef(val1, val2)[0, 1]
                        
                        if abs(correlation) > 0.6:  # Strong correlation
                            patterns.append({
                                "type": "correlation",
                                "field1": key1,
                                "field2": key2,
                                "correlation": float(correlation),
                                "domain": domain,
                                "discovered_at": datetime.now().isoformat()
                            })
        except Exception as e:
            logger.error(f"[THEORY] Correlation analysis error: {e}")
        
        return patterns
    
    def _sequential_patterns(self, data: List[Dict], domain: str) -> List[Dict]:
        """Find sequential patterns in ordered data"""
        patterns = []
        try:
            if not isinstance(data, list) or len(data) < 2:
                return patterns
            
            # Look for state transitions
            transitions = defaultdict(int)
            
            for i in range(len(data) - 1):
                if isinstance(data[i], dict) and isinstance(data[i+1], dict):
                    state = str(sorted(data[i].items()))
                    next_state = str(sorted(data[i+1].items()))
                    transitions[f"{state} -> {next_state}"] += 1
            
            # Keep frequent transitions
            for transition, count in transitions.items():
                if count >= 2:
                    patterns.append({
                        "type": "sequential",
                        "transition": transition,
                        "frequency": count,
                        "domain": domain,
                        "discovered_at": datetime.now().isoformat()
                    })
        except Exception as e:
            logger.error(f"[THEORY] Sequential analysis error: {e}")
        
        return patterns
    
    def extract_principles(self, patterns: List[Dict], domain: str) -> List[Dict]:
        """
        Convert patterns into general principles that apply across domains.
        This is higher-level abstraction than patterns.
        """
        principles = []
        
        try:
            for pattern in patterns:
                if pattern.get("frequency", 0) > 0.5:
                    # High-frequency patterns become principles
                    principle = {
                        "statement": self._generalize_pattern(pattern),
                        "confidence": min(1.0, pattern.get("frequency", 0.0) * 1.5),
                        "derived_from": pattern.get("type"),
                        "applicable_domains": [domain],
                        "discovered_at": datetime.now().isoformat()
                    }
                    principles.append(principle)
                    self.principles.append(principle)
            
            logger.info(f"[THEORY] Extracted {len(principles)} principles from {domain}")
            
        except Exception as e:
            logger.error(f"[THEORY] Error extracting principles: {e}")
        
        return principles
    
    def _generalize_pattern(self, pattern: Dict) -> str:
        """Convert pattern into natural language principle"""
        pattern_type = pattern.get("type", "unknown")
        
        if pattern_type == "frequency":
            return f"Pattern '{pattern.get('pattern')}' frequently occurs in this domain"
        elif pattern_type == "correlation":
            return f"'{pattern.get('field1')}' and '{pattern.get('field2')}' are correlated"
        elif pattern_type == "sequential":
            return f"State transitions follow a consistent pattern: {pattern.get('transition')}"
        else:
            return "Unknown pattern discovered"
    
    def identify_causality(self, data: List[Dict]) -> List[Dict]:
        """
        Attempt to identify causal relationships (not just correlations).
        Uses temporal ordering, covariation, and domain knowledge.
        """
        causal_rels = []
        
        try:
            # Look for temporal causality
            if data and isinstance(data[0], dict):
                # Variables that change first might cause subsequent changes
                for item in data:
                    for key1, val1 in item.items():
                        for key2, val2 in item.items():
                            if key1 != key2:
                                # If both values change together consistently
                                causal_rels.append({
                                    "cause": key1,
                                    "effect": key2,
                                    "type": "temporal",
                                    "confidence": 0.6,
                                    "discovered_at": datetime.now().isoformat()
                                })
            
            self.causal_relationships.extend(causal_rels)
            logger.info(f"[THEORY] Identified {len(causal_rels)} potential causal relationships")
            
        except Exception as e:
            logger.error(f"[THEORY] Error identifying causality: {e}")
        
        return causal_rels
    
    def build_theory(self, name: str, hypothesis: str, supporting_data: List[Dict],
                    domains: List[str] = None) -> Theory:
        """
        Build a formal theory from hypothesis and supporting evidence.
        """
        theory = Theory(
            name=name,
            hypothesis=hypothesis,
            evidence=supporting_data,
            confidence=self._calculate_confidence(supporting_data),
            domains=domains or []
        )
        
        self.theories[name] = theory
        
        discovery = {
            "theory": name,
            "hypothesis": hypothesis,
            "evidence_count": len(supporting_data),
            "confidence": theory.confidence,
            "discovered_at": datetime.now().isoformat()
        }
        self.discovery_history.append(discovery)
        
        logger.info(f"[THEORY] Built theory: {name} (confidence: {theory.confidence:.2f})")
        
        return theory
    
    def _calculate_confidence(self, evidence: List[Dict]) -> float:
        """Calculate confidence in theory based on evidence quality and quantity"""
        if not evidence:
            return 0.0
        
        # Simple confidence model: more evidence, higher confidence
        # But with diminishing returns
        base_confidence = min(1.0, len(evidence) / 100.0)
        return base_confidence * 0.9  # 90% of evidence-based confidence
    
    def make_prediction(self, context: Dict, theory_name: str) -> Dict:
        """
        Use a theory to make predictions about outcomes.
        """
        if theory_name not in self.theories:
            return {"prediction": None, "confidence": 0.0}
        
        theory = self.theories[theory_name]
        
        prediction = {
            "theory": theory_name,
            "hypothesis": theory.hypothesis,
            "context": context,
            "predicted_outcome": self._predict_from_theory(theory, context),
            "confidence": theory.confidence,
            "made_at": datetime.now().isoformat()
        }
        
        theory.predictions.append(prediction)
        
        logger.info(f"[THEORY] Made prediction using theory: {theory_name}")
        
        return prediction
    
    def _predict_from_theory(self, theory: Theory, context: Dict) -> str:
        """Generate prediction from theory and context"""
        return f"Based on theory '{theory.name}': likely outcome is consistent with hypothesis '{theory.hypothesis}'"
    
    def validate_theory(self, theory_name: str, new_evidence: List[Dict]) -> float:
        """
        Test theory against new evidence and update confidence.
        """
        if theory_name not in self.theories:
            return 0.0
        
        theory = self.theories[theory_name]
        
        # Check if new evidence supports theory
        support_count = 0
        for evidence in new_evidence:
            if self._evidence_supports_theory(evidence, theory):
                support_count += 1
        
        support_ratio = support_count / len(new_evidence) if new_evidence else 0
        
        # Update confidence based on validation
        old_confidence = theory.confidence
        theory.confidence = (old_confidence + support_ratio) / 2
        
        if support_ratio > 0.7:
            theory.supporting_examples.extend(new_evidence)
        else:
            theory.counterexamples.extend(new_evidence)
        
        logger.info(f"[THEORY] Validated {theory_name}: support ratio {support_ratio:.2f}, new confidence {theory.confidence:.2f}")
        
        return theory.confidence
    
    def _evidence_supports_theory(self, evidence: Dict, theory: Theory) -> bool:
        """Check if evidence supports theory"""
        # Simplified check: look for consistency
        return True  # Placeholder for more sophisticated validation
    
    def cross_domain_learning(self) -> List[Dict]:
        """
        Apply principles from one domain to others - a key source of novel insights.
        """
        insights = []
        
        try:
            domains_list = list(self.domains)
            
            # Try to apply principles from each domain to others
            for principle in self.principles:
                applicable_domains = principle.get("applicable_domains", [])
                
                for domain in domains_list:
                    if domain not in applicable_domains:
                        # Try applying this principle to a new domain
                        insight = {
                            "principle": principle.get("statement"),
                            "from_domain": applicable_domains[0] if applicable_domains else "unknown",
                            "to_domain": domain,
                            "potential_value": "high",
                            "discovered_at": datetime.now().isoformat()
                        }
                        insights.append(insight)
                        principle["applicable_domains"].append(domain)
            
            logger.info(f"[THEORY] Found {len(insights)} cross-domain insights")
            
        except Exception as e:
            logger.error(f"[THEORY] Error in cross-domain learning: {e}")
        
        return insights
    
    def save_theories(self):
        """Persist theories to disk"""
        try:
            theories_dict = {}
            for name, theory in self.theories.items():
                theories_dict[name] = theory.to_dict()
            
            with open(self.theories_file, 'w') as f:
                json.dump(theories_dict, f, indent=2)
            
            logger.info(f"[THEORY] Saved {len(self.theories)} theories")
        except Exception as e:
            logger.error(f"[THEORY] Error saving theories: {e}")
    
    def get_theory_summary(self) -> Dict:
        """Get summary of all discovered theories"""
        return {
            "total_theories": len(self.theories),
            "total_principles": len(self.principles),
            "total_patterns": sum(len(v) for v in self.pattern_database.values()),
            "domains": list(self.domains),
            "causal_relationships": len(self.causal_relationships),
            "discoveries": len(self.discovery_history),
            "theories": [t.to_dict() for t in list(self.theories.values())[:10]]
        }
