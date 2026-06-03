# Recycling Website Competitive & Best-Practice Report
## RecycleBin.com — Pre-5am Improvement Plan
## Date: 2026-06-03

## 1. What Top Recycling Sites Offer That We Don’t (Yet)

| Capability | recyclecoach / earth911 / EPA / WM | RecycleBin Today | Gap |
|---|---|---|---|
| **Item-level lookup ("Can I recycle this?")** | Image search + barcode + text | None | ❌ High impact |
| **Hyper-localized rules by ZIP/city** | Real-time program rules | Generic guides only | ❌ High impact |
| **Printable posters & bin labels** | Downloadable PDFs | None | ❌ Easy win |
| **Search bar** | Site-wide search | None | ❌ Easy win |
| **Recycling 101 / Getting-started flow** | Dedicated onboarding | Scattered | ⚠️ Medium |
| **Myth-busting / contamination education** | Explicit dedicated sections | None | ⚠️ Medium |
| **K-12 lesson plans** | Teacher-ready packs | None | ⚠️ Medium |
| **Interactive quiz / self-check** | 2-min quiz + instant feedback | None | ⚠️ High engagement |
| **Impact calculator** | "Your recycling = X trees" | Static stats only | ⚠️ Medium |
| **Email/newsletter signup** | Recurring engagement | None | ⚠️ Medium |
| **Events by proximity** | Distance-sorted after geolocation | Sorted, but not true geo | ⚠️ Smaller gap |
| **QR/share flows** | "Share this item" | None | Low priority |
| **Accessibility / WCAG** | Basic a11y | Unknown / not audited | ❌ Legal + UX |
| **SEO basics (sitemap, OG, hreflang)** | Standard | Missing | ❌ Search visibility |

## 2. Recommended Priority Actions (Before 5am)

### Tier 1 — High value, low complexity
1. **"What goes where?" quick-lookup tool**  
   - Start with a curated lookup table of 60–100 common household items mapped to material type + do/don’t.  
   - Wire it to the existing state-filter pattern.  
   - Files to touch: `guides.html`, new `guides/lookup.html`, `js/site.js`.

2. **Site search**  
   - Client-side search index over titles + descriptions across all pages (index by build, query by JS).  
   - Files to touch: `js/site.js`, `index.html`, result panel.

3. **Printable guide PDFs**  
   - Generate 2–3 one-page PDFs: "Kitchen recycling cheat sheet", "Bin vs landfill", "E-waste drop-off list".  
   - Use Python (`reportlab` or `weasyprint`) to generate during build and commit to `/assets/pdf/`.

4. **SEO metadata + Open Graph**  
   - Add per-page `<meta name="description">`, `og:title`, `og:description`, `og:image`.  
   - Add `sitemap.xml` and `robots.txt`.

### Tier 2 — High engagement
5. **2-minute "Can I recycle this?" quiz**  
   - 8–10 scenario questions with instant score + tailored result.  
   - Can be a single-page app: `quiz.html`.

6. **Impact calculator (mini)**  
   - Input: households / tons recycled; Output: trees + water + CO₂ saved.  
   - Could be embedded in `index.html` or `impact.html`.

### Tier 3 — Ongoing quality
7. **Myth-busting section**  
   - 6–8 myth cards with short "truth" statements; reuse existing card component.

8. **Accessibility pass**  
   - Color contrast audit, skip-to-content link, focus styles, ARIA landmarks.  
   - This is table stakes for public-sector–adjacent content.

9. **Analytics + privacy-first metrics**  
   - Plausible or self-hosted; track page views and top lookup queries.

## 3. Concrete First-Implementation Plan (Tier 1)

### 3.1 Add `lookup.html`
- Pattern: search box + result cards
- Data source: `js/reference.json` (item → material + do/don't + local note)
- Use existing `js/site.js` helpers (`initLayout`, `initI18n`, `setLanguage`)

### 3.2 Add search
- `js/index.json` = `[{url, title, desc, section}]`
- Search input in shared header (desktop + mobile)
- Results dropdown under input

### 3.3 Add SEO skeleton
- `sitemap.xml` (can be manually maintained for static site)
- `robots.txt`
- Per-page meta tags in all HTML templates

## 4. Risk & constraints
- Static site only; no backend until backend folder is fully implemented.
- Keep JS under 50 KB total for fast load.
- Avoid new external runtime dependencies if possible.
- Don’t block 5am delivery — Tier 1 is the realistic scope for tonight.

## 5. Recommendation
Do **Tier 1 only** before 5am. It makes the site feel like a real product: usable search, a signature lookup tool, and real SEO hygiene. Tier 2 and 3 become next-session work.

---
Proposed by: assistant
Next review: after 5am build
