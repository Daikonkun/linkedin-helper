# Review follow-up: add missing prompt files for advertised slash commands

**ID**: REQ-1774770305  
**Status**: MERGED  
**Priority**: HIGH  
**Created**: 2026-03-29T07:45:05Z  

## Description

Source: code-review. Severity: HIGH. Evidence: copilot-instructions.md lists /worktree-create and /worktree-prune as available slash commands, and worktree-manager/SKILL.md advertises /worktree-status, but no corresponding .prompt.md files exist. REQ-1774628144 (DEPLOYED) was supposed to align commands but missed these three. Required outcome: either create worktree-create.prompt.md, worktree-prune.prompt.md, and worktree-status.prompt.md, or remove these commands from copilot-instructions.md and SKILL.md.

## Success Criteria

- [x] Every slash command in copilot-instructions.md table has a matching .prompt.md file
- [x] worktree-create.prompt.md created with proper workflow and constraints
- [x] worktree-prune.prompt.md created with proper workflow and constraints
- [x] worktree-status.prompt.md created with proper workflow and constraints
- [x] copilot-instructions.md prompt-backed commands paragraph updated to include all three
- [x] /worktree-status added to copilot-instructions.md slash command table (was only in SKILL.md)

## Technical Notes

**Approach**: Created all three missing prompt files rather than removing advertised commands, since each serves a distinct purpose:
- `/worktree-create` — manual worktree creation without status change (unlike `/start-work` which also transitions to IN_PROGRESS)
- `/worktree-prune` — cleanup orphaned worktrees and sync manifests
- `/worktree-status` — comprehensive dashboard with cross-reference between filesystem and manifest

**Out-of-scope finding**: `/review-requirement <req-id>` is also listed in the slash command table without a backing prompt file. It's effectively an alias for `/update-requirement <req-id> CODE_REVIEW`. Should be addressed in a separate follow-up.

## Dependencies

REQ-1774628144 (DEPLOYED) — original alignment work that missed these three commands.

## Worktree

N/A — changes applied directly to main (prompt files and copilot-instructions.md only).

---

* **Linked Worktree**: None
* **Branch**: main (direct)
* **Merged**: Yes
* **Deployed**: No
