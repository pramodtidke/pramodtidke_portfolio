# pramodtidke.in: version 4 (grouped navigation, self-hosted fonts, fixes)

The site is now **built** from your content on every push (and every 6 hours, which also publishes scheduled posts).
`build.py` turns `content/*.json` and `content/blog/*.md` into real pages: /about/, /writing/, /writing/<post>/, /projects/<project>/, /games/ and more.

## Upgrading the existing repo (important)
1. Upload everything from this zip to branch `main`, **except** your existing `content/*.json` files. Those hold edits you made in the dashboard. Only add the new `content/blog/` folder and `content/testimonials.json`.
2. Delete the old root `index.html` and `sitemap.xml` from the repo. They are now generated.
3. Settings > Pages > Source must be **GitHub Actions**. Check the Actions tab for a green tick.
4. If `build.py` fails on a broken internal link, the log names the page and link.

## Dashboard
- **Blog posts**: new collection. Markdown body, cover, tags, draft, and a date. A future date schedules the post.
- **Pages and text > Site settings**: hero status, headshot, rotating words, optional analytics domain (Plausible).
- **Projects**: new fields (role, screenshot, what I did) feed the case-study pages.
- **Testimonials**: leave empty unless you have real ones. The section only appears when there is at least one.
- Optional: add `publish_mode: editorial_workflow` under `backend:` in `admin/config.yml` for a review step.

## Notes
- Contact form uses formsubmit.co. The first message triggers a one-time activation email to the address on the form.
- Entries marked `sample` are hidden from search engines and the sitemap.
- Fonts still load from Google Fonts. Self-hosting them is a later improvement.

## What changed in version 4
- **Navigation**: 5 top-level items (About, Write & Watch, Projects, Explore, Connect) with sub-menus. Theme and Calm mode live in the gear menu. Search is an icon (⌘K still works). The old nav was oversized because the Connect page's `.links` CSS class also matched the nav; that class is now `.plinks`.
- **Mobile menu**: grouped with headings, scrolls if the screen is short, closes on outside tap, Esc or link tap, highlights the current page.
- **Fonts** are self-hosted in `assets/fonts/` (SIL Open Font License files included), so no request goes to Google.
- **GitHub list** on the home page is fetched during the build (`scripts/import_feeds.py` writes `content/github-repos.json`), not in visitors' browsers, so it no longer hits GitHub's rate limit.
- **SEO**: longer meta descriptions, BreadcrumbList data, BlogPosting image/publisher, external articles point their canonical tag at the original, and the RSS feed now includes them too.
- **Security**: Content-Security-Policy meta tag, email address entity-encoded in the HTML, CMS script pinned to a version with an integrity hash (update both together when upgrading Sveltia CMS).
- **Service worker** is versioned per build, caches only same-origin successful responses, and keeps at most 60 entries per cache.
- Added `manifest.webmanifest`, app icons, a restyled 404 page, and a darker light-mode accent colour (#C93514) so text meets WCAG AA contrast.
- `tests/browser_test.py` is the Playwright smoke test used for this release (optional, not part of the deploy).

## Upgrading from version 3
Upload everything except your `content/*.json` files (keep the ones you edited in the dashboard). New files to add: `assets/fonts/`, `assets/*.png`, `manifest.webmanifest`, `tests/`.
