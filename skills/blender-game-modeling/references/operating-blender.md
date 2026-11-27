# Operating Blender from an agent

Shared by blender-game-modeling, blender-game-surfacing, and blender-game-export. Checked against Blender 5.3; check `bpy.app.version` first and treat any API noted below as version-specific.

## Pick the channel

| Channel | Use for | Rules |
|---|---|---|
| Live session (an MCP bridge into the user's open Blender) | Editing someone's open scene, interactive brushes, viewport screenshots | One small idempotent change per call, returning a compact result. Never delete data you did not create, never reset to factory settings. Save a backup copy (`bpy.ops.wm.save_as_mainfile(filepath=..., copy=True)`) before destructive edits. A timed-out call has an unknown outcome: read the scene again before retrying. |
| Headless process | Repeatable exports, re-import checks, renders, bakes, batch work | `blender -b in.blend --factory-startup --python-exit-code 1 -P script.py -- args`. `--factory-startup` keeps the user's add-ons and preferences out of the run. Without `--python-exit-code 1` a failing script still exits 0. Print one machine-readable result line. |

Do not open a new GUI Blender window on the user's machine to test something. Live work goes through the session they already have open; everything else runs headless.

MCP bridges differ in tool names (some expose `execute_blender_code`, others `execute_python` with a preloaded `result` dict). Read the server's tool schemas before the first call.

## bpy rules that prevent most failures

- Prefer the data API (`bpy.data`, `bmesh`, `mesh.attributes`, `foreach_get`/`foreach_set`) over operators. Operators depend on context and selection, and many need a 3D View that background mode does not have.
- When an operator is unavoidable, use `with bpy.context.temp_override(object=ob, active_object=ob, selected_objects=[ob], selected_editable_objects=[ob]):` and check the result is `{'FINISHED'}`. Some operators return FINISHED after doing nothing (`uv.unwrap` on a closed island), so measure the result too.
- Find nodes by `type` (`n.type == "BSDF_PRINCIPLED"`), never by `name`: names are localized.
- Read enum values from RNA instead of guessing: `[i.identifier for i in T.bl_rna.properties[p].enum_items]`.
- Read evaluated geometry with `ob.evaluated_get(depsgraph).to_mesh()` and always call `to_mesh_clear()`. Exporters write evaluated geometry, so measure that.
- `ob.data` is stale while in Edit Mode. Use `bmesh.from_edit_mesh` or switch to Object Mode before reading.
- `matrix_world` is stale after changing location or scale until `bpy.context.view_layer.update()`.
- Applying a modifier or removing an object frees it. Collect names first and never touch the old Python reference afterward.
- Never rely on default names like `Cube.001`. Rename explicitly and look objects up by name.
- 1 unit = 1 m. Apply rotation and scale before bevels, distance-based modifiers, rigging, baking, and export.

## Blender 5.x changes that break remembered code

| Old | Now |
|---|---|
| Auto Smooth on the mesh | Removed in 4.1. Use `shade_smooth()` plus sharp edges, or the Smooth by Angle modifier (`bpy.ops.object.shade_auto_smooth`) |
| `BLENDER_EEVEE_NEXT` | `BLENDER_EEVEE` |
| Boolean solver `FAST` | `FLOAT`; `EXACT` is the default and `MANIFOLD` is faster for closed operands |
| `mesh.edges[i].bevel_weight`, `crease` | Attributes `bevel_weight_edge`, `crease_edge` (4.0) |
| `action.fcurves` | Channel bags per action slot (5.0): `bpy_extras.anim_utils.action_get_channelbag_for_slot(action, slot)` |
| `scene.node_tree` for compositing | `scene.compositing_node_group` (5.0) |
| `material.use_nodes = True` | Deprecated; new materials already have nodes |
| Armature layers | Bone collections (4.0) |
| Context dicts passed to operators | `bpy.context.temp_override(...)` |
| Brushes as data blocks | Brush assets (4.3), activated with `bpy.ops.brush.asset_activate(...)` |
| `uv.unwrap()` default method | `CONFORMAL` in 5.3, which distorts area on organic islands. Pass `method="ANGLE_BASED"` or `"MINIMUM_STRETCH"` explicitly |

When code fails with AttributeError or KeyError, suspect an API change before a logic bug, and check the Blender Python API docs for the installed version.

## Look at the result

Numbers do not show a bad silhouette, a smeared bevel, or a part floating 2 cm off the body. Render and look before calling anything done.

```bash
blender -b asset.blend --factory-startup --python-exit-code 1 \
  -P <skills>/blender-game-modeling/scripts/review_renders.py -- \
  --out /abs/review --views front side threequarter --modes solid wire silhouette \
  --gameplay-distance 4
```

- `solid` (matcap): forms and shading problems.
- `wire`: topology density and flow.
- `silhouette`: whether the shape reads with no shading at all.
- `gameplay_solid.png`: perspective from 1.7 m eye height at the given distance with a 1.8 m reference box. This is the view that decides whether proportions and detail level are right.

Open the PNGs with the image reader. In a live session the bridge's viewport screenshot tool serves the same purpose for quick looks; keep images small (about 768 px) because each one stays in context.
