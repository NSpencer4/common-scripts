# Competitive teardown framework

Use this when the user wants internal competitive intelligence (SWOT, feature matrices, pricing teardown, review mining, positioning maps), not just public comparison pages. Prefer browser tools, official pages, and web search. Do not require third-party CLIs.

The Facts Over Opinions principle from the main skill still applies: date facts, separate observation from interpretation, and never mark an absence as confirmed without a primary source.

## 7-layer analysis

| Layer | What to analyze | Data source |
|-------|-----------------|-------------|
| 1. Product | Features, UX, quality | Product UI, docs, free trial |
| 2. Pricing | Plans, model, hidden costs | Pricing page, sales materials |
| 3. Positioning | Messaging, tagline, ICP | Website, ads |
| 4. Traction | Users, revenue, growth | Press, funding announcements, credible directories |
| 5. Reviews | Strengths and weaknesses from users | G2, Capterra, app stores, Reddit |
| 6. Content | Blog, social, SEO strategy | Site and social profiles |
| 7. Team | Size, key hires, background | About page, LinkedIn (public) |

Focus on the top 3–5 direct competitors. Date every research pass.

## Feature matrix

```markdown
| Feature | Your Product | Competitor A | Competitor B | Competitor C |
|---------|:---:|:---:|:---:|:---:|
| Real-time collaboration | Yes | Yes | No | Yes |
| API access | Yes | Paid only | Yes | No |
| SSO/SAML | Yes | Enterprise | Yes | Enterprise |
| Free tier | Yes (unlimited) | Yes (3 users) | No | Yes (1 project) |
```

Rules:
- Use Yes / Partial / No (or equivalent). Avoid emoji-only cells in shipped docs if the audience is formal.
- Note conditions: Paid only, Enterprise tier, Beta.
- Lead with features where you win; stay honest about competitor strengths.
- "Not listed" is not "does not have."

## Pricing comparison

Capture free tier, starter/pro/enterprise, billing cadence, annual discount, seat minimums, and hidden costs (setup fees, metered API, overages, lock-in).

## SWOT (per competitor)

| Strengths | Weaknesses |
|-----------|------------|
| … | … |

| Opportunities | Threats |
|---------------|---------|
| … | … |

End each SWOT with implications for your product, not just a list.

## Positioning map

Pick two meaningful axes (for example Simple↔Complex and SMB↔Enterprise). Avoid Good↔Bad or Cheap↔Expensive. Place you and each competitor, then write the "so what" for messaging and packaging.

## Review mining

| Platform | Best for |
|----------|----------|
| G2 | B2B SaaS |
| Capterra | Business software |
| App stores | Consumer / mobile |
| Product Hunt | Launch reaction |
| Reddit | Unfiltered switching stories |

Extract: most praised, most complained, switching triggers, feature requests, and comparison mentions.

## Deliverables

**Executive summary (1 page):** market size/growth if known, key competitors, your positioning, one key insight, and a compact metric table (users/pricing/ratings) with as-of dates.

**Detailed report (per competitor):** overview, product, pricing, SWOT, reviews, positioning vs you, opportunity summary.

## Common mistakes

| Mistake | Fix |
|---------|-----|
| Features only | Use all seven layers |
| Biased write-up | State competitor strengths plainly |
| Undated facts | Date research; refresh before publishing |
| Too many competitors | Cap at 3–5 direct |
| No implications | End sections with what it means for you |
