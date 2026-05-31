# Example: Capture an existing site's design

## Context

A small WordPress brochure site (home, about, services, contact) is being
rebuilt. We want its exact look preserved before touching content.

## What you say to the agent

> "Capture the design of yourdomain.com and its main pages (about, services,
> contact). Screenshot each section at desktop and mobile, read the real colours
> and fonts from the DOM, download the logo and key images into public/images,
> and write a component spec plus a token sheet to capture/."

## What the agent does

1. Opens each page with built-in computer-use, screenshots desktop + mobile.
2. Evaluates computed styles to extract the palette and fonts:

```js
const b = getComputedStyle(document.body);
({ font: b.fontFamily, color: b.color, bg: b.backgroundColor,
   h1: getComputedStyle(document.querySelector('h1')).fontFamily,
   link: getComputedStyle(document.querySelector('a')).color })
```

3. Writes `capture/tokens.json`, `capture/components.md`, saves assets.

## Output

```
capture/
├── screenshots/        home-desktop.png, home-mobile.png, ...
├── tokens.json         { navy:"#10118b", body:"Inter", h1:"Playfair Display", ... }
└── components.md       header / hero / cards / footer specs
public/images/          logo + key images
```

These are framework-neutral and feed Phase D (Assemble).
