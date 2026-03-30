"""Tests for JobStore (SQLite deduplication)."""

import os
import tempfile

import pytest

from src.job_store import JobStore


@pytest.fixture()
def store(tmp_path):
    """Create a JobStore backed by a temp database."""
    db = str(tmp_path / "test_jobs.db")
    s = JobStore(db_path=db)
    yield s
    s.close()


class TestJobStore:
    def test_new_job_is_not_seen(self, store):
        assert store.is_seen("job-1") is False

    def test_mark_seen_then_is_seen(self, store):
        store.mark_seen("job-1")
        assert store.is_seen("job-1") is True

    def test_mark_seen_is_idempotent(self, store):
        store.mark_seen("job-1")
        store.mark_seen("job-1")  # no error
        assert store.is_seen("job-1") is True

    def test_mark_many_seen(self, store):
        store.mark_many_seen(["a", "b", "c"])
        assert store.is_seen("a") is True
        assert store.is_seen("b") is True
        assert store.is_seen("c") is True
        assert store.is_seen("d") is False

    def test_count(self, store):
        assert store.count() == 0
        store.mark_seen("x")
        store.mark_seen("y")
        assert store.count() == 2

    def test_persistence_across_reopen(self, tmp_path):
        db = str(tmp_path / "persist.db")
        s1 = JobStore(db_path=db)
        s1.mark_seen("persisted")
        s1.close()

        s2 = JobStore(db_path=db)
        assert s2.is_seen("persisted") is True
        s2.close()
