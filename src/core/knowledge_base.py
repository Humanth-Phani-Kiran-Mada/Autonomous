"""
Advanced Knowledge Base with vector embeddings and semantic search.

Provides intelligent storage and retrieval of knowledge with:
- Semantic similarity search using embeddings
- Automatic relevance scoring
- Knowledge pruning and compression
- Persistent storage with recovery
- Type categorization
"""
import json
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
import numpy as np
from pathlib import Path
import pickle
import config
from .logger import logger
from .exceptions import KnowledgeBaseException, PersistenceException, ValidationException
from . import validators

try:
    from sentence_transformers import SentenceTransformer
    EMBEDDINGS_AVAILABLE = True
except ImportError:
    EMBEDDINGS_AVAILABLE = False
    logger.warning("sentence-transformers not available, using basic search")


class KnowledgeBase:
    """
    Intelligent knowledge base with semantic understanding and evolution.
    
    Features:
    - Vector embeddings for semantic search
    - Automatic relevance scoring
    - Knowledge compression when reaching capacity
    - Persistent storage with JSON + pickle
    - Keyword fallback search
    
    Attributes:
        entries: List of knowledge entries
        embeddings: NumPy array of embedding vectors
        model: Sentence transformer model for embeddings
    """
    
    def __init__(self) -> None:
        """
        Initialize knowledge base.
        
        Loads stored knowledge from disk if available.
        Initializes embedding model if sentence-transformers is installed.
        
        Raises:
            PersistenceException: If loading stored data fails
        """
        self.entries: List[Dict[str, Any]] = []
        self.embeddings: Optional[np.ndarray] = None
        self.kb_file = config.KNOWLEDGE_DIR / "knowledge_base.json"
        self.embeddings_file = config.KNOWLEDGE_DIR / "embeddings.pkl"
        self.metadata_file = config.KNOWLEDGE_DIR / "metadata.json"
        
        # Initialize embeddings model if available
        self.model = None
        if EMBEDDINGS_AVAILABLE:
            try:
                logger.info(" Loading embedding model...")
                self.model = SentenceTransformer(config.KNOWLEDGE_EMBEDDING_MODEL)
                logger.info(" Embedding model loaded successfully")
            except Exception as e:
                logger.error(f"Failed to load embedding model: {e}")
                raise KnowledgeBaseException(
                    f"Failed to initialize embedding model: {e}",
                    error_code="EMBEDDER_INIT_FAILED"
                )
        
        self.load_knowledge_base()
        logger.info(f" Knowledge Base initialized with {len(self.entries)} entries")
    
    def load_knowledge_base(self) -> None:
        """
        Load knowledge base from persistent storage.
        
        Loads both entries and embeddings from disk.
        Handles missing files gracefully.
        
        Raises:
            PersistenceException: If load fails after retry
        """
        try:
            if self.kb_file.exists():
                with open(self.kb_file, 'r', encoding='utf-8') as f:
                    self.entries = json.load(f)
                logger.info(f" Loaded {len(self.entries)} knowledge entries")
            else:
                logger.info(" No existing knowledge base found, starting fresh")
            
            if self.embeddings_file.exists() and self.model:
                try:
                    with open(self.embeddings_file, 'rb') as f:
                        self.embeddings = pickle.load(f)
                    logger.info(f" Loaded {len(self.embeddings)} embeddings")
                except Exception as e:
                    logger.warning(f"Failed to load embeddings, will regenerate: {e}")
                    self.embeddings = None
        except json.JSONDecodeError as e:
            raise PersistenceException(
                f"Failed to parse knowledge base JSON: {e}",
                error_code="JSON_PARSE_ERROR"
            )
        except Exception as e:
            raise PersistenceException(
                f"Error loading knowledge base: {e}",
                error_code="LOAD_FAILED"
            )
    
    def save_knowledge_base(self) -> None:
        """
        Persist knowledge base to disk.
        
        Saves entries as JSON and embeddings as pickle.
        Creates directories if they don't exist.
        
        Raises:
            PersistenceException: If save fails
        """
        try:
            config.KNOWLEDGE_DIR.mkdir(parents=True, exist_ok=True)
            
            # Save entries
            with open(self.kb_file, 'w', encoding='utf-8') as f:
                json.dump(self.entries, f, indent=2)
            
            # Save embeddings
            if self.embeddings is not None:
                with open(self.embeddings_file, 'wb') as f:
                    pickle.dump(self.embeddings, f)
            
            logger.debug(f" Knowledge base saved: {len(self.entries)} entries")
        except Exception as e:
            raise PersistenceException(
                f"Failed to save knowledge base: {e}",
                error_code="SAVE_FAILED"
            )
    
    def add_knowledge(
        self,
        content: str,
        source: str,
        knowledge_type: str = "general",
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Add new knowledge entry to the base.
        
        Automatically generates embeddings if model is available.
        Triggers pruning if maximum capacity is reached.
        
        Args:
            content: The knowledge content to store
            source: Where this knowledge came from (URL, file, etc.)
            knowledge_type: Category of knowledge (article, link, concept, etc.)
            metadata: Additional structured metadata
        
        Returns:
            Unique knowledge entry ID
        
        Raises:
            ValidationException: If inputs are invalid
            KnowledgeBaseException: If operation fails
        
        Example:
            >>> kb = KnowledgeBase()
            >>> kid = kb.add_knowledge(
            ...     "AI is transforming industries",
            ...     "https://example.com/ai",
            ...     "article",
            ...     {"author": "Jane Doe"}
            ... )
        """
        # Validate inputs
        content = validators.validate_content(content, min_length=10)
        source = validators.validate_url(source)
        knowledge_type = validators.validate_knowledge_type(knowledge_type)
        metadata = validators.validate_metadata(metadata or {})
        
        try:
            knowledge_id = self._generate_id()
            
            entry: Dict[str, Any] = {
                "id": knowledge_id,
                "content": content,
                "source": source,
                "type": knowledge_type,
                "created_at": datetime.now().isoformat(),
                "accessed_count": 0,
                "relevance_score": 0.0,
                "metadata": metadata
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
                    raise KnowledgeBaseException(
                        f"Failed to create embedding: {e}",
                        error_code="EMBEDDING_FAILED"
                    )
            
            # Maintain size limit
            if len(self.entries) > config.MAX_KNOWLEDGE_ENTRIES:
                self._prune_knowledge()
            
            logger.info(f"📝 Added knowledge: {knowledge_id}")
            return knowledge_id
        except (ValidationException, KnowledgeBaseException):
            raise
        except Exception as e:
            raise KnowledgeBaseException(
                f"Failed to add knowledge: {e}",
                error_code="ADD_KNOWLEDGE_FAILED"
            )
    
    def _generate_id(self) -> str:
        """
        Generate unique knowledge entry ID.
        
        Returns:
            Unique identifier combining timestamp and index
        """
        timestamp = datetime.now().isoformat().replace(":", "").replace(".", "")
        return f"KB_{timestamp}_{len(self.entries)}"
    
    def search(
        self,
        query: str,
        top_k: int = 5,
        threshold: float = 0.3
    ) -> List[Dict[str, Any]]:
        """
        Search knowledge base using semantic or keyword matching.
        
        Uses semantic similarity if embeddings available, otherwise falls back
        to keyword matching. Scores results and returns top matches.
        
        Args:
            query: Search query string
            top_k: Maximum number of results to return
            threshold: Minimum similarity score to include result
        
        Returns:
            List of knowledge entries matching query, sorted by relevance
        
        Raises:
            ValidationException: If query is invalid
            KnowledgeBaseException: If search fails
        
        Example:
            >>> results = kb.search("machine learning", top_k=5)
            >>> for result in results:
            ...     print(result['content'], result['similarity_score'])
        """
        try:
            query = validators.validate_content(query, min_length=1)
            query = validators.validate_batch_size(top_k)  # Reuse for range validation
            
            results: List[Dict[str, Any]] = []
            
            if self.model and self.embeddings is not None and len(self.embeddings) > 0:
                try:
                    results = self._semantic_search(query, top_k, threshold)
                    logger.info(f" Semantic search found {len(results)} results")
                except Exception as e:
                    logger.warning(f"Semantic search failed, falling back to keyword: {e}")
                    results = self._keyword_search(query, top_k)
            else:
                results = self._keyword_search(query, top_k)
            
            return results
        except ValidationException:
            raise
        except Exception as e:
            raise KnowledgeBaseException(
                f"Search failed: {e}",
                error_code="SEARCH_FAILED"
            )
    
    def _semantic_search(
        self,
        query: str,
        top_k: int,
        threshold: float
    ) -> List[Dict[str, Any]]:
        """
        Perform semantic similarity search using embeddings.
        
        Args:
            query: Search query
            top_k: Number of results to return
            threshold: Minimum similarity threshold
        
        Returns:
            List of matching entries with similarity scores
        """
        if not self.model or self.embeddings is None:
            return []
        
        query_embedding = self.model.encode(query, convert_to_numpy=True)
        
        # Compute cosine similarity
        norms = np.linalg.norm(self.embeddings, axis=1, keepdims=True)
        similarities = np.dot(self.embeddings, query_embedding) / (norms.flatten() * np.linalg.norm(query_embedding) + 1e-10)
        
        top_indices = np.argsort(-similarities)[:top_k]
        results = []
        
        for idx in top_indices:
            if similarities[idx] > threshold:
                try:
                    entry = self.entries[idx].copy()
                    entry["similarity_score"] = float(similarities[idx])
                    entry["accessed_count"] += 1
                    results.append(entry)
                except IndexError:
                    logger.warning(f"Index mismatch: {idx} out of range")
                    continue
        
        return results
    
    def _keyword_search(self, query: str, top_k: int) -> List[Dict[str, Any]]:
        """
        Fallback keyword-based search.
        
        Performs simple term matching for when semantic search is unavailable.
        
        Args:
            query: Search query
            top_k: Number of results to return
        
        Returns:
            List of matching entries
        """
        query_terms = set(query.lower().split())
        scored_entries: List[tuple[Dict[str, Any], float]] = []
        
        for entry in self.entries:
            content_terms = set(entry["content"].lower().split())
            overlap = len(query_terms & content_terms)
            
            if overlap > 0:
                score = overlap / (len(query_terms | content_terms) + 1e-10)
                scored_entries.append((entry, score))
        
        scored_entries.sort(key=lambda x: x[1], reverse=True)
        results = [entry for entry, _ in scored_entries[:top_k]]
        
        logger.info(f"🔑 Keyword search found {len(results)} results")
        return results
    
    def _prune_knowledge(self) -> None:
        """
        Remove least relevant knowledge when reaching capacity limit.
        
        Keeps entries with best prune scores based on recency, access frequency,
        and relevance. Rebuilds embeddings after pruning.
        """
        logger.info("🗑 Pruning knowledge base...")
        
        try:
            # Score entries by relevance
            for entry in self.entries:
                try:
                    created = datetime.fromisoformat(entry["created_at"])
                    age_days = (datetime.now() - created).days
                    recency_score = 1.0 / (1.0 + abs(age_days) / 30)
                except (ValueError, KeyError):
                    recency_score = 0.5
                
                access_count = entry.get("accessed_count", 0)
                access_score = min(access_count / 100, 1.0)
                relevance = entry.get("relevance_score", 0)
                
                entry["prune_score"] = (recency_score * 0.4 + 
                                       access_score * 0.4 + 
                                       relevance * 0.2)
            
            # Keep top entries
            self.entries.sort(key=lambda x: x.get("prune_score", 0), reverse=True)
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
            
            logger.info(f"✂️  Pruned {removed_count} entries, kept {keep_count}")
        except Exception as e:
            raise KnowledgeBaseException(
                f"Pruning failed: {e}",
                error_code="PRUNE_FAILED"
            )
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get comprehensive statistics about the knowledge base.
        
        Returns:
            Dictionary containing:
            - total_entries: Number of entries
            - types: Unique knowledge types
            - sources: Unique sources
            - avg_access_count: Average access count
            - embeddings_available: Whether embeddings exist
            - total_memory_mb: Approximate memory usage
        
        Example:
            >>> stats = kb.get_statistics()
            >>> print(f"Total entries: {stats['total_entries']}")
        """
        try:
            access_counts = [e.get("accessed_count", 0) for e in self.entries]
            
            return {
                "total_entries": len(self.entries),
                "types": list(set(e.get("type", "unknown") for e in self.entries)),
                "sources": list(set(e.get("source", "unknown") for e in self.entries)),
                "avg_access_count": float(np.mean(access_counts)) if access_counts else 0.0,
                "embeddings_available": self.embeddings is not None and len(self.embeddings) > 0,
                "embeddings_count": len(self.embeddings) if self.embeddings is not None else 0,
                "capacity_used_percent": (len(self.entries) / config.MAX_KNOWLEDGE_ENTRIES) * 100
            }
        except Exception as e:
            logger.error(f"Failed to compute statistics: {e}")
            return {"error": str(e)}
    
    def get_all_by_type(self, knowledge_type: str) -> List[Dict[str, Any]]:
        """
        Get all knowledge entries of a specific type.
        
        Args:
            knowledge_type: Type to filter by (article, link, concept, etc.)
        
        Returns:
            List of entries matching the type
        
        Raises:
            ValidationException: If type is invalid
        """
        knowledge_type = validators.validate_knowledge_type(knowledge_type)
        return [e for e in self.entries if e.get("type") == knowledge_type]
    
    def update_relevance_score(self, knowledge_id: str, score: float) -> None:
        """
        Update relevance score for a knowledge entry.
        
        Args:
            knowledge_id: ID of entry to update
            score: New relevance score (0.0 to 1.0)
        
        Raises:
            ValidationException: If score is invalid
            KnowledgeBaseException: If entry not found
        """
        score = validators.validate_skill_level(score)  # Reuse for 0-1 range
        
        found = False
        for entry in self.entries:
            if entry["id"] == knowledge_id:
                entry["relevance_score"] = score
                found = True
                break
        
        if not found:
            raise KnowledgeBaseException(
                f"Knowledge entry not found: {knowledge_id}",
                error_code="ENTRY_NOT_FOUND"
            )
