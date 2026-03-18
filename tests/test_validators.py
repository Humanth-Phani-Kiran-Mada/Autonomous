"""
Unit tests for validators module

Tests cover all validation functions with various input cases:
- Valid inputs (pass)
- Invalid inputs (raise)
- Edge cases (boundaries)
- Type handling
"""

import pytest
from src.validators import (
    validate_url, validate_content, validate_skill_level,
    validate_priority, validate_numeric_range, validate_list_items
)
from src.exceptions import ValidationException


class TestURLValidation:
    """Tests for URL validation function"""
    
    def test_valid_urls(self):
        """URLs with http/https should be valid"""
        assert validate_url("https://example.com")
        assert validate_url("http://sub.example.co.uk")
        assert validate_url("https://example.com/path?query=1")
    
    def test_invalid_urls(self):
        """Invalid URLs should raise ValidationException"""
        with pytest.raises(ValidationException):
            validate_url("not a url")
        with pytest.raises(ValidationException):
            validate_url("ftp://example.com")  # Only http/https
    
    def test_url_normalization(self):
        """URLs should be normalized"""
        result = validate_url("HTTPS://EXAMPLE.COM")
        assert result == result.lower()


class TestContentValidation:
    """Tests for content validation"""
    
    def test_valid_content(self):
        """Non-empty strings pass validation"""
        assert validate_content("Valid content")
        assert validate_content("x")  # Single character ok
    
    def test_empty_content(self):
        """Empty strings should raise"""
        with pytest.raises(ValidationException):
            validate_content("")
    
    def test_content_length_constraints(self):
        """Custom length constraints"""
        with pytest.raises(ValidationException):
            validate_content("short", min_length=10)
        
        result = validate_content("valid length", min_length=5)
        assert result == "valid length"


class TestSkillLevelValidation:
    """Tests for skill level (0.0 to 1.0)"""
    
    def test_valid_skill_levels(self):
        """Values in [0.0, 1.0] should pass"""
        assert validate_skill_level(0.0) == 0.0
        assert validate_skill_level(0.5) == 0.5
        assert validate_skill_level(1.0) == 1.0
    
    def test_out_of_range_levels(self):
        """Values outside [0.0, 1.0] should be clamped"""
        assert validate_skill_level(-0.5) == 0.0
        assert validate_skill_level(1.5) == 1.0
    
    def test_invalid_type(self):
        """Non-numeric values should raise"""
        with pytest.raises(ValidationException):
            validate_skill_level("not a number")


class TestPriorityValidation:
    """Tests for priority (0.0 to 1.0)"""
    
    def test_valid_priorities(self):
        """Values in [0.0, 1.0] pass"""
        assert validate_priority(0.0) == 0.0
        assert validate_priority(0.5) == 0.5
        assert validate_priority(1.0) == 1.0
    
    def test_priority_clamping(self):
        """Out of range automatically clamped"""
        assert validate_priority(-1.0) == 0.0
        assert validate_priority(2.0) == 1.0


class TestNumericRangeValidation:
    """Tests for generic numeric range validation"""
    
    def test_within_range(self):
        """Values within range pass"""
        result = validate_numeric_range(5, min_val=0, max_val=10)
        assert result == 5
    
    def test_outside_range_raises(self):
        """Values outside range raise error"""
        with pytest.raises(ValidationException):
            validate_numeric_range(15, min_val=0, max_val=10)
    
    def test_boundary_values(self):
        """Boundary values included"""
        assert validate_numeric_range(0, min_val=0, max_val=10) == 0
        assert validate_numeric_range(10, min_val=0, max_val=10) == 10


class TestListValidation:
    """Tests for list item validation"""
    
    def test_valid_list(self):
        """Valid items pass"""
        items = ["url1", "url2"]
        result = validate_list_items(items, validator=validate_url, min_length=1)
        assert len(result) == 2
    
    def test_invalid_items_in_list(self):
        """Invalid items raise"""
        items = ["valid_url.com", "invalid item"]
        with pytest.raises(ValidationException):
            validate_list_items(items, validator=validate_url)
    
    def test_empty_list(self):
        """Empty list below minimum"""
        with pytest.raises(ValidationException):
            validate_list_items([], validator=validate_url, min_length=1)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
