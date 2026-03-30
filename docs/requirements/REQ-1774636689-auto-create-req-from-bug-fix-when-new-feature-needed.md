# Auto-create REQ from bug-fix when new feature needed

**ID**: REQ-1774636689  
**Status**: DEPLOYED  
**Priority**: MEDIUM  
**Created**: 2026-03-27T18:38:09Z  

## Description

During a /bug-fix session, if the bug fix requires implementing a new function or feature of the vibe project to complete, the debug skill should automatically create a new REQ to track that work and link it as a dependency.

## Success Criteria

- [x] Debug skill SKILL.md includes a "Feature Escalation" section describing when and how to create a new REQ during a bug fix
- [x] Instructions specify using `create-requirement.sh` with appropriate name/description/priority
- [x] Instructions specify linking the new REQ as a dependency in the original bug-fix REQ

## Technical Notes

Implementation is documentation-only: add a new workflow section to the debug SKILL.md that instructs the agent to detect when a bug fix needs new functionality and auto-create a tracked REQ for it.

## Dependencies

(none)

## Worktree

feature/REQ-1774636689-auto-create-req-from-bug-fix-when-new-feature-needed

---

* **Linked Worktree**: feature/REQ-1774636689-auto-create-req-from-bug-fix-when-new-feature-needed
* **Branch**: feature/REQ-1774636689-auto-create-req-from-bug-fix-when-new-feature-needed
* **Merged**: Yes
* **Deployed**: Yes
