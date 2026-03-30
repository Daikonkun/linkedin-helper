# LinkedIn Job Agent

Automated LinkedIn job monitor that polls for new postings matching your criteria and sends real-time alerts to Telegram.

## Features

- **Hourly job polling** — searches LinkedIn via RapidAPI on a configurable schedule
- **Deduplication** — SQLite store ensures you never get alerted for the same job twice
- **Telegram notifications** — formatted job cards delivered instantly to your chat
- **Heartbeat monitoring** — periodic API connectivity checks with logging
- **Graceful shutdown** — handles SIGINT/SIGTERM cleanly

## Prerequisites

- Python 3.9+
- A [RapidAPI](https://rapidapi.com/) account with a subscription to **[LinkedIn Jobs Search](https://rapidapi.com/jaypat87/api/linkedin-jobs-search)**
- A Telegram bot (create one via [@BotFather](https://t.me/BotFather))

## Quick Start

### 1. Clone and install

```bash
git clone https://github.com/Daikonkun/linkedin-helper.git
cd linkedin-helper
pip install -r requirements.txt
```

### 2. Configure secrets

Copy the example and fill in your keys:

```bash
cp .env.example .env
```

```dotenv
RAPIDAPI_KEY=your_rapidapi_key_here
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_CHAT_ID=your_telegram_chat_id_here
```

**Getting your Telegram chat ID:**

1. Start a chat with your bot on Telegram (send `/start`).
2. Visit `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`.
3. Find `"chat":{"id": 123456789}` in the response — that number is your chat ID.

### 3. Configure job search

Copy and edit the config file:

```bash
cp config.yaml.example config.yaml
```

```yaml
linkedin:
  keywords: "product manager"
  location: "Hong Kong"
  experience_level: ""          # entry_level, mid_senior_level, director
  date_posted: "past24Hours"    # anyTime, pastMonth, pastWeek, past24Hours
  remote: ""                    # on_site, remote, hybrid
  sort_by: "mostRecent"

agent:
  polling_interval_minutes: 60
  heartbeat_interval_minutes: 5
  max_results_per_poll: 25
  db_path: "jobs.db"
```

### 4. Run

```bash
python -m src.agent
```

The agent will:
1. Run an initial poll immediately on startup
2. Send Telegram alerts for every new job found
3. Continue polling on the configured interval
4. Log heartbeat checks to verify API connectivity

Stop with `Ctrl+C`.

## Project Structure

```
src/
  agent.py              # Entry point — scheduler, poll loop, shutdown
  linkedin_client.py    # RapidAPI job fetcher
  job_store.py          # SQLite deduplication store
  telegram_notifier.py  # Telegram Bot API notifier
tests/
  test_linkedin_client.py
  test_job_store.py
  test_telegram_notifier.py
config.yaml.example     # Search & agent settings template
.env.example            # API keys template
requirements.txt        # Python dependencies
```

## Running Tests

```bash
pip install pytest
python -m pytest tests/ -v
```

## How It Works

1. **Poll** — `LinkedInClient` sends a POST request to the RapidAPI LinkedIn Jobs Search endpoint with your keywords and location.
2. **Deduplicate** — `JobStore` checks each returned job ID against a local SQLite database. Only unseen jobs proceed.
3. **Notify** — `TelegramNotifier` formats each new job as a Markdown card and sends it via the Telegram Bot API.
4. **Record** — Successfully notified jobs are marked as seen in the database.
5. **Repeat** — APScheduler triggers the next poll cycle after the configured interval.

## Troubleshooting

| Problem | Fix |
|---|---|
| `Missing required environment variable` | Ensure `.env` contains all three keys |
| `403 Forbidden` from RapidAPI | Verify your RapidAPI subscription is active |
| `404 Not Found` from RapidAPI | Check that you are subscribed to the correct API (LinkedIn Jobs Search by jaypat87) |
| No Telegram messages received | Confirm you sent `/start` to the bot and the chat ID is correct |
| `YAML parse error` | Use plain strings in `config.yaml` — avoid bare commas between values |

## License

MIT
