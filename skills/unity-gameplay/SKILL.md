---
name: unity-gameplay
description: >-
  Builds and fixes Unity 6 3D gameplay systems: Input System actions and rebinding, Rigidbody and
  CharacterController movement, collisions, triggers and raycasts, NavMesh agents, Animator,
  blend trees, IK and Timeline, Cinemachine 3 cameras, NPC perception and decision making, and
  vector and quaternion math. Use when a character will not move, collide, animate, path or aim
  correctly, or when adding controls, cameras or enemy AI. Not for 2D physics or tilemaps
  (unity-2d), general C# lifecycle and state machine code (unity-csharp), or rendering and VFX
  (unity-rendering).
license: MIT AND Apache-2.0
compatibility: Unity 6.0 or newer, written against 6.3 LTS. Input System 1.x, AI Navigation 2.x, Cinemachine 3.x.
---

# Unity Gameplay

Wire input to movement, collisions, navigation, animation and cameras, and prove each piece
works with a number, not a look. Lifecycle, `.meta` safety and test assembly setup are in
`unity-csharp`; read it first if the change adds or moves scripts.

## Workflow

1. **Read the project's settings as text before changing code.**
   - Input handling: `ProjectSettings/ProjectSettings.asset` `activeInputHandler` (0 old Input
     Manager, 1 Input System, 2 both).
   - Physics: `ProjectSettings/DynamicsManager.asset` (`m_QueriesHitTriggers`,
     `m_ContactPairsMode`, layer collision matrix).
   - Packages: `Packages/manifest.json` for `com.unity.inputsystem`, `com.unity.ai.navigation`,
     `com.unity.cinemachine`.
