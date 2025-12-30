"""
Data cleaning functions for paper data.
论文数据清洗函数
"""

import json
import re
from typing import Any, Union


def clean_keywords(raw: Union[str, list[str], None]) -> list[str]:
    """
    Clean and parse keywords from raw data.
    
    Handles:
    - JSON string format: '["keyword1", "keyword2"]'
    - Already parsed list
    - Empty/None values
    - Malformed JSON
    
    Args:
        raw: Raw keywords data (string, list, or None)
        
    Returns:
        List of cleaned keyword strings
    """
    if raw is None:
        return []
    
    if isinstance(raw, list):
        return [str(k).strip() for k in raw if k]
    
    if not isinstance(raw, str):
        return []
    
    raw = raw.strip()
    if not raw:
        return []
    
    # Try to parse as JSON
    try:
        parsed = json.loads(raw)
        if isinstance(parsed, list):
            return [str(k).strip() for k in parsed if k]
        return []
    except (json.JSONDecodeError, TypeError):
        return []


def clean_abstract(raw: Union[str, None]) -> str:
    """
    Clean abstract text by removing extra whitespace.
    
    Args:
        raw: Raw abstract text or None
        
    Returns:
        Cleaned abstract string
    """
    if raw is None:
        return ""
    
    if not isinstance(raw, str):
        return str(raw)
    
    # Replace multiple whitespace with single space
    cleaned = re.sub(r'\s+', ' ', raw)
    # Strip leading/trailing whitespace
    cleaned = cleaned.strip()
    
    return cleaned


def clean_title(raw: Union[str, None]) -> str:
    """
    Clean paper title.
    
    Args:
        raw: Raw title text or None
        
    Returns:
        Cleaned title string
    """
    if raw is None:
        return ""
    
    if not isinstance(raw, str):
        return str(raw)
    
    # Remove extra whitespace
    cleaned = re.sub(r'\s+', ' ', raw)
    return cleaned.strip()


def safe_int(value: Any, default: int = 0) -> int:
    """
    Safely convert value to integer.
    
    Args:
        value: Value to convert
        default: Default value if conversion fails
        
    Returns:
        Integer value
    """
    if value is None:
        return default
    
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


def safe_str(value: Any, default: str = "") -> str:
    """
    Safely convert value to string.
    
    Args:
        value: Value to convert
        default: Default value if None
        
    Returns:
        String value
    """
    if value is None:
        return default
    
    return str(value).strip()
