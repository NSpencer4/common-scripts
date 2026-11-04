# HTML Report Format (offline)

The architectural review is a single self-contained HTML file in the OS temp
directory. **Do not load Tailwind, Mermaid, or any other CDN or remote asset.**
All CSS and diagrams must be inline so the file works with no network.

Use inline SVG, HTML structure, and a small `<style>` block for visuals. Prefer
hand-built boxes-and-arrows and simple SVG flow diagrams over graph libraries.

## Scaffold

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>Architecture review for {{repo name}}</title>
    <style>
      :root {
        --bg: #f5f5f4;
        --ink: #0f172a;
        --muted: #475569;
        --card: #ffffff;
        --border: #e2e8f0;
        --strong: #059669;
        --explore: #d97706;
        --speculative: #64748b;
        --leak: #dc2626;
        --deep: #0f172a;
      }
      * { box-sizing: border-box; }
      body {
        margin: 0;
        font-family: ui-sans-serif, system-ui, sans-serif;
        background: var(--bg);
        color: var(--ink);
        line-height: 1.45;
      }
      main { max-width: 56rem; margin: 0 auto; padding: 2.5rem 1.5rem; }
      h1 { font-size: 1.75rem; margin: 0 0 0.25rem; }
      .meta { color: var(--muted); margin-bottom: 2rem; }
      .legend { display: flex; flex-wrap: wrap; gap: 1rem; font-size: 0.875rem; color: var(--muted); margin-bottom: 2rem; }
      .legend span { display: inline-flex; align-items: center; gap: 0.4rem; }
      .swatch { width: 0.9rem; height: 0.9rem; border: 1px solid var(--border); display: inline-block; }
      .swatch.deep { background: var(--deep); }
      .swatch.leak { background: var(--leak); }
      .swatch.seam { border-style: dashed; }
      article {
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 0.75rem;
        padding: 1.25rem 1.5rem;
        margin: 0 0 1.5rem;
      }
      .badges { display: flex; flex-wrap: wrap; gap: 0.5rem; margin: 0.5rem 0 1rem; }
      .badge {
        font-size: 0.75rem;
        font-weight: 600;
        padding: 0.2rem 0.55rem;
        border-radius: 999px;
        color: #fff;
      }
      .badge.strong { background: var(--strong); }
      .badge.explore { background: var(--explore); }
      .badge.speculative { background: var(--speculative); }
      .badge.tag { background: #334155; }
      .files { font-family: ui-monospace, monospace; font-size: 0.8125rem; color: var(--muted); }
      .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin: 1rem 0; }
      @media (max-width: 720px) { .grid { grid-template-columns: 1fr; } }
      .panel {
        border: 1px solid var(--border);
        border-radius: 0.5rem;
        padding: 0.75rem;
        background: #fafafa;
        min-height: 10rem;
      }
      .panel h3 { margin: 0 0 0.75rem; font-size: 0.875rem; color: var(--muted); text-transform: uppercase; letter-spacing: 0.04em; }
      .wins { padding-left: 1.1rem; }
      .wins li { margin: 0.2rem 0; }
      .adr {
        margin-top: 0.75rem;
        padding: 0.6rem 0.75rem;
        background: #fffbeb;
        border: 1px solid #fcd34d;
        border-radius: 0.5rem;
        font-size: 0.875rem;
      }
      .module {
        border: 2px solid var(--ink);
        border-radius: 0.4rem;
        padding: 0.5rem 0.65rem;
        margin: 0.35rem 0;
        background: #fff;
        font-size: 0.875rem;
      }
      .module.deep {
        background: var(--deep);
        color: #fff;
        border-width: 3px;
      }
      .module.shallow { border-style: solid; opacity: 0.85; }
      .arrow { color: var(--muted); font-size: 0.8rem; margin: 0.15rem 0 0.15rem 0.5rem; }
      .arrow.leak { color: var(--leak); font-weight: 600; }
      svg.flow { width: 100%; height: auto; display: block; }
    </style>
  </head>
  <body>
    <main>
      <header>
        <h1>Architecture review — {{repo name}}</h1>
        <p class="meta">{{date}}</p>
        <div class="legend">
          <span><i class="swatch deep"></i> deep module</span>
          <span><i class="swatch seam"></i> seam</span>
          <span><i class="swatch leak"></i> leakage</span>
        </div>
      </header>
      <section id="candidates">...</section>
      <section id="top-recommendation">...</section>
    </main>
  </body>
</html>
```

## Header

Repo name, date, and the compact legend above. No introduction paragraph. Straight into candidates.

## Candidate card

Use `/codebase-design` vocabulary exactly (module, interface, depth, seam, adapter, leverage, locality).

Each candidate is one `<article>`:

- **Title**: short deepening name
- **Badge row**: `Strong` / `Worth exploring` / `Speculative`, plus dependency-category tag
- **Files**: monospaced list
- **Before / After**: two-column `.grid` with hand-built modules or inline SVG
- **Problem** / **Solution**: one sentence each
- **Wins**: short bullets
- **ADR callout** when needed

## Diagram patterns (offline only)

### Nested module boxes

```html
<div class="panel">
  <h3>Before</h3>
  <div class="module shallow">OrderHandler</div>
  <div class="arrow">→</div>
  <div class="module shallow">OrderValidator</div>
  <div class="arrow leak">leak → PricingClient</div>
</div>
```

### Inline SVG flow

Use a small SVG with rectangles and paths. Colour leakage edges `#dc2626`. Colour the deepened module fill `#0f172a` with white text. Keep labels short.

### Mass / depth diagram

One thick `.module.deep` containing greyed internal parts vs many shallow siblings. Prefer this for "collapse into one deep module" candidates.

## Top recommendation

End with which candidate to tackle first and why, still in glossary vocabulary.

## Writing location

Resolve temp dir from `$TMPDIR`, else `/tmp` (or `%TEMP%` on Windows). Write
`<tmpdir>/architecture-review-<timestamp>.html`. Open with `xdg-open` / `open` /
`start` and tell the user the absolute path. Never commit the report into the repo.
