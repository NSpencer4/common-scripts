# Snapshot provenance

Static skill (not installed via `npx skills`). Do not auto-update.

- Origin: https://github.com/Nice-Wolf-Studio/unity-claude-skills at a149d3e (MIT)
  - `unity-graphics` (now `references/graphics-overview.md`), `references/urp-guide.md` (now `urp.md`), `references/hdrp-guide.md` (now `hdrp.md`), `references/shader-graph.md`, `references/materials-textures.md`
  - `unity-lighting-vfx` (now `references/lighting-vfx-overview.md`), `references/lighting-guide.md` (now `lighting.md`), `references/particle-system.md`, `references/vfx-graph.md`
- Origin: https://github.com/JosiahSiegel/claude-plugin-marketplace `plugins/unity-master/skills/unity-shaders-rendering` at 5a1b112 (MIT), now `references/hlsl-shaders.md` without its renderer feature section (it used the pre-Render Graph `Execute` API) and without its links to reference files that are not in the source repo
- Snapshot date: 2026-11-25
- Changes: SKILL.md is a new merge of the sources above. The URP Render Graph renderer feature
  example, the post-processing checklist and the Built-in to URP notes are written here from
  Unity's URP 17 documentation and have not been compiled in a project. Reference files are the
  source skill bodies without frontmatter and "Related skills" sections, with cross-references
  renamed and em dashes replaced. Nothing was taken from Unity-Technologies/skills (Unity
  Companion License).
- Licenses and notices: `licenses/`.
