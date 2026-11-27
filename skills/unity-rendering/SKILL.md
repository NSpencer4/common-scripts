---
name: unity-rendering
description: >-
  Sets up and fixes Unity 6 rendering: choosing URP or HDRP, moving Built-in projects to URP,
  materials and textures, Shader Graph and Custom Function nodes, hand-written URP HLSL, URP
  renderer features on the Render Graph API, Volume post-processing, lights, lightmaps, probes,
  Particle System and VFX Graph. Use for pink materials, post effects that do not show, too dark
  or blown-out lighting, shader authoring, or visual effects. Not for 2D lights and pixel
  perfect cameras (unity-2d), GPU profiling and build size (unity-build-perf), or importing
  Blender materials (blender-to-unity).
license: MIT
compatibility: Unity 6.0 or newer, written against 6.3 LTS with URP 17. HDRP notes in references.
---

# Unity Rendering

Find the active pipeline before anything else. Materials, shaders and post-processing do not
carry between pipelines, and the wrong pipeline is the usual cause of pink materials.

```csharp
// Read with a script eval or an editor script
UnityEngine.Rendering.GraphicsSettings.currentRenderPipeline   // null means Built-in
```

Or read `ProjectSettings/GraphicsSettings.asset` (`m_CustomRenderPipeline`) and the per-quality
overrides in `ProjectSettings/QualitySettings.asset`. Quality levels can point at different
pipeline assets; check the one the target platform uses.

## References

| Task | Read |
|---|---|
| Pipeline comparison, cameras, batching, occlusion, material anti-patterns | [references/graphics-overview.md](references/graphics-overview.md) |
| URP setup, rendering paths, anti-aliasing, SRP Batcher, 2D Renderer, quality | [references/urp.md](references/urp.md) |
| HDRP setup, ray tracing, volumetrics, custom passes | [references/hdrp.md](references/hdrp.md) |
| Shader Graph nodes, Custom Function, Sub Graphs, keywords | [references/shader-graph.md](references/shader-graph.md) |
| Hand-written URP ShaderLab and HLSL | [references/hlsl-shaders.md](references/hlsl-shaders.md) |
| Material API, property blocks, upgrades, texture import | [references/materials-textures.md](references/materials-textures.md) |
| Light modes, GI, probes, APV, reflection probes, day-night | [references/lighting-vfx-overview.md](references/lighting-vfx-overview.md), [references/lighting.md](references/lighting.md) |
| Particle System modules and scripting | [references/particle-system.md](references/particle-system.md) |
| VFX Graph contexts, events, C# API | [references/vfx-graph.md](references/vfx-graph.md) |

## Pipeline choice

- New project: URP, unless it needs ray tracing, volumetric clouds or a physical sky (HDRP).
  URP covers mobile, WebGL and consoles.
- Built-in to URP: use Window > Rendering > Render Pipeline Converter for built-in materials.
  Custom Built-in shaders (`CGPROGRAM`, Surface Shaders, `UnityCG.cginc`) must be rewritten as
  Shader Graphs or URP HLSL. Post Processing Stack v2 profiles must be rebuilt as URP Volume
  profiles. Commit before converting and convert one scene first.

## Materials and shaders

- Per-object variation: `MaterialPropertyBlock` or `renderer.material` (an instance you must
  destroy). Writing `sharedMaterial` changes the asset for every object.
- Never create materials every frame. Never call `Shader.Find` at runtime; reference shaders
  from assets so they ship.
- URP HLSL: `HLSLPROGRAM`, the URP `Core.hlsl` include, `TEXTURE2D`/`SAMPLER` macros, and every
  material property inside `CBUFFER_START(UnityPerMaterial)` so the SRP Batcher works.
- Shader Graph Custom Function node: a file-mode function is named `Name_float` (and
  `Name_half` for half precision), takes inputs then `out` parameters, and lives in an `.hlsl`
  file in the project. Guard includes with `#ifndef` so the graph can include it twice.
- Keep shader keywords few; every keyword multiplies variants and build time.

## URP renderer features (Render Graph)

Unity 6 URP records passes through Render Graph. Override `RecordRenderGraph`; the old
`Execute`/`Configure` methods only run in Compatibility Mode, which is deprecated.

