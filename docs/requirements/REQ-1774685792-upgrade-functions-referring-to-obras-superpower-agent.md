# upgrade functions referring to obra's superpower agent

**ID**: REQ-1774685792  
**Status**: MERGED  
**Priority**: MEDIUM  
**Created**: 2026-03-28T08:16:32Z  

## Description

read the repo https://github.com/obra/superpowers and suggest what functions can be referred to upgrade vibe master, yet not changing current workflow and standards significantly

## Success Criteria

- [x] Research and summarize key skills from https://github.com/obra/superpowers (brainstorming, writing-plans, using-git-worktrees, test-driven-development, requesting-code-review, systematic-debugging, subagent-driven-development)
- [x] Identify 3-5 specific functions/skills in superpowers that align with Vibe Master's current patterns in .github/skills/, copilot-instructions.md, and scripts/
- [x] Update relevant prompt files (add-requirement.prompt.md, agent-customization/SKILL.md, etc.) to reference compatible superpowers skills without altering core workflow or slash-command standards
- [x] Add concrete references in technical notes and update REQUIREMENTS.md via regeneration
- [x] Verify no breaking changes to existing requirement lifecycle or worktree management

## Technical Notes

- Review superpowers skills in `skills/` dir (e.g. `brainstorming`, `writing-plans`, `using-git-worktrees`, `systematic-debugging`, `test-driven-development`).
- Vibe Master already implements similar patterns via SKILL.md files in `.github/skills/`, `copilot-instructions.md`, `add-requirement.prompt.md`, and scripts like `create-requirement.sh`, `start-work.sh`.
- Approach: Map compatible superpowers skills to existing Vibe skills without replacing core orchestrator logic or requirement manifest handling. Update references in prompt files and SKILL.md only where they enhance without disruption.
- Affected areas: `.github/skills/*/*.md`, `copilot-instructions.md`, `docs/requirements/*.md`, `.requirement-manifest.json` notes field.
- Risks: Over-alignment could break custom Vibe Agent Orchestrator mode; keep changes minimal and backward-compatible.

## Development Plan

1. Open the worktree at `/Users/bluoaa/Desktop/Work/Vibe Coding Stuff/feature/REQ-1774685792-upgrade-functions-referring-to-obra-s-superpower-agent` (or use VS Code "Open Folder" on that path).
2. Read relevant skill files: `.github/skills/*/SKILL.md`, `copilot-instructions.md`, `.github/prompts/*.prompt.md`.
3. Identify 3-5 superpowers skills/functions that map directly (e.g. systematic-debugging → debug/SKILL.md, using-git-worktrees → worktree-manager/SKILL.md).
4. Update `copilot-instructions.md` and affected SKILL.md/prompt files with minimal references to compatible superpowers patterns.
5. Run `./scripts/regenerate-docs.sh` and test with `/status` to verify no workflow changes.

**Review fixes applied**: Success criteria checked, skill registration clarified in copilot-instructions.md, whitespace cleaned.











## Dependencies

None

## Worktree

feature/REQ-1774685792-upgrade-functions-referring-to-obra-s-superpower-agent (active at /Users/bluoaa/Desktop/Work/Vibe Coding Stuff/feature/REQ-1774685792-upgrade-functions-referring-to-obra-s-superpower-agent)

---

* **Linked Worktree**: feature/REQ-1774685792-upgrade-functions-referring-to-obra-s-superpower-agent
* **Branch**: feature/REQ-1774685792-upgrade-functions-referring-to-obra-s-superpower-agent
* **Merged**: No
* **Deployed**: No
