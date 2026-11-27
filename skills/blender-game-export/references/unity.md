# Unity (Unity 6, 2022 LTS)

FBX is the default path. glTF needs a package (glTFast).

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

## Scale reference

Unity's default capsule is 2 m tall.
