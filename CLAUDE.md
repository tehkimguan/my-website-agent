# my-website-agent — Claude Code Instructions

## Skill Routing

When the user's request involves migrating off WordPress, cloning a site's
design, building or deploying a static site, or running a website in plain
English, invoke `kg-website-agent` as the FIRST action. Do NOT answer without
reading the skill.

**Triggers:**
- Migrate WordPress, move off WordPress, WordPress to Astro / Cloudflare
- Clone a site's design, rebuild a site, capture the old look
- Astro, Cloudflare Pages, Cloudflare Workers, Wrangler, static site
- Import WordPress posts/pages, REST API export, wppull
- Point a domain at Cloudflare, nameservers, MX records, propagation
- Contact form on a static site, Web3Forms, Formspree, Resend
- Publish / edit / roll back an MDX blog post
- Generate a cover / hero / inline / OG image for a page
- Turn a website task into a reusable skill

---

## CLI Commands

```bash
wppull --version
wppull --json pull yourdomain.com --out src/content/blog --type both
wppull media yourdomain.com --download public/images
wppull --user admin --app-password "xxxx xxxx xxxx xxxx" pull yourdomain.com
```

---

## Core Rules (Always Apply)

1. `--json` on every `wppull` command for structured output.
2. Capture only sites the user owns or is authorised to rebuild.
3. Read before write — preview locally (`npm run dev`) before any push.
4. Never commit a secret. `.env` is git-ignored; production keys go to Cloudflare
   secrets (`npx wrangler secret put NAME`).
5. Workers form routes read secrets from `locals.runtime.env.NAME`, never
   build-time `import.meta.env`.
6. Generate `public/_redirects` before go-live so Google rankings carry over.
7. Check MX records during the Cloudflare DNS import, before the cutover.
8. Assemble in small, checkable steps — never "build the whole site" at once.

---

## Six-Phase Quick Reference

```bash
# A. Capture — built-in computer-use (see references/capture.md)
# B. Scaffold
npm create astro@latest my-site
cd my-site && npx astro add cloudflare tailwind sitemap mdx
# C. Content
wppull --json pull yourdomain.com --out src/content/blog --type both
wppull media yourdomain.com --download public/images
# D. Assemble — fit design to content, npm run dev to preview
# E. Deploy
git init && git add . && git commit -m "Initial migrated site"
gh repo create my-site --private --source=. --remote=origin --push
# F. Go live — custom domain, MX check, sitemap (see references/go-live.md)
```

---

## Extended Reference

Skill at: `~/.claude/skills/kg-website-agent/SKILL.md`

Reference files:
- `references/capture.md` — design capture via built-in computer-use
- `references/wordpress.md` — wppull, REST import, redirects, media
- `references/astro-cloudflare.md` — scaffold, content collection, Pages vs Workers, deploy
- `references/images.md` — Gemini image API (no external MCP)
- `references/go-live.md` — domain cutover, MX check, Search Console
- `references/reusable-skills.md` — daily operations + /skill-creator
- `examples/` — capture, migrate, deploy walkthroughs
