---
name: blender-core
description: >-
  Foundation for any Blender 5.2+ task an agent drives: running bpy live through a Blender MCP
  server or headless from the CLI, context overrides, locale-safe node lookup, enum discovery,
  5.x API changes, scene setup and naming, batch pipelines, and verification. Use first for any
  Blender, bpy, .blend or 3D-asset request, then route to blender-game-assets,
  blender-rigging-animation or blender-to-unity.
license: MIT
compatibility: Blender 5.2 LTS or newer, verified upstream on 5.3. Optional Blender MCP server for live sessions.
---

# Blender Core (5.2 LTS+, 5.3)

## Route to the specialized skill

| Task | Skill |
|---|---|
| Units, collections, naming (`SM_`/`SK_`/`T_`/`M_`), origins, linking, asset libraries | this skill, [references/scene-setup.md](references/scene-setup.md) |
| Batch and headless jobs, format conversion, CI | this skill, [references/pipeline-automation.md](references/pipeline-automation.md) |
| Hard-surface modeling, retopology, UVs, PBR materials, texturing, baking, LODs, collision, poly budgets, asset QA, environment kits | `blender-game-assets` |
| Rigging, weight painting, shape keys, keyframes, actions, NLA, retargeting, root motion | `blender-rigging-animation` |
| Exporting to Unity (FBX, glTF), import settings, Blender MCP to Unity MCP handoff | `blender-to-unity` |

Sculpting, Geometry Nodes, simulation, hair, rendering and add-on development are not covered by
these skills.

## Execute

**Live (Blender MCP `execute_blender_code`)**: work in small steps and print only what you need.
To call a skill script, import it:

```python
import sys, importlib; sys.path.insert(0, r"<skills_dir>/blender-game-assets/scripts")
import qa_check; importlib.reload(qa_check); print(qa_check.run(objects=["Chair"]))
```

Each MCP call runs in a fresh namespace: re-`import` in every call. Modules stay cached in
`sys.modules`, so that is cheap. `reload` only after editing a script. Tool selection, health
checks and known MCP failure modes: [references/blender-mcp.md](references/blender-mcp.md),
[references/blender-mcp-errors.md](references/blender-mcp-errors.md).

**Headless (any agent with a shell)**: this prints only the script's JSON (`@@JSON@@` lines):

```bash
python3 <skills_dir>/blender-core/scripts/run_in_blender.py --blend in.blend <script.py> -- --objects Chair --save out.blend
python3 <skills_dir>/blender-core/scripts/run_in_blender.py --expr "import bpy; print(len(bpy.data.objects))"
```

Raw form: `blender -b in.blend --factory-startup --python-exit-code 1 -P x.py -- args`. Every
script in these skills exposes `run(**kw) -> dict` and the same flags after `--`.

**First call in a session**: `scripts/env_report.py`, which returns the version, engines, GPU,
add-ons, units, color management and scene counts.

## Rules

- **Data API over operators**: use `bpy.data`, `bmesh`, `mesh.attributes`, and
  `foreach_get/set` with numpy. Operators depend on context and selection, and many need a 3D
  View, which background mode does not have.
- If an operator is unavoidable: `with bpy.context.temp_override(object=ob, active_object=ob,
  selected_objects=[ob], selected_editable_objects=[ob]): bpy.ops...`. Check that the result is
  `{'FINISHED'}`.
- **Edit mode isolation**: `ob.data` is not updated while in Edit Mode. Use
  `bmesh.from_edit_mesh` + `bmesh.update_edit_mesh`, or switch to Object mode before reading.
- **Nodes**: find them by `type` (`n.type == "BSDF_PRINCIPLED"`), never by `name`, because names
  are localized. Sockets by English name or `identifier` are fine.
- **Enums**: read valid values with `[i.identifier for i in T.bl_rna.properties[p].enum_items]`.
  Dynamic enums (`render.engine`, `view_transform`, `look`) under-report, so assign them inside
  `try/except TypeError` and report the failure.
- **Evaluated data**: `ob.evaluated_get(depsgraph)`, then `.to_mesh()`, then always
  `.to_mesh_clear()`. Call `view_layer.update()` before reading `matrix_world` after a change.
- **Freed data**: applying or removing a modifier, or removing an object or ID, frees it. Collect
  names first and never touch the old Python reference afterward.
- **Never trust default names** ("Cube.001"). Keep object references, rename explicitly, and look
  objects up via `bpy.data.objects[name]`.
- **Scale**: 1 unit = 1 m. Apply rotation and scale before bevels, distance-based modifiers,
  rigging, physics, baking and export.
- **Paths**: `bpy.path.abspath("//textures/x.png")` resolves relative to the .blend. Save
  explicitly; use `save_as_mainfile(filepath=..., copy=True)` for backups.
- **Live sessions are the user's work**: never `read_factory_settings`, never delete data you did
  not create, and save a backup copy before destructive batch edits.
- **GPU module in background**: call `gpu.init()` first (5.2+). `bgl` no longer exists.
- **Big meshes**: no per-vertex `bpy.ops`. Use numpy `foreach_get`
  ([references/bpy-patterns.md](references/bpy-patterns.md)).

## 5.x API changes that break old tutorials and model memory

`action.fcurves` → channelbags · `scene.node_tree` → `scene.compositing_node_group` ·
`material.use_nodes` is deprecated (new materials already have nodes) · `mod["Socket_2"]` →
`mod.properties.inputs.Socket_2.value` (5.2) · `BLENDER_EEVEE_NEXT` → `BLENDER_EEVEE` · Boolean
`FAST` → `FLOAT` · bone layers → bone collections · `bl_info` add-ons → extensions
(`blender_manifest.toml`) · `bpy.props` values are no longer dict-accessible · 5.3: glTF WebP
options → compressed-image options. Full table:
[references/api-changes-5x.md](references/api-changes-5x.md).

## Scene setup in one pass

Run `scripts/scene_audit.py` (add `--fix purge scale paths` only on files you own). Metric, Unit
Scale 1.0, every object in a named collection, `SM_`/`SK_`/`M_`/`T_` names with no `.001`
suffixes, props with the origin at bottom-center, characters at the world origin between the
feet. Details and the collection layout: [references/scene-setup.md](references/scene-setup.md).

## Batch jobs

`blender -b -P scripts/batch_process.py -- --in "assets/**/*.fbx" --op convert --to glb --out export/`
converts, inventories or runs any skill script over a folder, one JSON line per file, with
`--shard i/N` for parallel processes. Never write into the source folder.
[references/pipeline-automation.md](references/pipeline-automation.md).

## Verify (required before saying "done")

1. Numbers, not adjectives: report tris, objects, materials, dimensions (`ob.dimensions`) and the
   output files written.
2. Geometry changed: run `blender-game-assets/scripts/qa_check.py` (z-fighting, detached parts,
   non-manifold, flipped normals, scale).
3. Look at it: the MCP viewport screenshot, or headless
   `blender-game-assets/scripts/review_shots.py` for contact sheets.
4. Re-read your own output: confirm exported files exist and are non-zero in size.
