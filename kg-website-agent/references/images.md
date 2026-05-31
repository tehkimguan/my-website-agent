# Reference: Generate images with the Gemini API

A static site needs pictures: a hero, blog covers, and the social preview (OG)
image shown when a link is shared. The capture phase brings across the old site's
images. For anything new, the agent calls Google's Gemini image API directly.

No external MCP server or plug-in is required. The key lives in `.env`, the agent
writes the small call, and the image lands in `public/images/`.

## Get a key

[aistudio.google.com](https://aistudio.google.com) -> Get API key -> Create API
key. It starts with `AIza`. Put it in the project `.env` (which is git-ignored):

```
GEMINI_API_KEY=AIza...
```

Trying it is free. In bulk it costs roughly four US cents (~RM 0.18) per image on
the standard model, so a brochure site's images cost under one dollar. Confirm
current pricing at ai.google.dev/pricing before committing to volume.

## How the agent generates an image

The agent writes a short script that posts a prompt to the Gemini image model,
saves the returned image, converts it to web-friendly JPEG/WebP, and wires it in.
A minimal Node shape:

```js
// gen-image.mjs — generate one image with the Gemini API
import { GoogleGenAI } from "@google/genai";
import { writeFileSync } from "node:fs";

const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY });
const res = await ai.models.generateContent({
  model: "gemini-2.5-flash-image",
  contents: "A clean, modern hero image for an IT-solutions company, "
          + "brand navy and white, wide 16:9, abstract geometric, no text.",
});
for (const part of res.candidates[0].content.parts) {
  if (part.inlineData) {
    writeFileSync("public/images/hero.png", Buffer.from(part.inlineData.data, "base64"));
  }
}
```

The agent then converts the PNG to JPEG/WebP and adds it to the page. You only
ever say, in plain English: "make a 16:9 hero for the home page in our brand
style, save it to public/images, and use it."

## Good practice for the web

- **One consistent style.** Lock a palette per site so every image matches.
- **Right size, not huge.** ~1,500px wide for a hero/cover is plenty. 4K is
  slower, costs more, and the visitor never sees the difference.
- **Make an OG image.** 1200x630 is the social preview size. One per page.
- **Convert and compress.** The model outputs large PNGs; ship JPEG or WebP.
- **Write alt text.** Short descriptions help search engines and accessibility.

## Why no MCP plug-in

The migration does not need an always-on image server. A direct API call with the
key in `.env` is simpler, has nothing extra to install or keep running, and keeps
the whole stack to the three core tools plus one image key.
