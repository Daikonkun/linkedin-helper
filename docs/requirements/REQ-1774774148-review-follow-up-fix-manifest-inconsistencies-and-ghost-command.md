# Review follow-up: fix manifest inconsistencies and ghost command

**ID**: REQ-1774774148  
**Status**: MERGED  
**Priority**: MEDIUM  
**Created**: 2026-03-29T08:49:08Z  

## Description

Source: code-review pass 2. Severity: MEDIUM. Fix: (1) two stale ACTIVE worktree entries for MERGED REQs, (2) ghost review-requirement command in copilot-instructions, (3) PRUNED status not in worktree schema, (4) SKILL.md heredoc single-quoted EOF.

## Success Criteria

- [x] Worktree entries for REQ-1774639240 and REQ-1774770314 in `.worktree-manifest.json` have `status: "MERGED"` (not `ACTIVE`)
- [x] Ghost `/review-requirement` row removed from `copilot-instructions.md` slash-command table
- [x] `PRUNED` added to `.worktree-manifest.schema.json` status enum
- [x] `requirement-tracker/SKILL.md` heredoc uses unquoted `EOF` so shell variables expand

## Technical Notes

- **Issue 1 – Stale ACTIVE worktree entries**: `.worktree-manifest.json` has two entries still marked `ACTIVE` for requirements that are `MERGED`: `feature/REQ-1774639240-…` (line ~62) and `feature/REQ-1774770314-…` (line ~109). Set their `status` to `"MERGED"` and add `mergedAt` timestamps matching the requirement manifest `updatedAt`.
- **Issue 2 – Ghost command**: `copilot-instructions.md` line 66 lists `/review-requirement <req-id>` but no `.github/prompts/review-requirement.prompt.md` file exists. Remove the row.
- **Issue 3 – PRUNED not in schema**: `.worktree-manifest.schema.json` status enum is `["ACTIVE","MERGED","ABANDONED"]`. `worktree-prune.prompt.md` references `PRUNED`. Add `"PRUNED"` to the schema enum.
- **Issue 4 – Heredoc quoting**: `.github/skills/requirement-tracker/SKILL.md` line 57 uses `<< 'EOF'` which suppresses variable expansion, but the body uses `$NAME`, `$REQ_ID`, etc. Change to `<< EOF`.

## Development Plan

1. Fix stale worktree entries in `.worktree-manifest.json`: set REQ-1774639240 and REQ-1774770314 entries to `"MERGED"`, add `mergedAt`.
2. Remove the `/review-requirement` row from `copilot-instructions.md`.
3. Add `"PRUNED"` to the status enum in `.worktree-manifest.schema.json`.
4. Change `<< 'EOF'` to `<< EOF` in `.github/skills/requirement-tracker/SKILL.md`.
5. Run `./scripts/regenerate-docs.sh` and validate with `./scripts/show-requirement.sh REQ-1774774148`.

**Last updated**: 2026-03-29T09:09:19Z

## Dependencies

(List other requirement IDs if applicable, e.g., REQ-XXX, REQ-YYY)

## Worktree

(Will be populated when work starts: feature/REQ-ID-slug)

---

* **Linked Worktree**: None yet
* **Branch**: None yet
* **Merged**: No
* **Deployed**: No
