import json
import re
from typing import Any, Dict, List, Optional
from openai import OpenAI

from src.config import settings
from src.config.settings import LLM_API_KEY, LLM_BASE_URL, LLM_MODEL
from src.memory.cv_store import get_cv, is_cv_loaded
from src.tools import TOOL_DEFINITIONS, execute_tool

SYSTEM_PROMPT = """You are an ultra-fast, expert AI job hunting assistant.
Your mission is to find the best live job vacancies matching the candidate's profile, seniority, and preferences, and immediately write a highly tailored, compelling cover letter for each.

You must follow this fast 2-step sequence:
1. Review the candidate's profile, target experience level, and remote preference:
   - Pick ONE single concise search query (1-4 words) matching their exact career stage:
     * For "Intern / Student": choose internship/trainee titles (e.g. "Software Engineer Intern", "Python Intern", "Data Science Intern").
     * For "Fresh Graduate / Entry Level": choose graduate/junior titles (e.g. "Junior Python Developer", "Graduate Software Engineer", "Entry Level Developer").
     * For "Junior": choose junior titles (e.g. "Junior Developer", "Junior Data Analyst").
     * For "Senior": choose senior titles (e.g. "Senior Python Developer", "Lead Engineer").
   - If Remote work is requested, append "Remote" to the query (e.g. "Software Engineer Intern Remote", "Junior Python Developer Remote").
   - Hard rule: Never pass multiple comma-separated roles or long descriptions as query.
2. Call search_jobs (or job_search) ONCE using that single concise job title as query, along with the location and count.
3. Immediately use the returned job titles, companies, salaries, locations, and descriptions to write a tailored 3-paragraph cover letter for each job.
4. Return your final response immediately as a raw JSON array.

Cover Letter Rules:
- Address the specific company and job title by name.
- Tailor the pitch to their career stage:
  * For students and fresh graduates: emphasize academic projects, capstones, coursework, hunger to learn, and foundational skills.
  * For experienced candidates: emphasize measurable impact, system delivery, and domain expertise.
- Only use skills and experience actually present in the candidate's CV (no fabrication).
- Write exactly 3 paragraphs: opening, value pitch, closing.
- Use a professional but warm tone. Avoid cliché phrases like "I am writing to apply".

Final Response Format:
Return your response as a raw JSON array ONLY, with no markdown, no code fences, and no extra explanation.
Each item in the JSON array must contain exactly these keys:
- job_title: The title of the job (string)
- company: The hiring company name (string)
- location: The job location (string)
- salary: Salary range or "Not specified" (string)
- job_url: Direct link to the job listing (string)
- description: Summary of job requirements and responsibilities (string)
- cover_letter: The tailored 3-paragraph cover letter (string)
"""


