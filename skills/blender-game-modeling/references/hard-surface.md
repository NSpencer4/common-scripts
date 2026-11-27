# Hard-surface props

Weapons, vehicles, crates, machinery, architecture. Good hard surface is controlled light on edges: every visible edge catches a highlight from a bevel, flat faces read perfectly flat, and cuts stay editable until the design is settled.

## Modifier stack order

Mirror, then Booleans, then the angle-limited micro Bevel, then Weighted Normal, then Triangulate (export copy only).

- Booleans sit above the micro bevel so cut edges get beveled too. A boolean below the bevel leaves razor-sharp cut edges while everything else is soft.
- Weighted Normal sits at the very bottom (above Triangulate). Anything below it can destroy the custom normals.
- Pinned modifiers (5.x) keep their relative order and new modifiers land above them. `ob.modifiers.move()` silently refuses moves involving pinned modifiers: unpin, move, re-pin bottom-up.

## Settings

| Item | Setting |
|---|---|
| Boolean solver | `EXACT` by default. `MANIFOLD` is much faster but needs closed manifold operands and can silently skip a cut on an open cutter. Use `FLOAT` only to diagnose. Many cutters: `operand_type="COLLECTION"`. |
| Cutters | In a `Cutters` collection, display `WIRE`, `hide_render=True`, scale applied, smooth shaded, parented to the target. Extend past every surface they enter. Keep cutter edges clearly away from target edges or exactly on them. |
| Round cutters | Offset by half a segment against a target with the same segment count; in-phase facets create slivers and non-manifold edges. |
| Design bevel | `limit_method="WEIGHT"` on chosen silhouette edges (`bevel_weight_edge` attribute), 8 to 12 segments, applied before cuts. |
| Micro bevel | `limit_method="ANGLE"` (30 degrees), `harden_normals=True`, `miter_outer="MITER_ARC"`, `use_clamp_overlap=True`. Game mid-poly: 1 to 2 segments. Width about 0.5 to 2% of the part, consistent across the asset. |
| Weighted Normal | `mode="FACE_AREA"`, `keep_sharp=True`, weight 50. Faces must be smooth shaded. |
| Mirror | `use_clip=True`, `use_mirror_merge=True`, model the half at x >= 0. |
| Triangulate | Export copy only: `quad_method="BEAUTY"`, `keep_custom_normals=True`. The bake mesh and the export mesh must triangulate identically or the normal map shows seams. |

## Minimum feature size

Every wall, step, groove, and rounding facet must be wider than twice the micro bevel width. A thinner feature makes Clamp Overlap shrink the bevel across the whole object, not just locally. If bevels everywhere look narrower after adding one cut, that cut is the cause: move it, widen it, or thin the bevel.

## Edge attributes from Python (4.0+ names)

```python
me = ob.data
bevel = me.attributes.get("bevel_weight_edge") or me.attributes.new("bevel_weight_edge", "FLOAT", "EDGE")
sharp = me.attributes.get("sharp_edge") or me.attributes.new("sharp_edge", "BOOLEAN", "EDGE")
bevel.data[edge_index].value = 1.0
sharp.data[edge_index].value = True
me.edges[edge_index].use_seam = True  # seams are still an edge property
```

Select sharp edges by angle in bmesh: `edge.calc_face_angle(0) > math.radians(30)`.

## Shading check

Render `solid` (matcap) views and close-ups of each cut (see operating-blender.md). Look for:

| Symptom | Cause | Fix |
|---|---|---|
| Gradient smear across a flat face | Weighted Normal missing or above another modifier; or the face is not planar | Fix stack order; flatten the face. If Harden Normals or Weighted Normal changes nothing, the face is not flat. |
| Bevel narrower everywhere after a cut | Clamp Overlap triggered by a thin feature near the cut | Move the cutter clearly away or snap it exactly; widen the feature |
| Stretching at a cut on a curved surface | Cut on curvature | More segments on the target, or transfer normals from an uncut copy (Data Transfer after Weighted Normal) |
| Butterfly shading on a mirror seam | Normals disagree across the seam | Bevel face strength plus Weighted Normal face influence |
| Facets on cut walls | Flat-shaded cutter | Smooth-shade the cutter |

## Mid-poly vs high-to-low

Mid-poly (bevels plus weighted normals, tiling or trim materials) ships the beveled mesh directly and needs no bake. It costs more triangles and fewer texture pixels. High-to-low keeps a cheap low poly and moves edge detail into a baked normal map; it costs a unique texture set and a bake pass. For a 15k-triangle budget with one 2K map, high-to-low is typical; for modular props sharing a trim sheet, mid-poly is typical.
