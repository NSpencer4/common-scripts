---
name: unity-csharp
description: >-
  Writes and fixes Unity 6 C# gameplay code: MonoBehaviour lifecycle, serialization, .meta/GUID
  safety, fake-null, coroutines and Awaitable, ScriptableObjects, events, architecture
  (services, composition, bootstrap), state machines and behavior trees, data-driven config, and
  save/load. Use for any new or changed .cs file in a Unity project, "Missing script", a field
  missing from the Inspector, MissingReferenceException, or async code that outlives its object.
  Not for physics, input, navigation or animation (unity-gameplay), 2D (unity-2d), rendering
  (unity-rendering), UI, text and localization (unity-ui), or builds and profiling
  (unity-build-perf).
license: MIT AND Apache-2.0
compatibility: Unity 6.0 or newer, written against 6.3 LTS (6000.3). Python 3.10+ for the project checker.
---

# Unity C#

Write gameplay code that compiles, survives refactors, and behaves the same in the Editor and a
build. Prove each change with the cheapest check that covers it, and say which checks ran.

If the official `unity-cli` skill is installed, use it to compile, run tests and read live
Editor state. This skill does not repeat its commands.

## Workflow

1. **Read the project's versions first.** `ProjectSettings/ProjectVersion.txt` gives the Editor
   version, `Packages/manifest.json` the packages, and any `*.asmdef` decides which assembly a new
   script lands in. Keep the project's version unless asked to upgrade.
2. **Pick the callback by purpose** (table below). Expose tunables as `[SerializeField] private`.
3. **Move every file with its `.meta`.** The `.meta` holds the GUID that scenes and prefabs
   reference. A new file needs no `.meta`; Unity writes one on import. One `MonoBehaviour` or
   `ScriptableObject` class per file, with the file named after the class.
4. **Run the checker** after creating, moving, renaming or deleting files outside the Editor:
   `python3 scripts/check_unity_project.py <project-dir>` (add `--json` to parse). Fix every
   `ERROR` and re-run until it exits 0. It is read-only.
5. **Compile**, then **prove behavior** with an EditMode or PlayMode test, or by reading the value
   back from a running Editor. Commands, test `.asmdef` files and how to read NUnit results:
   [references/verify-from-cli.md](references/verify-from-cli.md).

## Lifecycle

| Callback | Runs | Use for |
|---|---|---|
| `Awake` | Once, when the GameObject is active (even if the component is disabled) | Cache own components |
| `OnEnable` / `OnDisable` | Every enable and disable, and before `OnDestroy` | Subscribe and unsubscribe |
| `Start` | Once, before the first `Update`, only if enabled | Wire to other objects |
| `FixedUpdate` | 0 to N times per frame | Physics |
| `Update` | Once per frame | Game logic, read input |
| `LateUpdate` | After all `Update` calls | Cameras, follow |
| `OnDestroy` | Once | Release own resources |
| `OnApplicationPause(true)` | App backgrounded | Save on mobile (`OnApplicationQuit` may never fire) |
| `OnValidate` / `Reset` | Editor only, stripped from builds | Clamp fields, defaults |

- All `Awake` calls finish before any `Start`, but order among `Awake`s is undefined unless
  Script Execution Order or `[DefaultExecutionOrder]` sets it. Do cross-object wiring in `Start`.
- Subscribe in `OnEnable`, unsubscribe in `OnDisable`. `Start`/`OnDestroy` pairs break with pooling.
- `SetActive(false)` stops the object's coroutines; `enabled = false` does not.
- With Enter Play Mode Options (no domain reload), static fields keep last session's values.
  Reset them in `[RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.SubsystemRegistration)]`.

Full order, edit-mode behavior and the quit sequence:
[references/lifecycle-and-coroutines.md](references/lifecycle-and-coroutines.md),
[references/editor-runtime-init.md](references/editor-runtime-init.md).

## Rules that prevent the common bugs

**Fake-null.** Unity overrides `==` so a destroyed object equals `null`. `?.`, `??`, `is null`,
`is not null` and pattern matching skip that override.

```csharp
// Wrong: may call into a destroyed object
target?.TakeDamage(1);
// Right
if (target != null) target.TakeDamage(1);
```

**Destroy is deferred.** `Destroy` runs at end of frame; `OnDisable`/`OnDestroy` fire later.
`DestroyImmediate` is for editor code only.

**Serialized renames lose data.** Add `[FormerlySerializedAs("oldName")]`
(`UnityEngine.Serialization`) when renaming a serialized field. It does not help JSON.

**Plain classes need `[System.Serializable]`** to appear in the Inspector. Use
`[SerializeReference]` for interface or polymorphic fields.

**Find APIs.** `FindObjectOfType` is obsolete. Use `FindAnyObjectByType<T>()` or
`FindObjectsByType<T>(FindObjectsSortMode.None)`, never in `Update`; cache the result.

**Physics timing.** Read input in `Update`, apply forces or `MovePosition` in `FixedUpdate`.

## Coroutines and Awaitable

| Need | Use |
|---|---|
| Frame-stepped sequence on one object | Coroutine; store the `Coroutine` handle to stop it |
| Async that returns a value or needs try/catch | `async Awaitable` / `Awaitable<T>` |
| CPU work off the main thread | `await Awaitable.BackgroundThreadAsync()`, then `await Awaitable.MainThreadAsync()` before any Unity API |

