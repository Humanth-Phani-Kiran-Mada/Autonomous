"""
Validation utilities for the autonomous AI system.

Provides commonly used validation functions with clear error messages
and consistent error reporting.
"""
from typing import Any, Callable, List, Optional
from urllib.parse import urlparse
import config
from .exceptions import ValidationException
from .types_and_constants import SystemConstants
from .logger import logger


def validate_url(url: str) -> str:
    """
    Validate and normalize a URL.
    
    Args:
        url: URL string to validate
    
    Returns:
        Normalized URL
    
    Raises:
        ValidationException: If URL is invalid
    """
    if not isinstance(url, str):
        raise ValidationException(
            f"URL must be string, got {type(url).__name__}",
            error_code="INVALID_URL_TYPE"
        )
    
    if not url.strip():
        raise ValidationException("URL cannot be empty", error_code="EMPTY_URL")
    
    try:
        result = urlparse(url)
        if not all([result.scheme, result.netloc]):
            raise ValidationException(
                f"Invalid URL format: {url}",
                error_code="INVALID_URL_FORMAT"
            )
        return url.strip()
    except Exception as e:
        raise ValidationException(
            f"URL validation failed: {e}",
            error_code="URL_PARSE_ERROR"
        )


def validate_content(content: str, min_length: int = 1, max_length: Optional[int] = None) -> str:
    """
    Validate text content.
    
    Args:
        content: Content string to validate
        min_length: Minimum length required
        max_length: Maximum length allowed
    
    Returns:
        Validated content
    
    Raises:
        ValidationException: If validation fails
    """
    if not isinstance(content, str):
        raise ValidationException(
            f"Content must be string, got {type(content).__name__}",
            error_code="INVALID_CONTENT_TYPE"
        )
    
    if len(content) < min_length:
        raise ValidationException(
            f"Content is too short (minimum {min_length} characters)",
            error_code="CONTENT_TOO_SHORT"
        )
    
    if max_length and len(content) > max_length:
        raise ValidationException(
            f"Content exceeds maximum length ({max_length} characters)",
            error_code="CONTENT_TOO_LONG"
        )
    
    return content.strip()


def validate_skill_level(level: float) -> float:
    """
    Validate skill level (must be 0.0 to 1.0).
    
    Args:
        level: Skill level value
    
    Returns:
        Validated and clamped skill level
    
    Raises:
        ValidationException: If validation fails
    """
    if not isinstance(level, (int, float)):
        raise ValidationException(
            f"Skill level must be numeric, got {type(level).__name__}",
            error_code="INVALID_SKILL_TYPE"
        )
    
    clamped = max(min(float(level), 1.0), 0.0)
    if clamped != level:
        logger.warning(f"Skill level {level} was clamped to {clamped}")
    
    return clamped


def validate_priority(priority: float) -> float:
    """
    Validate priority level (must be 0.0 to 1.0).
    
    Args:
        priority: Priority value
    
    Returns:
        Validated priority
    
    Raises:
        ValidationException: If validation fails
    """
    if not isinstance(priority, (int, float)):
        raise ValidationException(
            f"Priority must be numeric, got {type(priority).__name__}",
            error_code="INVALID_PRIORITY_TYPE"
        )
    
    if not 0.0 <= priority <= 1.0:
        raise ValidationException(
            f"Priority must be between 0.0 and 1.0, got {priority}",
            error_code="PRIORITY_OUT_OF_RANGE"
        )
    
    return float(priority)


def validate_memory_key(key: str) -> str:
    """
    Validate memory key format.
    
    Args:
        key: Memory key to validate
    
    Returns:
        Validated key
    
    Raises:
        ValidationException: If key is invalid
    """
    if not isinstance(key, str):
        raise ValidationException(
            f"Memory key must be string, got {type(key).__name__}",
            error_code="INVALID_KEY_TYPE"
        )
    
    if not key.strip():
        raise ValidationException("Memory key cannot be empty", error_code="EMPTY_KEY")
    
    if len(key) > 256:
        raise ValidationException(
            "Memory key exceeds maximum length (256 characters)",
            error_code="KEY_TOO_LONG"
        )
    
    return key.strip()


