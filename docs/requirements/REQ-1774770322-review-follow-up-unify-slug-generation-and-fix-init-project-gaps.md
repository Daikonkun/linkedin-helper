# Review follow-up: unify slug generation and fix init-project gaps

**ID**: REQ-1774770322  
**Status**: MERGED  
**Priority**: MEDIUM  
**Created**: 2026-03-29T07:45:22Z  

## Description

Source: code-review. Severity: MEDIUM. Evidence: (1) create-requirement.sh slug generation does not lowercase or collapse hyphens, while start-work.sh does — causing mismatched spec filenames vs branch names. (2) init-project.sh never creates docs/requirements/ directory or an initial git commit despite comments suggesting it should. (3) init-project.sh sed substitution is vulnerable to special characters in project name — should use jq --arg instead. (4) REQ-1774630000 manifest entry has updatedAt before createdAt. Required outcome: unify slug logic, complete init-project.sh setup, fix manifest timestamp, and add timestamp validation.

## Success Criteria

- [x] `create-requirement.sh` slug generation lowercases and collapses consecutive hyphens, matching `start-work.sh` logic
- [x] `init-project.sh` creates `docs/requirements/` directory and makes an initial git commit
- [x] `init-project.sh` uses `jq --arg` instead of `sed` for project name substitution
- [x] REQ-1774630000 manifest entry has `updatedAt >= createdAt`
- [x] Manifest write helpers reject `updatedAt < createdAt` (timestamp validation)

## Technical Notes

- **Slug mismatch**: `create-requirement.sh` line 11 uses `sed 's/ /-/g' | sed 's/[^a-zA-Z0-9-]//g' | tr '[:upper:]' '[:lower:]'` — strips non-alphanum but does NOT collapse consecutive hyphens. `start-work.sh` line 52 uses `tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | sed 's/^-//; s/-$//'` — proper slug. Extract a shared function or align both to the same pipeline.
- **init-project.sh**: Missing `mkdir -p docs/requirements` and `git add -A && git commit -m 'chore: init project'`. The `sed -i.bak` on `PROJECT_PLACEHOLDER` breaks if project name has `/`, `&`, or other sed metacharacters — replace with `jq --arg name "$PROJECT_NAME" '.projectName = $name'`.
- **Timestamp fix**: REQ-1774630000 has `createdAt: 2026-03-28T00:30:00Z` but `updatedAt: 2026-03-27T17:24:03Z`. Set `updatedAt` to match `createdAt` since actual merge-time is unknown.

## Development Plan

1. **Unify slug generation** — In `scripts/create-requirement.sh`, replace the slug pipeline (line 11) with the same logic used in `scripts/start-work.sh` (lowercase, strip non-alphanum to hyphens, collapse consecutive hyphens, trim leading/trailing hyphens).
2. **Fix init-project.sh** — Add `mkdir -p docs/requirements`; replace `sed` placeholder substitution with `jq --arg`; add a final `git add -A && git commit -m 'chore: init project'` step.
3. **Fix REQ-1774630000 timestamp** — In `.requirement-manifest.json`, set `updatedAt` for REQ-1774630000 to `"2026-03-28T00:30:00Z"` so it is not earlier than `createdAt`.
4. **Run `./scripts/regenerate-docs.sh`** and confirm generated docs reflect updates.
5. **Verify** — Run `./scripts/show-requirement.sh REQ-1774770322`, manually inspect slug output from `create-requirement.sh`, and confirm all success criteria pass.

## Dependencies

(List other requirement IDs if applicable, e.g., REQ-XXX, REQ-YYY)

## Worktree

(Will be populated when work starts: feature/REQ-ID-slug)

---

* **Linked Worktree**: None yet
* **Branch**: None yet
* **Merged**: No
* **Deployed**: No
