# Internal variable to hold the CV in memory
_cv_data = None

def save_cv(cv_dict: dict) -> None:
    """Save a CV dictionary in memory."""
    global _cv_data
    _cv_data = cv_dict

def get_cv() -> dict:
    """Retrieve the saved CV dictionary from memory."""
    return _cv_data

def clear_cv() -> None:
    """Clear the CV dictionary from memory."""
    global _cv_data
    _cv_data = None

def is_cv_loaded() -> bool:
    """Return True if a CV is currently loaded, otherwise False."""
    return _cv_data is not None
