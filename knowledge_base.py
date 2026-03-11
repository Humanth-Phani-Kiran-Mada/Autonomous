"""
Advanced Knowledge Base with vector embeddings and semantic search
"""
import json
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
import numpy as np
from pathlib import Path
import pickle
import config
from src.logger import logger

try:
    from sentence_transformers import SentenceTransformer
    EMBEDDINGS_AVAILABLE = True
except ImportError:
    EMBEDDINGS_AVAILABLE = False
    logger.warning("sentence-transformers not available, using basic search")

class KnowledgeBase:
    """Intelligent knowledge base with semantic understanding and evolution"""
    
    def __init__(self):
        self.entries: List[Dict] = []
        self.embeddings: Optional[np.ndarray] = None
        self.kb_file = config.KNOWLEDGE_DIR / "knowledge_base.json"
        self.embeddings_file = config.KNOWLEDGE_DIR / "embeddings.pkl"
        self.metadata_file = config.KNOWLEDGE_DIR / "metadata.json"
        
        # Initialize embeddings model if available
        self.model = None
        if EMBEDDINGS_AVAILABLE:
            try:
                logger.info("🤖 Loading embedding model...")
                self.model = SentenceTransformer(config.KNOWLEDGE_EMBEDDING_MODEL)
                logger.info("✅ Embedding model loaded")
            except Exception as e:
                logger.error(f"Failed to load embedding model: {e}")
        
        self.load_knowledge_base()
        logger.info("💾 Knowledge Base initialized")
    
    def load_knowledge_base(self):
        """Load knowledge base from disk"""
        try:
            if self.kb_file.exists():
                with open(self.kb_file, 'r') as f:
                    self.entries = json.load(f)
                logger.info(f"📂 Loaded {len(self.entries)} knowledge entries")
            
            if self.embeddings_file.exists() and self.model:
                with open(self.embeddings_file, 'rb') as f:
                    self.embeddings = pickle.load(f)
                logger.info(f"🔍 Loaded {len(self.embeddings)} embeddings")
        except Exception as e:
            logger.error(f"Error loading knowledge base: {e}")
    
    def save_knowledge_base(self):
        """Save knowledge base to disk"""
        try:
            config.KNOWLEDGE_DIR.mkdir(parents=True, exist_ok=True)
            
            with open(self.kb_file, 'w') as f:
                json.dump(self.entries, f, indent=2)
            
            if self.embeddings is not None:
                with open(self.embeddings_file, 'wb') as f:
                    pickle.dump(self.embeddings, f)
            
            logger.debug("💾 Knowledge base saved to disk")
        except Exception as e:
            logger.error(f"Error saving knowledge base: {e}")
    
    def add_knowledge(self, content: str, source: str, knowledge_type: str = "general",
                      metadata: Optional[Dict] = None) -> str:
        """Add new knowledge with automatic embedding"""
        knowledge_id = self._generate_id()
        
        entry = {
            "id": knowledge_id,
            "content": content,
            "source": source,
            "type": knowledge_type,
            "created_at": datetime.now().isoformat(),
            "accessed_count": 0,
            "relevance_score": 0.0,
            "metadata": metadata or {}
        }
        
        self.entries.append(entry)
        
        # Generate embedding if model available
        if self.model:
            try:
                embedding = self.model.encode(content, convert_to_numpy=True)
                if self.embeddings is None:
                    self.embeddings = np.array([embedding])
                else:
                    self.embeddings = np.vstack([self.embeddings, embedding])
            except Exception as e:
                logger.warning(f"Failed to generate embedding: {e}")
        
        # Maintain size limit
        if len(self.entries) > config.MAX_KNOWLEDGE_ENTRIES:
            self._prune_knowledge()
        
        logger.info(f"📝 Added knowledge: {knowledge_id}")
        return knowledge_id
    
    def _generate_id(self) -> str:
        """Generate unique knowledge ID"""
        timestamp = datetime.now().isoformat().replace(":", "").replace(".", "")
        return f"KB_{timestamp}_{len(self.entries)}"
    
    def search(self, query: str, top_k: int = 5, threshold: float = 0.3) -> List[Dict]:
        """Search knowledge base using semantic similarity or keyword matching"""
        results = []
        
        if self.model and self.embeddings is not None:
            try:
                # Semantic search using embeddings
                query_embedding = self.model.encode(query, convert_to_numpy=True)
                
                # Compute cosine similarity
                similarities = np.dot(self.embeddings, query_embedding) / (
                    np.linalg.norm(self.embeddings, axis=1) * np.linalg.norm(query_embedding) + 1e-10
                )
                
                top_indices = np.argsort(-similarities)[:top_k]
                
                for idx in top_indices:
                    if similarities[idx] > threshold:
                        entry = self.entries[idx].copy()
                        entry["similarity_score"] = float(similarities[idx])
                        entry["accessed_count"] += 1
                        results.append(entry)
                
                logger.info(f"🔍 Semantic search found {len(results)} results for: {query[:50]}")
            except Exception as e:
                logger.warning(f"Semantic search failed, falling back to keyword search: {e}")
                results = self._keyword_search(query, top_k)
        else:
            # Fallback to keyword search
            results = self._keyword_search(query, top_k)
        
        return results
    
    def _keyword_search(self, query: str, top_k: int) -> List[Dict]:
        """Fallback keyword-based search"""
        query_terms = set(query.lower().split())
        scored_entries = []
        
        for entry in self.entries:
            content_terms = set(entry["content"].lower().split())
            overlap = len(query_terms & content_terms)
            
            if overlap > 0:
                score = overlap / len(query_terms | content_terms)
                scored_entries.append((entry, score))
        
        scored_entries.sort(key=lambda x: x[1], reverse=True)
        results = [entry for entry, _ in scored_entries[:top_k]]
        
        logger.info(f"🔑 Keyword search found {len(results)} results")
        return results
    
    def _prune_knowledge(self):
        """Remove least relevant knowledge when reaching limit"""
        logger.info("🗑️ Pruning knowledge base...")
        
        # Score entries by relevance
        for entry in self.entries:
            age_days = (datetime.fromisoformat(entry["created_at"]) - datetime.now()).days
            recency_score = 1.0 / (1.0 + abs(age_days) / 30)
            access_score = min(entry["accessed_count"] / 100, 1.0)
            
            entry["prune_score"] = (recency_score * 0.4 + 
                                   access_score * 0.4 + 
                                   entry.get("relevance_score", 0) * 0.2)
        
        # Keep top entries
        self.entries.sort(key=lambda x: x["prune_score"], reverse=True)
        keep_count = int(config.MAX_KNOWLEDGE_ENTRIES * config.MEMORY_COMPRESSION_RATIO)
        
        removed_count = len(self.entries) - keep_count
        self.entries = self.entries[:keep_count]
        
        # Rebuild embeddings
        if self.model and self.entries:
            try:
                contents = [entry["content"] for entry in self.entries]
                self.embeddings = self.model.encode(contents, convert_to_numpy=True)
            except Exception as e:
                logger.warning(f"Failed to rebuild embeddings: {e}")
        
        logger.info(f"✂️ Pruned {removed_count} entries, kept {len(self.entries)}")
    
    def get_statistics(self) -> Dict:
        """Get knowledge base statistics"""
        return {
            "total_entries": len(self.entries),
            "types": list(set(e.get("type", "unknown") for e in self.entries)),
            "sources": list(set(e.get("source", "unknown") for e in self.entries)),
            "avg_access_count": np.mean([e.get("accessed_count", 0) for e in self.entries]) if self.entries else 0,
            "embeddings_available": self.embeddings is not None and len(self.embeddings) > 0
        }
    
    def get_all_by_type(self, knowledge_type: str) -> List[Dict]:
        """Get all knowledge of a specific type"""
        return [e for e in self.entries if e.get("type") == knowledge_type]
    
    def update_relevance_score(self, knowledge_id: str, score: float):
        """Update relevance score for a knowledge entry"""
        for entry in self.entries:
            if entry["id"] == knowledge_id:
                entry["relevance_score"] = min(max(score, 0), 1.0)
                break
