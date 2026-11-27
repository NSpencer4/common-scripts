---
name: blender-game-modeling
description: Build or fix the shape of a game asset in Blender, from a brief, sketch, or reference images through blockout, real-world scale, silhouette, mesh construction, and topology. Covers hard-surface props, weapons, vehicles, and architecture, sculpt-to-low-poly retopology, cleaning up AI-generated or scanned meshes, matching orthographic or photo references, terrain and modular environment kits, scene setup and naming, batch jobs, and the mesh QA gate. Holds the shared scripts and rules for driving Blender live or headless. Use whenever someone asks to model, block out, sculpt, retopologize, or reshape a 3D asset for a game in Blender, or drives Blender through bpy, an MCP bridge, or headless scripts for modeling work, even if they do not say "game". For UVs, textures, materials, and baking use blender-game-surfacing; for budgets, LODs, collision, and export use blender-game-export.
---

# Blender game modeling

A game model is judged at gameplay distance first: silhouette, proportions, and scale against a player. Settle those with a blockout before spending time on bevels, topology, or detail, because a proportion problem found after texturing costs the whole asset.

How to drive Blender (live session or headless), the bpy rules that prevent most script failures, and how to render review images are in [references/operating-blender.md](references/operating-blender.md). Read it before the first Blender call in a session.

## Establish the brief in numbers

Write these down before building. When the brief is silent, pick the default and state it as an assumption in the report.

| Input | Why it changes the plan | Default when silent |
|---|---|---|
| Real size | Bevel widths, texel density, and engine placement are absolute | Ask; unattended, pick a plausible size and say so |
| Gameplay camera | Detail and density follow the closest view the player gets | Third person, 3 to 5 m away |
| Triangle budget | Decides mid-poly vs high-to-low, cylinder segments, how much is geometry vs normal map | Report triangles; see budgets in blender-game-export |
| Deforms? | Deforming meshes need edge loops at joints and all-quad flow; static props can use n-gons on flat faces | Static |
| Style | Low-poly, stylized, or realistic changes how much detail is geometry | Match the references |
| References | Silhouette and proportions are checked against them | None: block out from the brief and confirm |

## Workflow

1. **Inspect what exists.** For an existing file, list objects, scale, modifiers, and triangle counts before changing anything. Never delete data you did not create in someone's open scene.
2. **Block out at real size.** Primitives only, 1 unit = 1 m, the asset's front facing -Y, base on z = 0. Put a 1.8 m human-scale box beside it. Render the gameplay view and a silhouette view (see operating-blender.md). Gate: proportions read correctly from the gameplay camera, and against references if supplied.
3. **Choose the construction method per part.**

   | Method | Use when | Output |
   |---|---|---|
   | Mid-poly: booleans, bevels, weighted normals, no bake | Props seen up close, tiling or trim materials, fast iteration | The game mesh directly |
   | High-to-low: detailed high poly, clean low poly, bake | Hero assets, unique textures, tight budgets | `X_high` and `X_low` for blender-game-surfacing |
   | Sculpt, then retopology | Organic shapes, creatures, rocks, AI or scan cleanup | Sculpt plus a low poly at budget |
   | Subdivision with support loops | Smooth product-like shells feeding a bake | High poly only; never ship creases to an engine |

4. **Apply scale** on every object before bevels, booleans, solidify, arrays, or measurements. Modifier distances are in object space, so unapplied scale makes uneven bevels.
5. **Build primary, then secondary, then tertiary forms.** Primary forms carry the silhouette. Tertiary detail (bolts, seams, small panel lines) usually belongs in the normal map or as floaters on the high poly.
6. **Topology pass.** Follow the method's reference below. Gate: the shading check is clean in a matcap view, and the triangle count is within budget.
7. **Keep it editable.** Keep the modifier stack and cutters on the source. Apply modifiers only on an export copy.
8. **Deliver with evidence**: review renders (gameplay view, silhouette, wireframe), triangles per object, dimensions, and anything not verified. Do not call a model done without looking at a render of it.

## Topology rules that apply everywhere

