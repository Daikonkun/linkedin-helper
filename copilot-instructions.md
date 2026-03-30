---
name: Vibe Project Instructions
description: "Global instructions for all agents in vibe coding projects. Ensures consistent behavior, requirement tracking, and worktree management across all development workflows."
---

# Vibe Project Instructions

## Core Principles
- **User-centric AI coding**: The user only interfaces via VS Code and this agent
- **Transparent requirement tracking**: Every product requirement is visible, versioned, and linked to code
- **Parallel development**: Git worktrees enable safe, isolated feature work
- **Automated orchestration**: Minimal manual git/CLI work; agent handles branching, tracking, docs

## Best Practices

### When accepting a requirement:
1. Ask clarifying questions if vague
2. Identify dependencies on other requirements  
3. Suggest a worktree strategy (standalone vs. grouped)
4. Record the requirement with a unique ID (REQ-{timestamp-based})

### Before creating code:
1. Check if a related worktree already exists
2. If not, create one with a clear naming convention: `feature/{req-id}-{slug}`
3. Document the requirement link in the worktree

### During development:
1. Keep requirement status updated in `.requirement-manifest.json`
2. Tag commits with requirement ID: `feat(REQ-123): description`
3. On state changes, auto-regenerate documentation

### On merge/deployment:
1. Move requirement to MERGED/DEPLOYED
2. Clean up associated worktree
3. Regenerate all dashboards and timelines

## Key Files (Keep Updated)
- `REQUIREMENTS.md` — Human-readable requirement list
- `.requirement-manifest.json` — Structured requirement data (machine-readable)
- `docs/requirements/{id}-{name}.md` — Detailed requirement specs
- `.worktree-manifest.json` — Map of worktrees to requirements
- `docs/STATUS.md` — Auto-generated status dashboard

## Documentation Auto-Generation
After any state change, regenerate:
- `docs/STATUS.md` (kanban board + stats)
- `docs/ROADMAP.md` (timeline + milestones)
- `docs/DEPENDENCIES.md` (requirement dependency graph)
- Root `REQUIREMENTS.md` (summary table)

## Slash Commands Available

| Command | Purpose |
|---------|---------|
| `/add-requirement` | Submit new product requirement |
| `/status` | View current project status |
| `/start-work <req-id>` | Move requirement to IN_PROGRESS, create worktree |
| `/update-requirement <req-id> <new-status> [--force] [--no-refresh]` | Update requirement status using validated lifecycle transitions |
| `/show-requirement <req-id>` | Show detailed requirement info |
| `/list-requirements [status]` | List all requirements, optionally filtered by status |
| `/worktree-list` | Show all active worktrees and their linked requirements |
| `/worktree-create <req-id>` | Manually create a worktree for a requirement |
| `/worktree-prune` | Remove orphaned worktrees |
| `/worktree-status` | Show comprehensive worktree status dashboard |
| `/worktree-merge <branch>` | Merge associated worktree and update docs |
| `/dependency-graph` | Visualize requirement dependencies |
| `/roadmap` | Show timeline view of all requirements |
| `/bug-fix "issue summary" [scope]` | Run structured debugging workflow and root-cause analysis |
| `/update-manual [scope]` | Generate and refresh user manual content |
| `/code-review [scope]` | Review code and create REQ follow-up threads for unresolved findings |
| `/work-on <req-id>` | Work on a requirement until it reaches its next lifecycle status |

Slash commands appear in chat only when they are backed by prompt files or valid skill definitions. `/add-requirement`, `/list-requirements`, `/update-requirement`, `/start-work`, `/show-requirement`, `/status`, `/worktree-list`, `/worktree-create`, `/worktree-prune`, `/worktree-status`, `/worktree-merge`, `/dependency-graph`, `/roadmap`, `/regen-docs`, `/bug-fix`, `/update-manual`, `/code-review`, and `/work-on` are implemented by prompt files in `.github/prompts/`; skill files must keep lowercase hyphenated `name` values that match their folder names.

Note: Use `/worktree-merge <branch-name>` (not `/merge-requirement`) to complete a requirement.

## Git Worktree Convention
```
main/develop (default)
  ├── feature/REQ-001-auth-system
  ├── feature/REQ-002-user-dashboard
  ├── fix/REQ-003-login-bug
  └── feature/REQ-004+REQ-005-related-features (grouped)
```

Naming: `{type}/{req-ids}-{slug}`  
Types: `feature`, `fix`, `refactor`, `docs`

## Conflict Resolution
If multiple requirements:
- Conflict in files → flag and suggest sequential or grouped worktrees
- Dependency chain → order them in worktree creation
- Same goal, different users → consolidate into single requirement with variants

## Notes for AI-Only Workflow
- No manual git cherry-pick or complex rebasing — agent handles it
- No context switching between files and CLI — everything happens here
- Clear requirement → worktree → code → merge pipeline
- User reviews agent decisions; agent auto-executes approved work

## Superpowers Alignment (REQ-1774685792)
Compatible references (minimal, non-breaking):
- `systematic-debugging` → aligns with `debug/SKILL.md` workflow
- `using-git-worktrees` → aligns with `worktree-manager/SKILL.md` + `start-work.prompt.md`
- `writing-plans` / `brainstorming` → aligns with requirement-tracker and `generate-plan.sh`
- `test-driven-development` → aligns with code-review and execution standards
- `agent-customization` skill now created (with matching prompt registration below) to handle prompt/SKILL.md updates

These enhance documentation and consistency without changing slash commands, manifest logic, or orchestrator mode.

**Slash command registry update**: `agent-customization` skill is now available via its SKILL.md (no dedicated prompt needed for single-file edits per its own guidelines).
