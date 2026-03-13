"""
Knowledge Integrator: Autonomous knowledge absorption and integration

Enables system to:
- Monitor and absorb new algorithms
- Integrate best practices from environment
- Update knowledge base dynamically
- Learn from external sources
"""
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

import config
from logger import logger


class KnowledgeType(Enum):
    """Types of knowledge"""
    ALGORITHM = "algorithm"
    PATTERN = "pattern"
    OPTIMIZATION = "optimization"
    BEST_PRACTICE = "best_practice"
    FAILURE_MODE = "failure_mode"
    OPPORTUNITY = "opportunity"


@dataclass
class KnowledgeEntry:
    """A piece of knowledge"""
    entry_id: str
    knowledge_type: KnowledgeType
    
    name: str
    description: str
    source: str  # Where it came from
    
    created_at: datetime = field(default_factory=datetime.now)
    integrated: bool = False
    integrated_at: Optional[datetime] = None
    
    # Impact tracking
    predicted_impact: float = 0.0  # Estimated improvement
    actual_impact: float = 0.0  # Measured improvement
    success_count: int = 0
    total_uses: int = 0
    
    # Implementation
    implementation_code: Optional[str] = None
    dependencies: List[str] = field(default_factory=list)
    
    @property
    def success_rate(self) -> float:
        return self.success_count / max(self.total_uses, 1)


class KnowledgeSource:
    """Source of knowledge"""
    
    def __init__(self, name: str, fetch_function: Callable):
        self.name = name
        self.fetch_function = fetch_function
        self.last_checked: Optional[datetime] = None
        self.knowledge_count = 0
    
    def fetch_knowledge(self) -> List[Dict[str, Any]]:
        """Fetch new knowledge from source"""
        try:
            result = self.fetch_function()
            self.last_checked = datetime.now()
            return result if isinstance(result, list) else [result]
        except Exception as e:
            logger.error(f"Error fetching from {self.name}: {e}")
            return []


