---
name: unity-2d
description: >-
  Builds and fixes Unity 6 2D games: Rigidbody2D movement, ground checks, one-way platforms and
  kinematic Slide controllers, Tilemaps, Tile Palettes, Rule Tiles and tilemap colliders, sprite
  import, slicing, 9-slicing and Sprite Atlases, sorting layers, 2D lights in URP, and pixel
  perfect cameras. Use for any 2D task, including pixel art that looks blurry or jitters,
  characters catching on tile seams, or callbacks that never fire on 2D objects. Not for 3D
  physics (unity-gameplay) or general C# (unity-csharp).
license: MIT AND Apache-2.0
compatibility: Unity 6.0 or newer, written against 6.3 LTS. 2D Tilemap Extras for Rule Tiles. URP for 2D lights and the URP Pixel Perfect Camera.
---

# Unity 2D

2D and 3D physics are separate engines with separate types and callbacks. Confirm which one an
object uses before touching it: grep the scene or prefab YAML for `Rigidbody2D:` vs `Rigidbody:`
and `BoxCollider2D:` vs `BoxCollider:`. Mixed 2D and 3D on interacting objects is a bug.

## References

| Task | Read |
|---|---|
| Body types, platformer mover, ground check, `Slide`, one-way platforms, layer settings | [references/physics-2d.md](references/physics-2d.md) |
| Grid and Tilemap setup, painting and querying in code, tiles from a sliced sheet, collider merging, verification | [references/tilemap-workflow.md](references/tilemap-workflow.md) |
| Tilemap API, Rule Tiles, procedural generation, palette tools | [references/tilemap-api.md](references/tilemap-api.md) |
| Sprite import, slicing, 9-slicing, masks, Sprite Atlas, late binding | [references/sprites-and-atlas.md](references/sprites-and-atlas.md) |
| SpriteRenderer, 2D lights, sorting layers and groups, top-down movement | [references/2d-overview.md](references/2d-overview.md) |

## 2D physics rules

| 3D habit | 2D reality |
|---|---|
| `isKinematic` | `bodyType` (`Dynamic`, `Kinematic`, `Static`); `isKinematic` is obsolete |
| `OnCollisionEnter(Collision)` | `OnCollisionEnter2D(Collision2D)`; the 3D name never runs on a 2D object, with no error |
| `Physics.Raycast` returns `bool` | `Physics2D.Raycast` returns `RaycastHit2D`; test `if (hit)` |
| A ray starting inside a collider misses it | `queriesStartInColliders` is on, so a ground ray from the player's centre hits the player |
| `*NonAlloc` queries | Deprecated in 2D; pass a `ContactFilter2D` and a results list |
| `angularVelocity` in rad/s, `Vector3` | `float`, degrees per second |

- Move bodies with `MovePosition`, `linearVelocity` or `AddForce` in `FixedUpdate`, never the
  Transform.
- Ground checks: `ContactFilter2D` with the ground layer and `useTriggers = false`, or exclude
  the player's layer.
- Kinematic characters: `Rigidbody2D.Slide` handles slopes and gravity without a hand-written
  cast loop.
- Kinematic vs kinematic contacts need `useFullKinematicContacts`.
- If nothing moves, check `Physics2D.simulationMode`; `Script` means you must call
  `Physics2D.Simulate`.
- Unity 6.3 also has a separate low-level 2D API (`UnityEngine.LowLevelPhysics2D`, renamed
  Physics Core 2D in 6.5). Use it only if the project already does.

## Tilemap rules

- One `Grid`, one `Tilemap` per layer (background, ground, foreground), each
  `TilemapRenderer` with an explicit Sorting Layer and Order.
- Rule Tiles and Animated Tiles need `com.unity.2d.tilemap.extras`. Check
  `Packages/packages-lock.json` and ask before adding it.
- Solid layer: `TilemapCollider2D` with Composite Operation = Merge, plus a
  `CompositeCollider2D` and a `Static` `Rigidbody2D`. One collider per tile catches characters
  on seams. Unity 6 replaced `usedByComposite` with `compositeOperation`.
- Small gaps after merging: raise the tilemap collider's Extrusion Factor.
- Edit in cell coordinates (`WorldToCell`, `SetTile`, `SetTilesBlock`), refresh only the
  edited cells, and call `CompressBounds()` after erasing or generating.
- Chunk render mode for static maps; Individual only when tiles must sort against sprites.
- Create tile assets with `AssetDatabase.CreateAsset` from editor code, never hand-written YAML.

## Sprites and atlases

- Import as Sprite (2D and UI). For a sheet, Sprite Mode Multiple and slice in the Sprite
  Editor, or set rects in an `AssetPostprocessor` or editor script.
- Resize UI-like and tiled sprites with `SpriteRenderer.drawMode` Sliced or Tiled and `size`,
  not `localScale`.
- Pack sprites that draw together into one Sprite Atlas. Leave Read/Write off (it doubles
  memory) and Allow Rotation off for UI sprites.
- Use sorting layers (Background, Characters, Foreground) and keep Order in Layer for fine
  ordering. Group multi-part characters with a `SortingGroup`.

## Pixel perfect

For pixel art that looks blurry, shimmers or jitters:

1. Textures: Filter Mode Point, Compression None, Pixels Per Unit the same on every sprite
   (for example 16 or 32).
2. Camera: add the Pixel Perfect Camera (URP: the one in `UnityEngine.Rendering.Universal`,
   added to the camera with the 2D Renderer). Set Asset Pixels Per Unit to that PPU and
   Reference Resolution to the art's native resolution (for example 320x180).
3. Turn on upscaling to a render texture for the cleanest result, and choose crop or
   stretch for screens that are not an integer multiple of the reference resolution.
4. Snap moving sprites to the pixel grid, or move them in whole-pixel steps. Camera follow
   that lerps in sub-pixel steps is the usual source of jitter.
5. Verify at the target resolution in a build or the Game view at 1x, not the Scene view.

## Related skills

- `unity-csharp`: lifecycle, `.meta` safety, test assemblies.
- `unity-rendering`: URP setup, 2D Renderer, post-processing.
- `unity-ui`: Canvas UI and TextMeshPro.
- `unity-cli` (official): drive the Editor and read live values.
