import html
import re
import requests


def scrape_job_details(url: str) -> str:
    """
    Fetch and extract clean text details from a job listing URL.

    Args:
        url: Full web URL of the job posting.

    Returns:
        str: Cleaned text content up to 1500 characters, or fallback error message.
    """
    fallback_message = "Could not fetch job details from the provided URL."

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        raw_html = response.text

        # Remove script and style elements
        cleaned = re.sub(
            r"<(script|style|noscript|header|footer|nav)[\s\S]*?</\1>",
            " ",
            raw_html,
            flags=re.IGNORECASE,
        )

        # Remove all HTML tags
        cleaned = re.sub(r"<[^>]+>", " ", cleaned)

        # Unescape HTML entities (&amp;, &nbsp;, etc.)
        cleaned = html.unescape(cleaned)

        # Collapse whitespace
        cleaned = re.sub(r"\s+", " ", cleaned).strip()

        print(f"Scraped job URL: {url}")
        return cleaned[:1500]

    except Exception as err:
        print(f"Warning: Failed to scrape URL '{url}': {err}")
        return fallback_message


# Aliases
scrape_job = scrape_job_details
job_scraper = scrape_job_details
