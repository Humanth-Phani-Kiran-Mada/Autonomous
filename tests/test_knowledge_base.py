"""
Unit tests for the Knowledge Base module.

Demonstrates code quality improvements including:
- Comprehensive test coverage
- Type safety validation
- Error handling verification
- Integration testing
"""
import pytest
import json
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import config
from exceptions import (
    ValidationException, KnowledgeBaseException, PersistenceException
)
from validators import validate_content, validate_url, validate_knowledge_type
from knowledge_base import KnowledgeBase


class TestKnowledgeBaseValidation:
    """Test input validation"""
    
    def test_validate_content_success(self):
        """Valid content should pass"""
        result = validate_content("This is a valid content with enough length")
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_validate_content_too_short(self):
        """Content shorter than minimum should raise error"""
        with pytest.raises(ValidationException) as exc_info:
            validate_content("short")
        assert "too short" in str(exc_info.value).lower()
    
    def test_validate_content_type_error(self):
        """Non-string content should raise error"""
        with pytest.raises(ValidationException) as exc_info:
            validate_content(12345)
        assert "string" in str(exc_info.value).lower()
    
    def test_validate_url_success(self):
        """Valid URL should pass"""
        url = "https://example.com"
        result = validate_url(url)
        assert result == url
    
    def test_validate_url_invalid_format(self):
        """Invalid URL format should raise error"""
        with pytest.raises(ValidationException):
            validate_url("not-a-valid-url")
    
    def test_validate_knowledge_type_valid(self):
        """Valid types should pass"""
        for ktype in ["article", "link", "concept", "pattern"]:
            result = validate_knowledge_type(ktype)
            assert result == ktype
    
    def test_validate_knowledge_type_invalid(self):
        """Invalid type should raise error"""
        with pytest.raises(ValidationException) as exc_info:
            validate_knowledge_type("invalid_type")
        assert "invalid" in str(exc_info.value).lower()


class TestKnowledgeBaseOperations:
    """Test core knowledge base operations"""
    
    @pytest.fixture
    def kb(self):
        """Fixture for knowledge base instance"""
        with patch('config.KNOWLEDGE_DIR', Path(tempfile.gettempdir())):
            kb = KnowledgeBase()
            yield kb
    
    def test_add_knowledge_success(self, kb):
        """Adding valid knowledge should succeed"""
        kid = kb.add_knowledge(
            "This is a comprehensive article about artificial intelligence",
            "https://example.com/ai",
            "article",
            {"author": "Jane Doe"}
        )
        assert isinstance(kid, str)
        assert kid.startswith("KB_")
        assert len(kb.entries) == 1
    
    def test_add_knowledge_invalid_content(self, kb):
        """Adding invalid content should raise error"""
        with pytest.raises(ValidationException):
            kb.add_knowledge(
                "short",  # Too short
                "https://example.com",
                "article"
            )
    
    def test_add_knowledge_invalid_url(self, kb):
        """Adding with invalid URL should raise error"""
        with pytest.raises(ValidationException):
            kb.add_knowledge(
                "This is comprehensive content about something",
                "not-a-url",
                "article"
            )
    
    def test_add_knowledge_invalid_type(self, kb):
        """Adding with invalid type should raise error"""
        with pytest.raises(ValidationException):
            kb.add_knowledge(
                "This is comprehensive content about something",
                "https://example.com",
                "invalid_type"
            )
    
    def test_search_keyword_fallback(self, kb):
        """Search should work with keyword fallback"""
        kb.add_knowledge(
            "Machine learning is a subset of artificial intelligence",
            "https://example.com/ml",
            "article"
        )
        
        results = kb.search("machine learning")
        assert len(results) > 0
        assert results[0]["type"] == "article"
    
    def test_search_empty_result(self, kb):
        """Search with no matches should return empty list"""
        kb.add_knowledge(
            "The sky is blue and vast",
            "https://example.com/sky",
            "article"
        )
        
        results = kb.search("quantum computing", top_k=5)
        assert len(results) == 0
    
    def test_get_by_type(self, kb):
        """Filtering by type should work"""
        kb.add_knowledge(
            "Article about AI",
            "https://example.com/1",
            "article"
        )
        kb.add_knowledge(
            "Link to resources",
            "https://example.com/2",
            "link"
        )
        
        articles = kb.get_all_by_type("article")
        links = kb.get_all_by_type("link")
        
        assert len(articles) == 1
        assert len(links) == 1
    
    def test_update_relevance_score(self, kb):
        """Updating relevance should work"""
        kid = kb.add_knowledge(
            "Important article about AI research",
            "https://example.com/important",
            "article"
        )
        
        kb.update_relevance_score(kid, 0.9)
        entry = next(e for e in kb.entries if e["id"] == kid)
        assert entry["relevance_score"] == 0.9
    
    def test_update_relevance_invalid_entry(self, kb):
        """Updating non-existent entry should raise error"""
        with pytest.raises(KnowledgeBaseException):
            kb.update_relevance_score("INVALID_ID", 0.5)


class TestKnowledgeBasePersistence:
    """Test persistence operations"""
    
    def test_save_and_load(self):
        """Data should persist across save/load"""
        with patch('config.KNOWLEDGE_DIR', Path(tempfile.gettempdir())):
            # Create and populate
            kb1 = KnowledgeBase()
            kb1.add_knowledge(
                "This is test knowledge for persistence testing",
                "https://example.com/test",
                "article"
            )
            kb1.save_knowledge_base()
            
            # Load in new instance
            kb2 = KnowledgeBase()
            assert len(kb2.entries) == 1
            assert kb2.entries[0]["type"] == "article"


class TestKnowledgeBaseStatistics:
    """Test statistics and introspection"""
    
    @pytest.fixture
    def kb_with_data(self):
        """Knowledge base with sample data"""
        with patch('config.KNOWLEDGE_DIR', Path(tempfile.gettempdir())):
            kb = KnowledgeBase()
            kb.add_knowledge(
                "Article about machine learning fundamentals",
                "https://example.com/ml",
                "article"
            )
            kb.add_knowledge(
                "Link to research papers",
                "https://example.com/papers",
                "link"
            )
            yield kb
    
    def test_statistics(self, kb_with_data):
        """Statistics should be accurate"""
        stats = kb_with_data.get_statistics()
        
        assert stats["total_entries"] == 2
        assert "article" in stats["types"]
        assert "link" in stats["types"]
        assert stats["avg_access_count"] >= 0


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