```csharp
using UnityEngine;
using UnityEngine.Rendering;
using UnityEngine.Rendering.RenderGraphModule;
using UnityEngine.Rendering.RenderGraphModule.Util;
using UnityEngine.Rendering.Universal;

public class TintFeature : ScriptableRendererFeature
{
    [SerializeField] private Material material;
    private TintPass pass;

    public override void Create()
    {
        pass = new TintPass { renderPassEvent = RenderPassEvent.BeforeRenderingPostProcessing };
    }

    public override void AddRenderPasses(ScriptableRenderer renderer, ref RenderingData renderingData)
    {
        if (material == null) return;   // feature added but not configured yet
        pass.Setup(material);
        renderer.EnqueuePass(pass);
    }
}

class TintPass : ScriptableRenderPass
{
    private Material material;

    public void Setup(Material tintMaterial)
    {
        material = tintMaterial;
        requiresIntermediateTexture = true;
    }

    public override void RecordRenderGraph(RenderGraph renderGraph, ContextContainer frameData)
    {
        var resources = frameData.Get<UniversalResourceData>();
        if (resources.isActiveTargetBackBuffer) return;   // cannot read the back buffer

        TextureHandle source = resources.activeColorTexture;
        TextureDesc desc = renderGraph.GetTextureDesc(source);
        desc.name = "_TintColor";
        desc.clearBuffer = false;
        TextureHandle destination = renderGraph.CreateTexture(desc);

        renderGraph.AddBlitPass(new RenderGraphUtils.BlitMaterialParameters(source, destination, material, 0), "Tint");
        resources.cameraColor = destination;
    }
}
```

Review checklist for a renderer feature:
- Every texture the pass reads or writes is declared on the builder (`UseTexture`,
  `SetRenderAttachment`) or goes through a helper such as `AddBlitPass`.
- No `RTHandle` allocation per frame; create textures through `renderGraph.CreateTexture`.
- Materials are created once and destroyed in the feature's `Dispose`.
- Check the Render Graph Viewer (Window > Analysis > Render Graph Viewer) for culled passes and
  resource lifetimes.

## Post-processing (URP)

When effects do not show, check in order:

1. The camera's Post Processing checkbox is on.
2. A Volume exists: Global, or Local with a collider the camera is inside, and its weight is
   above 0.
3. The Volume has a profile, and each override in it is ticked and active.
4. The camera's Volume Mask includes the Volume's layer.
5. Tonemapping and bloom need HDR on in the URP asset; bloom needs pixels above its threshold.

Change values at runtime through `volume.profile.TryGet<Bloom>(out var bloom)` and
`bloom.intensity.Override(v)`. `volume.profile` instantiates a copy; `sharedProfile` edits the
asset.

## Lighting

- Baked and Mixed lights need Baked Global Illumination on, or they act as Realtime.
- Static scenery: Baked or Mixed lights, Contribute GI on the meshes, lightmap UVs (generate on
  import or bring from Blender). Moving objects: Light Probes or Adaptive Probe Volumes.
- Area lights are bake only.
- Overlapping reflection probes need distinct Importance values or they flicker.
- Shadow acne means bias too low; detached shadows mean bias too high.
- Keep few realtime lights, especially on mobile and with Forward rendering.

## VFX

| Need | Use |
|---|---|
| Mobile, Built-in, gameplay collisions, CPU scripting | Particle System |
| Tens of thousands of particles or more, URP or HDRP, GPU simulation | VFX Graph |

- Particle System: cache module structs, use Local space for effects attached to moving
  objects, pool and stop effects you no longer need.
- VFX Graph: set Capacity and Bounds in Initialize, and throttle `SendEvent` calls.

## Verify

- Read state back: pipeline asset name, active Volume overrides, light modes, through the
  official `unity-cli` skill's `script eval` or an editor script.
- For visuals, capture a frame in a development build or the Game view, not the Scene view,
  and say which one you looked at.

## Related skills

- `unity-2d`: 2D Renderer, 2D lights, pixel perfect.
- `unity-build-perf`: GPU profiling, shader variant stripping, build size.
- `blender-to-unity`: PBR textures and lightmap UVs from Blender.
