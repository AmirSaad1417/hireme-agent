import os
from dotenv import load_dotenv

# Load all four environment variables from .env
load_dotenv()

# Retrieve keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY")
ADZUNA_COUNTRY = os.getenv("ADZUNA_COUNTRY")
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

# Check if any of the first three keys are missing
missing_keys = []
if not GROQ_API_KEY or GROQ_API_KEY.strip() == "":
    missing_keys.append("GROQ_API_KEY")
if not ADZUNA_APP_ID or ADZUNA_APP_ID.strip() == "":
    missing_keys.append("ADZUNA_APP_ID")
if not ADZUNA_APP_KEY or ADZUNA_APP_KEY.strip() == "":
    missing_keys.append("ADZUNA_APP_KEY")

if missing_keys:
    raise EnvironmentError(
        f"The following required environment variables are missing from configuration: {', '.join(missing_keys)}"
    )

# Default ADZUNA_COUNTRY to "gb" if not set
if not ADZUNA_COUNTRY or ADZUNA_COUNTRY.strip() == "":
    ADZUNA_COUNTRY = "gb"
else:
    ADZUNA_COUNTRY = ADZUNA_COUNTRY.strip()
