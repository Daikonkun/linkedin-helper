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
            resp = self._session.get(
                RAPIDAPI_URL,
                params={"keywords": "test", "locationId": "", "datePosted": "", "sort": "mostRelevant"},
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

        params: dict[str, str | int] = {
            "keywords": keywords,
            "locationId": location,
            "datePosted": date_posted,
            "sort": sort_by,
        }
        if experience_level:
            params["experienceLevel"] = experience_level
        if remote:
            params["onsiteRemote"] = remote

        try:
            resp = self._session.get(RAPIDAPI_URL, params=params, timeout=30)
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
                jobs.append(
                    JobPost(
                        job_id=str(item.get("id", "")),
                        title=item.get("title", "Unknown"),
                        company=item.get("company", {}).get("name", "Unknown"),
                        location=item.get("location", "Unknown"),
                        url=item.get("url", ""),
                        date_posted=item.get("postDate", ""),
                        description_snippet=item.get("description", "")[:200],
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
