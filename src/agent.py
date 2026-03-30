"""LinkedIn Job Agent — main entry point.

Polls LinkedIn for new job postings at a configurable interval,
deduplicates against previously seen posts, and sends alerts
to Telegram.
"""

import logging
import os
import signal
import sys
from pathlib import Path

import yaml
from apscheduler.schedulers.blocking import BlockingScheduler
from dotenv import load_dotenv

from src.job_store import JobStore
from src.linkedin_client import LinkedInClient
from src.telegram_notifier import TelegramNotifier

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("linkedin-agent")

# ---------------------------------------------------------------------------
# Configuration helpers
# ---------------------------------------------------------------------------

def load_config(config_path: str = "config.yaml") -> dict:
    """Load YAML config, falling back to defaults."""
    defaults: dict = {
        "linkedin": {
            "keywords": "software engineer",
            "location": "",
            "experience_level": "",
            "date_posted": "past24Hours",
            "remote": "",
            "sort_by": "mostRecent",
        },
        "agent": {
            "polling_interval_minutes": 60,
            "heartbeat_interval_minutes": 5,
            "max_results_per_poll": 25,
            "db_path": "jobs.db",
        },
        "telegram": {
            "message_format": "markdown",
        },
    }
    path = Path(config_path)
    if path.exists():
        with open(path) as f:
            user_cfg = yaml.safe_load(f) or {}
        # Merge: user overrides defaults
        for section in defaults:
            if section in user_cfg:
                defaults[section].update(user_cfg[section])
    else:
        logger.warning("Config file %s not found — using defaults", config_path)
    return defaults


def require_env(name: str) -> str:
    """Return an environment variable or exit with a clear error."""
    value = os.environ.get(name)
    if not value:
        logger.critical("Missing required environment variable: %s", name)
        sys.exit(1)
    return value


# ---------------------------------------------------------------------------
# Core poll cycle
# ---------------------------------------------------------------------------

def poll_jobs(
    client: LinkedInClient,
    store: JobStore,
    notifier: TelegramNotifier,
    cfg: dict,
) -> None:
    """Single poll cycle: fetch → deduplicate → notify.

    Wrapped in a top-level error boundary so a transient failure
    (e.g. SQLite lock, unexpected API response) does not kill the
    scheduler job — it will simply retry on the next cycle.
    """
    try:
        linkedin_cfg = cfg["linkedin"]
        agent_cfg = cfg["agent"]

        logger.info("Polling LinkedIn for jobs (keywords=%r) …", linkedin_cfg["keywords"])

        jobs = client.fetch_jobs(
            keywords=linkedin_cfg["keywords"],
            location=linkedin_cfg["location"],
            date_posted=linkedin_cfg["date_posted"],
            experience_level=linkedin_cfg["experience_level"],
            remote=linkedin_cfg["remote"],
            sort_by=linkedin_cfg["sort_by"],
            max_results=agent_cfg["max_results_per_poll"],
        )

        new_jobs = [j for j in jobs if not store.is_seen(j.job_id)]
        logger.info("Found %d new jobs out of %d fetched", len(new_jobs), len(jobs))

        for job in new_jobs:
            sent = notifier.send_job_alert(
                title=job.title,
                company=job.company,
                location=job.location,
                url=job.url,
                date_posted=job.date_posted,
            )
            if sent:
                store.mark_seen(job.job_id)
                logger.info("Notified: %s at %s", job.title, job.company)
            else:
                logger.warning("Failed to notify for job %s — will retry next cycle", job.job_id)
    except Exception:
        logger.exception("Poll cycle failed — will retry next cycle")


def heartbeat_tick(client: LinkedInClient) -> None:
    """Log a heartbeat pulse and verify API connectivity."""
    healthy = client.heartbeat()
    if healthy:
        logger.info("💓 Heartbeat OK — API reachable")
    else:
        logger.warning("💔 Heartbeat FAILED — API unreachable")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    load_dotenv()

    cfg = load_config()

    # Required secrets
    rapidapi_key = require_env("RAPIDAPI_KEY")
    telegram_token = require_env("TELEGRAM_BOT_TOKEN")
    telegram_chat_id = require_env("TELEGRAM_CHAT_ID")

    # Components
    client = LinkedInClient(api_key=rapidapi_key)
    store = JobStore(db_path=cfg["agent"]["db_path"])
    notifier = TelegramNotifier(bot_token=telegram_token, chat_id=telegram_chat_id)

    scheduler = BlockingScheduler()
    polling_minutes = cfg["agent"]["polling_interval_minutes"]
    heartbeat_minutes = cfg["agent"]["heartbeat_interval_minutes"]

    # Schedule recurring jobs
    scheduler.add_job(
        poll_jobs,
        "interval",
        minutes=polling_minutes,
        args=[client, store, notifier, cfg],
        id="poll_jobs",
        name=f"Poll LinkedIn every {polling_minutes}m",
    )
    scheduler.add_job(
        heartbeat_tick,
        "interval",
        minutes=heartbeat_minutes,
        args=[client],
        id="heartbeat",
        name=f"Heartbeat every {heartbeat_minutes}m",
    )

    # Shutdown guard — prevents double-close on signal + finally
    _shutting_down = False

    def _cleanup() -> None:
        nonlocal _shutting_down
        if _shutting_down:
            return
        _shutting_down = True
        client.close()
        store.close()

    # Graceful shutdown
    def _shutdown(signum: int, _frame: object) -> None:
        sig_name = signal.Signals(signum).name
        logger.info("Received %s — shutting down gracefully …", sig_name)
        scheduler.shutdown(wait=False)
        _cleanup()

    signal.signal(signal.SIGINT, _shutdown)
    signal.signal(signal.SIGTERM, _shutdown)

    # Run first poll immediately, then let scheduler take over
    logger.info(
        "LinkedIn Job Agent started — polling every %d min, heartbeat every %d min",
        polling_minutes,
        heartbeat_minutes,
    )
    poll_jobs(client, store, notifier, cfg)

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Agent stopped.")
    finally:
        _cleanup()


if __name__ == "__main__":
    main()
