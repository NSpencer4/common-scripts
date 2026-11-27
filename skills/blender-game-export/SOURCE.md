# Snapshot provenance

Original skill adapted from the sources below. Scripts listed under the merge section are vendored from el4cteo/blender-skills. Not installed via `npx skills`. Do not auto-update.

- Origin: https://github.com/el4cteo/blender-skills at 1a1cc6c (blender-game-optimization, blender-export-pipelines, blender-asset-qa), MIT
- Origin: https://github.com/scenario-labs/skills at 3c4d18c (scenario-blender-export), MIT
- scripts/inspect_asset.py written for this skill and tested with .blend, GLB, and FBX round trips on Blender 5.3.0
- Selected from a review of the skills.sh "blender" search results
- Snapshot date: 2026-11-25

## Upstream licenses

Both sources are MIT licensed. Their notices apply to the adapted portions:

- Copyright (c) 2026 EL4CTEO
- Copyright (c) 2026 Scenario Inc.

## Merged in from the Unity skills branch (2026-11-27)

- From el4cteo/blender-skills at 1a1cc6c (MIT), unchanged: `scripts/export_asset.py`, `mesh_stats.py`, `make_lods.py`, `_bpyx.py`
- From CoplayDev/unity-mcp at 19b66ec (MIT): `.claude/skills/blender-to-unity` body and `references/bridge-fidelity.md` (now `references/unity-mcp-handoff.md`, `references/unity-bridge-fidelity.md`); the format choice in `references/unity.md` is drawn from its test results
- Run in Blender 5.3.0 headless: `mesh_stats`, `make_lods`, and `export_asset` with the `unity`, `unity_skeletal` and `gltf` presets.
- License files: `licenses/`.