- Pass `destroyCancellationToken` to every `Awaitable` wait, or the method keeps running after
  its object is destroyed. It throws `OperationCanceledException` on cancel; let it propagate or
  catch that type only.
- Await each `Awaitable` instance once. They are pooled; a second await can see another
  operation's state.
- `async void` loses exceptions; use `async Awaitable`. Lifecycle methods (`Start`) may be
  `async Awaitable`.
- `Task.Delay` ignores `timeScale` and frame sync. Use `Awaitable.WaitForSecondsAsync`.
- `WaitForEndOfFrame` / `EndOfFrameAsync` never complete in batch mode or headless tests. Use
  `yield return null` / `Awaitable.NextFrameAsync` there.
- Exceptions inside a coroutine stop it silently; the caller never sees them.
- Do not mix UniTask and Awaitable without a clear boundary.
- Release every Addressables `LoadAssetAsync` handle with `Addressables.Release`.

Token chains, timeouts, debounce and Addressables loading:
[references/async-cancellation.md](references/async-cancellation.md).

## ScriptableObjects

Use them for designer-edited config, one value shared by unrelated systems, event channels, and
runtime sets. State that differs per object belongs on the MonoBehaviour.

- `[CreateAssetMenu]` on the class. Create assets with `AssetDatabase.CreateAsset` from editor
  code, never by hand-writing `.asset` YAML (the `m_Script` GUID must match).
- Play-mode changes to an asset persist in the Editor and are lost in builds. Keep runtime
  values in `[System.NonSerialized]` fields and reset them on Play.
- Assets ship only if referenced from a built scene, another shipped asset, `Resources`, or
  Addressables.
- Never use an SO as save data.

Event channels and runtime sets: [references/event-channels.md](references/event-channels.md).

## Architecture choices

| Question | Default |
|---|---|
| Infrastructure (audio, save, analytics) | Interface-backed service locator, registered at bootstrap |
| Gameplay dependencies | Serialized references or constructor injection; no singletons |
| Pure logic | Plain C# class owned by a MonoBehaviour, tested in EditMode |
| Shared behavior across entity types | Composition of small components and interfaces (`TryGetComponent<IDamageable>`) |
| Cross-system events | C# events for local, SO event channels for designer-wired, typed struct event bus for global |
| Startup order | `[RuntimeInitializeOnLoadMethod(BeforeSceneLoad)]` creates one bootstrap object; async init in its `Start` |

Avoid: god MonoBehaviours, manager-of-managers, `FindObjectOfType` lookups at runtime, static
state without a reset. Full service locator, event bus and DI comparison:
[references/architecture-patterns.md](references/architecture-patterns.md).

## State machines

| States | Use |
|---|---|
| 2 or 3 | `if` and an enum |
| Up to about 15 | `IState` classes (plain C#) with `Enter`/`Tick`/`Exit` and a shared context |
| Grouped (Locomotion > Idle/Walk/Run) | Hierarchical FSM; exit sub-state before super-state |
| Priority-based, interruptible AI | Behavior tree with a blackboard |
| UI screens, pause menus | Stack machine (push/pop), with a depth limit |

Do not use an Animator as a logic FSM. Pass `deltaTime` into `Tick` so states test in EditMode.
Scaffolds: [references/state-machines.md](references/state-machines.md).

## Data-driven config

| Data | Store as |
|---|---|
| Designer-tuned, references assets | ScriptableObject |
| Large tables from spreadsheets | CSV or JSON imported by an editor script into SOs |
| Loaded at runtime, moddable | JSON in `StreamingAssets` |

`JsonUtility` cannot handle dictionaries, top-level arrays, polymorphism, nulls or properties.
Use Newtonsoft (`com.unity.nuget.newtonsoft-json`) for those. Give designers `[Tooltip]`,
`[Range]`, `[Header]` on every field. Pipelines and import scripts:
[references/data-pipeline.md](references/data-pipeline.md).

## Save and load

- Serialize plain `[System.Serializable]` DTOs, never MonoBehaviours or SOs. Include an `int
  version` from the first release and migrate on raw JSON before deserializing.
- Write under `Application.persistentDataPath`, to a `.tmp` file first, then rename, so a crash
  mid-write cannot corrupt the save.
- `BinaryFormatter` is a security hole; replace it with JSON.
- PlayerPrefs only for settings, with prefixed keys (`audio.master`).
- Save on `OnApplicationPause(true)` for mobile; in `OnApplicationQuit` use synchronous I/O.
- Cloud save: save locally first, sync in the background, never block play on network errors.

Full SaveManager, `ISaveable` and migration code: [references/save-load.md](references/save-load.md).

## Pooling

Use `UnityEngine.Pool.ObjectPool<T>` for anything spawned often (projectiles, hit effects).
Reset state in the release callback and subscribe in `OnEnable`, not `Start`.
API and patterns: [references/object-pool.md](references/object-pool.md).

## Related skills

- `unity-gameplay`: physics, input, navigation, animation, cameras, NPC behavior.
- `unity-build-perf`: profiling, GC allocations, builds and test runs in CI.
- `unity-cli` (official): compile, test, run C# in a live Editor.
