---
name: blender-rigging-animation
description: >-
  Rigs and animates characters and creatures in Blender 5.2+ for game engines: Rigify metarigs,
  joint placement, skinning with heat or proxy weights, weight painting rules, stress poses, a
  clean deform-only game skeleton, Unity Humanoid mapping, ARKit and viseme shape keys,
  correctives, keyframe workflow, 5.x actions and slots, loops, root motion, mocap retargeting
  (Mixamo, BVH), and baking clips for export. Use for anything that deforms or moves. Not for
  static props (blender-game-modeling) or the export settings (blender-game-export).
license: MIT
compatibility: Blender 5.2 LTS or newer, verified upstream on 5.3. Rigify is bundled.
---

# Blender Rigging and Animation

Run every script the way `blender-game-modeling` describes (`operating-blender.md`). The mesh must
pass the `blender-game-modeling` QA gate before rigging: scale applied, facing -Y, feet at Z = 0, symmetric on X.

## Rig a character

1. `scripts/rigify_build.py -- --add basic_human --fit Body` (games: `--no-face`, use shape keys).
2. Move joints to the pivot of rotation, with a slight bend at elbows and knees.
3. `scripts/rigify_build.py -- --metarig META_Body --generate` gives the control rig `RIG_Body`.
4. `scripts/bind_mesh.py -- --armature RIG_Body --meshes Body` (heat weights, proxy fallback,
   cleaned to 4 influences, normalized).
5. `scripts/stress_poses.py -- --armature RIG_Body`, then look at the frames. Fix elbows,
   forearm twist, shoulders and hips.
6. `scripts/rigify_build.py -- --rig RIG_Body --game-skeleton` gives `GAME_RIG_Body`: `root` plus
   deform bones only, `DEF-` stripped, constrained to the control rig.
7. `scripts/rig_check.py -- --armature GAME_RIG_Body --profile unity [--fix]`.

Details, bone and weight rules: [references/character-rigging.md](references/character-rigging.md).

## Unity Humanoid requirements

- Hips is the root of the deform hierarchy (a `root` bone above it is fine for root motion), then
  Spine, Chest, Neck, Head, and the limb chains. `rig_check --profile unity` shows the mapping.
- Bind pose in T-pose. Unity can enforce it in Configure Avatar.
- At most 4 influences per vertex for mobile, normalized, no weights on the root.
- Armature object scale 1 and rotation 0. No animated bone scale.

## Faces

ARKit 52 blendshapes or Oculus visemes: `scripts/shapekeys.py -- --mesh Head --create arkit`,
then sculpt each key, `--split` and `--mirror` for sides, `--report` until every key moves.
Names are case-sensitive and must match the spec. Jaw and eyes as bones.
[references/facial-shapekeys.md](references/facial-shapekeys.md).

## Animate and bake clips

- Blocking, breakdowns, spline, polish. One action per clip with a fake user, quaternion rotation
  on game bones, authored at 30 fps.
- Loops: first and last frames identical; bake `CYCLES` modifiers, which do not export.
  `scripts/loop_check.py` verifies.
- Root motion: the root carries translation and yaw, hips keep the bob.
- Bake the control rig onto the game skeleton:
  `scripts/bake_action.py -- --source RIG_Body --target GAME_RIG_Body --root-motion xy --hips spine`.
- Mocap: `scripts/retarget.py -- --source Mocap --target GAME_RIG --map auto --show-map` first;
  rest poses must match (T vs A).
- 5.x data model: actions have slots and channelbags; `action.fcurves` no longer exists.

[references/animation.md](references/animation.md).

## Related skills

- `blender-game-modeling`: execution, API rules, keyframe and driver snippets, QA.
- `blender-game-export`: `unity_skeletal` export preset, clip naming, Humanoid import.
- `unity-gameplay`: Animator, blend trees, root motion and IK on the Unity side.