- Spend density where the silhouette or deformation needs it, never on flat faces.
- Cylinder segments by on-screen size: bolts 6 to 8, handles 12 to 16, barrels 24 to 32, hero close-ups 48+. Use multiples of 4 or 8 so mirrors and booleans line up with loops.
- N-gons are fine on flat faces that never deform or subdivide. Triangulate them on export.
- Poles (3 or 5+ edges) go on flat, still areas, never on a bend, a bevel, or a curvature peak.
- No long thin triangles across visible curved areas: they shade badly and collapse first in LODs.
- Hidden faces (back-to-back boxes, faces buried inside other parts) waste triangles and break bakes. Delete them.

## Common failures

| Symptom | Usual cause | Fix |
|---|---|---|
| Uneven or blobby bevels | Unapplied or non-uniform scale | Apply scale, then re-check the stack |
| Gradient smears on flat faces | Missing Weighted Normal, or the face is not planar | Add Weighted Normal at the bottom of the stack; flatten the face |
| Boolean removes everything or leaves holes | Cutter not closed, inverted normals, coplanar faces | Repair the cutter, extend it past the surface, use the EXACT solver |
| Model looks right in Blender, wrong in game | Judged from the wrong distance or without scale reference | Re-render from the gameplay camera next to the human-scale box |

## Scripts

Each takes its flags after `--`, returns one JSON result, and exposes `run(**kw)` for live sessions. Run headless through the runner, which finds Blender and prints only the JSON:

```bash
python3 <skills>/blender-game-modeling/scripts/run_in_blender.py --blend in.blend <script.py> -- <flags>
```

| Script | Does |
|---|---|
| `env_report.py` | Blender version, engines, GPU, add-ons, units, color management. Run first in a session. |
| `scene_audit.py` | Units, unapplied or negative scale, default names, root-level objects, missing images, orphans. `--fix purge scale paths` only on files you own. |
| `apply_stack.py` | Builds the hard-surface stack (`--preset midpoly --cutters ...`); `--apply` on an export copy only. |
| `auto_retopo.py` | `--tris N --method quadriflow\|decimate\|planar`, writes `<name>_low` and keeps the source. |
| `qa_check.py` | The QA gate: z-fighting, floating parts, non-manifold, flipped normals, n-gons, scale, UVs. `--profile game`; fix until `"pass": true`. |
| `review_shots.py` | Contact sheets; `--mode random` colors each object so detached parts show. |
| `review_renders.py` | Solid, wire and silhouette views plus the gameplay view with a 1.8 m box (see operating-blender.md). |
| `terrain.py`, `scatter.py`, `kit_check.py` | Terrain with Unity-friendly 2^n+1 heightmaps, slope-aware scatter, modular kit grid and pivot checks. |
| `batch_process.py` | Convert, inventory, or run any script over a folder of files, one JSON line per file, `--shard i/N`. |

## References

- [references/operating-blender.md](references/operating-blender.md): live vs headless execution, bpy rules, Blender 5.x API traps, review render snippet. Load before scripting.
- [references/api-changes-5x.md](references/api-changes-5x.md) and [references/bpy-patterns.md](references/bpy-patterns.md): the full 4.x to 5.3 migration table and verified bmesh, numpy, depsgraph, driver and handler snippets.
- [references/blender-mcp.md](references/blender-mcp.md) and [references/blender-mcp-errors.md](references/blender-mcp-errors.md): Blender MCP tool choice, health check, export timeouts and known errors.
- [references/scene-setup.md](references/scene-setup.md): units, collection layout, `SM_`/`SK_`/`M_`/`T_` naming, real-world sizes, linking, asset libraries.
- [references/pipeline-automation.md](references/pipeline-automation.md): headless CLI flags, batch jobs, the `bpy` pip module, CI.
- [references/asset-qa.md](references/asset-qa.md): what each `qa_check.py` finding means and how to fix it.
- [references/environment-kits.md](references/environment-kits.md): terrain, scatter densities, modular kit metrics.
- [references/lowpoly-style.md](references/lowpoly-style.md) and [references/ps1-aesthetic.md](references/ps1-aesthetic.md): low-poly and retro looks.
- [references/hard-surface.md](references/hard-surface.md): modifier stack order, bevel and boolean settings, shading checks for mechanical props.
- [references/organic-and-retopology.md](references/organic-and-retopology.md): sculpt workflow, automatic vs manual retopology, edge flow for deforming meshes, cleaning AI-generated and scanned meshes.
- [references/reference-matching.md](references/reference-matching.md): matching orthographic or photo references, separating visible from inferred geometry.
