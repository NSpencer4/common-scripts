---
name: unity-build-perf
description: >-
  Builds, measures and speeds up Unity 6 games: scripted and CI player builds, Build Profiles,
  code stripping and link.xml, build size against store and host limits (WebGL, Android, iOS,
  Steam), Profiler, Frame Debugger and Memory Profiler work, GC allocations, mobile and WebGL
  settings, platform defines, IL2CPP, and the Unity Test Framework in batch mode and CI. Use when
  a build fails or is too big, the game stutters or drops frames, memory grows, or tests must run
  headless. Not for writing gameplay code (unity-csharp) or shader and lighting setup
  (unity-rendering).
license: MIT AND Apache-2.0
compatibility: Unity 6.0 or newer, written against 6.3 LTS. Python 3.10+ for the bundled scripts.
---

# Unity Build and Performance

Measure first, change one thing, measure again. Report numbers in milliseconds and megabytes,
from a development player on the lowest target device when possible. Editor Play mode numbers
are for iteration only.

If the official `unity-cli` skill is installed, use it to run builds and tests and keep their
logs. This skill does not repeat its commands.

## References

| Task | Read |
|---|---|
| Scripted builds, Build Profiles, CI flags, `link.xml` | [references/build-pipeline.md](references/build-pipeline.md), [references/ci-build-script.md](references/ci-build-script.md) |
| Build too big: measure, find causes, fix, compare | [references/build-size.md](references/build-size.md) |
| Per-target size limits and levers | [references/platform-web.md](references/platform-web.md), [references/platform-android.md](references/platform-android.md), [references/platform-ios.md](references/platform-ios.md), [references/platform-desktop-steam.md](references/platform-desktop-steam.md) |
| Textures inside glTF models | [references/gltf-textures.md](references/gltf-textures.md) |
| Profiler, Frame Debugger, IL2CPP, quality settings, common bottlenecks | [references/performance.md](references/performance.md), [references/profiler.md](references/profiler.md) |
| GC allocations, NativeArray, texture and audio memory, Memory Profiler | [references/memory.md](references/memory.md) |
| Platforms, Build Profiles, WebGL, Addressables, mobile settings, defines | [references/platforms.md](references/platforms.md), [references/mobile-optimization.md](references/mobile-optimization.md), [references/platform-defines.md](references/platform-defines.md) |
| Test Framework: EditMode vs PlayMode, async tests, command line | [references/testing.md](references/testing.md), [references/test-framework.md](references/test-framework.md) |

## Scripts

Both are read-only and use the Python standard library. Run them from this skill's folder or
pass absolute paths.

- `python3 scripts/build_report.py <Editor.log> --top 20` summarizes the last player Build
  Report in an Editor log (Linux: `~/.config/unity3d/Editor.log`, or the `-logFile` path).
  `--budget-mb N` fails when over budget.
- `python3 scripts/check_unity_build_size.py <project> --platform WebGL` finds oversized or
  uncompressed textures, PCM audio and heavy glTF models. `--json` for tools.

## Build rules

- Check `BuildReport.summary.result`; `BuildPlayer` returning is not success.
- In batch mode pass `-buildTarget` (or `-activeBuildProfile`) at launch. A target switch inside
  the job keeps the old platform's defines.
- A Build Profile has its own Scene List; a scene missing from it does not load with
  `SceneManager.LoadScene`.
- Build Addressables content explicitly in CI (`AddressableAssetSettings.BuildPlayerContent`).
- `MissingMethodException` only in a build means stripping removed reflection-only code: add a
  `link.xml` entry or lower Managed Stripping Level.
- IL2CPP needs the platform toolchain (Android NDK, platform build tools); Mono does not.
- Release builds without `BuildOptions.Development`. Clear Build Profile Asset Import Overrides
  before a release build.

## Size rules

- Pin which file is limited and by how much before changing anything (itch.io file limit, Play
  download size, Steam patch size).
- Fix the biggest Build Report category first; textures usually dominate.
- On Steam and Android leave Compression Method on Default; LZ4HC inflates patches.
- A Web build several times too big is often a development build, which Unity never compresses.

## Performance rules

- Find the bound first: CPU main thread, render thread, or GPU. The Profiler's timeline and the
  Frame Debugger answer this; guessing does not.
- Budget per frame: 16.67 ms at 60 fps, 33.33 ms at 30. Leave headroom on mobile for thermals.
- Zero allocations per frame in steady gameplay: cache `GetComponent`, reuse `WaitForSeconds`,
  pool spawned objects, use non-allocating physics queries, `SetText` for numbers, no LINQ or
  string concatenation in `Update`.
- Wrap suspect code in `ProfilerMarker` so it shows by name in the Profiler.
- Draw calls: SRP Batcher on, shared materials, GPU instancing for repeated meshes, static
  batching for scenery. Dynamic batching rarely pays off.
- Mobile: target frame rate set explicitly, ASTC textures, fewer realtime lights, adaptive
  quality tiers.
- WebGL: no threads by default, memory growth limits, compressed builds served with the right
  `Content-Encoding` headers.

## Test rules

- Logic in plain C# classes, tested in EditMode. PlayMode only for frames, physics, animation.
- Batch mode: `-runTests` without `-quit`, absolute `-testResults` and `-logFile` paths. Read the
  NUnit XML totals and failures, not the exit code alone.
- Async tests: `[UnityTest]` returning `IEnumerator`, or `async Awaitable` tests where the Test
  Framework version supports them.
- Test assembly `.asmdef` setup is in `unity-csharp/references/verify-from-cli.md`.

## Related skills

- `unity-csharp`: code changes the profiler points at, test assemblies.
- `unity-rendering`: GPU-side fixes (shaders, lighting, post-processing).
- `unity-ui`: Canvas rebuild and TextMeshPro memory.
- `blender-game-assets`: polygon budgets and texture sizes at the source.