def run_agent(
    location: str = "",
    count: int = 3,
    experience_level: str = "Auto-detect",
    remote_only: bool = False,
    country: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Run the ultra-fast end-to-end job hunting agent loop with instant Adzuna job descriptions,
    seniority level matching (Student/Intern, Fresh Graduate, Junior, Senior),
    and Remote preference support.

    Args:
        location: Target location for job search (e.g. 'London', 'Remote', or '').
        count: Desired number of job vacancies to search for.
        experience_level: Seniority tier ('Intern / Student', 'Fresh Graduate / Entry Level', 'Junior', 'Senior', etc.).
        remote_only: Whether the user wants 100% remote / work-from-home vacancies.
        country: Two-letter country code ('gb', 'us', 'ca', 'de', 'in', etc.).

    Returns:
        list of dict: Recommended jobs with tailored cover letters.

    Raises:
        ValueError: If no CV has been loaded in cv_store.
        RuntimeError: If the agent loop fails to reach a final response within 15 iterations.
    """
    if not is_cv_loaded():
        raise ValueError("No CV has been loaded. Please upload and parse a CV before running the agent.")

    cv = get_cv()
    if not cv:
        raise ValueError("CV data in memory is empty. Please upload and parse a valid CV.")

    # Configure active country in settings for tools
    if country:
        settings.ADZUNA_COUNTRY = country.lower().strip()

    candidate_name = cv.get("name", "Candidate")
    summary = cv.get("summary", "")
    skills = cv.get("skills", [])
    preferred_roles = cv.get("preferred_roles", [])
    experience = cv.get("experience", [])
    education = cv.get("education", [])
    detected_level = cv.get("experience_level", "Fresh Graduate / Entry Level")

    # Resolve effective experience level
    if not experience_level or experience_level == "Auto-detect" or experience_level == "Auto-detect from CV":
        effective_level = detected_level
    else:
        effective_level = experience_level

    # Resolve effective location
    if remote_only:
        search_loc = "Remote"
    else:
        search_loc = location if location else "Any / Nationwide"

    user_message = f"""Candidate Profile:
- Name: {candidate_name}
- Career Stage / Experience Level: {effective_level}
- Summary: {summary}
- Preferred Roles: {json.dumps(preferred_roles)}
- Skills: {json.dumps(skills)}
- Work Experience: {json.dumps(experience, indent=2)}
- Education: {json.dumps(education, indent=2)}

Search Requirements:
- Experience Level Target: {effective_level} (Crucial: search for roles matching this seniority, e.g. Intern, Junior, Graduate, or Senior)
- Remote Preference: {'Remote / Work From Home Only' if remote_only else 'Onsite / Hybrid / Any'}
- Target Location: {search_loc}
- Target Country: {(country or settings.ADZUNA_COUNTRY or 'gb').upper()}
- Results Count: {count}

Instruction:
1. Pick ONE single concise job title query aligned with the candidate's career level ({effective_level}) and remote preference.
2. Call search_jobs immediately.
3. Once results are returned, write the tailored cover letters right away using the provided job details.
"""

    messages: List[Dict[str, Any]] = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message},
    ]

    max_iterations = 4
    client = OpenAI(api_key=LLM_API_KEY, base_url=LLM_BASE_URL)

    # Pass search tool directly to ensure instant execution
    active_tools = [t for t in TOOL_DEFINITIONS if t["function"]["name"] == "job_search"]
    if not active_tools:
        active_tools = TOOL_DEFINITIONS

    active_model = LLM_MODEL or "openai/gpt-oss-20b"

    for iteration in range(1, max_iterations + 1):
        print(f"Agent iteration {iteration}/{max_iterations}")

        # Always provide tools so Groq never rejects with 'Tool choice is none'
        api_kwargs: Dict[str, Any] = {
            "model": active_model,
            "messages": messages,
            "tools": active_tools,
            "tool_choice": "auto",
            "temperature": 0.3,
        }

        try:
            response = client.chat.completions.create(**api_kwargs)
        except Exception as err:
            err_str = str(err).lower()
            from src.config.settings import GEMINI_API_KEY
            # If 429 rate limit hit on 120b, try 20b model first
            if ("429" in err_str or "rate limit" in err_str) and active_model != "openai/gpt-oss-20b":
                print(f"Switching from {active_model} to openai/gpt-oss-20b due to rate limits...")
                active_model = "openai/gpt-oss-20b"
                api_kwargs["model"] = active_model
                try:
                    response = client.chat.completions.create(**api_kwargs)
                except Exception as inner_err:
                    if GEMINI_API_KEY:
                        print(f"Both Groq models capped, seamlessly failing over agent to Google Gemini...")
                        gemini_client = OpenAI(
                            api_key=GEMINI_API_KEY,
                            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
                        )
                        active_model = "gemini-3.5-flash-lite"
                        api_kwargs["model"] = active_model
                        response = gemini_client.chat.completions.create(**api_kwargs)
                    else:
                        raise inner_err
            elif ("429" in err_str or "rate limit" in err_str or "quota" in err_str) and GEMINI_API_KEY:
                print(f"Groq rate limit hit. Seamlessly failing over agent to Google Gemini...")
                gemini_client = OpenAI(
                    api_key=GEMINI_API_KEY,
                    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
                )
                active_model = "gemini-3.5-flash-lite"
                api_kwargs["model"] = active_model
                response = gemini_client.chat.completions.create(**api_kwargs)
            else:
                raise err

        message = response.choices[0].message

        # Check for tool calls
        if message.tool_calls:
            messages.append(message)

            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name
                raw_args = tool_call.function.arguments or "{}"
                try:
                    args = json.loads(raw_args)
                except json.JSONDecodeError:
                    args = {}

                # Inject remote_only if requested by user and not present
                if remote_only and "remote_only" not in args:
                    args["remote_only"] = True

                print(f"Iteration {iteration}: Calling tool '{tool_name}' with args {args}")
                tool_result = execute_tool(tool_name, args)

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_name,
                    "content": tool_result,
                })

            # Explicit guidance for next turn to write cover letters immediately
            messages.append({
                "role": "user",
                "content": "Vacancies retrieved. Now write a tailored 3-paragraph cover letter for each job above and return ONLY the final JSON array. Do not call any further tools.",
            })
            continue

        # If no tool calls, check for final response
        content = message.content or ""
        if content.strip():
            print(f"Iteration {iteration}: Received final response from model.")
            cleaned = content.strip()

            # Strip accidental markdown code blocks if present
            fence_match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", cleaned)
            if fence_match:
                cleaned = fence_match.group(1).strip()
            elif cleaned.startswith("```"):
                cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
                cleaned = re.sub(r"\s*```$", "", cleaned).strip()

            try:
                parsed = json.loads(cleaned)
                if isinstance(parsed, list):
                    print(f"Agent finished successfully with {len(parsed)} job recommendation(s).")
                    return parsed
                elif isinstance(parsed, dict) and "jobs" in parsed and isinstance(parsed["jobs"], list):
                    return parsed["jobs"]
                elif isinstance(parsed, dict):
                    return [parsed]
            except json.JSONDecodeError as err:
                print(f"Warning: Failed to parse JSON on iteration {iteration}: {err}")
                # Try finding a bracketed array
                array_match = re.search(r"\[[\s\S]*\]", cleaned)
                if array_match:
                    try:
                        parsed_arr = json.loads(array_match.group(0))
                        if isinstance(parsed_arr, list):
                            return parsed_arr
                    except Exception:
                        pass

                messages.append(message)
                messages.append({
                    "role": "user",
                    "content": "Your previous response was not valid JSON. Please return ONLY a raw JSON array containing the job objects.",
                })
                continue

    raise RuntimeError(
        f"Agent failed to produce a final valid response within {max_iterations} iterations."
    )
