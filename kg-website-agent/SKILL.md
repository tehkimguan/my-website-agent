---
name: kg-website-agent
description: >
  Universal website agent: clone a site's design, migrate a WordPress site to a
  free Astro + Cloudflare stack, and run it day to day in plain English.

  Make sure to use this skill WHENEVER the user wants to move off or migrate
  WordPress, clone or rebuild a website's design, scaffold or deploy an Astro site,
  deploy to Cloudflare Pages or Workers, point a domain at Cloudflare (nameservers,
  MX records, propagation), add a contact form to a static site, publish or roll
  back an MDX blog post, or generate a cover, hero, or OG image for a site page.
  Trigger even when the user names no tool and only describes the problem, such as
  "my WordPress site keeps getting hacked", "my hosting is too expensive", or "how
  do I make my site load faster".

  Runs a six-phase migration (capture, scaffold, import, assemble, deploy, go-live)
  using the bundled wppull CLI for WordPress content, built-in computer-use for
  design capture, and the Gemini image API for images. By tehkimguan.com, free and
  open source.
---

# kg-website-agent

Clone, migrate, and run any website on a free Astro + Cloudflare stack, in plain English.

This is the AI-native replacement for WordPress: no server, no database, no plugins,
no login page to attack. The site is a folder of files. You describe a change, the
agent edits the files, GitHub saves them, and Cloudflare publishes within two minutes.

---

## When to Activate

- User wants to migrate or move a site off WordPress
- "Clone this site's design", "rebuild this site", "capture the old look"
- Scaffold an Astro (or Next.js) project for Cloudflare
- Import WordPress posts and pages into a content collection
- Deploy to Cloudflare Pages or Workers; point a domain at Cloudflare
- Add a contact form to a static site (Web3Forms / Formspree / Worker + Resend)
- Publish, edit, or roll back content on an Astro/MDX site
- Generate a cover, hero, inline, or social (OG) image for a page
- Turn a repeated website task into a reusable skill

## Do Not Activate

- Pure WordPress plugin or theme development (staying on WordPress)
- Server administration unrelated to static hosting
- Paid CMS migrations where the destination is another hosted CMS
- E-commerce platform selection advice

---

## The Stack

| Tool | Role | Cost |
|------|------|------|
| Astro | Compiles the site to static HTML at build time | Free |
| Cloudflare Pages / Workers | Serves the files from 300+ cities, free SSL | Free |
| GitHub | Version control + the undo button | Free |
| Claude Code Desktop | The editor you talk to in plain English | USD 20/mo (Pro) |
| `wppull` CLI | Pulls WordPress content out through the REST API | Free (this repo) |
| Gemini image API | Generates cover / hero / OG images | ~RM 0.18 per image |

Only one paid piece (Claude Code), and one subscription covers every site the team runs.

---

## CLI Setup Check

```bash
wppull --version          # confirm the content extractor is installed
node -v && npm -v         # Astro needs Node LTS
gh auth status            # GitHub CLI logged in
npx wrangler whoami       # Cloudflare CLI logged in
```

If `wppull` is missing: `pip install -e wppull/` from this repo, or run `./setup`.

---

## The Six-Phase Migration (router)

Read the matching reference before executing each phase.

| Phase | Goal | Reference |
|-------|------|-----------|
| A. Capture | Photograph and spec the old design | `references/capture.md` |
| B. Scaffold | Create the Astro project for Cloudflare | `references/astro-cloudflare.md` |
| C. Content | Pull WordPress posts/pages to Markdown | `references/wordpress.md` |
| D. Assemble | Fit captured design to imported content | `references/astro-cloudflare.md` |
| E. Deploy | Push to GitHub, connect Cloudflare | `references/astro-cloudflare.md` |
| F. Go live | Point the domain, MX check, sitemap | `references/go-live.md` |

Image generation: `references/images.md`. Daily operations and reusable skills:
`references/reusable-skills.md`.

### Phase A — Capture the old design

Do NOT depend on any third-party scraping template. Use the AI's built-in
computer-use / browser capability directly (every modern AI coding assistant has
it). Open the live site, screenshot each section at desktop and mobile widths,
read the exact colours and fonts from the DOM, and write a component spec
(header, hero, cards, footer) plus a token sheet to `capture/`. Download the
logo and key images into `public/images/`. See `references/capture.md`.

Only capture sites the user owns or is authorised to rebuild.

### Phase B — Scaffold

```bash
npm create astro@latest my-site      # choose minimal/empty, TypeScript yes
cd my-site
npx astro add cloudflare tailwind sitemap mdx
```

Define a `blog` content collection (title, description, publishedAt, tags, draft).
See `references/astro-cloudflare.md`.

### Phase C — Import content with wppull

```bash
wppull --json pull yourdomain.com --out src/content/blog --type both
```

This writes one Markdown file per post and page (frontmatter + the original
rendered HTML body) and a `media-manifest.json` of every referenced image. Then:

1. Convert each HTML body to clean Markdown (the agent's job, not the CLI's).
2. Download the manifest images into `public/images/` and fix the links
   (`wppull media yourdomain.com --download public/images`).
3. Generate a `_redirects` file mapping old WordPress URLs to new paths so Google
   rankings carry over. See `references/wordpress.md`.

### Phase D — Assemble

Fit the captured design (Phase A) to the imported content (Phase C), one piece at
a time: layout, then blog index, then single-post page. Preview with `npm run dev`
on `http://localhost:4321`. Work in small, checkable steps.

### Phase E — Deploy

```bash
git init && git add . && git commit -m "Initial migrated site"
gh repo create my-site --private --source=. --remote=origin --push
```

`.env` is excluded by `.gitignore` automatically. Then connect the repo in
Cloudflare (Pages for a normal site, Workers when a form/API is needed). Every
push rebuilds and republishes. See `references/astro-cloudflare.md`.

### Phase F — Go live

Add the custom domain, **check MX records before the nameserver cutover** (missing
MX = silent email loss), submit the sitemap to Google Search Console, enable free
Web Analytics, keep WordPress switched off (not deleted) for two weeks.
See `references/go-live.md`.

---

## Core Rules (Always Apply)

1. `--json` on every `wppull` command for structured output.
2. Capture only sites the user owns or is authorised to rebuild.
3. Read before write — preview locally (`npm run dev`) before any push.
4. Never commit a secret. `.env` stays git-ignored; production keys go to
   Cloudflare secrets (`npx wrangler secret put NAME`).
5. On Cloudflare Workers, a form route reads its secret from
   `locals.runtime.env.NAME`, never build-time `import.meta.env`.
6. Preserve old URLs with a `_redirects` file before go-live, not after.
7. Check MX records during the Cloudflare DNS import, before cutover.
8. Small, checkable steps when assembling — never "build the whole site" in one go.

---

## Reference Files

- `references/capture.md` — design capture via built-in computer-use
- `references/wordpress.md` — wppull, REST import, redirects, media
- `references/astro-cloudflare.md` — scaffold, content collection, Pages vs Workers, deploy
- `references/images.md` — Gemini image API (cover/hero/inline/OG), no external MCP
- `references/go-live.md` — domain cutover, MX check, propagation, Search Console
- `references/reusable-skills.md` — daily operations + turning tasks into skills
- `examples/` — copy-paste walkthroughs (capture, migrate, deploy)

## Browser / Computer-Use Fallback

Every AI coding assistant (Claude Code, Gemini Code Assist, Copilot / Codex)
includes computer-use. The agent uses it directly for design capture (Phase A)
and for any portal step with no API (registrar nameserver change, Search Console
verification). The CLI-first path is preferred where an API exists.
