# Baking

## Preparation (most bake bugs come from this list)

1. **Low poly**: unwrapped, no overlaps inside 0 to 1, padding at least res / 128, scale applied, hard edges on UV seams, triangulated the way the engine will triangulate it.
2. **High poly**: covers the low completely and sticks out of it only a little. Floaters (bolts, panel details hovering just above the surface) are fine within the projection distance. Flipped normals and floating fragments on the high cause most black or garbage areas.
3. **Names**: `X_low` / `X_high` pairs.
4. **Separate interpenetrating parts**: move each low and high pair apart along one axis (an exploded bake) or bake one pair at a time, so neighboring parts do not project onto each other. Put them back afterward.
5. **Hide everything else from render** during AO bakes, or other objects darken the AO.

## Blender bake setup

Baking uses Cycles. Selected to active: select the high, make the low active.

```python
scene = bpy.context.scene
scene.render.engine = "CYCLES"
scene.cycles.samples = 16  # normals; AO wants 64 to 256
bake = scene.render.bake
bake.use_selected_to_active = True
bake.cage_extrusion = 0.02  # meters; see below
bake.max_ray_distance = 0.0
bake.margin = 16  # pixels at 2K
bake.normal_space = "TANGENT"
```

- The target Image Texture node must be **selected and active** in **every** material on the low poly. If it is not, the bake returns CANCELED or writes nothing.
- Pass bake options explicitly to the operator (`bpy.ops.object.bake(type="NORMAL", ...)`); operator defaults differ from scene settings in some versions.
- Create bake images as Non-Color for data maps. A float image saved as PNG is 16-bit, which avoids banding on smooth gradients.
- Images are not saved automatically: call `image.save()` (with `filepath_raw` and `file_format` set). Unsaved generated images disappear on reload.
- Multires (no separate high object): `bake.use_multires = True`, then `bpy.ops.object.bake_image()`. The viewport level is the low, the sculpt level is the high. Multires bakes cast no rays, so they avoid projection errors entirely.

## Extrusion vs cage

- `cage_extrusion` pushes the ray start outward from the low. It must exceed the farthest distance the high sticks out of the low. Too small: holes and missing detail. Too large: other parts project in.
- One global value often fixes one area and breaks another (an ear next to a head). Then use a cage: a copy of the low with identical topology, inflated where needed, set with `bake.use_cage = True` and `bake.cage_object`.
- Measure instead of guessing: bake at 512 with two or three extrusion values and compare. Inverted pixels that do not change with extrusion point to a geometry problem (the high does not cover the low there), not a setting.

## Maps

| Map | Color space | Notes |
|---|---|---|
| Normal | Non-Color | Tangent space, OpenGL (Y+) by default. 16 samples is plenty. |
| AO | Non-Color | 64 to 256 samples; AO distance about 0.2 x the asset's diagonal (the default is often far too large or small for the asset size) |
| Curvature | Non-Color | Derived from the normal map or from geometry; 0.5 is flat. Drives edge wear. |
| ID | sRGB | One flat color per high-poly material; used as masks while texturing |
| Base color, roughness, metallic (self-bake) | Base color sRGB, others Non-Color | Bakes procedural materials into textures for export. Use the emission trick (route the socket to Emission, bake EMIT) for sockets Cycles has no pass for. |

## Diagnosing artifacts

| Symptom | Cause | Fix |
|---|---|---|
| Black or garbage patches | Rays miss or hit back faces | Raise extrusion, fix flipped normals on the high, check the high covers the low |
| Map almost entirely flat (128, 128, 255) | `max_ray_distance` shorter than extrusion, or the low carries the high's detail (Multires at render level) | Fix the distances; set Multires render level to 0 for the bake |
| Wavy lines on cylinders | Low poly too coarse for the smoothing gradient | More sides on the low, or a cage |
| Skewed details (bolts lean) | Rays follow averaged low-poly normals | Hard edge plus seam at that border, a cage, or bake the floater separately |
| Crack along a hard edge | Hard edge inside a UV island | Seam it |
| Seams visible in engine | Padding too small, tangent basis mismatch, different triangulation | Padding res/128 or more, export MikkTSpace tangents, triangulate before baking |
| Detail from a neighboring part | Parts too close during the bake | Exploded bake or per-pair bakes |
| Lighting looks inverted on bumps in engine | OpenGL vs DirectX green channel mismatch | Flip G for DirectX targets (Unreal) or tick the engine's flip-green option |
| AO ghost of another part | Shared texels (stacked UVs) or other objects visible to render | Unique UVs; hide other objects |
| Banding in smooth gradients | 8-bit bake | Bake to a float image and save as 16-bit PNG |

## Review

Render the low with its maps applied beside the high, under a light raking across the surface, from the gameplay camera and close up. Check the normal map's average color is near (128, 128, 255); a blue average under 200 means the wrong color space, or a height map labeled as normal.
