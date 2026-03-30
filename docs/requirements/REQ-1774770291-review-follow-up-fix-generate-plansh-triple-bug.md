# Review follow-up: fix generate-plan.sh triple bug

**ID**: REQ-1774770291  
**Status**: MERGED  
**Priority**: HIGH  
**Created**: 2026-03-29T07:44:51Z  

## Description

Source: code-review. Severity: HIGH. Evidence: (1) heredoc uses single-quoted EOF so variables are not expanded — plan text contains literal dollar-sign references instead of actual values. (2) awk system() calls reference unexported PLAN_FILE shell variable which is invisible to the subshell. (3) plan content is hardcoded to superpowers-research steps from REQ-1774685792 and is irrelevant for all other requirements. Required outcome: rewrite generate-plan.sh so it produces requirement-specific scaffolding with proper variable expansion, or remove the script and rely on the agent prompt workflow exclusively.

## Success Criteria

- [ ] Heredoc uses unquoted `EOF` so `$REL_SPEC`, `$REQ_ID`, date, and other shell variables expand correctly in the generated plan text.
- [ ] `PLAN_FILE` is properly passed to `awk` (via `-v` flag or `export`) so the `system("cat ...")` calls succeed without "No such file or directory" errors.
- [ ] Plan content is dynamically generated from the requirement's own Description, Success Criteria, and Technical Notes — not hardcoded to superpowers-research steps.
- [ ] Running `scripts/generate-plan.sh REQ-<any-id>` on any existing requirement produces a valid, requirement-specific `## Development Plan` section.
- [ ] Idempotent: running the script twice replaces (not duplicates) the plan section.

## Technical Notes

### Bug 1 — Single-quoted heredoc (`'EOF'`)
Line `cat > "$PLAN_FILE" << 'EOF'` prevents variable expansion. Fix: change to `<< EOF` (unquoted).

### Bug 2 — `$PLAN_FILE` invisible to awk subshell
`awk` executes `system("cat \"$PLAN_FILE\"")` but `$PLAN_FILE` is a shell variable not visible inside `awk`. Fix: pass the path via `awk -v planfile="$PLAN_FILE"` and use `system("cat " planfile)`.

### Bug 3 — Hardcoded superpowers plan content
The heredoc body references obra/superpowers skills. Fix: replace with a generic template that interpolates the requirement's `$DESCRIPTION`, `$SUCCESS`, `$TECH_NOTES`, and `$REL_SPEC` values already parsed earlier in the script.

### Files to modify
- `scripts/generate-plan.sh` — primary fix target

## Development Plan

1. Review Description, Success Criteria, and Technical Notes in `docs/requirements/REQ-1774770291-review-follow-up-fix-generate-plansh-triple-bug.md`.
   - **Summary**: Source: code-review. Severity: HIGH. Evidence: (1) heredoc uses single-quoted EO
   - **Key criteria**: - [ ] Heredoc uses unquoted `EOF` so `$REL_SPEC`, `$REQ_ID`, date, and other shell variables expand 
2. Analyse Technical Notes and identify implementation approach.
   - **Notes**: ### Bug 1 — Single-quoted heredoc (`'EOF'`)
3. Implement changes in the files/scripts referenced by the requirement spec.
4. Run `./scripts/regenerate-docs.sh` to update manifests and generated docs.
5. Validate with `./scripts/show-requirement.sh REQ-1774770291` and verify success criteria are met.

**Last updated**: 2026-03-29T07:49:16Z
## Dependencies

(List other requirement IDs if applicable, e.g., REQ-XXX, REQ-YYY)

## Worktree

(Will be populated when work starts: feature/REQ-ID-slug)

---

* **Linked Worktree**: None yet
* **Branch**: None yet
* **Merged**: No
* **Deployed**: No
