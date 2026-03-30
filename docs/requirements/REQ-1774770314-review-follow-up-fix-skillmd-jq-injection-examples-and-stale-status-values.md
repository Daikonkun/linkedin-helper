# Review follow-up: fix SKILL.md jq injection examples and stale status values

**ID**: REQ-1774770314  
**Status**: MERGED  
**Priority**: MEDIUM  
**Created**: 2026-03-29T07:45:14Z  

## Description

Source: code-review. Severity: MEDIUM. Evidence: (1) requirement-tracker/SKILL.md and worktree-manager/SKILL.md use direct shell variable interpolation in jq programs instead of --arg, creating injection risk in documentation examples. (2) requirement-tracker/SKILL.md lists REVERTED as a valid transition target but REVERTED is not in the manifest schema enum or update-requirement-status.sh. Required outcome: update all SKILL.md jq examples to use --arg parameterization and replace REVERTED with CANCELLED.

## Success Criteria

- [x] All jq examples in `requirement-tracker/SKILL.md` use `--arg` parameterization instead of direct shell variable interpolation
- [x] All jq examples in `worktree-manager/SKILL.md` use `--arg` parameterization instead of direct shell variable interpolation
- [x] REVERTED is removed from `requirement-tracker/SKILL.md` valid transitions and replaced with CANCELLED
- [x] No remaining `\"$VAR\"` patterns inside jq program strings in either SKILL.md file

## Technical Notes

**Files to modify:**
- `.github/skills/requirement-tracker/SKILL.md` — 4 jq code blocks with injection + REVERTED status
- `.github/skills/worktree-manager/SKILL.md` — 3 jq code blocks with injection

**Pattern to fix:** Replace `jq "... \"$VAR\" ..."` with `jq --arg varName "$VAR" '... $varName ...'`

**Status fix:** In requirement-tracker/SKILL.md section "Valid transitions", change `MERGED → DEPLOYED, REVERTED` to `MERGED → DEPLOYED, CANCELLED`. The schema enum in `.requirement-manifest.schema.json` and `update-requirement-status.sh` both use CANCELLED, not REVERTED.

## Development Plan

1. **Fix jq injection in `requirement-tracker/SKILL.md`** — Convert all 4 jq code blocks (Add Requirement, Update Status, Show Requirement, Update Requirement for docs) from `\"$VAR\"` interpolation to `--arg` parameterization.
2. **Fix REVERTED → CANCELLED in `requirement-tracker/SKILL.md`** — In the "Valid transitions" list, replace `REVERTED` with `CANCELLED` to match the schema enum and `update-requirement-status.sh`.
3. **Fix jq injection in `worktree-manager/SKILL.md`** — Convert all 3 jq code blocks (Create Worktree, Merge and Cleanup, Detect Conflicts) from `\"$VAR\"` interpolation to `--arg` parameterization.
4. **Verify no remaining injection patterns** — Grep both files for `\"$` inside jq program strings to confirm zero matches.
5. **Run `./scripts/regenerate-docs.sh`** and validate with `./scripts/show-requirement.sh REQ-1774770314`.

**Last updated**: 2026-03-29T08:11:12Z

## Dependencies

(List other requirement IDs if applicable, e.g., REQ-XXX, REQ-YYY)

## Worktree

(Will be populated when work starts: feature/REQ-ID-slug)

---

* **Linked Worktree**: None yet
* **Branch**: None yet
* **Merged**: No
* **Deployed**: No
