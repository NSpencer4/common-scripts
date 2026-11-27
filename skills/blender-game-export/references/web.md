# Web (three.js, Babylon.js, model-viewer, React Three Fiber)

GLB with compressed geometry and textures.

## Export

- `export_format="GLB"`, `export_apply=True`.
- Geometry compression: meshopt (`EXT_meshopt_compression`) or Draco (`export_draco_mesh_compression_enable=True`). Draco files are smaller for static meshes but decode slower and need `DRACOLoader`. A file that requires an extension its loader lacks will not load, so match the loader setup.
- Blender's meshopt support depends on a library bundled with official builds. On this machine's Blender 5.3 build (a distribution package) the exporter logged "MeshOptimizer is not available". Check the export log, or compress afterward with `gltf-transform` or `gltfpack`.
- Textures: WebP or KTX2. Blender 5.3 renamed the options: `export_image_add_compressed_images`, `export_compressed_images_type` (`WEBP` or `KTX2`), `export_compressed_images_fallback`.
- Outside Blender: `gltf-transform optimize in.glb out.glb --texture-compress ktx2`, or `gltfpack -cc -tc`.

## Budgets

Hero model 2 to 5 MB as GLB, whole scene 10 to 20 MB, textures 1K to 2K, 50 to 100 draw calls on mobile web.

## Loader side (three.js)

`GLTFLoader` with `MeshoptDecoder`, `DRACOLoader`, or `KTX2Loader` as the file requires. Set `renderer.outputColorSpace = SRGBColorSpace` and a tone mapping that matches how the asset was judged in Blender (Khronos PBR Neutral corresponds to `NeutralToneMapping`).

## Verify

Run the Khronos glTF Validator on the file, and view it in a glTF viewer (for example gltf-viewer.donmccurdy.com or model-viewer) in addition to the Blender re-import.
