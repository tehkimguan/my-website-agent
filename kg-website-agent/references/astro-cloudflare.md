# Reference: Scaffold, assemble, and deploy (Phases B, D, E)

## Phase B — Scaffold the Astro project

```bash
npm create astro@latest my-site      # minimal/empty starter, TypeScript: yes
cd my-site
npx astro add cloudflare      # run on Cloudflare
npx astro add tailwind        # styling
npx astro add sitemap mdx     # sitemap + MDX content
```

`astro.config.mjs` shape used in production:

```js
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import tailwindcss from '@tailwindcss/vite';
import cloudflare from '@astrojs/cloudflare';

export default defineConfig({
  site: 'https://my-site.com',
  output: 'static',                 // pre-build every page into HTML
  adapter: cloudflare(),
  trailingSlash: 'never',
  integrations: [ sitemap() ],
  vite: { plugins: [ tailwindcss() ] }
});
```

Content collection rule file (`src/content/config.ts`):

```ts
import { defineCollection, z } from 'astro:content';

const blog = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    publishedAt: z.coerce.date(),
    tags: z.array(z.string()).default([]),
    draft: z.boolean().default(false),
  }),
});

export const collections = { blog };
```

The frontmatter `wppull` writes matches this schema. A `draft: true` post never
publishes — the team's safety net.

If the site will become an application (logins, dashboards, live tools), scaffold
Next.js for Cloudflare instead. Everything from Phase C onward is identical.

## Phase D — Assemble

Fit the captured design to the imported content, one region at a time:

> "Using the header, footer, and colours from the capture/ specs, build the site
> layout in Astro. Then the blog index (newest first) and the single-post page.
> Match the old look. Keep it responsive on mobile."

Preview locally with `npm run dev` (usually `http://localhost:4321`). Build in
small, checkable steps — header, then list, then post — not all at once.

## Phase E — Deploy

```bash
git init
git add .
git commit -m "Initial migrated site"
gh repo create my-site --private --source=. --remote=origin --push
```

`.env` is excluded by the generated `.gitignore`. Confirm with the agent
("is any secret file about to be committed?") before pushing if unsure.

### Pages vs Workers

| | Cloudflare Pages | Cloudflare Workers |
|---|---|---|
| Best for | Normal site: pages, blog, brochure, directory | Site that also needs a form, search, or API |
| Setup | Connect the GitHub repo in the dashboard | `wrangler.jsonc` + `npx wrangler deploy` |
| Start here? | Yes | Move here when you need a form |

**Pages**: Workers and Pages -> Create -> Pages -> Connect to Git, pick the repo,
framework preset Astro, build `npm run build`, output `dist`, Save and Deploy.
Every push then rebuilds and republishes automatically.

**Workers** `wrangler.jsonc`:

```jsonc
{
  "name": "my-site",
  "main": "./dist/_worker.js/index.js",
  "compatibility_date": "2026-05-26",
  "compatibility_flags": ["nodejs_compat"],
  "assets": {
    "directory": "./dist",
    "binding": "ASSETS",
    "not_found_handling": "404-page",
    "html_handling": "drop-trailing-slash"
  }
}
```

```bash
npm run build
npx wrangler deploy
npx wrangler secret put EMAIL_API_KEY   # store form secrets, never in code
```

### Contact form gotcha (Workers)

A server-side form route must read its secret from the runtime:
`locals.runtime.env.EMAIL_API_KEY`, NOT build-time `import.meta.env`. Getting
this wrong makes the form fail silently with a "server configuration error" even
though the key is set.
