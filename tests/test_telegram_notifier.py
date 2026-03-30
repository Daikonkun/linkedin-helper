"""Tests for TelegramNotifier."""

from unittest.mock import MagicMock, patch

import pytest

from src.telegram_notifier import TelegramNotifier


@pytest.fixture()
def notifier():
    return TelegramNotifier(bot_token="fake-token", chat_id="12345")


class TestEscapeMd:
    def test_escapes_underscores(self):
        assert TelegramNotifier._escape_md("hello_world") == r"hello\_world"

    def test_escapes_asterisks(self):
        assert TelegramNotifier._escape_md("*bold*") == r"\*bold\*"

    def test_escapes_backticks(self):
        assert TelegramNotifier._escape_md("`code`") == r"\`code\`"

    def test_escapes_brackets(self):
        assert TelegramNotifier._escape_md("[link") == r"\[link"

    def test_plain_text_unchanged(self):
        assert TelegramNotifier._escape_md("plain text") == "plain text"

    def test_does_not_escape_v2_only_chars(self):
        """Chars like . - ! > # should NOT be escaped in Markdown v1."""
        text = "Senior .NET Dev - Remote! #hiring"
        assert TelegramNotifier._escape_md(text) == text


class TestSendJobAlert:
    @patch("src.telegram_notifier.requests.post")
    def test_success(self, mock_post, notifier):
        mock_resp = MagicMock()
        mock_resp.json.return_value = {"ok": True}
        mock_resp.raise_for_status = MagicMock()
        mock_post.return_value = mock_resp

        result = notifier.send_job_alert(
            title="Software Engineer",
            company="Acme Corp",
            location="Remote",
            url="https://linkedin.com/jobs/123",
            date_posted="2 hours ago",
        )

        assert result is True
        mock_post.assert_called_once()
        call_kwargs = mock_post.call_args
        payload = call_kwargs.kwargs.get("json") or call_kwargs[1].get("json")
        assert payload["chat_id"] == "12345"
        assert "Software Engineer" in payload["text"]

    @patch("src.telegram_notifier.requests.post")
    def test_api_error_returns_false(self, mock_post, notifier):
        mock_resp = MagicMock()
        mock_resp.json.return_value = {"ok": False, "description": "Bad Request"}
        mock_resp.raise_for_status = MagicMock()
        mock_post.return_value = mock_resp

        result = notifier.send_job_alert(
            title="Test", company="Co", location="NY", url="https://example.com"
        )
        assert result is False

    @patch("src.telegram_notifier.requests.post")
    def test_network_error_returns_false(self, mock_post, notifier):
        from requests.exceptions import ConnectionError
        mock_post.side_effect = ConnectionError("timeout")
        result = notifier.send_text("hello")
        assert result is False
