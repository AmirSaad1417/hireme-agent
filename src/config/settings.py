import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from local .env file if present
_env_path = Path(__file__).resolve().parent.parent.parent / ".env"
if _env_path.exists():
    load_dotenv(dotenv_path=_env_path)
else:
    load_dotenv()


def _get_config(key: str, default: str = "") -> str:
    """Retrieve configuration from Streamlit Cloud secrets first, then OS environment."""
    try:
        import streamlit as st
        if hasattr(st, "secrets") and key in st.secrets:
            return str(st.secrets[key]).strip()
    except Exception:
        pass
    val = os.getenv(key)
    return val.strip() if val else default


GROQ_API_KEY = _get_config("GROQ_API_KEY")
OPENAI_API_KEY = _get_config("OPENAI_API_KEY")
ADZUNA_APP_ID = _get_config("ADZUNA_APP_ID")
ADZUNA_APP_KEY = _get_config("ADZUNA_APP_KEY")
ADZUNA_COUNTRY = _get_config("ADZUNA_COUNTRY", "gb")

# Determine primary LLM provider (Groq or OpenAI)
if GROQ_API_KEY and not GROQ_API_KEY.startswith("your_"):
    LLM_PROVIDER = "groq"
    LLM_API_KEY = GROQ_API_KEY
    LLM_BASE_URL = "https://api.groq.com/openai/v1"
    LLM_MODEL = "openai/gpt-oss-120b"
    # Ensure OPENAI_API_KEY is non-empty for backwards compatibility if needed
    if not OPENAI_API_KEY:
        OPENAI_API_KEY = GROQ_API_KEY
elif OPENAI_API_KEY and not OPENAI_API_KEY.startswith("your_"):
    LLM_PROVIDER = "openai"
    LLM_API_KEY = OPENAI_API_KEY
    LLM_BASE_URL = None
    LLM_MODEL = "gpt-4o"
else:
    # Default to Groq if placeholder or fallback
    LLM_PROVIDER = "groq" if GROQ_API_KEY else "openai"
    LLM_API_KEY = GROQ_API_KEY or OPENAI_API_KEY
    LLM_BASE_URL = "https://api.groq.com/openai/v1" if GROQ_API_KEY else None
    LLM_MODEL = "openai/gpt-oss-120b" if GROQ_API_KEY else "gpt-4o"

# Validate required variables
_missing_keys = []
if not LLM_API_KEY:
    _missing_keys.append("GROQ_API_KEY or OPENAI_API_KEY")
if not ADZUNA_APP_ID:
    _missing_keys.append("ADZUNA_APP_ID")
if not ADZUNA_APP_KEY:
    _missing_keys.append("ADZUNA_APP_KEY")

if _missing_keys:
    raise EnvironmentError(
        f"Missing required environment variable(s): {', '.join(_missing_keys)}"
    )
