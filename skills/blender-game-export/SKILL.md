---
name: blender-game-export
description: Get a Blender asset into a game engine and prove it arrived intact - triangle and texture budgets, cleanup, LODs, collision meshes, pivot and scale, FBX/glTF/GLB/USD export for Unity, Unreal, Godot, or the web, and re-import verification. Also the inspection-only path for "is this asset ready?" or "check this export". Use whenever someone asks to export, optimize, decimate, make LODs or collision, fix an asset that imports at the wrong scale (100x, 0.01), rotated, facing backwards, missing textures, animations, or bones, or review an asset before handoff, even if they only say "get this into Unity" or "is this game-ready". For shape and topology use blender-game-modeling; for UVs, materials, and baking use blender-game-surfacing.
---

# Blender game export

An export is done when the exported file has been re-imported and measured, not when the exporter returned FINISHED. Exporters happily write files that land at 100x scale, without modifiers applied, or with their roughness maps dropped. Measure the source, export, measure the file, compare.

How to drive Blender is in [../blender-game-modeling/references/operating-blender.md](../blender-game-modeling/references/operating-blender.md).

## Inspection-only path

When asked whether an asset is ready, or to check an existing export, do not change anything. Run the inspection, review renders, and the budget table below, then report findings with numbers and say which checks need the target engine.

```bash
blender -b --factory-startup --python-exit-code 1 \
  -P <skills>/blender-game-export/scripts/inspect_asset.py -- \
  --file /abs/asset.blend [--objects SM_A SM_B] --json /abs/source.json
```

The report lists, per mesh: evaluated triangles, scale, UV maps, materials with the image maps feeding each Principled input and their color spaces, shape keys, max vertex weights; per armature: bones, deform bones, root bones, scale; actions; world bounds; and warnings (unapplied or negative scale, missing UVs or materials, more than 4 weights, more than one root bone, base not on z = 0).

## Export workflow

1. **Budget.** Compare triangles, materials, and texture sizes with the target (table below). Over budget: reduce in this order, cheapest visual loss first: hidden and interior faces, unneeded loops on flat areas (Limited Dissolve 1 to 5 degrees), over-segmented cylinders, Decimate, then move detail into the normal map (blender-game-surfacing).
2. **Clean.** Merge by distance (0.1 mm), remove degenerate faces and loose geometry, recalculate normals outward.
3. **Scale, rotation, pivot.** Scene unit scale 1.0. Apply rotation and scale on every exported object. Props: origin at the center of the base, base on z = 0. Characters: origin at world origin between the feet, facing -Y (Blender's front). Engines place objects by origin, so a centered origin sinks the asset halfway into the floor.
4. **LODs and collision** if the target needs them. See [references/lods-and-collision.md](references/lods-and-collision.md).
5. **Measure the source**: `inspect_asset.py --file source.blend --json source.json`.
6. **Export** with the target's settings from the engine reference. Export only the objects the file needs: a skinned mesh together with its armature, LODs with their group, collision beside its render mesh.
7. **Measure the export**: `inspect_asset.py --file export.glb --json export.json` (the script imports it into an empty scene).
8. **Compare**: `python3 inspect_asset.py --compare source.json export.json`. It lists differences in size (1 mm tolerance), base height, triangles, material maps, actions, shape keys, deform bones, and armature scale, and exits 2 when there are any. Fix each difference or state why it is expected, such as LODs or collision meshes present in only one of the two files.
9. **Engine check** when the engine is available: import, compare against the engine's scale reference, check smoothing, the normal map green channel, and animation. When no engine is available, say the verification stopped at a Blender re-import.

## Budgets (per asset, guidance not law)

| Platform | Hero character tris | Prop tris | Materials per asset | Max texture | Bones |
|---|---|---|---|---|---|
| Mobile | 5k to 15k | 300 to 3k | 1 to 2 | 1024 | 75 or fewer |
| Web (three.js, Babylon) | 10k to 30k | 1k to 10k | 1 to 2 | 2048 | 100 or fewer |
| Standalone VR | 10k to 40k | 1k to 10k | 1 to 3 | 2048 | 100 or fewer |
| Console or PC | 50k to 150k | 5k to 50k | 2 to 6 | 4096 | 150 to 300 |
| Unreal Nanite (static) | n/a | millions acceptable | few | 4096+ | n/a |

Compiled by el4cteo/blender-skills as 2026 guidance. Whole-scene limits matter more than single assets: mobile is roughly 100k to 300k visible triangles and under 100 to 200 draw calls. Engine vertex counts run 1.5 to 3x Blender's because every UV seam and hard edge splits vertices.

## Facts the check caught in testing (Blender 5.3)

- The glTF exporter's `export_apply` defaults to False: a beveled crate exported with 12 triangles instead of 44. Pass `export_apply=True` unless the modifiers are deliberately left out.
- A GLB re-import adds an `Icosphere` object used to display bones; it is not part of the asset. `inspect_asset.py` skips it.

## Scripts

Run them through `blender-game-modeling/scripts/run_in_blender.py` (see operating-blender.md). Each returns JSON.

| Script | Does |
|---|---|
| `mesh_stats.py` | `--budget mobile\|web\|vr\|console\|pc`: triangles, estimated draw calls, materials, texture memory, bones, and what is over budget |
| `make_lods.py` | `--cleanup` (merge by distance, dissolve degenerate, delete loose); `--rename` builds `_LOD1` to `_LOD3` at 50, 25 and 12.5% |
| `export_asset.py` | Export presets: `unity`, `unity_skeletal`, `gltf`, `unreal`, `unreal_skeletal`, `godot`, `web`, `usd`. `--batch` writes one file per object at the origin; `--set key=value` overrides any exporter option. GLB presets apply modifiers (`export_apply=True`). |
| `inspect_asset.py` | Measures a .blend or an export and compares two reports (above) |

Rigged characters: build the game skeleton and bake clips with `blender-rigging-animation` before exporting.

## Engine references

Load only the one for the target:

- [references/unity.md](references/unity.md), with [references/unity-bridge-fidelity.md](references/unity-bridge-fidelity.md) (what survives FBX vs GLB, tested) and [references/unity-mcp-handoff.md](references/unity-mcp-handoff.md) (Blender MCP to Unity MCP file handoff)
- [references/unreal.md](references/unreal.md)
- [references/godot.md](references/godot.md)
- [references/web.md](references/web.md)
- [references/lods-and-collision.md](references/lods-and-collision.md)

## Universal pre-export checklist

- Unique ASCII names with no spaces; engines key meshes and materials by name across reimports.
- Materials are Image Texture to Principled chains only (bake procedural nodes first).
- Triangulate the export copy (or let the exporter) the same way the bake mesh was triangulated.
- Armatures: deform bones only, no leaf bones, one root bone, rest pose equals bind pose, at most 4 weights per vertex.
- Animation: one action per clip, named as the clip should appear in the engine. Bake constraints and IK to keys.
- Keep the editable source; export from a copy with modifiers applied.
