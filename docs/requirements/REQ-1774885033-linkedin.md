# LinkedIn

**ID**: REQ-1774885033  
**Status**: CODE_REVIEW  
**Priority**: MEDIUM  
**Created**: 2026-03-30T15:37:13Z  

## Description

build an agent that can connect LinkedIn via API which has heartbeat and check if there is new job post that fits me every hour, and push notifications to Telegram

## Success Criteria

- [ ] Agent authenticates with LinkedIn API and maintains a persistent session (heartbeat/keep-alive) that auto-reconnects on failure
- [ ] Agent polls LinkedIn for new job postings matching user-defined criteria (keywords, location, experience level) at a configurable interval (default: every hour)
- [ ] New matching job posts are deduplicated against previously seen posts so the user is never notified twice for the same listing
- [ ] Notifications are sent to a configured Telegram chat via the Telegram Bot API, containing job title, company, location, and a direct link to the posting
- [ ] Agent runs as a long-lived background process with structured logging and graceful shutdown handling

## Technical Notes

- **LinkedIn Data Access**: LinkedIn's official API is restrictive for job scraping. Evaluate options: (1) LinkedIn API with proper OAuth 2.0 scopes if available, (2) a third-party job aggregator API (e.g., RapidAPI LinkedIn Jobs), or (3) RSS/scraping fallback. Document chosen approach and any rate-limit considerations.
- **Heartbeat / Scheduler**: Use a scheduling framework (e.g., Python `APScheduler`, Node.js `node-cron`, or a system-level cron) to trigger hourly job checks. Implement a health-check heartbeat endpoint or log pulse so liveness can be monitored.
- **Telegram Integration**: Use the Telegram Bot API (`/sendMessage`). Require `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` as environment variables. Format messages with Markdown for readability.
- **State Persistence**: Track seen job post IDs in a lightweight store (SQLite or JSON file) to enable deduplication across restarts.
- **Configuration**: Store user preferences (search keywords, location, polling interval) in a config file (e.g., `config.yaml` or `.env`).
- **Risks**: LinkedIn may block or rate-limit API/scraping access; Telegram rate limits (30 messages/sec) are unlikely to be hit but should be handled. API key leakage must be prevented (use `.env` + `.gitignore`).


## Development Plan

1. **Project scaffolding & configuration** — Initialize Python project structure (`src/`, `config.yaml.example`, `.env.example`, `requirements.txt`). Set up `.gitignore` for `.env`, `__pycache__`, and `*.db`. Define config schema for LinkedIn search criteria, polling interval, and Telegram credentials.
2. **LinkedIn job fetcher module** — Implement `src/linkedin_client.py` with API/aggregator integration (evaluate RapidAPI LinkedIn Jobs or similar). Include authentication, heartbeat keep-alive, rate-limit handling, and a `fetch_new_jobs(keywords, location)` function that returns structured job data.
3. **Deduplication & state persistence** — Implement `src/job_store.py` using SQLite to track seen job post IDs. Provide `is_seen(job_id)` and `mark_seen(job_id)` methods. Ensure persistence across agent restarts.
4. **Telegram notifier module** — Implement `src/telegram_notifier.py` using the Telegram Bot API (`/sendMessage`). Format messages with job title, company, location, and direct link. Read `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` from environment variables.
5. **Agent runner with scheduler** — Implement `src/agent.py` as the main entry point. Use `APScheduler` for hourly polling. Wire together LinkedIn fetcher → deduplication → Telegram notifier. Add structured logging, graceful shutdown (SIGINT/SIGTERM), and heartbeat logging.

**Last updated**: 2026-03-30T15:39:03Z

## Dependencies

None

## Worktree

feature/REQ-1774885033-linkedin

---

* **Linked Worktree**: feature/REQ-1774885033-linkedin
* **Branch**: feature/REQ-1774885033-linkedin
* **Merged**: No
* **Deployed**: No
