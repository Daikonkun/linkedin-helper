# Review follow-up: separate manifest schema from data

**ID**: REQ-1774770298  
**Status**: MERGED  
**Priority**: HIGH  
**Created**: 2026-03-29T07:44:58Z  

## Description

Source: code-review. Severity: HIGH. Evidence: .requirement-manifest.json and .worktree-manifest.json both embed JSON Schema keywords (properties, type, title, description) alongside actual data arrays at the same level. This fails JSON Schema validation and causes semantic ambiguity with the required keyword. Required outcome: move schema definitions to separate .schema.json files referenced by a top-level dollar-schema key, keeping manifests as pure data files.

## Success Criteria

- [x] `.requirement-manifest.json` contains only data fields (`version`, `projectName`, `requirements` array) — no JSON Schema keywords (`$schema`, `title`, `description`, `type`, `properties`, `required` as schema directives)
- [x] `.worktree-manifest.json` contains only data fields (`version`, `worktrees` array) — no JSON Schema keywords
- [x] Both manifest files include a top-level `"$schema"` key pointing to the corresponding `.schema.json` file
- [x] `.requirement-manifest.schema.json` exists with the extracted JSON Schema definition
- [x] `.worktree-manifest.schema.json` exists with the extracted JSON Schema definition
- [x] All scripts that initialize empty manifests (`create-requirement.sh`, `start-work.sh`, `init-project.sh`) produce manifests with the `$schema` reference and no embedded schema keywords
- [x] `jq .` passes on both refactored manifest files
- [x] Existing jq queries in scripts (`regenerate-docs.sh`, `update-requirement-status.sh`, `worktree-merge.sh`, `start-work.sh`) continue to work unchanged

## Technical Notes

Both manifest files currently embed JSON Schema keywords (`$schema`, `title`, `description`, `type`, `properties`, `required`) at the same level as actual data arrays. The `required` keyword is particularly ambiguous — it appears as both a schema directive listing required properties and could be confused with the `requirements` data array.

**Approach**: Extract schema definitions into separate `.schema.json` files. Keep manifests as pure data with a `$schema` reference. Scripts already use `.requirements[]` and `.worktrees[]` jq patterns, so data access is unaffected — only init blocks that create empty manifests need a `$schema` key added.

**Affected files**:
- `.requirement-manifest.json` — remove schema keywords, add `$schema` ref
- `.worktree-manifest.json` — remove schema keywords, add `$schema` ref
- `scripts/create-requirement.sh` — add `$schema` to init block
- `scripts/start-work.sh` — add `$schema` to worktree manifest init block
- `scripts/init-project.sh` — add `$schema` to both init blocks

## Dependencies

None

## Development Plan

1. **Create `.requirement-manifest.schema.json`** — Extract the JSON Schema from `.requirement-manifest.json` (properties, types, enums, required fields) into a standalone draft-07 schema file.
2. **Create `.worktree-manifest.schema.json`** — Extract the JSON Schema from `.worktree-manifest.json` into a standalone draft-07 schema file.
3. **Refactor `.requirement-manifest.json`** — Remove all schema keywords, keep only `$schema` reference + data (`version`, `projectName`, `requirements` array with actual entries).
4. **Refactor `.worktree-manifest.json`** — Same extraction, keep only `$schema` reference + data.
5. **Update script init blocks** — Add `"$schema"` key to the heredoc templates in `create-requirement.sh`, `start-work.sh`, and `init-project.sh`.
6. **Validate** — Run `jq .` on both manifests and verify all scripts' jq queries still work.
7. **Update REQ spec** — Mark success criteria, update status to MERGED, regenerate docs.

## Worktree

(Working directly on main — self-contained structural change)

---

* **Linked Worktree**: None yet
* **Branch**: None yet
* **Merged**: No
* **Deployed**: No
