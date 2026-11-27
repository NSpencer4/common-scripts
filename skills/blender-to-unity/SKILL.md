---
name: blender-to-unity
description: >-
  Moves assets from Blender 5.2+ into a Unity 6 project with the right scale, axes, materials,
  rigs and clips: FBX vs GLB (glTFast) choice, tested export presets for static and skeletal
  meshes, Unity Model importer settings, Humanoid avatars, animation clip naming, URP and HDRP
  texture packing, LOD and collider conventions, and the file handoff between a Blender MCP
  server and a Unity MCP server. Use whenever an asset leaves Blender for Unity, or when an
  imported model is 100 times too big, rotated -90 degrees, grey, missing emission or missing
  clips. Not for modeling (blender-game-assets) or rigging (blender-rigging-animation).
license: MIT
compatibility: Blender 5.2 LTS or newer, Unity 6.0 or newer. GLB import needs com.unity.cloud.gltfast in the Unity project.
---

# Blender to Unity

Run the `blender-game-assets` QA gate first, then export, then check the result in Unity with
numbers. Run scripts the way `blender-core` describes.

## Choose the format

Check the Unity project's `Packages/manifest.json` for `com.unity.cloud.gltfast`.

| Asset | Format |
|---|---|
| PBR textures, metallic/roughness, emission, alpha, vertex colors, and glTFast installed | GLB |
| Humanoid character that needs Unity's avatar pipeline, or no glTFast | FBX |
| Plain static geometry | either; FBX if the project already uses it |

FBX loses emission, resets metallic on URP conversion, leaves alpha materials opaque, and does
not assign embedded textures. GLB through glTFast carries all of those. Tested results:
[references/bridge-fidelity.md](references/bridge-fidelity.md).

## Export

```bash
python3 <skills_dir>/blender-core/scripts/run_in_blender.py --blend asset.blend \
  <skills_dir>/blender-to-unity/scripts/export_asset.py -- --preset unity --objects SM_Crate --out //export/SM_Crate.fbx
```

- `--preset unity`: static FBX with Apply Transform, so no -90 degree X rotation and no 100x
  scale on root objects.
- `--preset unity_skeletal`: FBX without Apply Transform (never use it with armatures), leaf
  bones off, deform bones only.
- `--preset gltf`: GLB for glTFast.
- `--batch` writes one file per top-level object at the origin. `--set key=value` passes any
  exporter option.

Pre-export checklist and format gotchas:
[references/export-pipelines.md](references/export-pipelines.md).

## Unity import settings

- Model tab: Scale Factor 1, Convert Units on. If a skeletal root still shows -90 degrees X,
  turn on Bake Axis Conversion.
- Normals: Import. Tangents: Import or Calculate Mikktspace (match the bake).
- Rig tab: Humanoid for characters (Configure Avatar, T-pose), Generic for everything else that
  animates. FBX animations only import with an animation type set.
- Animation tab: one FBX with all actions (`--set bake_anim_use_all_actions=true`), or one file
  per clip named `Hero@Run.fbx` so clips share the avatar. Loop Time on looping clips; Root
  Transform "Based upon" settings for root motion.
- Blend Shapes: Import BlendShapes on, Blend Shape Normals Calculate.

Full Unity notes: [references/unity-fbx.md](references/unity-fbx.md).

## Materials in Unity

- FBX does not build usable PBR materials. Extract and remap, or create URP Lit materials and
  assign the textures.
- URP Lit: Base Map (sRGB), Normal Map (OpenGL, no green flip), Metallic map with R = metallic
  and A = smoothness. HDRP Lit Mask Map: R metallic, G AO, B detail, A smoothness.
- Data textures (normal, mask, metallic) with sRGB off in the texture importer.
- Bake procedural Blender nodes to textures before export; they arrive grey or white otherwise.

## Conventions Unity reads

- `SM_X_LOD0`, `_LOD1`, `_LOD2` suffixes build a LOD Group.
- Colliders: export simple proxies and replace them with Box, Sphere, Capsule or convex Mesh
  Colliders in the prefab, or add primitive colliders in Unity.
- Lightmap UV2 shipped from Blender (`uv_pack.py --lightmap`) or Generate Lightmap UVs on import.

## Handoff between Blender MCP and Unity MCP

When both servers are connected, the seam is the filesystem: Blender writes a file, Unity
imports it. Export to a temp path, import with the Unity server's model import tool, place it,
normalize its size from renderer bounds, restore emission if FBX dropped it, and screenshot.
Step-by-step with code: [references/mcp-handoff.md](references/mcp-handoff.md). If the official
`unity-cli` skill is available, it can do the Unity side through `script eval` instead.

## Verify in Unity

Report numbers, not impressions:

- Bounds against a reference: a 1 m cube or the 2 m default capsule.
- Root rotation is 0 and scale is 1 on the imported prefab.
- Material count and that each has its textures assigned.
- LOD Group present with the expected levels; colliders present.
- For characters: Avatar valid (all required bones mapped), clip count and names, a clip plays
  in Play mode without the mesh exploding.

## Related skills

- `blender-game-assets`: QA, budgets, baking, ORM packing, LODs, collision proxies.
- `blender-rigging-animation`: game skeleton, baked clips, root motion.
- `unity-gameplay`: Animator setup once clips are in.
- `unity-rendering`: URP material and texture setup.
