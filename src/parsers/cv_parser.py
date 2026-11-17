import json
import re
from typing import Any, Dict
from openai import OpenAI

from src.config.settings import LLM_API_KEY, LLM_BASE_URL, LLM_MODEL, OPENAI_API_KEY
from src.memory.cv_store import save_cv
from src.parsers.cv_extractor import extract_cv_text

SYSTEM_PROMPT = """You are an expert CV parser. Analyze the provided CV text and extract structured information.

Return ONLY a raw JSON object with no markdown formatting, no explanation, and no code fences.
The JSON object must contain exactly the following fields:
- name: Candidate's full name (string)
- email: Candidate's email address (string or "")
- phone: Candidate's phone number (string or "")
- location: Candidate's location / city, country (string or "")
- summary: A concise professional summary of the candidate (string)
- skills: A list of candidate skills (list of strings)
- experience: A list of work experience objects, each with:
    - title: Job title (string)
    - company: Company name (string)
    - duration: Dates or duration of employment (string)
    - description: Summary of responsibilities and achievements (string)
- education: A list of education objects, each with:
    - degree: Degree or certification title (string)
    - institution: University or institution name (string)
    - year: Graduation year or years attended (string)
- preferred_roles: A list of target job roles inferred from the CV (list of strings)
- preferred_industries: A list of target industries inferred from the CV (list of strings)
- experience_level: Inferred candidate seniority level, exactly one of: 'Intern / Student', 'Fresh Graduate / Entry Level', 'Junior (1-2 years)', 'Mid-Level (3-5 years)', 'Senior (5+ years)' (string)
"""


def parse_cv_text(raw_text: str) -> Dict[str, Any]:
    """
    Send extracted CV text to the LLM (Groq or OpenAI) and parse the response into a structured dictionary.

    Args:
        raw_text: Full raw text extracted from a CV.

    Returns:
        dict: Parsed CV details matching the specified JSON structure.

    Raises:
        ValueError: If raw_text is empty or if JSON parsing fails.
    """
    if not raw_text or not raw_text.strip():
        raise ValueError("Cannot parse CV: Extracted text is empty.")

    client = OpenAI(api_key=LLM_API_KEY, base_url=LLM_BASE_URL)

    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"Extract structured candidate information from this CV:\n\n{raw_text}",
            },
        ],
        temperature=0.0,
        response_format={"type": "json_object"},
    )

    raw_response = response.choices[0].message.content or ""

    # Strip accidental markdown code fences if present
    cleaned_content = raw_response.strip()
    fence_match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", cleaned_content)
    if fence_match:
        cleaned_content = fence_match.group(1).strip()
    elif cleaned_content.startswith("```"):
        cleaned_content = re.sub(r"^```(?:json)?\s*", "", cleaned_content)
        cleaned_content = re.sub(r"\s*```$", "", cleaned_content).strip()

    try:
        parsed_data = json.loads(cleaned_content)
    except json.JSONDecodeError as err:
        raise ValueError(
            f"Failed to parse CV JSON from model response: {err}\n"
            f"Raw response:\n{raw_response}"
        ) from err

    candidate_name = parsed_data.get("name", "Unknown Candidate")
    print(f"Successfully parsed CV for candidate: {candidate_name}")
    return parsed_data


def ingest_cv(uploaded_file) -> Dict[str, Any]:
    """
    Main ingest pipeline for CV processing:
    1. Extracts text from the uploaded file (PDF or DOCX).
    2. Parses the raw text into structured data using the configured LLM.
    3. Saves the parsed result into cv_store.
    4. Returns the parsed CV dictionary.

    Args:
        uploaded_file: Streamlit UploadedFile object or file-like object.

    Returns:
        dict: Parsed CV data dictionary.
    """
    raw_text = extract_cv_text(uploaded_file)
    cv_data = parse_cv_text(raw_text)
    save_cv(cv_data)
    return cv_data


# Aliases
parse_cv = parse_cv_text
ingest = ingest_cv
