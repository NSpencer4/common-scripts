# Snapshot provenance

Original skill adapted from the sources below. Scripts listed under the merge section are vendored from el4cteo/blender-skills. Not installed via `npx skills`. Do not auto-update.

- Origin: https://github.com/el4cteo/blender-skills at 1a1cc6c (blender-retopology-uv, blender-texture-baking, blender-pbr-materials, blender-texturing), MIT
- Origin: https://github.com/scenario-labs/skills at 3c4d18c (scenario-blender-uv-baking), MIT
- Bake settings in references/baking.md tested with a high-to-low normal bake on Blender 5.3.0
- Selected from a review of the skills.sh "blender" search results
- Snapshot date: 2026-11-25

## Upstream licenses

Both sources are MIT licensed. Their notices apply to the adapted portions:

- Copyright (c) 2026 EL4CTEO
- Copyright (c) 2026 Scenario Inc.

## Merged in from the Unity skills branch (2026-11-27)

- From el4cteo/blender-skills at 1a1cc6c (MIT), unchanged: `scripts/uv_pack.py`, `texel_density.py`, `build_pbr_material.py`, `smart_material.py`, `decal.py`, `bake_maps.py`, `_bpyx.py`; references `pbr-values.md`, `trims-tiling-painting.md`, and the `blender-texturing` body (now `texturing.md`)
- Skill and file names in the moved text renamed to this repo's skills; em dashes replaced. Run in Blender 5.3.0 headless: `build_pbr_material`, `uv_pack`.
- License files: `licenses/`.
