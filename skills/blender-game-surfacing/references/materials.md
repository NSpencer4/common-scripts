# Game materials

## PBR rules

1. **Metallic is 0 or 1.** In-between values only on transition pixels (rust or dust edges on metal). Painted metal is a dielectric.
2. **Base color is albedo with no lighting**: no baked shadows, AO, or highlights. Dielectrics sit in sRGB 30 to 240 (charcoal about 50, fresh snow about 240). Metals use their reflectance color, sRGB 180 to 255, never dark.
3. **Roughness carries the realism.** A constant roughness reads as fake; vary it by 0.1 to 0.2 across a surface with grime and smudges.
4. **Color spaces**: base color and emission are sRGB. Roughness, metallic, normal, AO, height, opacity, ORM, and masks are Non-Color. Set `image.colorspace_settings.name` before baking or export; it is per image, so shared images change for every material.
5. **Leave IOR at 1.5** for nearly all dielectrics. Engines use a fixed specular for dielectrics anyway.
6. **AO is not multiplied into base color** for engines. Ship it in its own map or packed channel.

## Measured values

| Material | Base color (sRGB) | Metallic | Roughness |
|---|---|---|---|
| Iron or steel | 196, 199, 199 | 1 | 0.3 to 0.6 |
| Aluminum | 245, 246, 246 | 1 | 0.2 to 0.5 |
| Gold | 255, 226, 155 | 1 | 0.1 to 0.35 |
| Copper | 250, 208, 192 | 1 | 0.2 to 0.45 |
| Black rubber, tire | 40 to 50 | 0 | 0.8 to 0.95 |
| Black plastic | 30 to 45 | 0 | 0.3 to 0.6 |
| White plastic | 220 to 230 | 0 | 0.2 to 0.5 |
| Concrete | 130 to 150 | 0 | 0.8 to 0.95 |
| Unfinished oak | 160, 120, 80 | 0 | 0.6 to 0.8 |
| Red brick | 150, 80, 60 | 0 | 0.8 to 0.9 |
| Grass | 75, 110, 45 | 0 | 0.6 to 0.8 |

Sources: Unreal Engine physically based materials documentation and physicallybased.info, as compiled by el4cteo/blender-skills. Sanity checks for a texture set: dielectric base color averages sRGB 50 to 200; a metal under 180 means the metallic mask or albedo is wrong; a roughness map with almost no variation needs breakup.

## Channel packing per target

| Target | Maps | Packing | Normal |
|---|---|---|---|
| glTF, Godot, web | Base color (+alpha), metallic-roughness, normal, occlusion, emissive | glTF metallicRoughness: G = roughness, B = metallic; occlusion in R, so one ORM texture serves both | OpenGL |
| Unreal | BaseColor, Normal, ORM | R = AO, G = roughness, B = metallic; uncheck sRGB, Masks compression | DirectX (flip green, or tick Flip Green Channel on import) |
| Unity URP Lit | BaseMap, NormalMap, Metallic map, Occlusion | Metallic map: R = metallic, A = smoothness (1 - roughness) | OpenGL |
| Unity HDRP Lit | BaseColor, Normal, MaskMap | R = metallic, G = AO, B = detail mask, A = smoothness | OpenGL |

Build packed maps in Blender with numpy: read each grayscale image with `image.pixels.foreach_get`, write channels into a new Non-Color image, and save it as PNG. Never save normal maps as JPEG.

## Material rules for export

- Only Image Texture to Principled BSDF chains export. Procedural nodes and math become nothing in the engine: bake them.
- One material per texture set. Each extra material on a mesh is roughly one extra draw call.
- Power-of-two textures (512, 1024, 2048, 4096).
- Name materials `M_Asset` and textures `T_Asset_BC`, `_N`, `_ORM` (or the project's own convention). Engines key materials by name across reimports.

## Alpha

`mat.surface_render_method = "DITHERED"` for cutout (foliage cards, fences, hair cards); it sorts correctly and exports as glTF MASK. `"BLENDED"` for true transparency (glass); it exports as BLEND and has sorting costs in engines. Prefer cutout for games.

## Wear and grime

Layer from the inside out, each with a physical cause:

| Layer | Mask | Look |
|---|---|---|
| Edge wear | Convex curvature times noise | Reveals the under-material (bare metal, primer, raw wood) |
| Grime | Concave curvature and (1 - AO) | Darker, rougher, non-metal |
| Dust | Up-facing normal times patchy noise | Light, roughness about 0.9 |
| Roughness breakup | Fine noise, about 25% | The cheapest realism improvement |

Pure curvature looks procedural; multiply in noise so wear is heavy in places and absent in others. Wear around 0.2 to 0.4 reads as used, 0.7 and above as abandoned. On low-poly meshes, drive the masks from baked curvature and AO maps, then bake the result to the final texture set.

## Judging materials

Review with the view transform set to Khronos PBR Neutral (`scene.view_settings.view_transform`), which shows albedo close to how glTF viewers do. AgX (the default) is photographic and can mislead when judging albedo. Never author textures while a strong Look is applied.