class KnowledgeIntegrator:
    """
    Autonomous knowledge absorption and integration
    
    Features:
    - Monitor knowledge sources
    - Evaluate new knowledge
    - Integrate beneficial knowledge
    - Track impact
    """
    
    def __init__(self):
        self.knowledge_base: Dict[str, KnowledgeEntry] = {}
        self.sources: Dict[str, KnowledgeSource] = {}
        self.integration_history: List[Dict[str, Any]] = []
        
        logger.info("✓ Knowledge Integrator initialized")
    
    def register_knowledge_source(
        self,
        source_name: str,
        fetch_function: Callable
    ) -> None:
        """Register a source of knowledge"""
        
        source = KnowledgeSource(source_name, fetch_function)
        self.sources[source_name] = source
        
        logger.info(f"Registered knowledge source: {source_name}")
    
    def fetch_new_knowledge(self, source_name: Optional[str] = None) -> List[KnowledgeEntry]:
        """Fetch new knowledge from sources"""
        
        new_knowledge = []
        
        sources_to_check = [self.sources[source_name]] if source_name else self.sources.values()
        
        for source in sources_to_check:
            logger.info(f"Fetching knowledge from {source.name}...")
            
            try:
                knowledge_list = source.fetch_knowledge()
                
                for item in knowledge_list:
                    entry = self._create_knowledge_entry(item, source.name)
                    if entry:
                        self.knowledge_base[entry.entry_id] = entry
                        new_knowledge.append(entry)
                        source.knowledge_count += 1
                
                logger.info(f"  Found {len(knowledge_list)} new items")
            
            except Exception as e:
                logger.error(f"Error fetching from {source.name}: {e}")
        
        return new_knowledge
    
    def _create_knowledge_entry(
        self,
        item: Dict[str, Any],
        source: str
    ) -> Optional[KnowledgeEntry]:
        """Create knowledge entry from raw data"""
        
        try:
            entry_id = f"know_{hash(item.get('name', ''))}_{int(datetime.now().timestamp())}"
            
            entry = KnowledgeEntry(
                entry_id=entry_id,
                knowledge_type=KnowledgeType[item.get("type", "BEST_PRACTICE").upper()],
                name=item.get("name", "Unknown"),
                description=item.get("description", ""),
                source=source,
                implementation_code=item.get("code", None),
                dependencies=item.get("dependencies", []),
                predicted_impact=item.get("predicted_impact", 0.5)
            )
            
            logger.debug(f"Created knowledge entry: {entry.name}")
            
            return entry
        
        except Exception as e:
            logger.error(f"Error creating knowledge entry: {e}")
            return None
    
    def evaluate_knowledge(self, entry_id: str) -> bool:
        """Evaluate if knowledge is worth integrating"""
        
        if entry_id not in self.knowledge_base:
            return False
        
        entry = self.knowledge_base[entry_id]
        
        # Evaluate based on predicted impact and source reliability
        score = entry.predicted_impact
        
        # Boost for algorithms
        if entry.knowledge_type == KnowledgeType.ALGORITHM:
            score *= 1.2
        
        # Reduce for untested patterns
        if entry.knowledge_type == KnowledgeType.PATTERN and entry.success_count == 0:
            score *= 0.8
        
        is_valuable = score > 0.6
        
        logger.info(f"Evaluating knowledge: {entry.name}")
        logger.info(f"  Type: {entry.knowledge_type.value}")
        logger.info(f"  Predicted impact: {entry.predicted_impact:.2f}")
        logger.info(f"  Evaluation score: {score:.2f}")
        logger.info(f"  Worth integrating: {is_valuable}")
        
        return is_valuable
    
    def integrate_knowledge(self, entry_id: str) -> bool:
        """Integrate knowledge into system"""
        
        if entry_id not in self.knowledge_base:
            return False
        
        entry = self.knowledge_base[entry_id]
        
        if entry.integrated:
            logger.warning(f"Knowledge already integrated: {entry.name}")
            return True
        
        # Integration process depends on type
        if entry.knowledge_type == KnowledgeType.ALGORITHM:
            success = self._integrate_algorithm(entry)
        elif entry.knowledge_type == KnowledgeType.OPTIMIZATION:
            success = self._integrate_optimization(entry)
        elif entry.knowledge_type == KnowledgeType.PATTERN:
            success = self._integrate_pattern(entry)
        elif entry.knowledge_type == KnowledgeType.BEST_PRACTICE:
            success = self._integrate_practice(entry)
        else:
            success = False
        
        if success:
            entry.integrated = True
            entry.integrated_at = datetime.now()
            
            self.integration_history.append({
                "timestamp": entry.integrated_at.isoformat(),
                "entry_id": entry_id,
                "name": entry.name,
                "type": entry.knowledge_type.value,
                "source": entry.source
            })
            
            logger.info(f"✓ Integrated knowledge: {entry.name}")
        
        return success
    
    def _integrate_algorithm(self, entry: KnowledgeEntry) -> bool:
        """Integrate new algorithm"""
        logger.info(f"Integrating algorithm: {entry.name}")
        
        # In real implementation:
        # - Load algorithm code
        # - Register with algorithm registry
        # - Add to experimentation framework
        # - Track performance
        
        return True
    
    def _integrate_optimization(self, entry: KnowledgeEntry) -> bool:
        """Integrate optimization technique"""
        logger.info(f"Integrating optimization: {entry.name}")
        
        # In real implementation:
        # - Parse optimization code
        # - Apply to relevant components
        # - Measure impact
        
        return True
    
    def _integrate_pattern(self, entry: KnowledgeEntry) -> bool:
        """Integrate design pattern"""
        logger.info(f"Integrating pattern: {entry.name}")
        
        # In real implementation:
        # - Document pattern
        # - Add to decision logic
        # - Track when pattern applies
        
        return True
    
    def _integrate_practice(self, entry: KnowledgeEntry) -> bool:
        """Integrate best practice"""
        logger.info(f"Integrating practice: {entry.name}")
        
        # In real implementation:
        # - Update operating procedures
        # - Add to quality checks
        # - Enforce compliance
        
        return True
    
    def measure_knowledge_impact(self, entry_id: str, success: bool, impact: float) -> None:
        """Measure impact of integrated knowledge"""
        
        if entry_id not in self.knowledge_base:
            return
        
        entry = self.knowledge_base[entry_id]
        entry.total_uses += 1
        
        if success:
            entry.success_count += 1
            entry.actual_impact = impact
        
        logger.debug(f"Measured impact: {entry.name}")
        logger.debug(f"  Success rate: {entry.success_rate:.1%}")
        logger.debug(f"  Actual impact: {entry.actual_impact:.2f}")
    
    def get_knowledge_status(self) -> Dict[str, Any]:
        """Get status of knowledge base"""
        
        total = len(self.knowledge_base)
        integrated = sum(1 for e in self.knowledge_base.values() if e.integrated)
        
        by_type = {}
        for entry in self.knowledge_base.values():
            kt = entry.knowledge_type.value
            if kt not in by_type:
                by_type[kt] = {"total": 0, "integrated": 0, "avg_impact": 0.0}
            
            by_type[kt]["total"] += 1
            if entry.integrated:
                by_type[kt]["integrated"] += 1
                by_type[kt]["avg_impact"] = (
                    by_type[kt]["avg_impact"] * (by_type[kt]["integrated"] - 1) +
                    entry.actual_impact
                ) / by_type[kt]["integrated"]
        
        return {
            "total_knowledge": total,
            "integrated": integrated,
            "pending": total - integrated,
            "sources": len(self.sources),
            "by_type": by_type,
            "recent_integrations": [
                {
                    "timestamp": item["timestamp"],
                    "name": item["name"],
                    "type": item["type"]
                }
                for item in self.integration_history[-10:]
            ]
        }
    
    def recommend_integrations(self, top_n: int = 5) -> List[KnowledgeEntry]:
        """Recommend knowledge to integrate"""
        
        candidates = [
            e for e in self.knowledge_base.values()
            if not e.integrated and self.evaluate_knowledge(e.entry_id)
        ]
        
        # Sort by predicted impact
        candidates.sort(key=lambda e: e.predicted_impact, reverse=True)
        
        return candidates[:top_n]


# Global instance
_integrator: Optional[KnowledgeIntegrator] = None


def get_knowledge_integrator() -> KnowledgeIntegrator:
    """Get or create knowledge integrator"""
    global _integrator
    if _integrator is None:
        _integrator = KnowledgeIntegrator()
    return _integrator
