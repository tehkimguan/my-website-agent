# Reference: Capture the old design (Phase A)

The goal of Phase A is to preserve a site's visual identity without copying its
broken WordPress internals. You capture the *durable* material (colours, fonts,
images, section structure) and discard everything else.

There is no third-party template to install. Every modern AI coding assistant
includes computer-use, so the agent inspects the live page directly.

## What to capture

Open the live site (and each main page) with the built-in browser, then for each
page produce:

1. **Screenshots** of every section, at a desktop width (~1440px) and a mobile
   width (~390px). Save to `capture/screenshots/`.
2. **Design tokens** read from the rendered DOM and computed styles:
   - Brand colours (hex), background, text, link, and accent colours
   - Font families for headings and body, with weights actually used
   - Base font size, heading scale, and section spacing
   Save as `capture/tokens.json`.
3. **Component specs** — a short written description of each region: header/nav,
   hero, content cards, call-to-action blocks, footer. Note layout (columns,
   alignment), and which elements repeat. Save to `capture/components.md`.
4. **Assets** — download the logo and the key images into `public/images/`.

## How to read tokens from the DOM

Use the browser's evaluate/JS capability against the live page:

```js
// colours and fonts actually in use on the page
const body = getComputedStyle(document.body);
({
  bodyFont: body.fontFamily,
  bodyColor: body.color,
  bg: body.backgroundColor,
  h1Font: getComputedStyle(document.querySelector('h1') || document.body).fontFamily,
  linkColor: getComputedStyle(document.querySelector('a') || document.body).color,
})
```

Sample several elements (h1, h2, nav, button, footer) so the token sheet reflects
the real palette, not one element's defaults.

## Why specs, not a scrape

A pixel scrape locks you to the old HTML. A spec (tokens + component descriptions
+ assets) is framework-neutral. In Phase D the agent reads it and rebuilds each
region as a clean Astro component, responsive on mobile, with none of the old
plugin markup. You are reusing the surveyor's report, not the surveyor's
scaffolding.

## Boundary

Only capture sites the user owns or is authorised to rebuild. Do not clone a
third party's site to pass off their design or brand.
