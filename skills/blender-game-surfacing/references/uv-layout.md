# UV layout

## Seams by asset type

| Asset | Where seams go |
|---|---|
| Hard-surface prop | Every hard edge; then panel borders and the back or underside of each part |
| Cylinder or tube | One straight cut along the least-seen side; caps as separate islands |
| Character body | Inner arms and legs, under the arms, back of the head behind hair, around hands and feet at cuffs, inner mouth and eyelids |
| Rock or organic prop | Along natural creases and the underside; more seams rather than visible stretch when baking or painting in 3D |
| Modular wall or trim piece | Along the trim strip boundaries so islands land on trim rows |

An island with holes (a face with eye holes, a washer) flattens without extra cuts. Only closed shells and long tubes need them.

Seams in Python: `me.edges[i].use_seam = True`. Seams from sharp edges in bmesh: mark every edge whose `calc_face_angle()` exceeds the threshold, and set `sharp_edge` on the same edges so shading and seams agree.

## Unwrap methods (Blender 5.3)

| Method | Best for |
|---|---|
| `ANGLE_BASED` | Hard surface and most props; preserves angles |
| `MINIMUM_STRETCH` | Organic islands; most even area distribution |
| `CONFORMAL` | The operator default in 5.3; distorts area on organic islands, so do not rely on it implicitly |
| Smart UV Project (`uv.smart_project`, angle about 66 degrees) | Quick automatic seams on hard-surface or AI meshes where seam placement matters less |

UV operators run in Edit Mode on selected faces. Select everything first, and check afterward for zero-area UV faces, which mark islands that failed to unwrap.

## Texel density

Pixels per meter of surface. Set it before picking texture resolution. Everything in one scene should share a density; hero assets may go up to 2x.

| Context | px/m |
|---|---|
| First-person weapon or hero prop | 1024 to 2048 |
| First-person environment | 512 to 1024 |
| Third person (console or PC) | 512 |
| Third person (mobile) | 256 |
| Top-down or strategy | 128 to 256 |

These are common studio baselines, not engine requirements. Density mismatches of 10 to 20% between islands are not visible; larger ones are. When matching two texture sets, scale the denser one down rather than the other up.

Measure: for each face, compare its 3D area (world space, scale applied) with its UV area times the texture resolution squared. Density = sqrt(uv_area * res^2 / world_area).

## Packing

- Padding between islands: about res / 128 pixels. Blender's `uv.pack_islands` takes `margin_method="FRACTION"`; a margin m gives a gap of about 2m, so m = gap_px / (2 * res).
- Pack rotation: off (or cardinal only) after straightening, or the straightened grids tilt.
- `shape_method="CONCAVE"` packs tightest but can take seconds even on small meshes headless; use `"AABB"` while iterating.
- Coverage around 70% of the 0 to 1 tile is a reasonable target for props; organic characters often land at 55 to 65% with Blender's packer.

## Mirrored and stacked UVs

Stacking identical parts or mirrored halves on one island saves texture space but means they share baked lighting. Fine for tiling or hand-painted textures with no baked AO. For bakes, move the duplicate islands exactly +1 in U (outside 0 to 1) before baking so only one copy receives the bake, then move them back. Inside 0 to 1, the last island baked wins.

## Lightmap UVs

A second UV map (UV1) with no overlaps, every island inside 0 to 1, and generous padding. Unreal, Unity, and Godot can generate one on import; ship a hand-made one only when the target pipeline asks for it. Keep UV0 active for texturing.

## Trim sheets

A trim sheet is one texture with horizontal strips (bolts, panels, edges, grates) shared by many assets. Unwrap the mesh strips, straighten them, then scale and move each island onto the V range of the matching trim row. Islands may run past 0 to 1 in U because trims tile horizontally. Keep texel density consistent with the rest of the scene.

## UDIMs

Film and hero pipelines use UDIM tiles (1001, 1002, ...). Most game engines do not support them; use separate texture sets per material instead.
