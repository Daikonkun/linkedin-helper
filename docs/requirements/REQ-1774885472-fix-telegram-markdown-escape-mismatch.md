# Fix Telegram Markdown escape mismatch

**ID**: REQ-1774885472  
**Status**: PROPOSED  
**Priority**: HIGH  
**Created**: 2026-03-30T15:44:32Z  

## Description

Source: code-review of REQ-1774885033. Severity: HIGH. Evidence: telegram_notifier.py _escape_md() escapes MarkdownV2 characters but send_job_alert uses parse_mode=Markdown (v1). Messages with common chars like . - ! show literal backslashes. Required outcome: align escape logic with the parse_mode — either switch to MarkdownV2 and escape the full set, or reduce _escape_md to only v1 special chars (_*`[).

## Success Criteria

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Technical Notes

(Add implementation notes here)

## Dependencies

(List other requirement IDs if applicable, e.g., REQ-XXX, REQ-YYY)

## Worktree

(Will be populated when work starts: feature/REQ-ID-slug)

---

* **Linked Worktree**: None yet
* **Branch**: None yet
* **Merged**: No
* **Deployed**: No
