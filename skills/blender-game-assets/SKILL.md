---
name: blender-game-assets
description: >-
  Makes game-ready assets in Blender 5.2+: hard-surface and mid-poly modeling, low-poly and
  retro styles, retopology, UV seams, packing and texel density, lightmap UVs, PBR materials and
  color spaces, wear and grime texturing, trim sheets and decals, high-to-low baking with ORM
  packing, polygon and draw call budgets, LODs, collision proxies, terrain, scatter and modular
  kits, and the QA gate every mesh must pass. Use for any prop, weapon, vehicle, building or
  environment piece headed to a game engine. Not for rigging or animation
  (blender-rigging-animation) or the export itself (blender-to-unity).
license: MIT
compatibility: Blender 5.2 LTS or newer, verified upstream on 5.3. Baking uses Cycles.
---

# Blender Game Assets

Run every script the way `blender-core` describes (live MCP import, or headless through
`blender-core/scripts/run_in_blender.py`). Every script takes `--objects` and returns JSON.

## Pipeline

1. **Scene and scale** (`blender-core` scene setup): metric, 1 unit = 1 m, named collections,
   `SM_` names, origin at the bottom-center.
2. **Model**: pick mid-poly, high-to-low, or subdivision first.
   [references/hardsurface-modeling.md](references/hardsurface-modeling.md). Stack:
   `scripts/apply_stack.py -- --objects Body --preset midpoly --cutters Cut1 Cut2`.
   Retro or low-poly look: [references/lowpoly-style.md](references/lowpoly-style.md).
3. **Retopology and UVs**: `scripts/auto_retopo.py`, `scripts/uv_pack.py --seams-from-sharp 60`,
   `scripts/texel_density.py --res 2048`. Every hard edge must be a UV seam.
   [references/retopology-uv.md](references/retopology-uv.md).
4. **Materials**: `scripts/build_pbr_material.py -- --name M_Crate --textures //tex/crate`.
   Metallic is 0 or 1, base color has no lighting, data maps are Non-Color.
   [references/pbr-materials.md](references/pbr-materials.md),
   [references/pbr-values.md](references/pbr-values.md).
5. **Surface detail**: `scripts/smart_material.py` (wear, rust, grime, dust), `scripts/decal.py`.
   [references/texturing.md](references/texturing.md),
   [references/trims-tiling-painting.md](references/trims-tiling-painting.md).
6. **Bake** to textures, since engines do not run Blender node trees:
   `scripts/bake_maps.py -- --low SM_Crate --high Crate_high --maps normal ao curvature --pack-orm`.
   [references/texture-baking.md](references/texture-baking.md).
7. **Budget, LODs, collision**: `scripts/mesh_stats.py --budget mobile|web|vr|console|pc`,
   `scripts/make_lods.py --rename`. [references/game-optimization.md](references/game-optimization.md),
   [references/lod-pipeline.md](references/lod-pipeline.md),
   [references/collision-proxy.md](references/collision-proxy.md),
   [references/asset-optimization.md](references/asset-optimization.md).
8. **QA gate** (required): `scripts/qa_check.py -- --objects <all parts> --profile game` until
   `"pass": true`, then look at it with `scripts/review_shots.py`.
   [references/asset-qa.md](references/asset-qa.md).
9. **Export** with `blender-to-unity`.

Environments: `scripts/terrain.py`, `scripts/scatter.py`, `scripts/kit_check.py --grid 0.5`.
[references/environment-kits.md](references/environment-kits.md).

## Rules for Unity-bound assets

- Normal maps are OpenGL (Y+), the same as Blender. Do not flip green for Unity.
- URP Lit wants a Metallic map with R = metallic and A = smoothness (1 minus roughness). HDRP
  wants a Mask Map: R metallic, G AO, B detail mask, A smoothness. Bake roughness, then invert
  into alpha when packing.
- One material per texture set; each material slot is roughly one draw call.
- Power-of-two textures. PNG or TGA for data maps, never JPEG for normals.
- Lightmap UV2 for static scenery: ship one (`uv_pack.py --lightmap`) or let Unity generate it.
- LOD names `SM_X_LOD0`, `_LOD1`, `_LOD2`: Unity builds a LOD Group from the suffixes.
- Engine vertex counts run 1.5 to 3 times Blender's because seams and hard edges split vertices.
  Budget against the engine number.

## Budgets per asset (guidance)

| Platform | Hero character tris | Prop tris | Materials | Max texture |
|---|---|---|---|---|
| Mobile | 5k to 15k | 300 to 3k | 1 to 2 | 1024 |
| Web | 10k to 30k | 1k to 10k | 1 to 2 | 2048 |
| Standalone VR | 10k to 40k | 1k to 10k | 1 to 3 | 2048 |
| Console and PC | 50k to 150k | 5k to 50k | 2 to 6 | 4096 |

Scene totals matter more than single assets. Full table:
[references/game-optimization.md](references/game-optimization.md).

## Related skills

- `blender-core`: execution, API rules, scene setup, batch jobs.
- `blender-rigging-animation`: anything that deforms.
- `blender-to-unity`: export presets, import settings, materials in Unity.
- `unity-build-perf`: measuring what the assets cost in a real build.
