---
name: blender-game-surfacing
description: Give a game asset its surface in Blender - UV seams, unwrapping, packing, texel density, PBR materials, trim sheets, texture painting, and baking high-poly detail (normal, AO, curvature, ID) onto a low poly. Use whenever someone asks to UV unwrap, fix seams or stretching, set texel density, bake maps, set up or fix materials, pack ORM or mask textures, or diagnose bake artifacts (black patches, wavy lines, visible seams, inverted green channel) on a Blender model meant for a game engine, even if they only say "texture this" or "the normal map looks wrong". For shape and topology use blender-game-modeling; for budgets, LODs, and export use blender-game-export.
---

# Blender game surfacing

UVs, materials, and bakes share one acceptance test: the intended detail survives on the low-poly mesh, in the target engine's conventions, at gameplay distance. A bake that looks fine in Blender but cracks at every hard edge in the engine has failed, so check against the delivery conventions from the start.

How to drive Blender and render review images is in [../blender-game-modeling/references/operating-blender.md](../blender-game-modeling/references/operating-blender.md). Read it before the first Blender call in a session.

## Establish first

| Input | Why it changes the plan | Default when silent |
|---|---|---|
| Target engine | Normal map green channel, channel packing, UV set count | glTF conventions (OpenGL normals, ORM packing) |
| Gameplay camera | Texel density | Third person, 512 px/m |
| Texture budget | Resolution and number of texture sets | One 2048 set per asset |
| Texturing method | Unique bake, tiling material, trim sheet, or hand painting | Unique bake for a hero prop; trim or tiling for modular pieces |
| High-poly source | Selected-to-active bake vs self-bake of procedural materials | Separate `X_high` object |
| Mirrored or stacked UVs allowed? | Saves space but breaks unique bakes | Unique UVs on anything baked |

## Workflow

1. **Pre-flight.** Scale applied, normals consistent, no loose or duplicate geometry. If UVs already exist, inspect them before re-unwrapping: seam flags left over from retopology are often wrong.
2. **Seams.** Every hard edge (`sharp_edge`, roughly over 60 degrees) must be a UV seam, or the normal map cracks along it. Hide the rest where the camera rarely looks: undersides, inner limbs, back faces, behind parts. Closed shapes (cylinders, tubes) need one cut each.
3. **Unwrap.** Always pass `method=`: `"ANGLE_BASED"` for hard surface, `"MINIMUM_STRETCH"` for organic. Check every face got UVs; the operator can return FINISHED on an island it failed to solve.
4. **Straighten** rectangular islands so trims and pixel grids line up (Follow Active Quads in a live session).
5. **Texel density.** Set density before choosing texture size. Keep the spread within about 1.3x inside an asset; hero areas (faces, hands, front) may be denser, hidden areas less.
6. **Pack** with padding in pixels: about resolution / 128 (8 px at 1K, 16 px at 2K, 32 px at 4K). Pack without rotation after straightening. Gate: no overlaps (unless deliberately stacked), coverage around 70% or better.
7. **Materials.** Principled BSDF with image textures; correct color spaces; one material per texture set. See [references/materials.md](references/materials.md).
8. **Bake** high to low, or self-bake procedural materials to textures. Test at 512, then the final resolution. See [references/baking.md](references/baking.md).
9. **Review.** Render the low poly with its maps next to the high poly under a raking light, plus a checker-texture pass for stretch. The low with maps should read like the high from the gameplay camera.
10. **Report** resolution, texel density, padding, maps produced with their color spaces and conventions, and anything not checked in the target engine.

## Hard rules and why

- **Hard edge means UV seam.** A split normal inside a UV island has no padding to hide the discontinuity, so the baked map shows a crack.
- **Triangulate the bake mesh the way the engine will.** Tangent space depends on triangulation; mismatched triangulation shows as shading seams.
- **Never edit UVs after baking.** The maps are tied to that layout; re-bake instead.
- **Data maps are Non-Color.** Normal, roughness, metallic, AO, ORM, and masks in sRGB give washed-out normals and wrong roughness, the most common material bug.
- **Engines do not run Blender node trees.** Procedural noise, mix nodes, and math produce nothing after export; bake them to textures.

## Scripts

Run them through `blender-game-modeling/scripts/run_in_blender.py` (see operating-blender.md). Each returns JSON.

| Script | Does |
|---|---|
| `uv_pack.py` | `--seams-from-sharp 60` marks every hard edge as a seam, unwraps (`--method seams\|min_stretch\|smart`), packs with pixel margins, `--lightmap` adds a lightmap UV2 |
| `texel_density.py` | `--res 2048` measures px/m and spread; `--set <px/m>` scales islands to a target |
| `build_pbr_material.py` | `--name M_X --textures //tex/x` wires a texture set by filename with correct color spaces, splits ORM, flips DirectX normals; `--preset wood\|iron\|...` for solid materials |
| `smart_material.py` | Wear, rust, grime and dust layers (`--wear 0.4 --grime 0.3`), `--remove` restores the original exactly |
| `decal.py` | Projects an image decal onto a surface with a z-fight-safe offset |
| `bake_maps.py` | `--low X_low --high X_high --maps normal ao curvature id --pack-orm`, or a self-bake of procedural materials without `--high`; picks the GPU and names outputs `T_<name>_<map>.png` |

## References

- [references/uv-layout.md](references/uv-layout.md): seams by asset type, unwrap methods, texel density targets, packing math, lightmap UVs, trim-sheet layout.
- [references/baking.md](references/baking.md): bake setup, extrusion vs cage, map types and settings, artifact diagnosis table.
- [references/materials.md](references/materials.md): PBR rules, measured values, channel packing per engine, alpha, trim sheets, wear layering.
- [references/pbr-values.md](references/pbr-values.md): measured albedo and F0 tables.
- [references/texturing.md](references/texturing.md): how `smart_material.py` layers wear, rust, grime and dust, and how to bake the result for an engine.
- [references/trims-tiling-painting.md](references/trims-tiling-painting.md): trim sheets, tiling materials with vertex-color blends, texture painting.