2. **Open the reference for the system you touch** (table below) before writing code.
3. **Keep the frame split**: read input in `Update`, apply forces, velocity or `MovePosition` in
   `FixedUpdate`, move cameras in `LateUpdate` (Cinemachine's Brain does this for you).
4. **Verify** by reading state back: a body's `linearVelocity` after a second of Play mode, a
   callback count in a PlayMode test, an agent's `pathStatus`. The official `unity-cli` skill can
   read live values with `script eval`. For feel, ask the user for a countable answer ("jump five
   times, how many landings played?").

## References

| System | Read |
|---|---|
| Rigidbody movement, colliders, triggers, collision detection modes | [references/physics-3d.md](references/physics-3d.md) |
| Raycast, SphereCast, overlap, non-alloc buffers, LayerMask, joints | [references/raycasting-and-joints.md](references/raycasting-and-joints.md), [references/physics-queries.md](references/physics-queries.md) |
| CharacterController | [references/character-controller.md](references/character-controller.md) |
| Input System actions, maps, PlayerInput, tests with `InputTestFixture` | [references/input.md](references/input.md) |
| Input timing, processors vs interactions, prompts, local multiplayer, scheme switching | [references/input-correctness.md](references/input-correctness.md) |
| Rebinding and saving overrides | [references/rebinding.md](references/rebinding.md) |
| Animator parameters, transitions, layers, root motion | [references/animation.md](references/animation.md) |
| Blend trees and IK | [references/blend-trees-and-ik.md](references/blend-trees-and-ik.md) |
| Timeline cutscenes | [references/timeline.md](references/timeline.md) |
| NavMeshSurface, agents, obstacles, links | [references/navigation.md](references/navigation.md) |
| Cinemachine 3 cameras, blends, impulse shake, v2 migration | [references/cinemachine.md](references/cinemachine.md), [references/cinemachine-api.md](references/cinemachine-api.md) |
| NPC perception, blackboard, actions, factions, memory, squads | [references/npc-behavior.md](references/npc-behavior.md), [references/npc-scaffolds.md](references/npc-scaffolds.md) |
| Spaces, quaternions, angles, screen to world | [references/3d-math.md](references/3d-math.md) |

## Physics rules

- Move dynamic bodies with `AddForce`, `linearVelocity` or `MovePosition`, never by writing
  `transform.position`.
- Unity 6 names: `linearVelocity`, `linearDamping`, `angularDamping`, `PhysicsMaterial`.
  `PhysicMaterial` is a compile error.
- A trigger or collision callback needs a Rigidbody on at least one of the pair and both
  colliders enabled. Two kinematic bodies, or kinematic and static, report nothing under the
  default Contact Pairs Mode.
- `CharacterController.Move` never calls `OnCollisionEnter`; use `OnControllerColliderHit`.
- Queries hit triggers by default. Pass `QueryTriggerInteraction.Ignore` for ground and line of
  sight checks.
- Fast objects tunnel through walls on `Discrete`. Use `ContinuousSpeculative`, or a cast along
  the path for bullets.
- Concave `MeshCollider` only on static or kinematic bodies. Use Convex or primitive compounds
  for moving ones, with one Rigidbody on the root.
- Runtime `IgnoreLayerCollision` is not saved. For a lasting change, edit the matrix in Project
  Settings or ask the user to.

## Input rules

- Default to project-wide actions: `InputSystem.actions.FindAction("Player/Move")`. Add to
  `Assets/InputSystem_Actions.inputactions` rather than creating a second asset.
- Project-wide actions enable every map at startup. Disable the UI map in `Start` and switch
  maps for context instead of guarding handlers.
- Buttons are edges: `WasPressedThisFrame()` in `Update`, or the `performed` callback. Never read
  presses in `FixedUpdate`.
- `.triggered` respects interactions (Hold, Tap). `WasPressedThisFrame()` ignores them.
  Processors change values; interactions change timing.
- Copy `InputValue` with `.Get<T>()` inside the callback; the wrapper is reused.
- `Gamepad.current` is the last used pad, not a player's pad. Use `PlayerInput` and
  `PlayerInputManager` for local multiplayer.
- Leftover `Input.GetAxis` throws when `activeInputHandler` is 1. Port it or set 2 while
  migrating; changing the setting restarts the Editor, so tell the user.

## Animation rules

- Cache parameter hashes with `Animator.StringToHash`. Misspelled names fail silently.
- Turn off Has Exit Time for condition-driven transitions (jump, hit).
- Choose root motion or scripted movement per character, not both.
- `CrossFade` duration is normalized; `CrossFadeInFixedTime` takes seconds.
- IK runs only inside `OnAnimatorIK`, with IK Pass on the layer and a Humanoid Avatar.
- Pooled characters restart in the default state. Set `keepAnimatorStateOnDisable` or reset
  parameters on reuse.

## Navigation rules

- AI Navigation 2: bake from a `NavMeshSurface`. There is no Bake tab or Navigation Static.
- Snap spawns with `NavMesh.SamplePosition` and move agents with `agent.Warp`.
- `PathPartial` means another island: add a `NavMeshLink` (not the deprecated `OffMeshLink`).
- Runtime props need a carving `NavMeshObstacle` or a rebake. Never put an enabled agent and an
  enabled obstacle on the same object.
- An agent and a non-kinematic Rigidbody fight over the Transform. Make the body kinematic.
- Re-path on a timer or when the target moves past a threshold, not every frame.

## Camera rules

- Cinemachine 3: `using Unity.Cinemachine;`, `CinemachineCamera` plus a Body and Aim component,
  `CinemachineBrain` on the Main Camera. v2 types (`CinemachineVirtualCamera`,
  `CinemachineFreeLook`, `CinemachineTransposer`) are gone; map them with the table in
  `references/cinemachine.md`.
- Switch shots by priority and let the Brain blend. Do not move `Camera.main` yourself.
- Shake with Impulse sources and listeners, not by offsetting the camera.

## NPC rules

- Separate perception (staggered queries on an interval), decision (FSM or behavior tree from
  `unity-csharp`), and action execution (interruptible, cancels pending effects).
- One blackboard instance per NPC, allocated in `Awake`.
- Memory stores world positions, not live references.

## Math rules

- `TransformPoint` for positions, `TransformDirection` for directions, `TransformVector` when
  scale matters.
- Quaternion order: `A * B` applies `B` in `A`'s local space. Never edit `x/y/z/w` directly;
  interpolate with `Slerp`, never Euler angles.
- Guard `Quaternion.LookRotation` against zero vectors. Compare distances with `sqrMagnitude`.
- `Vector3.Angle` is unsigned; use `SignedAngle` with an axis.

## Related skills

- `unity-csharp`: lifecycle, async, state machines, test assemblies, `.meta` checker.
- `unity-2d`: Rigidbody2D, tilemaps, sprites.
- `blender-game-export`: importing rigs and animation clips from Blender.
- `unity-cli` (official): drive the Editor and Play mode, read live values.
