import re
from typing import Any, Dict, List, Optional
import requests

from src.config.settings import ADZUNA_APP_ID, ADZUNA_APP_KEY, ADZUNA_COUNTRY


def search_jobs(
    query: str,
    location: str = "",
    count: int = 3,
    country: Optional[str] = None,
    remote_only: bool = False,
) -> List[Dict[str, Any]]:
    """
    Search for job listings using the Adzuna API with smart multi-tier fallback
    to ensure rapid, instant returns without empty-result retry loops.

    Args:
        query: Search keywords or job title (e.g. 'Software Engineer Intern', 'Junior Python Developer').
        location: City, region, or location filter.
        count: Number of job listings to retrieve.
        country: Two-letter country code (e.g. 'gb', 'us', 'ca', 'de', 'in'). Defaults to ADZUNA_COUNTRY.
        remote_only: Whether to search for remote vacancies.

    Returns:
        list of dict: Clean list of job dictionaries, or empty list on complete failure.
    """
    target_country = (country or ADZUNA_COUNTRY or "gb").lower().strip()
    endpoint = f"https://api.adzuna.com/v1/api/jobs/{target_country}/search/1"

    loc_clean = (location or "").strip()
    is_remote = remote_only or loc_clean.lower() == "remote" or "remote" in loc_clean.lower()

    effective_query = query.strip()
    if is_remote and "remote" not in effective_query.lower():
        effective_query = f"{effective_query} Remote"

    def _fetch(q: str, loc: str) -> List[Dict[str, Any]]:
        params: Dict[str, Any] = {
            "app_id": ADZUNA_APP_ID,
            "app_key": ADZUNA_APP_KEY,
            "results_per_page": count,
            "what": q,
            "content-type": "application/json",
        }
        if loc and loc.lower() != "remote":
            params["where"] = loc

        try:
            resp = requests.get(endpoint, params=params, timeout=6)
            if resp.status_code == 200:
                return resp.json().get("results", [])
        except Exception:
            pass
        return []

    # Attempt 1: with effective query
    raw_results = _fetch(effective_query, loc_clean)

    # Attempt 2: if 0 results and remote was appended, try base query
    if not raw_results and is_remote and effective_query != query.strip():
        raw_results = _fetch(query.strip(), loc_clean)

    # Attempt 3: if still 0 and query has more than 2 words, try simplified 2-word query
    if not raw_results:
        words = query.strip().split()
        if len(words) > 2:
            raw_results = _fetch(" ".join(words[:2]), loc_clean)

    if not raw_results:
        print(f"Warning: Adzuna API returned 0 job listings for query='{effective_query}', country='{target_country}'.")
        return []

    jobs: List[Dict[str, Any]] = []
    for item in raw_results:
        # Format salary range
        salary_min = item.get("salary_min")
        salary_max = item.get("salary_max")
        if salary_min is not None and salary_max is not None:
            if salary_min == salary_max:
                salary = f"{salary_min:,.0f}"
            else:
                salary = f"{salary_min:,.0f} - {salary_max:,.0f}"
        elif salary_min is not None:
            salary = f"From {salary_min:,.0f}"
        elif salary_max is not None:
            salary = f"Up to {salary_max:,.0f}"
        else:
            salary = "Not specified"

        # Clean description and cap at 600 characters
        raw_desc = item.get("description", "") or ""
        clean_desc = re.sub(r"<[^>]+>", " ", raw_desc)
        clean_desc = re.sub(r"\s+", " ", clean_desc).strip()
        if len(clean_desc) > 600:
            clean_desc = clean_desc[:600]

        company_name = item.get("company", {}).get("display_name", "Unknown")
        loc_display = item.get("location", {}).get("display_name", "Unknown")
        job_url = item.get("redirect_url", "")

        jobs.append({
            "id": str(item.get("id", "")),
            "title": item.get("title", "").strip(),
            "company": company_name,
            "company_name": company_name,
            "location": loc_display,
            "salary": salary,
            "salary_range": salary,
            "description": clean_desc,
            "url": job_url,
            "job_url": job_url,
            "country": target_country.upper(),
        })

    print(f"Found {len(jobs)} job(s) for query='{effective_query}', country='{target_country}', location='{loc_clean}'")
    return jobs


# Alias
job_search = search_jobs
