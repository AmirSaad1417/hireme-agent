import json
from typing import Any, Callable, Dict, List

from src.tools.job_scraper import scrape_job_details
from src.tools.job_search import search_jobs

TOOL_DEFINITIONS: List[Dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "job_search",
            "description": "Search for live job vacancies using the Adzuna jobs API by query keywords, location, and result count.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Job title, keywords, or skills to search for (e.g. 'Software Engineer Intern', 'Junior Python Developer', 'Python Developer Remote').",
                    },
                    "location": {
                        "type": "string",
                        "description": "Target city, region, or 'Remote' for work-from-home vacancies.",
                    },
                    "count": {
                        "type": "integer",
                        "description": "Number of job listings to retrieve (e.g. 3 to 10).",
                    },
                },
                "required": ["query", "location", "count"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "job_scraper",
            "description": "Scrape and extract clean text details from a job listing webpage to inspect full requirements and responsibilities.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The full direct URL of the job vacancy webpage to scrape.",
                    },
                },
                "required": ["url"],
            },
        },
    },
]


def execute_tool(tool_name: str, args: Dict[str, Any]) -> str:
    """
    Execute a registered tool by name with provided arguments and return the result as a string.

    Args:
        tool_name: Name of the tool to execute ('job_search' or 'job_scraper').
        args: Dictionary of keyword arguments to pass to the tool.

    Returns:
        str: Serialized result string or error message.
    """
    print(f"Executing tool: {tool_name}")

    if tool_name in ["job_search", "search_jobs"]:
        func: Callable[..., Any] = search_jobs
    elif tool_name in ["job_scraper", "scrape_job_details", "scrape_job", "fetch_job_details"]:
        func = scrape_job_details
    else:
        return f"Error: Tool '{tool_name}' is not recognized. Available tools: ['job_search', 'job_scraper', 'fetch_job_details']"

    try:
        result = func(**args)
        if isinstance(result, (dict, list)):
            return json.dumps(result, indent=2)
        return str(result)
    except Exception as err:
        return f"Error executing tool '{tool_name}': {err}"
