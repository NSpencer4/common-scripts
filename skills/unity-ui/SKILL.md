---
name: unity-ui
description: >-
  Builds and fixes Unity 6 game UI: choosing UI Toolkit or uGUI, UXML, USS and data binding,
  Canvas layout, screen flow and HUD architecture, list views, UI feedback and transitions,
  TextMeshPro fonts, fallbacks and memory, and the Localization package with string tables and
  CJK fonts. Use for menus, HUDs, inventories, text that renders as boxes or blurry, or adding
  languages. Not for editor tooling beyond inspectors (use unity-csharp), input bindings
  (unity-gameplay), or 2D sprites (unity-2d).
license: MIT
compatibility: Unity 6.0 or newer, written against 6.3 LTS. TextMeshPro ships inside com.unity.ugui 2.x. Localization is com.unity.localization.
---

# Unity UI

Match the UI system the project already uses. Check for `UIDocument` components and `.uxml`
files (UI Toolkit) or `Canvas` components (uGUI) before writing anything. If the official
`create-ui` skill is installed, it can build UI in a connected Editor; this skill covers the
design rules and code.

## References

| Task | Read |
|---|---|
| UI Toolkit vs uGUI vs IMGUI, setup, layout, anti-patterns | [references/ui-overview.md](references/ui-overview.md) |
| UI Toolkit elements, UQuery, USS, events, manipulators, performance | [references/ui-toolkit.md](references/ui-toolkit.md) |
| SerializedObject and runtime binding | [references/ui-data-binding.md](references/ui-data-binding.md) |
| Canvas, RectTransform, layout groups, EventSystem | [references/ugui.md](references/ugui.md) |
| Screen stack, view/view-model, HUD, feedback, list views, transitions | [references/ui-patterns.md](references/ui-patterns.md), [references/ui-scaffolds.md](references/ui-scaffolds.md) |
| TextMeshPro API, rich text, font assets | [references/textmeshpro.md](references/textmeshpro.md) |

## Choosing a system

- New runtime UI and editor windows: UI Toolkit.
- Existing uGUI project: stay on uGUI and migrate a screen at a time only if asked.
- IMGUI only for quick editor debug overlays.
- uGUI is still needed for some world-space and VR cases; check the target before choosing.

## UI Toolkit rules

- Shared styles in USS files, not inline styles. Class names over deep selectors; avoid `*`.
- Put `transition-property` and `transition-duration` on the base state, not on the class you
  toggle, and list every animated property.
- One `UIDocument` per layer (screens, HUD, popups); `sortingOrder` decides which draws on top.
- `ListView`: call `RefreshItems()` after data changes; `Rebuild()` only when the template
  changes.
- Register callbacks in `OnEnable`, unregister in `OnDisable`.
- For gameplay UI, push values with C# events or explicit setters. The built-in binding system
  suits editor tooling better than fast-changing HUD values.

## uGUI rules

- Exactly one `EventSystem` per scene, with the Input System UI module when the project uses
  the Input System.
- Split static and frequently changing elements into separate Canvases; any change rebuilds its
  whole Canvas.
- Turn off Raycast Target on images and text that are not interactive.
- Avoid nested layout groups on elements that change every frame.

## Screen flow

- Screens on a stack (push, pop, replace) with guards against pushing during a transition and
  popping the last screen. Scaffold in `references/ui-scaffolds.md`.
- Views render; a view model or presenter holds state and talks to game systems. Views never
  reach into gameplay objects directly.
- Pause gameplay input while a menu is open by switching action maps (see `unity-gameplay`).

## TextMeshPro

- Use `TextMeshProUGUI` on Canvases and `TextMeshPro` for world text. Never legacy `UI.Text`.
- Update numbers with `SetText("Score: {0}", score)` to avoid string allocations.
- Font assets: static atlases for fixed character sets (UI labels), dynamic atlases for user
  text and large languages. Keep the main atlas small (for example 1024) and add fallback font
  assets rather than one huge atlas.
- Boxes instead of characters mean the glyph is in no font in the fallback chain. Add a
  fallback font asset for that script (CJK, Arabic, Cyrillic) to the font asset's fallback list
  or the global fallback list in TMP Settings.
- Clear dynamic font data before committing or building so atlases filled in Play mode do not
  bloat the build.
- Blurry text: raise Sampling Point Size or atlas padding, and check Canvas scale. Text that
  must change outline or color per instance needs Material Presets, not edited font materials.

## Localization (com.unity.localization)

1. Create Localization Settings (Project Settings > Localization), add Locales, and set the
   project locale and the startup selectors.
2. Put UI strings in a String Table Collection; keys are stable identifiers such as
   `menu.play`, never the English text.
3. Bind text with a `LocalizeStringEvent` on the TMP object, or a `LocalizedString` field in
   code (`localizedString.StringChanged += text => label.SetText(text)`). Use Smart Strings for
   plurals and variables.
4. Localize sprites, audio and fonts through Asset Table Collections, and swap TMP font assets
   or fallbacks per locale for CJK.
5. Switch at runtime with `LocalizationSettings.SelectedLocale`, after
   `LocalizationSettings.InitializationOperation` completes.
6. Verify each locale by switching in Play mode and looking for missing-entry markers and boxes.

## Related skills

- `unity-csharp`: architecture, events, async loading.
- `unity-gameplay`: input actions and map switching for menus.
- `unity-build-perf`: Canvas rebuild and UI profiling.
