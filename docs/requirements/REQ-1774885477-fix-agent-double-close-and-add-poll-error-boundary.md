# Fix agent double-close and add poll error boundary

**ID**: REQ-1774885477  
**Status**: MERGED  
**Priority**: MEDIUM  
**Created**: 2026-03-30T15:44:37Z  

## Description

Source: code-review of REQ-1774885033. Severity: MEDIUM. Evidence: (1) agent.py _shutdown() and finally block both call client.close()/store.close(), causing ProgrammingError on SQLite double-close. (2) poll_jobs() has no top-level try/except so a transient DB error kills the scheduler job. Required outcome: guard against double-close and wrap poll_jobs body in error boundary that logs and continues.

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
