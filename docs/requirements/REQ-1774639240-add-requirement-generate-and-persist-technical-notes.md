# Add-requirement: populate spec sections after creation

**ID**: REQ-1774639240  
**Status**: MERGED  
**Priority**: HIGH  
**Created**: 2026-03-27T19:20:40Z  

## Description

Source: code-review. Severity: HIGH. Evidence: `add-requirement.prompt.md` defines 5 workflow steps but none instruct the agent to populate the spec file sections after the shell script creates it. `create-requirement.sh` writes static placeholders for Success Criteria (`Criterion 1/2/3`), Technical Notes (`Add implementation notes here`), Dependencies (`List other requirement IDs...`), and Worktree (`Will be populated when work starts`). The prompt workflow ends with a summary — it never tells the agent to fill in any of these sections from the user's input or by analysis.

Required outcome: add a step in `add-requirement.prompt.md` (between steps 3 and 4) instructing the agent to read the generated spec file and populate:
1. **Success Criteria** — derive 3-5 testable acceptance criteria from the description
2. **Technical Notes** — analyze the description and note implementation approach, affected areas, risks
3. **Dependencies** — detect references to other REQ IDs in the description and link them
4. **Worktree** — no action needed (populated by `/start-work`), but the prompt should clarify this

Also populate the manifest `notes` field with a summary of the technical notes.

## Success Criteria

- [ ] After `/add-requirement`, the spec file's `## Success Criteria` contains requirement-specific acceptance items (not placeholders)
- [ ] After `/add-requirement`, the spec file's `## Technical Notes` contains agent-generated implementation considerations
- [ ] After `/add-requirement`, the spec file's `## Dependencies` lists any REQ IDs mentioned in the description (or states "None")
- [ ] The manifest `notes` field is populated with a brief technical summary
- [ ] The `## Worktree` section placeholder is acceptable (populated later by `/start-work`)

## Technical Notes

- The fix is a prompt workflow change in `add-requirement.prompt.md`, not a shell script rewrite
- The shell script's job is to scaffold the file; the agent's job (per the prompt) should be to enrich it
- Add a new step 4: "Read the generated spec file. Derive success criteria from the description and replace the placeholder items. Generate technical notes (approach, risks, affected areas). Detect any REQ-ID references in the description and list them under Dependencies. Update the manifest `notes` field."
- Renumber existing steps 4-5 to 5-6
- Consider also having the agent ask the user to confirm/refine the generated criteria

## Dependencies

None

## Worktree

(Will be populated when work starts: feature/REQ-ID-slug)

---

* **Linked Worktree**: feature/REQ-1774639240-add-requirement-populate-spec-sections-after-creation
* **Branch**: feature/REQ-1774639240-add-requirement-populate-spec-sections-after-creation
* **Merged**: Yes
* **Deployed**: No
