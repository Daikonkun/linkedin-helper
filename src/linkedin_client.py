"""LinkedIn job fetcher using RapidAPI LinkedIn Jobs Search."""

import logging
import time
from dataclasses import dataclass, field

import requests

logger = logging.getLogger(__name__)

RAPIDAPI_HOST = "linkedin-jobs-search.p.rapidapi.com"
RAPIDAPI_URL = f"https://{RAPIDAPI_HOST}/"


@dataclass
class JobPost:
    """Represents a single LinkedIn job posting."""

    job_id: str
    title: str
    company: str
    location: str
    url: str
    date_posted: str = ""
    description_snippet: str = ""


@dataclass
class LinkedInClient:
    """Client for fetching LinkedIn jobs via RapidAPI."""

    api_key: str
    _session: requests.Session = field(default_factory=requests.Session, repr=False)
    _last_request_time: float = field(default=0.0, repr=False)
    _min_request_interval: float = 1.0  # seconds between requests

    def __post_init__(self) -> None:
        self._session.headers.update(
            {
                "x-rapidapi-key": self.api_key,
                "x-rapidapi-host": RAPIDAPI_HOST,
            }
        )

    def heartbeat(self) -> bool:
        """Check if the API is reachable. Returns True if healthy."""
        try:
            resp = self._session.post(
                RAPIDAPI_URL,
                json={"search_terms": "test", "location": "United States", "page": "1"},
                timeout=10,
            )
            return resp.status_code in (200, 429)  # 429 = rate-limited but reachable
        except requests.RequestException as exc:
            logger.warning("Heartbeat failed: %s", exc)
            return False

    def fetch_jobs(
        self,
        keywords: str,
        location: str = "",
        date_posted: str = "past24Hours",
        experience_level: str = "",
        remote: str = "",
        sort_by: str = "mostRecent",
        max_results: int = 25,
    ) -> list[JobPost]:
        """Fetch job listings matching the given criteria.

        Returns a list of JobPost objects. On failure, returns an empty list
        and logs the error.
        """
        self._rate_limit()

        payload: dict[str, str] = {
            "search_terms": keywords,
            "location": location,
            "page": "1",
        }

        try:
            resp = self._session.post(RAPIDAPI_URL, json=payload, timeout=30)
            resp.raise_for_status()
        except requests.RequestException as exc:
            logger.error("Failed to fetch jobs: %s", exc)
            return []

        data = resp.json()
        if not isinstance(data, list):
            logger.error("Unexpected API response format: %s", type(data))
            return []

        jobs: list[JobPost] = []
        for item in data[:max_results]:
            try:
                job_id = item.get("linkedin_job_url_cleaned", "") or item.get("job_url", "")
                jobs.append(
                    JobPost(
                        job_id=job_id,
                        title=item.get("job_title", "Unknown"),
                        company=item.get("company_name", item.get("normalized_company_name", "Unknown")),
                        location=item.get("job_location", "Unknown"),
                        url=item.get("linkedin_job_url_cleaned", item.get("job_url", "")),
                        date_posted=item.get("posted_date", ""),
                    )
                )
            except (AttributeError, TypeError) as exc:
                logger.warning("Skipping malformed job entry: %s", exc)
                continue

        logger.info("Fetched %d jobs for keywords=%r", len(jobs), keywords)
        return jobs

    def _rate_limit(self) -> None:
        """Enforce minimum interval between API requests."""
        elapsed = time.monotonic() - self._last_request_time
        if elapsed < self._min_request_interval:
            time.sleep(self._min_request_interval - elapsed)
        self._last_request_time = time.monotonic()

    def close(self) -> None:
        """Close the underlying HTTP session."""
        self._session.close()
