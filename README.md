# my-website-agent

**Universal website agent for moving off WordPress** — one skill, zero servers.

Clone an existing site's design, migrate it to a free **Astro + Cloudflare**
stack, and run it day to day in plain English. Designed for Claude Code, Google
Gemini Code Assist, and GitHub Copilot / OpenAI Codex.

**Free and open source.** By [Teh Kim Guan](https://tehkimguan.com) — product consultant, Malaysia.

---

## What This Does

Install this agent and ask your AI assistant things like:

> "Capture the design of mysite.com and rebuild it in Astro"
> "Migrate every post and page off my WordPress site"
> "Deploy this to Cloudflare and point my domain at it"
> "Write a new blog post from these notes and publish it"
> "Generate a 16:9 hero image for the home page in our brand style"
> "Add a contact form that emails submissions to us"
> "Turn 'publish a blog post' into a reusable skill"

Two components:

1. **`kg-website-agent`** — an AI skill covering the full six-phase migration
   (capture, scaffold, content, assemble, deploy, go live), daily operations,
   image generation, and reusable-skill creation, with references and examples.
2. **`wppull` CLI** — pulls a WordPress site's posts, pages, and media out
   through the REST API and writes them as Markdown files for an Astro content
   collection.

---

## Why This Exists

WordPress runs a program on a live server for every visit: PHP, a MySQL database,
and a stack of plugins. That is why it is slow, and why it gets hacked through an
outdated plugin or a brute-forced `/wp-admin` login.

A static site is the opposite. Astro builds every page into plain HTML ahead of
time. Cloudflare serves those files from 300+ cities for free. There is no
database, no login page, and no plugins on the public side, so there is almost
nothing to hack and nothing to slow it down. You edit it by talking to an AI
assistant on your own computer; GitHub saves every change; Cloudflare republishes
in about two minutes.

---

## The Stack

| Tool | Role | Cost |
|------|------|------|
| Astro | Compiles the site to static HTML at build time | Free |
| Cloudflare Pages / Workers | Serves files from 300+ cities, free SSL + CDN | Free |
| GitHub | Version control and the undo button | Free |
| Claude Code Desktop | The editor you talk to in plain English | USD 20/mo (Pro) |
| `wppull` | Pulls WordPress content out through the REST API | Free (this repo) |
| Gemini image API | Generates cover / hero / OG images | ~RM 0.18 per image |

One paid piece (Claude Code), and one subscription covers every site you run.

---

## Why Computer-Use Is Built In

All modern AI coding assistants — **Claude Code** (computer use), **GitHub Copilot
/ Codex** (browser), **Google Gemini Code Assist** (browser) — can drive a browser
on your behalf. This agent uses that directly for two things with no public API:

1. **Capturing the old design** (Phase A): the AI opens the live site, screenshots
   each section, and reads the real colours and fonts from the DOM. No third-party
   scraping template to install.
2. **Portal steps** with no API: the registrar nameserver change and Google Search
   Console DNS verification.

The CLI-first path (`wppull`, `wrangler`, `gh`) is preferred wherever an API
exists — faster, more reliable, fully auditable.

---

## Install

### Prerequisites

- Python 3.10+ (for the `wppull` CLI)
- Node.js LTS, Git, and the GitHub CLI (`gh`) — for Astro and deploys
- An AI assistant: Claude Code, Gemini Code Assist, or GitHub Copilot / Codex
- Free Cloudflare and GitHub accounts

### One-command install

```bash
git clone https://github.com/tehkimguan/my-website-agent
cd my-website-agent
./setup
```

The setup script:
1. Installs the `wppull` CLI via pip
2. Copies `kg-website-agent/` to `~/.claude/skills/` (Claude Code)
3. Prints next steps for Gemini and Codex

### Manual install

```bash
# wppull CLI
cd wppull && pip install -e .     # installs the 'wppull' command

# Claude Code — copy the skill
cp -r kg-website-agent ~/.claude/skills/

# Gemini Code Assist — copy GEMINI.md to your project root
cp GEMINI.md your-project/

# GitHub Copilot / Codex — copy AGENTS.md to your project root
cp AGENTS.md your-project/
```

---

## The Six-Phase Migration

| Phase | Goal |
|-------|------|
| A. Capture | Screenshot and spec the old design (built-in computer-use) |
| B. Scaffold | `npm create astro@latest` + Cloudflare, Tailwind, sitemap, MDX |
| C. Content | `wppull pull` posts and pages, then convert + redirect |
| D. Assemble | Fit the captured design to the imported content |
| E. Deploy | Push to GitHub, connect Cloudflare Pages or Workers |
| F. Go live | Point the domain, check MX records, submit the sitemap |

A first migration of a small site takes an afternoon. The second takes two hours.

---

## Usage Examples

```bash
# Pull all WordPress content into an Astro collection
wppull --json pull yourdomain.com --out src/content/blog --type both

# Pull only posts, stripped to plain text
wppull pull yourdomain.com --type posts --strip-html

# List or download every media file
wppull media yourdomain.com
wppull media yourdomain.com --download public/images

# Authenticated REST API (WordPress Application Password)
wppull --user admin --app-password "xxxx xxxx xxxx xxxx" pull yourdomain.com
```

---

## AI Platform Support

| Platform | File | Activation |
|----------|------|------------|
| Claude Code | `~/.claude/skills/kg-website-agent/SKILL.md` | Auto-triggers on website/migration tasks after install |
| Gemini Code Assist | `GEMINI.md` in project root | Copy to your project |
| GitHub Copilot / Codex | `AGENTS.md` in project root | Copy to your project |

---

## Repository Structure

```
my-website-agent/
├── README.md                    ← This file
├── CLAUDE.md                    ← Claude Code routing + agent instructions
├── AGENTS.md                    ← GitHub Copilot / OpenAI Codex instructions
├── GEMINI.md                    ← Google Gemini Code Assist instructions
├── setup                        ← One-command installer
│
├── kg-website-agent/            ← Universal AI agent skill
│   ├── SKILL.md                 ← Six-phase router, core rules, gotchas
│   ├── references/
│   │   ├── capture.md           ← Design capture via built-in computer-use
│   │   ├── wordpress.md         ← wppull, REST import, redirects, media
│   │   ├── astro-cloudflare.md  ← Scaffold, content collection, Pages vs Workers, deploy
│   │   ├── images.md            ← Gemini image API (cover/hero/OG), no external MCP
│   │   ├── go-live.md           ← Domain cutover, MX check, propagation, Search Console
│   │   └── reusable-skills.md   ← Daily operations + /skill-creator patterns
│   └── examples/
│       ├── capture-design.md
│       ├── migrate-wordpress.md
│       └── deploy-cloudflare.md
│
└── wppull/                      ← WordPress content extractor CLI (pip: wppull-agent)
    └── kg_cli/wppull/           ← Python package, namespace: kg_cli
```

---

## Malaysian Context

Written from real migrations of Malaysian sites:

- **Hosting reality:** RM 50 to 300/month WordPress hosting plus a security plugin
  plus developer call-out fees, versus ~RM 94/month total on this stack.
- **Registrars:** Exabytes, Shinjiru, WebNIC, MYNIC — the nameserver change is the
  same everywhere. `go-live.md` covers the Exabytes client-area and email-support
  paths.
- **Email safety:** the MX-record check before cutover is mandatory — a missing MX
  row silently kills inbound email to the domain.

---

## Roadmap

| Version | What |
|---------|------|
| v0.1 (current) | `wppull` CLI, universal skill, six-phase playbook, 3 examples |
| v0.2 | `wppull` unit tests; HTML-to-Markdown helper command |
| v0.3 | Next.js scaffold reference; redirects auto-generator command |
| v0.4 | Additional sources (Wix, Squarespace export) |

---

## Contributing

PRs welcome. If you find a WordPress quirk `wppull` misses, or a migration step
that needs covering, please open an issue. This is a free community tool; it gets
better because practitioners contribute back.

---

## Credits and Prior Art

Built by [Teh Kim Guan](https://tehkimguan.com) — product consultant, Malaysia.

- The stack in this repo runs [tehkimguan.com](https://tehkimguan.com),
  [businessdataguide.com](https://businessdataguide.com), and the 2,000+ page
  [ttkbuildingmaterials.com](https://ttkbuildingmaterials.com).
- The "capture an old site's design with an AI" pattern was popularised by
  several open-source website-cloner templates; this repo reimplements it with
  built-in computer-use rather than a separate scraper.
- Image generation uses Google's Gemini image model (nicknamed Nano Banana).

---

## License

MIT — free to use, modify, and distribute. See `LICENSE`.
