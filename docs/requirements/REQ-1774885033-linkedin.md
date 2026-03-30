# LinkedIn

**ID**: REQ-1774885033  
**Status**: PROPOSED  
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

## Dependencies

None

## Worktree

(Will be populated when work starts: feature/REQ-ID-slug)

---

* **Linked Worktree**: None yet
* **Branch**: None yet
* **Merged**: No
* **Deployed**: No