def validate_goal_name(name: str) -> str:
    """
    Validate goal name.
    
    Args:
        name: Goal name to validate
    
    Returns:
        Validated name
    
    Raises:
        ValidationException: If name is invalid
    """
    if not isinstance(name, str):
        raise ValidationException(
            f"Goal name must be string, got {type(name).__name__}",
            error_code="INVALID_GOAL_NAME_TYPE"
        )
    
    if not name.strip():
        raise ValidationException("Goal name cannot be empty", error_code="EMPTY_GOAL_NAME")
    
    if len(name) < 3:
        raise ValidationException(
            "Goal name must be at least 3 characters",
            error_code="GOAL_NAME_TOO_SHORT"
        )
    
    if len(name) > 128:
        raise ValidationException(
            "Goal name exceeds maximum length (128 characters)",
            error_code="GOAL_NAME_TOO_LONG"
        )
    
    return name.strip()


def validate_knowledge_type(ktype: str) -> str:
    """
    Validate knowledge type.
    
    Args:
        ktype: Knowledge type to validate
    
    Returns:
        Validated knowledge type
    
    Raises:
        ValidationException: If type is invalid
    """
    valid_types = ["article", "link", "header", "concept", "pattern", "skill", "theory"]
    
    if not isinstance(ktype, str):
        raise ValidationException(
            f"Knowledge type must be string, got {type(ktype).__name__}",
            error_code="INVALID_KTYPE_TYPE"
        )
    
    if ktype not in valid_types:
        raise ValidationException(
            f"Invalid knowledge type: {ktype}. Must be one of {valid_types}",
            error_code="INVALID_KTYPE_VALUE"
        )
    
    return ktype


def validate_batch_size(size: int) -> int:
    """
    Validate batch size.
    
    Args:
        size: Batch size to validate
    
    Returns:
        Validated batch size
    
    Raises:
        ValidationException: If size is invalid
    """
    if not isinstance(size, int):
        raise ValidationException(
            f"Batch size must be integer, got {type(size).__name__}",
            error_code="INVALID_BATCH_SIZE_TYPE"
        )
    
    if size <= 0:
        raise ValidationException(
            f"Batch size must be positive, got {size}",
            error_code="BATCH_SIZE_INVALID"
        )
    
    if size > 10000:
        raise ValidationException(
            f"Batch size exceeds reasonable maximum (10000), got {size}",
            error_code="BATCH_SIZE_TOO_LARGE"
        )
    
    return size


def validate_timeout(timeout: float) -> float:
    """
    Validate timeout value.
    
    Args:
        timeout: Timeout in seconds
    
    Returns:
        Validated timeout
    
    Raises:
        ValidationException: If timeout is invalid
    """
    if not isinstance(timeout, (int, float)):
        raise ValidationException(
            f"Timeout must be numeric, got {type(timeout).__name__}",
            error_code="INVALID_TIMEOUT_TYPE"
        )
    
    if timeout <= 0:
        raise ValidationException(
            f"Timeout must be positive, got {timeout}",
            error_code="TIMEOUT_INVALID"
        )
    
    if timeout > 86400:  # 24 hours
        raise ValidationException(
            f"Timeout exceeds reasonable maximum (86400s), got {timeout}",
            error_code="TIMEOUT_TOO_LARGE"
        )
    
    return float(timeout)


def validate_metadata(metadata: dict) -> dict:
    """
    Validate metadata dictionary.
    
    Args:
        metadata: Metadata dict to validate
    
    Returns:
        Validated metadata
    
    Raises:
        ValidationException: If metadata is invalid
    """
    if not isinstance(metadata, dict):
        raise ValidationException(
            f"Metadata must be dictionary, got {type(metadata).__name__}",
            error_code="INVALID_METADATA_TYPE"
        )
    
    if len(metadata) > 100:
        raise ValidationException(
            "Metadata exceeds maximum number of entries (100)",
            error_code="METADATA_TOO_LARGE"
        )
    
    return metadata


class ValidationChain:
    """
    Fluent validation builder for complex validation scenarios.
    
    Example:
        result = (ValidationChain()
                 .validate(url, validate_url, "URL")
                 .validate(content, validate_content, "Content")
                 .validate(priority, validate_priority, "Priority")
                 .execute())
    """
    
    def __init__(self):
        self.validators: List[tuple[Any, Callable, str]] = []
    
    def validate(self, value: Any, validator: Callable, name: str) -> "ValidationChain":
        """Add a validation step"""
        self.validators.append((value, validator, name))
        return self
    
    def execute(self) -> Any:
        """Execute all validations"""
        results = []
        for value, validator, name in self.validators:
            try:
                result = validator(value)
                results.append(result)
                logger.debug(f"✓ Validation passed: {name}")
            except ValidationException as e:
                logger.error(f"✗ Validation failed: {name} - {e.message}")
                raise
        return results if len(results) > 1 else results[0] if results else None
