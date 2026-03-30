# add /work-on command

**ID**: REQ-1774775901  
**Status**: MERGED  
**Priority**: MEDIUM  
**Created**: 2026-03-29T09:18:21Z  

## Description

add a command to work on a specific REQ until next status

## Success Criteria

- [ ] A `/work-on <REQ-ID>` slash command exists and is backed by a prompt file at `.github/prompts/work-on.prompt.md`
- [ ] Running `/work-on REQ-XXXXXXXXXX` loads the requirement spec, switches context to (or validates) the linked worktree, and begins iterative implementation toward the next valid status transition
- [ ] The command reads the requirement's current status from `.requirement-manifest.json` and determines the correct "next status" using the lifecycle transition map (e.g., PROPOSED→IN_PROGRESS, IN_PROGRESS→CODE_REVIEW)
- [ ] When the next status is reached the command invokes `update-requirement-status.sh` to persist the transition and triggers `regenerate-docs.sh`
- [ ] The command validates that the requirement exists and has a valid next status before starting; invalid or terminal statuses (DEPLOYED, CANCELLED) produce a clear error message

## Technical Notes

- **Prompt file**: Create `.github/prompts/work-on.prompt.md` following the existing pattern (see `start-work.prompt.md`, `show-requirement.prompt.md`).
- **Status lifecycle**: Reuse the transition map already enforced in `scripts/update-requirement-status.sh` — PROPOSED→IN_PROGRESS, IN_PROGRESS→CODE_REVIEW, CODE_REVIEW→MERGED, MERGED→DEPLOYED.
- **Worktree awareness**: The command should check for an active worktree via `.worktree-manifest.json`; if none exists, suggest running `/start-work` first.
- **Iterative loop**: The agent reads the spec's Success Criteria and Technical Notes, implements changes, and loops until the acceptance criteria are met, then advances the status.
- **Affected files**: `.github/prompts/work-on.prompt.md` (new), `copilot-instructions.md` (add `/work-on` to the slash-command table), `docs/requirements/` (spec enrichment).
- **Risk**: If the requirement spec is vague, the agent may not know when to stop — the prompt should instruct the agent to confirm with the user before advancing status.


## Development Plan

1. **Create `.github/prompts/work-on.prompt.md`** — Write the prompt file with YAML frontmatter (`name`, `description`, `argument-hint`, `agent`) and a workflow that: validates the REQ-ID, reads the manifest for current status, determines next status via the lifecycle map, checks for an active worktree, reads the spec, drives iterative implementation, and advances status on completion.
2. **Register `/work-on` in `copilot-instructions.md`** — Add a row to the slash-command table and include `work-on` in the prompt-file registry paragraph.
3. **Validate lifecycle map coverage** — Confirm the prompt handles all non-terminal statuses (PROPOSED→IN_PROGRESS, IN_PROGRESS→CODE_REVIEW, CODE_REVIEW→MERGED, MERGED→DEPLOYED) and rejects terminal ones (DEPLOYED, CANCELLED) with a clear message.
4. **Run `./scripts/regenerate-docs.sh`** — Ensure REQUIREMENTS.md and docs stay in sync after edits.
5. **End-to-end verification** — Read back the prompt file and `copilot-instructions.md` to confirm all success criteria are met.

**Last updated**: 2026-03-29T09:22:24Z

## Dependencies

None

## Worktree

(Will be populated when work starts: feature/REQ-ID-slug)

---

* **Linked Worktree**: feature/REQ-1774775901-add-work-on-command
* **Branch**: feature/REQ-1774775901-add-work-on-command
* **Merged**: No
* **Deployed**: No
