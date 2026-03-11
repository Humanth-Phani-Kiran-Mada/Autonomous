"""
Bayesian Reasoning Core: Probabilistic reasoning with uncertainty management
Enables principled reasoning under uncertainty and belief updating
"""
import json
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import numpy as np
from pathlib import Path
import config
from .logger import logger


class BayesianReasoner:
    """
    Implements Bayesian inference for reasoning with uncertainty.
    Maintains beliefs as probability distributions and updates them based on evidence.
    """
    
    def __init__(self):
        self.beliefs: Dict[str, Dict] = {}
        self.evidence_log: List[Dict] = []
        self.inference_history: List[Dict] = []
        self.prior_knowledge: Dict[str, float] = {}
        self.conditional_probabilities: Dict[str, Dict] = {}
        
        self.beliefs_file = config.DATA_DIR / "bayesian_beliefs.json"
        self.evidence_file = config.DATA_DIR / "evidence_log.json"
        
        self._initialize_base_beliefs()
        self.load_beliefs()
        logger.info("🎯 Bayesian Reasoning Core initialized")
    
    def _initialize_base_beliefs(self):
        """Initialize base beliefs about the world and AI capabilities"""
        self.prior_knowledge = {
            "knowledge_acquisition_effectiveness": 0.5,
            "learning_capability": 0.5,
            "reasoning_reliability": 0.5,
            "skill_improvement_rate": 0.5,
            "task_success_probability": 0.5,
            "error_recovery_capability": 0.5
        }
    
    def load_beliefs(self):
        """Load Bayesian beliefs from disk"""
        try:
            if self.beliefs_file.exists():
                with open(self.beliefs_file, 'r') as f:
                    data = json.load(f)
                    self.beliefs = data.get("beliefs", {})
                    self.prior_knowledge.update(data.get("prior_knowledge", {}))
            logger.info("📂 Bayesian beliefs loaded")
        except Exception as e:
            logger.error(f"Error loading beliefs: {e}")
    
    def save_beliefs(self):
        """Persist Bayesian beliefs"""
        try:
            beliefs_data = {
                "beliefs": self.beliefs,
                "prior_knowledge": self.prior_knowledge,
                "saved_at": datetime.now().isoformat()
            }
            with open(self.beliefs_file, 'w') as f:
                json.dump(beliefs_data, f, indent=2)
            logger.debug("💾 Bayesian beliefs saved")
        except Exception as e:
            logger.error(f"Error saving beliefs: {e}")
    
    def set_belief(self, belief_name: str, mean: float, variance: float = 0.01,
                  description: str = ""):
        """Set a belief with Bayesian parameters (mean and variance)"""
        self.beliefs[belief_name] = {
            "name": belief_name,
            "description": description,
            "mean": min(max(mean, 0), 1),
            "variance": min(max(variance, 0.001), 0.25),
            "confidence": 1 - variance,
            "last_updated": datetime.now().isoformat(),
            "evidence_count": 0,
            "updates_count": 0
        }
        logger.info(f"📌 Belief set: {belief_name} = {mean:.3f} ± {np.sqrt(variance):.3f}")
    
    def update_belief_bayesian(self, belief_name: str, observation: float, 
                              likelihood: float = 0.8, importance: float = 1.0):
        """Update belief using Bayesian inference (posterior = prior × likelihood)"""
        if belief_name not in self.beliefs:
            self.set_belief(belief_name, 0.5)
        
        belief = self.beliefs[belief_name]
        
        # Get prior
        prior_mean = belief["mean"]
        prior_variance = belief["variance"]
        
        # Calculate likelihood based on observation
        observation_variance = (1.0 - likelihood) ** 2
        
        # Bayesian update: posterior = (prior + likelihood-weighted observation)
        posterior_variance = 1 / (1/prior_variance + 1/observation_variance)
        posterior_mean = posterior_variance * (prior_mean/prior_variance + observation/observation_variance)
        
        # Apply importance weighting
        belief["mean"] = prior_mean * (1 - importance) + posterior_mean * importance
        belief["variance"] = min(posterior_variance, 0.25)
        belief["confidence"] = 1 - belief["variance"]
        belief["evidence_count"] += 1
        belief["updates_count"] += 1
        belief["last_updated"] = datetime.now().isoformat()
        
        # Log evidence
        evidence_record = {
            "timestamp": datetime.now().isoformat(),
            "belief": belief_name,
            "observation": observation,
            "likelihood": likelihood,
            "prior_mean": prior_mean,
            "posterior_mean": belief["mean"],
            "posterior_variance": belief["variance"]
        }
        self.evidence_log.append(evidence_record)
        
        logger.debug(f"🔄 Belief updated: {belief_name} {prior_mean:.3f} → {belief['mean']:.3f}")
    
    def get_belief_probability(self, belief_name: str, threshold: float = None) -> Tuple[float, float]:
        """Get probability estimate and confidence for a belief"""
        if belief_name not in self.beliefs:
            return 0.5, 0.0
        
        belief = self.beliefs[belief_name]
        mean = belief["mean"]
        confidence = belief["confidence"]
        
        if threshold and mean < threshold:
            uncertainty = np.sqrt(belief["variance"])
            probability_below_threshold = self._normal_cdf(threshold, mean, uncertainty)
            return probability_below_threshold, confidence
        
        return mean, confidence
    
    def _normal_cdf(self, x: float, mean: float, std: float) -> float:
        """Calculate CDF of normal distribution"""
        return 0.5 * (1 + np.tanh((x - mean) / (std * np.sqrt(2/np.pi))))
    
    def reason_about(self, subject: str, context: Dict = None, evidence: List[Dict] = None) -> Dict:
        """Perform Bayesian reasoning about a subject"""
        if evidence is None:
            evidence = []
        
        logger.info(f"🧠 Bayesian reasoning about: {subject}")
        
        reasoning = {
            "subject": subject,
            "timestamp": datetime.now().isoformat(),
            "context": context or {},
            "prior_probability": self.prior_knowledge.get(subject, 0.5),
            "posterior_probability": 0.5,
            "confidence": 0.0,
            "evidence_processed": len(evidence),
            "inference_chain": []
        }
        
        # Start with prior
        posterior = reasoning["prior_probability"]
        
        # Update with evidence
        for evidence_item in evidence:
            # Likelihoods P(E|H) and P(E|¬H)
            likelihood_h = evidence_item.get("likelihood_true", 0.7)  # P(E|H)
            likelihood_not_h = evidence_item.get("likelihood_false", 0.3)  # P(E|¬H)
            
            # Bayes' rule: P(H|E) = P(E|H) * P(H) / P(E)
            p_evidence = likelihood_h * posterior + likelihood_not_h * (1 - posterior)
            
            posterior = (likelihood_h * posterior) / max(p_evidence, 0.001)
            
            reasoning["inference_chain"].append({
                "evidence": evidence_item.get("description", ""),
                "likelihood_true": likelihood_h,
                "posterior": posterior
            })
        
        reasoning["posterior_probability"] = posterior
        reasoning["confidence"] = self._calculate_confidence(len(evidence), 
                                                            reasoning["prior_probability"],
                                                            posterior)
        
        self.inference_history.append(reasoning)
        logger.info(f"✅ Reasoning complete: P({subject}) = {posterior:.2%} ± {1-reasoning['confidence']:.2%}")
        
        return reasoning
    
    def _calculate_confidence(self, evidence_count: int, prior: float, posterior: float) -> float:
        """Calculate confidence in inference"""
        # More evidence = higher confidence
        evidence_confidence = min(evidence_count / 10, 1.0)
        
        # Less change from prior = higher confidence
        stability = 1 - abs(posterior - prior)
        
        return evidence_confidence * 0.6 + stability * 0.4
    
    def predict_outcome(self, action: str, context: Dict, 
                       historical_success_rate: float = 0.5) -> Dict:
        """Predict outcome probability using Bayesian network"""
        logger.info(f"🔮 Predicting outcome for: {action}")
        
        # Gather relevant beliefs
        relevant_beliefs = self._find_relevant_beliefs(action, context)
        
        # Calculate likelihood components
        success_likelihood = historical_success_rate
        
        # Adjust based on context
        for belief_name, weight in relevant_beliefs.items():
            belief_prob, confidence = self.get_belief_probability(belief_name)
            success_likelihood += belief_prob * weight * confidence
        
        success_likelihood = min(success_likelihood / (1 + len(relevant_beliefs)), 1.0)
        
        prediction = {
            "action": action,
            "context": context,
            "timestamp": datetime.now().isoformat(),
            "predicted_success_probability": success_likelihood,
            "predicted_failure_probability": 1 - success_likelihood,
            "contributing_beliefs": relevant_beliefs,
            "confidence": min(len(relevant_beliefs) / 5, 1.0) if relevant_beliefs else 0.5
        }
        
        logger.info(f"✅ Prediction: {action} success probability = {success_likelihood:.2%}")
        
        return prediction
    
    def _find_relevant_beliefs(self, action: str, context: Dict) -> Dict:
        """Find beliefs relevant to an action"""
        relevant = {}
        
        # Match beliefs based on keywords
        action_lower = action.lower()
        
        for belief_name in self.beliefs.keys():
            if any(keyword in action_lower for keyword in belief_name.split('_')):
                relevant[belief_name] = 0.1  # Base weight
        
        # Add context-specific beliefs
        for ctx_key, ctx_val in context.items():
            for belief_name in self.beliefs.keys():
                if ctx_key in belief_name:
                    relevant[belief_name] = min(relevant.get(belief_name, 0) + 0.15, 1.0)
        
        return relevant
    
    def calculate_posterior_interval(self, belief_name: str, 
                                    confidence_level: float = 0.95) -> Tuple[float, float]:
        """Calculate credible interval for a belief estimate"""
        if belief_name not in self.beliefs:
            return (0.0, 1.0)
        
        belief = self.beliefs[belief_name]
        mean = belief["mean"]
        std = np.sqrt(belief["variance"])
        
        # Use z-score for credible interval
        z_score = 1.96 if confidence_level == 0.95 else 2.576
        
        lower = max(mean - z_score * std, 0)
        upper = min(mean + z_score * std, 1)
        
        return (lower, upper)
    
    def decision_analysis(self, options: List[Dict], criteria: Dict) -> Dict:
        """Bayesian decision analysis for comparing options"""
        logger.info(f"⚖️ Making Bayesian decision among {len(options)} options")
        
        weighted_utilities = {}
        
        for option in options:
            option_id = option.get("id", len(weighted_utilities))
            utility = 0.0
            
            # Calculate expected utility for each criterion
            for criterion, weight in criteria.items():
                # Get probability of this option satisfying the criterion
                criterion_prob = option.get(f"{criterion}_probability", 0.5)
                criterion_value = option.get(f"{criterion}_value", 1.0)
                
                # Expected value = probability × value × weight
                utility += criterion_prob * criterion_value * weight
            
            weighted_utilities[option_id] = utility
        
        # Find best option
        best_option_id = max(weighted_utilities.items(), key=lambda x: x[1])[0]
        best_utility = weighted_utilities[best_option_id]
        
        decision = {
            "timestamp": datetime.now().isoformat(),
            "options_analyzed": len(options),
            "options_utilities": weighted_utilities,
            "selected_option_id": best_option_id,
            "selected_utility": best_utility,
            "confidence": min(best_utility, 1.0)
        }
        
        logger.info(f"✅ Decision: Option {best_option_id} (utility={best_utility:.2%})")
        
        return decision
    
    def get_bayesian_summary(self) -> Dict:
        """Get comprehensive Bayesian reasoning summary"""
        return {
            "beliefs_count": len(self.beliefs),
            "evidence_count": len(self.evidence_log),
            "inferences_made": len(self.inference_history),
            "average_belief_confidence": np.mean([b["confidence"] for b in self.beliefs.values()]) if self.beliefs else 0,
            "prior_knowledge": self.prior_knowledge,
            "most_confident_beliefs": sorted(
                [(name, b["confidence"]) for name, b in self.beliefs.items()],
                key=lambda x: x[1],
                reverse=True
            )[:5]
        }
