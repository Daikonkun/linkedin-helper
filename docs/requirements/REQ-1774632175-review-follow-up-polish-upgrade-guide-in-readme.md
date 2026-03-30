# Review follow-up: polish upgrade guide in README

**ID**: REQ-1774632175  
**Status**: MERGED  
**Priority**: LOW  
**Created**: 2026-03-27T17:22:55Z  

## Description

Source: code-review of REQ-1774630000. Severity: LOW. Evidence: (1) Step 3 of the upgrade workflow tells users to place template files but gives no concrete command to fetch/clone them — users won't know how to obtain the latest template. (2) Step 1 creates a branch via checkout -b that is never used because Step 2 immediately creates a worktree with a different branch name. Required outcome: add a concrete fetch/clone example in Step 3, and simplify Step 1 to only create the safety tag (drop the unused branch).

## Success Criteria

- [x] Step 3 includes a concrete command (clone/curl) to fetch the latest Vibe Master template
- [x] Step 1 no longer creates an unused branch; only the safety tag remains
- [x] Optional: add a cleanup step for `.upgrade-template/` after migration

## Technical Notes

(Add implementation notes here)

## Dependencies

REQ-1774630000 (parent: upgrade guide must be merged first)

## Worktree

(Will be populated when work starts: feature/REQ-ID-slug)

---

* **Linked Worktree**: None yet
* **Branch**: None yet
* **Merged**: No
* **Deployed**: No
