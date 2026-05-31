# Reference: Import WordPress content (Phase C)

WordPress exposes its content as clean data through the REST API. The `wppull`
CLI in this repo pulls it out and writes Markdown files; the agent then converts
and tidies them.

## The REST endpoints

Almost every WordPress site serves these (swap in the real domain):

```
https://yourdomain.com/wp-json/wp/v2/pages?per_page=100&page=1
https://yourdomain.com/wp-json/wp/v2/posts?per_page=100&page=1
https://yourdomain.com/wp-json/wp/v2/media?per_page=100&page=1
```

If the API is disabled, fall back to the WordPress export (Tools -> Export -> All
content), drop the XML into the project, and ask the agent to convert it.

## Pull with wppull

```bash
# posts + pages into an Astro content collection
wppull --json pull yourdomain.com --out src/content/blog --type both

# if the REST API needs auth, use an Application Password (Users -> Profile)
wppull --user admin --app-password "xxxx xxxx xxxx xxxx" pull yourdomain.com
```

`wppull pull` writes one `<slug>.md` per item with frontmatter (title,
description, publishedAt, tags, slug, draft) and the original rendered HTML as the
body. It also writes `media-manifest.json` listing every referenced image URL.

## After the pull — the agent's three jobs

1. **Convert HTML bodies to clean Markdown.** The CLI leaves the body as rendered
   HTML on purpose; semantic conversion (headings, lists, links, removing plugin
   wrappers) is the agent's job.
2. **Bring the images across.**
   ```bash
   wppull media yourdomain.com --download public/images
   ```
   Then fix the body image links to point at `/images/...`.
3. **Preserve old URLs** so Google rankings carry over. Create `public/_redirects`:
   ```
   # old path      new path       code
   /services/      /solutions     301
   /our-team/      /about         301
   /blog/*         /news/:splat   301
   ```
   Cloudflare reads this automatically. Build the full map from the imported
   slugs. Do this before go-live, not after.

## Gotchas

- WordPress returns at most 100 items per page; `wppull` paginates until the
  `X-WP-TotalPages` header (or a short final page) says it is done.
- Tags and categories come back as term IDs; `wppull` resolves them to names via
  `/tags` and `/categories`. If those endpoints are locked down, the raw IDs are
  written instead.
- `draft: false` is set on every imported file. Flip to `true` to hide a page.
