# SEO implementation notes (from web-quality-skills/seo)

Evidence-led workflow and fix patterns to use alongside the main audit skill. Prefer measured signals over guessed ranking weights. Do not promise ranking changes.

## Evidence-led workflow

When a rendered page is available:

1. Run live Lighthouse SEO (and Agentic Browsing if relevant). With Chrome DevTools MCP, use `lighthouse_audit` when available.
2. Inspect what Lighthouse misses: response headers, redirects, `robots.txt`, sitemap coverage, canonical consistency, structured-data eligibility, and Search Console evidence when provided.
3. Separate crawl/index findings from content quality and authority.
4. Fix the source and re-run the same checks. For indexation or ranking outcomes, report that search-engine validation remains pending.

If live tools are unavailable, use category-specific Lighthouse CLI output plus direct source and HTTP inspection. A Lighthouse SEO score is not a ranking forecast.

## Implementation snippets

### robots.txt (example)

```text
User-agent: *
Allow: /
Disallow: /admin/
Disallow: /api/
Disallow: /private/
Sitemap: https://example.com/sitemap.xml
```

Do not block static assets required for rendering.

### Meta robots

```html
<meta name="robots" content="index, follow">
<meta name="robots" content="noindex, follow">
<meta name="robots" content="max-snippet:150, max-image-preview:large">
```

### Canonical

```html
<link rel="canonical" href="https://example.com/page">
```

Self-referencing canonicals are preferred on indexable templates. Paginated series need an explicit canonical strategy.

### XML sitemap habits

- Max 50,000 URLs or 50MB per sitemap; use a sitemap index when larger
- Only canonical, indexable URLs
- Update `lastmod` when content changes
- Submit in Search Console

## Structured data

See [STRUCTURED-DATA.md](STRUCTURED-DATA.md) for Organization, Article, Product, FAQ, and Breadcrumb examples.

- Describe visible, accurate content only
- Prefer the most specific applicable type
- Validate rendered output; syntax pass ≠ rich-result eligibility

Schema detection still requires a JS-capable check (browser tool, Rich Results Test, or Screaming Frog). `web_fetch`/`curl` alone are not enough.

## Agentic browsing vs AI citation

Keep these separate:

- **Lighthouse Agentic Browsing** measures technical agent-facing signals (accessibility tree, optional `llms.txt`, WebMCP when present)
- **Search indexing/ranking** cannot be inferred from that score
- **AI citation** is product-specific; browsability does not prove citation

Prioritize semantic HTML, descriptive labels, crawlable content, and accurate metadata. Add WebMCP only when the app has useful actions and the user wants that integration.

### Crawler controls (product-specific)

Audit each user agent separately. Training bots (`GPTBot`, `ClaudeBot`) are not the same as search/user-fetch bots (`OAI-SearchBot`, `PerplexityBot`, `Claude-SearchBot` / `Claude-User`). `Google-Extended` does not control Google Search inclusion. Verify current names in vendor docs before recommending blocks.

### `llms.txt`

Optional and experimental. Do not treat as a ranking or citation factor. Add only when requested or a documented consumer exists.

## Fix checklist (critical → ongoing)

**Critical:** HTTPS; robots allows crawling; no accidental `noindex`; unique titles; clear heading hierarchy.

**High:** Meta descriptions; sitemap submitted; canonicals; mobile-responsive; Core Web Vitals evidence.

**Medium:** Structured data; internal linking; image alt; descriptive URLs; breadcrumbs; agentic browsing failures when agent access matters.

**Ongoing:** Search Console crawl errors; sitemap freshness; ranking monitors; broken links.

## Tools

| Tool | Use |
|------|-----|
| Google Search Console | Indexing and issues |
| PageSpeed Insights | CWV |
| Rich Results Test | Structured data (renders JS) |
| Lighthouse (DevTools MCP or CLI) | Rendered SEO / agentic checks |
| Screaming Frog | Crawl analysis |
