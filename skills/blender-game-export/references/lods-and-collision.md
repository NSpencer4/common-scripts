# LODs and collision

## LODs

- Halve the triangles per level (LOD1 50%, LOD2 25%, LOD3 12.5%). Switch at roughly 0.5, 0.25, 0.125 screen size.
- Make LODs from a copy with modifiers applied. Decimate modes:

  | Mode | Use |
  |---|---|
  | `COLLAPSE` (ratio) | Organic shapes, scans, general LODs. `use_symmetry`, and a vertex group to protect faces and hands. |
  | `UNSUBDIV` | Meshes built by subdividing quads |
  | `DISSOLVE` (planar, angle) | Hard surface. Delimit seams, sharp edges, materials, and UVs to keep borders. |

- Weld vertices split at UV seams (common after a glTF import) before decimating, or the LODs crack open along the seams.
- LODs keep the same pivot, bounds, and materials (or fewer materials at LOD2 and beyond).
- Render every LOD's silhouette from the distance it will be seen. Decimation collapses thin parts first.
- Skeletal LODs keep the same skeleton; drop finger and face bones at LOD2+ through the engine's bone reduction tools.
- Engines that generate LODs (Godot on import, Unreal Nanite, Unreal auto LOD) usually make a hand-made chain unnecessary.

Naming: `X_LOD0`, `X_LOD1`, ... for Unity and Unreal.

## Collision

Keep collision separate from the render mesh and simple: boxes or convex hulls, a few dozen vertices each (Unreal's hard limit is 255 per hull). Never use the render mesh as physics for anything that moves.

| Engine | How collision travels |
|---|---|
| Unreal | `UCX_<Mesh>_00` convex, `UBX_` box, `USP_` sphere, `UCP_` capsule in the same FBX |
| Godot | Name suffixes: `-convcolonly` (convex), `-colonly` (trimesh, static only), `-col` (mesh plus collision) |
| Unity | Set colliders in the editor; ship a simplified mesh for a MeshCollider if needed |

Build a convex hull in Blender with bmesh: `bmesh.ops.convex_hull(bm, input=bm.verts)` on a copy, then decimate it to the vertex budget. Multiple non-overlapping hulls follow a concave shape better than one.
