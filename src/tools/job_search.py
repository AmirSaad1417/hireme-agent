import requests
from src.config import settings
from typing import List, Dict, Any

def search_adzuna_jobs(query: str, location: str = "", count: int = 5) -> List[Dict[str, Any]]:
    """
    Query the Adzuna API for job recommendations based on key phrases and location.
    
    Parameters:
        query (str): Job role or key skills to search for (maps to 'what').
        location (str): Target city or region (maps to 'where').
        count (int): Max number of job recommendations to fetch.
        
    Returns:
        List[Dict[str, Any]]: List of normalized job matching dicts.
    """
    # Fetch country code from settings, default to "gb"
    country = settings.ADZUNA_COUNTRY or "gb"
    
    # Adzuna search endpoint (Querying page 1)
    url = f"https://api.adzuna.com/v1/api/jobs/{country.lower()}/search/1"
    
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
