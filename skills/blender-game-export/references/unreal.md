# Unreal Engine 5

FBX is the most tested path for skeletal meshes. UE 5.4+ also imports glTF and USD through Interchange.

Neither source measured these settings inside Unreal; Scenario Labs reports its Unreal presets pass the Blender round trip only. Treat the scale setting as something to confirm on first import.

## FBX export settings

| Setting | Value |
|---|---|
| Scene unit scale | 1.0 (meters) |
| `apply_scale_options` | Sources disagree: el4cteo uses `FBX_SCALE_UNITS` (unit in the FBX header, UE converts to cm), Scenario Labs uses `FBX_SCALE_NONE`. Either way the check is the same: a root bone or armature that imports at scale 100 means the wrong mode. |
| `axis_forward` / `axis_up` | `-Z` / `Y` |
| `mesh_smooth_type` | `FACE` (avoids the "no smoothing groups" warning) |
| `use_triangles`, `use_tspace` | True |
| `add_leaf_bones` | False |
| `use_armature_deform_only` | True |
| `armature_nodetype` | `NULL` |

If the armature object is named `Armature`, Unreal drops it and the first bone becomes the root. Any other name becomes an extra root bone. Keep exactly one root bone: Unreal reports "Found multiple roots" otherwise.

## Skeleton

To retarget onto the UE5 mannequin, match its hierarchy names (`root > pelvis > spine_01 ...`, `thigh_l > calf_l > foot_l > ball_l`) and compare orientation with the mannequin in the Skeletal Mesh editor after the first import.

## Static meshes

- Collision in the same FBX: `UCX_<Mesh>_00` convex hulls (non-overlapping, under 255 vertices each), `UBX_` boxes, `USP_` spheres, `UCP_` capsules. Unreal skips auto-generated collision when the file carries one.
- LODs: `<Mesh>_LOD0..N` in one FBX with Import Mesh LODs, all sharing one pivot. Or let Unreal generate them.
- Sockets: empties named `SOCKET_<Name>` parented to the mesh.
- Nanite (static, opaque or masked): ship dense geometry directly; no LODs or normal bake needed for geometric detail.

## Materials

BaseColor (sRGB), Normal (DirectX: flip green when baking or tick Flip Green Channel on the texture), ORM with R = AO, G = roughness, B = metallic, sRGB unchecked, Masks compression. Name textures `T_<Asset>_BC/_N/_ORM`.

## Animation

One action per clip, imported against the existing Skeleton asset. Root motion: animate the `root` bone, not the armature object, and enable Root Motion on the sequence. Shape keys become morph targets with Import Morph Targets.

## Scale reference

The UE5 mannequin is about 180 cm tall.
