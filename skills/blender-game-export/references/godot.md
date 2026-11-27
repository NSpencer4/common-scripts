# Godot 4

GLB is the native path and keeps every PBR map. Godot can also import `.blend` files directly when Blender's path is set in its settings; it converts through glTF.

## glTF export settings

| Setting | Value |
|---|---|
| `export_format` | `GLB` |
| `export_apply` | True (defaults to False; modifiers are otherwise left out) |
| `export_yup` | True (default) |
| `export_animations` | True for animated assets; each action becomes an AnimationPlayer clip |
| `export_extras` | True to carry custom properties as node metadata |

Do not use a compressed web GLB (meshopt or Draco) for Godot: check that the file's `extensionsRequired` is empty.

## Import hints from object names

| Suffix | Result |
|---|---|
| `-col` | Mesh plus static collision |
| `-colonly` | Collision only (trimesh, static bodies), mesh removed |
| `-convcolonly` | Convex collision only |
| `-rigid` | RigidBody |
| `-navmesh` | Navigation mesh |
| `-noimp` | Skipped |
| `-loop` / `-cycle` on an action name | Looping clip |

Example: `Crate-convcolonly` beside `Crate`.

## LODs and lightmaps

Godot generates mesh LODs on import (`meshes/generate_lods`); hand-made LODs are rarely needed. For static lightmaps, enable Light Baking: Static Lightmaps on import to auto-unwrap UV2, or ship one.

## Characters

Godot retargets humanoids through SkeletonProfileHumanoid (Bone Map in the import dock).

## Headless engine check

Godot runs without a window (`--headless`), so a small project plus a GDScript that loads the imported scene can print node transforms, mesh sizes, and material maps. Scenario Labs documents such a check (scenario-labs/skills, `scenario-blender-export/references/engines.md`). Check the flags against the installed Godot version's `--help`. When Godot is not installed, report that verification stopped at a Blender re-import.
