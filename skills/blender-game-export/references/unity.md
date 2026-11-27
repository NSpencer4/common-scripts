# Unity (Unity 6, 2022 LTS)

FBX is Unity's built-in path. GLB needs the glTFast package (`com.unity.cloud.gltfast` in `Packages/manifest.json`).

## Choose the format

| Asset | Format |
|---|---|
| PBR textures, metallic/roughness, emission, alpha, or vertex colors, and glTFast is installed | GLB |
| Humanoid character that needs Unity's avatar pipeline, or no glTFast | FBX |
| Plain static geometry | Either; follow what the project already uses |

Tested by CoplayDev on Unity 6000.4 with URP: FBX dropped emission, reset metallic to 0, left alpha materials opaque, and did not assign embedded textures; GLB through glTFast carried all of them. Details: [unity-bridge-fidelity.md](unity-bridge-fidelity.md).

## Export presets

`scripts/export_asset.py -- --preset unity` (static FBX, Apply Transform on), `--preset unity_skeletal` (FBX, Apply Transform off, deform bones only, no leaf bones), or `--preset gltf` (GLB with modifiers applied). The `unity` preset follows el4cteo in using Apply Transform; see the disagreement below and check the root rotation on import.

## FBX export settings

| Setting | Static mesh | Character |
|---|---|---|
| `apply_scale_options` | `FBX_SCALE_ALL` | `FBX_SCALE_ALL` |
| `axis_forward` / `axis_up` | `-Z` / `Y` | `-Z` / `Y` |
| `use_triangles` | True | True |
| `mesh_smooth_type` | `FACE` | `FACE` |
| `add_leaf_bones` | n/a | False |
| `use_armature_deform_only` | n/a | True |
| `bake_anim_use_all_actions` | n/a | True (one clip per action) |
| `path_mode` / `embed_textures` | `COPY` / True | `COPY` / True |

`FBX_SCALE_ALL` was measured importing at file scale 1 in Unity 6000.3 by Scenario Labs. The sources disagree on `bake_space_transform` (Apply Transform) for static meshes: el4cteo recommends it to remove the -90 degree X rotation on root objects; Scenario Labs warns against it and against Bake Axis Conversion for characters. Never use it with armatures. If a static mesh imports with a -90 degree X rotation, try it on that export and confirm in the engine.

## Import settings to check

Model tab: Scale Factor 1, Convert Units on. Normals: Import. Tangents: Import or Calculate Mikktspace. Embedded textures stay inside the FBX until Materials > Extract Textures assigns them.

## Materials

Unity does not build useful PBR materials from FBX; recreate them or extract and remap. Measured by Scenario Labs: Unity's FBX import assigned only the base color even when the file carried metallic and roughness maps.

- URP Lit: BaseMap (sRGB), NormalMap (OpenGL), Metallic map with R = metallic and A = smoothness (1 - roughness), sRGB unchecked.
- HDRP Lit: MaskMap with R = metallic, G = AO, B = detail mask, A = smoothness.

## Characters

- Humanoid (Mecanim) needs at least Hips, Spine, Head, upper and lower legs, feet, upper and lower arms, hands. Bind pose in T-pose. An extra `root` bone above Hips is fine for root motion.
- Unity names clips `Armature|Action`; name actions as the clips should read. `Hero@Run.fbx` per-clip files can share one avatar.
- Blend shapes: enable Import BlendShapes.

## LODs and lightmaps

Name meshes `X_LOD0`, `X_LOD1`, ...; Unity builds a LOD Group from the suffixes. Unity colliders are set in the editor, not from FBX names. Lightmap UVs: ship UV1 or tick Generate Lightmap UVs.

## Verify in Unity

Report numbers: bounds against Unity's default 2 m capsule or a 1 m cube, root rotation 0 and scale 1 on the prefab, material count with textures assigned, the LOD Group levels, colliders, and for characters a valid Avatar, the clip names, and one clip playing in Play mode. When both a Blender MCP and a Unity MCP server are connected, [unity-mcp-handoff.md](unity-mcp-handoff.md) covers the export, import, size normalization and emission restore; the `unity-cli` skill can do the Unity side with `script eval`.
