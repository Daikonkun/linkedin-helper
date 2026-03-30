# Review follow-up: align slash commands with actual skill invocations

**ID**: REQ-1774628144  
**Status**: DEPLOYED  
**Priority**: MEDIUM  
**Created**: 2026-03-27T16:15:44Z  

## Description

Source: code-review. Severity: MEDIUM. Evidence: New skill docs advertise additional slash commands (/debug-repro, /debug-root-cause, /debug-validate, /manual-audit, /manual-changelog, /code-review-req, /code-review-create-threads) that are not implemented as standalone prompts/skills, which can mislead users. Required outcome: either implement these commands as actual prompts/agents or reword docs to describe them as workflow phases under /bug-fix, /update-manual, and /code-review.

## Success Criteria

- [x] Reworded pseudo slash commands in `debug` skill into workflow phases under `/bug-fix`
- [x] Reworded pseudo slash commands in `update-manual` skill into optional outputs of `/update-manual`
- [x] Reworded pseudo slash commands in `code-review` skill into workflow actions under `/code-review`

## Technical Notes

Completed using documentation-only changes to avoid introducing non-functional slash commands.
This keeps the command surface accurate while preserving the intended multi-phase workflows.

## Dependencies

(List other requirement IDs if applicable, e.g., REQ-XXX, REQ-YYY)

## Worktree

feature/REQ-1774628144-review-follow-up-align-slash-commands-with-actual-skill-invocations

---

* **Linked Worktree**: feature/REQ-1774628144-review-follow-up-align-slash-commands-with-actual-skill-invocations
* **Branch**: feature/REQ-1774628144-review-follow-up-align-slash-commands-with-actual-skill-invocations
* **Merged**: Yes
* **Deployed**: Yes
