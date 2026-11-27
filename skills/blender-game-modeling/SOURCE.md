# Snapshot provenance

Original skill adapted from the sources below. Scripts listed under the merge section are vendored from el4cteo/blender-skills. Not installed via `npx skills`. Do not auto-update.

- Origin: https://github.com/el4cteo/blender-skills at 1a1cc6c (blender-core, blender-hardsurface-modeling, blender-retopology-uv, blender-sculpting), MIT
- Origin: https://github.com/scenario-labs/skills at 3c4d18c (scenario-blender-expert, scenario-blender-hard-surface, scenario-blender-retopology), MIT
- scripts/review_renders.py written for this skill and tested on Blender 5.3.0
- Selected from a review of the skills.sh "blender" search results
- Snapshot date: 2026-11-25

## Upstream licenses

Both sources are MIT licensed. Their notices apply to the adapted portions:

- Copyright (c) 2026 EL4CTEO
- Copyright (c) 2026 Scenario Inc.

## Merged in from the Unity skills branch (2026-11-27)

- From el4cteo/blender-skills at 1a1cc6c (MIT), unchanged apart from skill names in docstrings: `scripts/run_in_blender.py`, `env_report.py`, `_bpyx.py`, `scene_audit.py`, `batch_process.py`, `apply_stack.py`, `auto_retopo.py`, `qa_check.py`, `review_shots.py`, `terrain.py`, `scatter.py`, `kit_check.py`; references `api-changes-5x.md`, `bpy-patterns.md`, and the bodies of `blender-scene-setup`, `blender-pipeline-automation`, `blender-asset-qa`, `blender-environment-kits` (now `scene-setup.md`, `pipeline-automation.md`, `asset-qa.md`, `environment-kits.md`)
- From vladmdgolam/agent-skills at b66d157 (MIT): `blender-mcp` body and `references/errors.md` (now `blender-mcp.md`, `blender-mcp-errors.md`)
- From arjun988/blender-skills at 904f095 (MIT): `lowpoly-style` body and `references/ps1-aesthetic.md`
- Skill names in the moved text renamed to this repo's skills; em dashes replaced. Run in Blender 5.3.0 headless: `env_report`, `scene_audit`, `qa_check`.
- License files: `licenses/`.
