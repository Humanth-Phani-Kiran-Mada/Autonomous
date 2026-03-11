"""
Knowledge Synthesis Engine: Combines knowledge from multiple domains to create novel insights
Enables analogical reasoning, transfer learning, and emergent understanding
A key mechanism for achieving competitive intelligence
"""
import json
from typing import Dict, List, Tuple, Optional, Any, Set
from datetime import datetime
from collections import defaultdict
import numpy as np
from pathlib import Path
import config
from .logger import logger


class InsightNode:
    """Represents a synthesized insight"""
    def __init__(self, insight_id: str, description: str, source_domains: List[str],
                 confidence: float = 0.5):
        self.insight_id = insight_id
        self.description = description
        self.source_domains = source_domains
        self.confidence = confidence
        self.supporting_concepts = []
        self.applications = []
        self.created_at = datetime.now()
        self.validation_count = 0
        
    def to_dict(self) -> Dict:
        return {
            "insight_id": self.insight_id,
            "description": self.description,
            "source_domains": self.source_domains,
            "confidence": self.confidence,
            "validation_count": self.validation_count,
            "applications": len(self.applications)
        }


class KnowledgeSynthesisEngine:
    """
    Synthesizes knowledge from multiple domains to generate novel insights.
    Performs analogical reasoning, finds common principles, and creates
    emergent understanding that goes beyond individual domains.
    """
    
    def __init__(self):
        self.insights: Dict[str, InsightNode] = {}
        self.domain_knowledge: Dict[str, List[Dict]] = defaultdict(list)
        self.analogies: List[Dict] = []
        self.conceptual_bridges: List[Dict] = []
        self.emergent_theories: List[Dict] = []
        self.synthesis_history: List[Dict] = []
        self.novelty_scores: Dict[str, float] = {}
        
        self.insights_file = config.DATA_DIR / "insights.json"
        self.load_insights()
        
        logger.info("[SYNTHESIS] Knowledge Synthesis Engine initialized")
    
    def load_insights(self):
        """Load previously synthesized insights"""
        try:
            if self.insights_file.exists():
                with open(self.insights_file, 'r') as f:
                    insights_data = json.load(f)
                    logger.info(f"[SYNTHESIS] Loaded {len(insights_data)} insights")
        except Exception as e:
            logger.error(f"[SYNTHESIS] Error loading insights: {e}")
    
    def add_domain_knowledge(self, domain: str, concepts: List[Dict]):
        """Add knowledge from a domain for synthesis"""
        self.domain_knowledge[domain].extend(concepts)
        logger.info(f"[SYNTHESIS] Added {len(concepts)} concepts from domain: {domain}")
    
    def find_analogies(self, source_domain: str, target_domain: str) -> List[Dict]:
        """
        Find analogical relationships between domains.
        If source domain has principle X, target domain might have similar principle Y.
        """
        analogies = []
        
        try:
            source_concepts = self.domain_knowledge.get(source_domain, [])
            target_concepts = self.domain_knowledge.get(target_domain, [])
            
            if not source_concepts or not target_concepts:
                return analogies
            
            # Find structurally similar concepts
            for source_concept in source_concepts:
                for target_concept in target_concepts:
                    similarity = self._compute_concept_similarity(source_concept, target_concept)
                    
                    if similarity > 0.6:
                        analogy = {
                            "source_domain": source_domain,
                            "target_domain": target_domain,
                            "source_concept": source_concept.get("name", "unknown"),
                            "target_concept": target_concept.get("name", "unknown"),
                            "similarity": similarity,
                            "explanation": self._explain_analogy(source_concept, target_concept),
                            "discovered_at": datetime.now().isoformat()
                        }
                        analogies.append(analogy)
                        self.analogies.append(analogy)
            
            logger.info(f"[SYNTHESIS] Found {len(analogies)} analogies between {source_domain} and {target_domain}")
            
        except Exception as e:
            logger.error(f"[SYNTHESIS] Error finding analogies: {e}")
        
        return analogies
    
    def _compute_concept_similarity(self, concept1: Dict, concept2: Dict) -> float:
        """
        Compute similarity between two concepts using multiple metrics.
        """
        similarity = 0.0
        
        try:
            # Metric 1: Attribute overlap
            attrs1 = set(concept1.get("attributes", []))
            attrs2 = set(concept2.get("attributes", []))
            
            if attrs1 or attrs2:
                overlap = len(attrs1.intersection(attrs2))
                union = len(attrs1.union(attrs2))
                attr_similarity = overlap / union if union > 0 else 0
                similarity += attr_similarity * 0.4
            
            # Metric 2: Category similarity
            category1 = concept1.get("category", "")
            category2 = concept2.get("category", "")
            
            if category1 == category2:
                similarity += 0.3
            elif category1 and category2 and (category1 in category2 or category2 in category1):
                similarity += 0.15
            
            # Metric 3: Function/role similarity
            func1 = concept1.get("function", "")
            func2 = concept2.get("function", "")
            
            if func1 and func2 and func1 == func2:
                similarity += 0.3
            
            similarity = min(1.0, similarity)
            
        except Exception as e:
            logger.error(f"[SYNTHESIS] Error computing similarity: {e}")
        
        return similarity
    
    def _explain_analogy(self, source: Dict, target: Dict) -> str:
        """Generate natural language explanation of analogy"""
        source_name = source.get("name", "concept")
        target_name = target.get("name", "concept")
        source_domain_prop = source.get("category", "property")
        target_domain_prop = target.get("category", "property")
        
        return (f"'{source_name}' in source domain (a {source_domain_prop}) is analogous to "
                f"'{target_name}' in target domain (a {target_domain_prop})")
    
    def synthesize_from_analogies(self) -> List[Dict]:
        """
        Use analogies to generate novel insights.
        If domain A has principle P achieved through mechanism M,
        and domain B has analogous structure, maybe B can also use M to achieve similar results.
        """
        insights = []
        
        try:
            for analogy in self.analogies:
                source_domain = analogy.get("source_domain")
                target_domain = analogy.get("target_domain")
                
                insight = {
                    "type": "analogical_transfer",
                    "source_domain": source_domain,
                    "target_domain": target_domain,
                    "description": f"Principle from {source_domain} may apply to {target_domain}",
                    "confidence": analogy.get("similarity", 0.5),
                    "synthesized_at": datetime.now().isoformat()
                }
                insights.append(insight)
                self.emergent_theories.append(insight)
            
            logger.info(f"[SYNTHESIS] Synthesized {len(insights)} insights from analogies")
            
        except Exception as e:
            logger.error(f"[SYNTHESIS] Error synthesizing from analogies: {e}")
        
        return insights
    
    def find_conceptual_bridges(self, concept1: Dict, concept2: Dict) -> Dict:
        """
        Find conceptual bridges - intermediate concepts that connect two ideas.
        Enables transfer of learning across domains.
        """
        bridge = {
            "from_concept": concept1.get("name", "unknown"),
            "to_concept": concept2.get("name", "unknown"),
            "bridge_concepts": [],
            "bridge_strength": 0.0
        }
        
        try:
            # Find concepts that have properties of both
            all_concepts = []
            for domain_concepts in self.domain_knowledge.values():
                all_concepts.extend(domain_concepts)
            
            for middle_concept in all_concepts:
                # Check if it's similar to both endpoints
                sim1 = self._compute_concept_similarity(concept1, middle_concept)
                sim2 = self._compute_concept_similarity(concept2, middle_concept)
                
                avg_similarity = (sim1 + sim2) / 2
                
                if avg_similarity > 0.5:
                    bridge["bridge_concepts"].append({
                        "concept": middle_concept.get("name", "unknown"),
                        "similarity_to_start": sim1,
                        "similarity_to_end": sim2
                    })
            
            bridge["bridge_strength"] = min(1.0, len(bridge["bridge_concepts"]) * 0.2)
            self.conceptual_bridges.append(bridge)
            
            logger.info(f"[SYNTHESIS] Found bridge from {concept1.get('name')} to {concept2.get('name')}")
            
        except Exception as e:
            logger.error(f"[SYNTHESIS] Error finding conceptual bridge: {e}")
        
        return bridge
    
    def synthesize_insight(self, name: str, description: str, 
                          source_domains: List[str]) -> InsightNode:
        """
        Create a new synthesized insight combining knowledge from multiple domains.
        """
        insight_id = f"insight_{datetime.now().timestamp()}"
        insight = InsightNode(insight_id, description, source_domains)
        
        # Collect relevant concepts from source domains
        supporting_concepts = []
        for domain in source_domains:
            domain_concepts = self.domain_knowledge.get(domain, [])
            supporting_concepts.extend(domain_concepts[:3])  # Top 3 per domain
        
        insight.supporting_concepts = supporting_concepts
        
        self.insights[insight_id] = insight
        
        synthesis_record = {
            "insight_id": insight_id,
            "name": name,
            "description": description,
            "source_domains": source_domains,
            "domain_count": len(source_domains),
            "created_at": datetime.now().isoformat()
        }
        self.synthesis_history.append(synthesis_record)
        
        logger.info(f"[SYNTHESIS] Synthesized insight: {name}")
        
        return insight
    
    def cross_pollinate_knowledge(self) -> List[Dict]:
        """
        Transfer successful strategies from one domain to others.
        Returns list of potential transfers worth exploring.
        """
        transfers = []
        
        try:
            domains = list(self.domain_knowledge.keys())
            
            for i, domain1 in enumerate(domains):
                for domain2 in domains[i+1:]:
                    # Find key concepts in domain1
                    concepts1 = self.domain_knowledge.get(domain1, [])
                    concepts2 = self.domain_knowledge.get(domain2, [])
                    
                    for concept in concepts1:
                        # Check if this concept improves domain2
                        potential_transfer = {
                            "from_domain": domain1,
                            "to_domain": domain2,
                            "concept": concept.get("name", "unknown"),
                            "application_potential": "high",
                            "should_explore": True,
                            "discovered_at": datetime.now().isoformat()
                        }
                        transfers.append(potential_transfer)
            
            logger.info(f"[SYNTHESIS] Identified {len(transfers)} potential knowledge transfers")
            
        except Exception as e:
            logger.error(f"[SYNTHESIS] Error in cross-pollination: {e}")
        
        return transfers
    
    def validate_synthesis(self, insight_id: str, validation_outcome: bool) -> float:
        """
        Validate a synthesized insight against real data.
        Update confidence based on validation results.
        """
        if insight_id not in self.insights:
            return 0.0
        
        insight = self.insights[insight_id]
        
        if validation_outcome:
            # Increase confidence
            insight.confidence = min(1.0, insight.confidence + 0.1)
        else:
            # Decrease confidence
            insight.confidence = max(0.0, insight.confidence - 0.15)
        
        insight.validation_count += 1
        
        logger.info(f"[SYNTHESIS] Validated insight {insight_id}: confidence now {insight.confidence:.2f}")
        
        return insight.confidence
    
    def get_novel_combinations(self) -> List[Dict]:
        """
        Identify novel combinations of concepts from different domains.
        These represent potential breakthroughs.
        """
        combinations = []
        
        try:
            domains = list(self.domain_knowledge.keys())
            
            if len(domains) < 2:
                return combinations
            
            # Try combining top concepts from each domain
            for d1 in domains:
                for d2 in domains:
                    if d1 != d2:
                        concepts1 = self.domain_knowledge.get(d1, [])
                        concepts2 = self.domain_knowledge.get(d2, [])
                        
                        if concepts1 and concepts2:
                            # Take top concept from each
                            combo = {
                                "domain1": d1,
                                "concept1": concepts1[0].get("name", "unknown"),
                                "domain2": d2,
                                "concept2": concepts2[0].get("name", "unknown"),
                                "novelty_potential": "high",
                                "explored": False
                            }
                            combinations.append(combo)
            
            logger.info(f"[SYNTHESIS] Found {len(combinations)} novel combinations")
            
        except Exception as e:
            logger.error(f"[SYNTHESIS] Error finding novel combinations: {e}")
        
        return combinations
    
    def save_insights(self):
        """Persist synthesized insights to disk"""
        try:
            insights_dict = {}
            for insight_id, insight in self.insights.items():
                insights_dict[insight_id] = insight.to_dict()
            
            with open(self.insights_file, 'w') as f:
                json.dump(insights_dict, f, indent=2)
            
            logger.info(f"[SYNTHESIS] Saved {len(self.insights)} insights")
        except Exception as e:
            logger.error(f"[SYNTHESIS] Error saving insights: {e}")
    
    def get_synthesis_summary(self) -> Dict:
        """Get comprehensive summary of synthesis system status"""
        return {
            "total_insights": len(self.insights),
            "total_analogies": len(self.analogies),
            "total_bridges": len(self.conceptual_bridges),
            "emergent_theories": len(self.emergent_theories),
            "domains_integrated": len(self.domain_knowledge),
            "synthesis_history_size": len(self.synthesis_history),
            "avg_insight_confidence": float(np.mean([i.confidence for i in self.insights.values()])) if self.insights else 0.0
        }
