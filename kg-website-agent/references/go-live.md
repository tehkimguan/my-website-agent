# Reference: Go live (Phase F)

The new site is running on a free `.pages.dev` or `.workers.dev` address. Going
live means pointing the real domain at it. This is the step that most often goes
wrong, so work through it deliberately.

## 1. Move the domain to Cloudflare

In the Cloudflare dashboard: Add a site, enter the domain, choose the Free plan.
Cloudflare scans and imports the existing DNS records. **Review that list before
continuing.**

### Check MX records before the cutover (critical)

MX records route email for the domain. If they are missing from the imported
list and you complete the migration, inbound email stops the moment the domain
goes live on Cloudflare. No bounce, no error, messages just disappear.

Look for rows with type **MX**. If present, proceed. If the list has only A and
CNAME rows and the domain uses email, stop and add the MX records by hand first.

### Update nameservers

Cloudflare gives two nameserver addresses. Log in to the domain registrar, find
the Nameservers setting, and replace the existing entries with Cloudflare's two.
If you cannot access the registrar, email their support with the domain and the
two nameservers and ask them to change it.

### Wait for propagation

Propagation takes 30 minutes to 48 hours. Track it at
[whatsmydns.net](https://www.whatsmydns.net): search the domain, choose record
type NS. When Cloudflare's nameservers appear across most of the world map, the
Cloudflare dashboard shows the domain as **Active**. Only then connect the domain
to the project (Workers and Pages -> project -> custom domain). SSL issues
automatically and free.

## 2. Submit the sitemap to Google

Astro publishes `/sitemap-index.xml` on every deploy.

1. [Google Search Console](https://search.google.com/search-console) -> Add
   property -> Domain -> enter the domain.
2. Verify by DNS: Google shows a TXT record; add it in Cloudflare DNS, then
   Verify (quick, because the domain is already on Cloudflare).
3. Sitemaps -> type `sitemap-index.xml` -> Submit.
4. URL Inspection -> request indexing for the homepage and a few key pages.

Submit the sitemap the same day as the cutover so Google re-crawls quickly and
sees the Phase C redirects that carry the old rankings across. Optionally repeat
at Bing Webmaster Tools.

## 3. Go-live checklist

- [ ] Custom domain added; site loads on the real domain with a valid padlock.
- [ ] MX records confirmed present (email still works).
- [ ] Smoke test: home, a few posts, the menu, footer, and a couple of old URLs
      (they should redirect). Checked on a phone.
- [ ] Sitemap submitted to Search Console.
- [ ] Cloudflare Web Analytics enabled (one toggle, free, no cookie banner).
- [ ] WordPress switched off but NOT deleted. Retire it after two clean weeks.
