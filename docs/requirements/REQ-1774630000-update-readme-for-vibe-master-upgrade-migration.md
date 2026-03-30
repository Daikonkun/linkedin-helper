# Update README for Vibe Master upgrade migration

**ID**: REQ-1774630000  
**Status**: MERGED  
**Priority**: MEDIUM  
**Created**: 2026-03-28T00:30:00Z  

## Description

Update README so agents and users understand how to upgrade Vibe Master in an existing project that was built with an older Vibe Master version.

## Success Criteria

- [x] README includes an "Upgrading Existing Projects" section for migration from older Vibe Master versions.
- [x] Section explains which files/folders to compare, replace, or merge when adopting the latest template.
- [x] Section includes a safe upgrade workflow (backup, branch/worktree, validate manifests/docs, run review) and compatibility notes.

## Technical Notes

Cover migration steps for `.github/agents`, `.github/prompts`, `.github/skills`, `copilot-instructions.md`, manifest files, and docs regeneration expectations.

Implementation complete in feature branch `feature/REQ-1774630000-update-readme-for-vibe-master-upgrade-migration`:
- Added `Upgrading Existing Projects` section to `README.md`
- Added safe migration workflow with backup/worktree/validation/review commands
- Added replace-vs-merge table for key repo paths used during upgrades
- Added compatibility notes and post-upgrade verification checklist

## Dependencies

(List other requirement IDs if applicable, e.g., REQ-XXX, REQ-YYY)

## Worktree

feature/REQ-1774630000-update-readme-for-vibe-master-upgrade-migration

---

* **Linked Worktree**: feature/REQ-1774630000-update-readme-for-vibe-master-upgrade-migration
* **Branch**: feature/REQ-1774630000-update-readme-for-vibe-master-upgrade-migration
* **Merged**: No
* **Deployed**: No
