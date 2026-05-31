# Example: Migrate WordPress content into Astro

## Context

The new Astro project is scaffolded (Phase B). Now bring every WordPress post and
page across, with images and redirects.

## Steps

```bash
# 1. Pull posts + pages into the content collection
wppull --json pull yourdomain.com --out src/content/blog --type both
# → writes one <slug>.md per item + media-manifest.json

# 2. Download the referenced images
wppull media yourdomain.com --download public/images
```

## What you say to the agent next

> "The bodies in src/content/blog are still rendered WordPress HTML. Convert each
> to clean Markdown, remove plugin wrappers, and fix every image link to point at
> /images/. Then generate public/_redirects mapping each old WordPress URL to its
> new path with a 301."

## What the agent produces

```
src/content/blog/
├── about-us.md          # frontmatter + clean Markdown
├── solutions.md
├── hello-world.md
└── ...
public/
├── images/              # downloaded media, links rewritten
├── _redirects           # /services/ /solutions 301, ...
└── media-manifest.json
```

## Verify

```bash
npm run dev   # preview at http://localhost:4321, click through the imported pages
```

Old URLs should redirect; images should load locally; no WordPress markup left.
