from typing import Any, Dict, Optional

_cv_data: Optional[Dict[str, Any]] = None


def save_cv(cv: Dict[str, Any]) -> None:
    """Save a CV dictionary to memory."""
    global _cv_data
    _cv_data = cv


def get_cv() -> Optional[Dict[str, Any]]:
    """Retrieve the stored CV dictionary from memory."""
    return _cv_data


def clear_cv() -> None:
    """Clear the stored CV dictionary from memory."""
    global _cv_data
    _cv_data = None


def is_cv_loaded() -> bool:
    """Return True if a CV is currently loaded in memory, False otherwise."""
    return _cv_data is not None


# Aliases for flexibility
save_cv_data = save_cv
get_cv_data = get_cv
clear_cv_data = clear_cv
has_cv = is_cv_loaded
