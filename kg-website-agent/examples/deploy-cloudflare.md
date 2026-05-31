# Example: Deploy to Cloudflare and go live

## Context

The site is assembled and previews correctly. Ship it.

## Steps

```bash
# 1. Put it on GitHub (.env is git-ignored automatically)
git init
git add .
git commit -m "Initial migrated site"
gh repo create my-site --private --source=. --remote=origin --push
```

```text
# 2. Connect Cloudflare Pages (normal site)
Cloudflare dashboard -> Workers and Pages -> Create -> Pages -> Connect to Git
  repo: my-site
  framework preset: Astro
  build command: npm run build
  output directory: dist
  -> Save and Deploy
```

From now on, every `git push` rebuilds and republishes automatically. You get a
free `my-site.pages.dev` URL to test immediately.

## Go live

> "Add the custom domain yourdomain.com in Cloudflare. Before I confirm the
> nameserver change, check the imported DNS records include the MX rows so email
> keeps working. Then walk me through submitting the sitemap to Search Console."

Checklist the agent runs through: MX present, custom domain added, SSL valid,
smoke-test on the real domain and on mobile, sitemap submitted, Web Analytics on,
WordPress switched off (not deleted) for two weeks.

## Needs a contact form?

Use Cloudflare Workers instead of Pages, and store the email key as a secret:

```bash
npx wrangler secret put RESEND_API_KEY
```

The Worker form route reads it from `locals.runtime.env.RESEND_API_KEY` at
runtime, never `import.meta.env`.
