"""SQLite-backed store for tracking seen job post IDs."""

import logging
import sqlite3
from pathlib import Path

logger = logging.getLogger(__name__)


class JobStore:
    """Lightweight SQLite store for job deduplication.

    Tracks which job IDs have already been seen so notifications
    are never sent twice for the same listing.
    """

    def __init__(self, db_path: str = "jobs.db") -> None:
        self._db_path = Path(db_path)
        self._conn = sqlite3.connect(str(self._db_path))
        self._init_schema()

    def _init_schema(self) -> None:
        """Create the seen_jobs table if it doesn't exist."""
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS seen_jobs (
                job_id   TEXT PRIMARY KEY,
                seen_at  TEXT DEFAULT (datetime('now'))
            )
            """
        )
        self._conn.commit()

    def is_seen(self, job_id: str) -> bool:
        """Return True if this job_id has already been recorded."""
        cur = self._conn.execute(
            "SELECT 1 FROM seen_jobs WHERE job_id = ?", (job_id,)
        )
        return cur.fetchone() is not None

    def mark_seen(self, job_id: str) -> None:
        """Record a job_id as seen. Idempotent (INSERT OR IGNORE)."""
        self._conn.execute(
            "INSERT OR IGNORE INTO seen_jobs (job_id) VALUES (?)", (job_id,)
        )
        self._conn.commit()

    def mark_many_seen(self, job_ids: list[str]) -> None:
        """Batch-mark multiple job IDs as seen."""
        self._conn.executemany(
            "INSERT OR IGNORE INTO seen_jobs (job_id) VALUES (?)",
            [(jid,) for jid in job_ids],
        )
        self._conn.commit()

    def count(self) -> int:
        """Return the total number of seen jobs."""
        cur = self._conn.execute("SELECT COUNT(*) FROM seen_jobs")
        row = cur.fetchone()
        return row[0] if row else 0

    def close(self) -> None:
        """Close the database connection."""
        self._conn.close()
