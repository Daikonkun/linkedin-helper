"""Tests for LinkedInClient."""

from unittest.mock import MagicMock, patch

import pytest

from src.linkedin_client import LinkedInClient, JobPost


@pytest.fixture()
def client():
    c = LinkedInClient(api_key="fake-key")
    c._min_request_interval = 0  # disable rate limiting in tests
    yield c
    c.close()


class TestHeartbeat:
    def test_healthy(self, client):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        client._session.get = MagicMock(return_value=mock_resp)
        assert client.heartbeat() is True

    def test_rate_limited_still_healthy(self, client):
        mock_resp = MagicMock()
        mock_resp.status_code = 429
        client._session.get = MagicMock(return_value=mock_resp)
        assert client.heartbeat() is True

    def test_unreachable(self, client):
        from requests.exceptions import ConnectionError
        client._session.get = MagicMock(side_effect=ConnectionError("down"))
        assert client.heartbeat() is False


class TestFetchJobs:
    def test_parses_response(self, client):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.raise_for_status = MagicMock()
        mock_resp.json.return_value = [
            {
                "id": "111",
                "title": "Backend Dev",
                "company": {"name": "Acme"},
                "location": "Remote",
                "url": "https://linkedin.com/jobs/111",
                "postDate": "1 day ago",
                "description": "Build cool stuff",
            }
        ]
        client._session.get = MagicMock(return_value=mock_resp)

        jobs = client.fetch_jobs(keywords="python")
        assert len(jobs) == 1
        assert jobs[0].job_id == "111"
        assert jobs[0].company == "Acme"

    def test_error_returns_empty(self, client):
        from requests.exceptions import ConnectionError
        client._session.get = MagicMock(side_effect=ConnectionError("fail"))
        jobs = client.fetch_jobs(keywords="python")
        assert jobs == []

    def test_max_results_limits_output(self, client):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.raise_for_status = MagicMock()
        mock_resp.json.return_value = [
            {"id": str(i), "title": f"Job {i}", "company": {"name": "Co"}, "location": "NY", "url": f"https://x/{i}"}
            for i in range(10)
        ]
        client._session.get = MagicMock(return_value=mock_resp)

        jobs = client.fetch_jobs(keywords="test", max_results=3)
        assert len(jobs) == 3
