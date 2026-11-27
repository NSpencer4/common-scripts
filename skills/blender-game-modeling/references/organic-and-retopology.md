# Organic shapes and retopology

Creatures, characters, rocks, trees, food, cloth-like props, and cleanup of AI-generated or scanned meshes.

## Sculpt workflow

1. Block out with primitives or a low-resolution base at real size. Check the silhouette before sculpting.
2. Voxel remesh to an even density while shapes are still changing (`ob.data.remesh_voxel_size`, then `bpy.ops.object.voxel_remesh()`). Voxel remesh output is flat shaded until `shade_smooth()`.
3. Primary forms at low resolution, secondary forms after a finer remesh or Multires, surface detail last. Most surface detail ends up in the normal map, so stop sculpting at what the gameplay camera can see.
4. Brush strokes (`sculpt.brush_stroke`) need a window: they work in a live session, not headless. Headless sculpting means editing mesh data directly.

## Choosing a retopology method

| Asset | Method | Notes |
|---|---|---|
| Static prop, rock, scan, background asset, bake-only | Automatic: QuadriFlow (`bpy.ops.object.quadriflow_remesh`) or Decimate | QuadriFlow needs a manifold input (voxel remesh first) and loses UVs. Set `use_mesh_symmetry=False` on posed or asymmetric meshes. Decimate keeps UVs but produces triangles. |
| Hard-surface boolean result, CAD | Planar decimate (`decimate_type="DISSOLVE"`, delimit seams, sharp, material, UV) | Keeps the silhouette, makes n-gons to triangulate on export |
| Anything that deforms (characters, creatures, faces) | Manual or hybrid: a new mesh with a Shrinkwrap modifier onto the sculpt | Automatic retopology does not place loops around eyes, mouth, or joints. Plan the loops first, then build. |

## Edge flow for deforming meshes

- Concentric loops around eyes and mouth, at least three rings each. Upper and lower lid or lip loop counts match.
- Three loops over each bending joint (elbow, knee, knuckles), plus one on each side to hold volume. Shoulders need extra loops for raising the arm.
- Poles (3 or 5 edges) go where nothing bends: chest, back of the skull. Never on a crease loop or the center line of a mirrored face.
- All quads where the mesh bends; triangles only in hidden, rigid spots.
- A snapped cage shrinks inside the sculpt when subdivided. Judge the subdivided surface, not the cage.

## Game low poly from a sculpt

- Silhouette first: the low poly must match the high's outline from the gameplay camera, slightly proud of the high so the bake projects outward.
- Face density about three times the body's on characters; hands and face get loops for animation, everything rigid gets triangles freely.
- Hard edges on the low poly must also be UV seams (see blender-game-surfacing).
- Rough game character budgets: head 2,000 to 3,000 triangles, both hands about 1,000, body 5,000 to 6,000 for a mid-range third-person character. Platform budgets are in blender-game-export.

## Cleaning AI-generated or scanned meshes

These arrive with arbitrary scale, the origin at the center, triangle soup, holes, internal faces, and often one object per part.

1. Measure: dimensions, triangle count, non-manifold edges, loose parts, holes (boundary edges).
2. Set real size and put the base on z = 0 before anything else.
3. Delete fragments and internal geometry; merge by distance (0.1 mm).
4. Static and seen from afar: decimate to budget and keep the generated texture.
5. Needs clean topology or a better texture: retopologize (table above), unwrap, and bake the generated mesh's color and normals onto the new low poly (blender-game-surfacing).
6. Holes and edges shared by three or more faces have no automatic fix that holds up. Rebuild the surface or report the asset as not ready for targets that need closed meshes.
