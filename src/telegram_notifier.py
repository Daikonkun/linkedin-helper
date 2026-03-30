"""Telegram Bot API notifier for job alerts."""

import logging
from dataclasses import dataclass

import requests

logger = logging.getLogger(__name__)

TELEGRAM_API_BASE = "https://api.telegram.org"


@dataclass
class TelegramNotifier:
    """Send job alert messages via the Telegram Bot API."""

    bot_token: str
    chat_id: str

    def send_job_alert(
        self,
        title: str,
        company: str,
        location: str,
        url: str,
        date_posted: str = "",
    ) -> bool:
        """Send a single job alert message. Returns True on success."""
        lines = [
            f"*New Job Alert*",
            f"*{self._escape_md(title)}*",
            f"Company: {self._escape_md(company)}",
            f"Location: {self._escape_md(location)}",
        ]
        if date_posted:
            lines.append(f"Posted: {self._escape_md(date_posted)}")
        lines.append(f"[View on LinkedIn]({url})")

        text = "\n".join(lines)
        return self._send_message(text, parse_mode="Markdown")

    def send_text(self, text: str) -> bool:
        """Send a plain-text message. Returns True on success."""
        return self._send_message(text)

    def _send_message(self, text: str, parse_mode: str = "") -> bool:
        """Call the Telegram sendMessage endpoint."""
        api_url = f"{TELEGRAM_API_BASE}/bot{self.bot_token}/sendMessage"
        payload: dict[str, str] = {
            "chat_id": self.chat_id,
            "text": text,
        }
        if parse_mode:
            payload["parse_mode"] = parse_mode

        try:
            resp = requests.post(api_url, json=payload, timeout=10)
            resp.raise_for_status()
            result = resp.json()
            if not result.get("ok"):
                logger.error("Telegram API error: %s", result.get("description"))
                return False
            return True
        except requests.RequestException as exc:
            logger.error("Failed to send Telegram message: %s", exc)
            return False

    @staticmethod
    def _escape_md(text: str) -> str:
        """Escape Markdown v1 special characters.

        Telegram Markdown v1 only treats _ * ` [ as formatting triggers.
        Do NOT escape MarkdownV2-only chars (. ! - etc.) — they would
        appear as literal backslashes in the message.
        """
        for ch in ("_", "*", "`", "["):
            text = text.replace(ch, f"\\{ch}")
        return text
