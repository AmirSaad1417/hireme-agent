import requests
from src.config import settings
from typing import List, Dict, Any

def search_adzuna_jobs(query: str, location: str = "", count: int = 5, country: str = "") -> List[Dict[str, Any]]:
    """
    Query the Adzuna API for job recommendations based on key phrases and location.
    
    Parameters:
        query (str): Job role or key skills to search for (maps to 'what').
        location (str): Target city or region (maps to 'where').
        count (int): Max number of job recommendations to fetch.
        country (str): The country code of the Adzuna site to query.
        
    Returns:
        List[Dict[str, Any]]: List of normalized job matching dicts.
    """
    # Fetch country code from parameter or settings, default to "gb"
    country_code = country or settings.ADZUNA_COUNTRY or "gb"
    
    # Adzuna search endpoint (Querying page 1)
    url = f"https://api.adzuna.com/v1/api/jobs/{country_code.lower()}/search/1"
    
    # Build query parameters
    params = {
        "app_id": settings.ADZUNA_APP_ID,
        "app_key": settings.ADZUNA_APP_KEY,
        "results_per_page": count,
        "what": query,
        "content-type": "application/json"
    }
    
    # Filter by location if specified
    if location and location.strip():
        params["where"] = location.strip()
        
    try:
        response = requests.get(url, params=params, timeout=10)
        
        # Handle non-200 responses
        if response.status_code != 200:
            raise RuntimeError(
                f"Adzuna API responded with status code {response.status_code}. "
                f"Response body: {response.text}"
            )
            
        data = response.json()
        results = data.get("results", [])
        
        # Normalize and filter job objects
        jobs = []
        for item in results:
            company_name = item.get("company", {}).get("display_name", "Unknown Company")
            location_name = item.get("location", {}).get("display_name", "Unknown Location")
            
            jobs.append({
                "id": str(item.get("id")),
                "title": item.get("title", "Job Opportunity"),
                "company": company_name,
                "location": location_name,
                "salary_min": item.get("salary_min"),
                "salary_max": item.get("salary_max"),
                "description": item.get("description", ""),
                "url": item.get("redirect_url", ""),
                "created": item.get("created", "")
            })
            
        return jobs
        
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Network error communicating with Adzuna: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Unexpected error fetching jobs: {str(e)}")

def search_jsearch_jobs(query: str, location: str = "", count: int = 5, api_key: str = "") -> List[Dict[str, Any]]:
    """
    Query the JSearch API (via RapidAPI) for jobs matching LinkedIn, Indeed, etc.
    """
    active_key = api_key or settings.RAPIDAPI_KEY
    if not active_key or not active_key.strip():
        raise ValueError("RapidAPI key is not configured in environment or Streamlit secrets.")
        
    url = "https://jsearch.p.rapidapi.com/search"
    
    # Combine query and location for JSearch
    full_query = query
    if location and location.strip():
        full_query = f"{query} in {location}"
        
    headers = {
        "x-rapidapi-key": active_key,
        "x-rapidapi-host": "jsearch.p.rapidapi.com"
    }
    
    params = {
        "query": full_query,
        "page": "1",
        "num_pages": "1"
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=12)
        if response.status_code != 200:
            raise RuntimeError(f"JSearch API responded with {response.status_code}: {response.text}")
            
        data = response.json()
        results = data.get("data", [])
        
        # Limit to the count requested
        results = results[:count]
        
        jobs = []
        for item in results:
            # Construct location string
            city = item.get("job_city")
            country = item.get("job_country")
            loc = ""
            if city and country:
                loc = f"{city}, {country}"
            elif city:
                loc = city
            elif country:
                loc = country
            else:
                loc = "Remote / Worldwide"
                
            jobs.append({
                "id": item.get("job_id", ""),
                "title": item.get("job_title", "Job Opportunity"),
                "company": item.get("employer_name", "Unknown Company"),
                "location": loc,
                "salary_min": item.get("job_min_salary"),
                "salary_max": item.get("job_max_salary"),
                "description": item.get("job_description", ""),
                "url": item.get("job_apply_link", ""),
                "created": item.get("job_posted_at_datetime_utc", "")
            })
        return jobs
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Network error communicating with JSearch: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Unexpected JSearch error: {str(e)}")
