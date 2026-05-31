#!/usr/bin/env python3
"""wppull — pull a WordPress site's content out through the REST API and write
it as Markdown files with frontmatter, ready for an Astro content collection.

By Teh Kim Guan (https://tehkimguan.com). Free and open source (MIT).

The CLI is a faithful extractor: it pulls posts, pages, and a media manifest.
It deliberately leaves the post body as the original rendered HTML and lets the
AI agent (kg-website-agent) convert it to clean Markdown, because semantic
conversion is the AI's job, not a brittle regex's.
"""

import json
import os
import re
import sys
from pathlib import Path

import click
import requests

from . import __version__


# ── helpers ──────────────────────────────────────────────────────────────────

def api_base(site: str) -> str:
    """Normalise a domain or URL into a WP REST v2 base."""
    site = site.strip().rstrip("/")
    if not site.startswith("http://") and not site.startswith("https://"):
        site = "https://" + site
    return site + "/wp-json/wp/v2"


def make_session(user: str | None, app_password: str | None) -> requests.Session:
    s = requests.Session()
    s.headers.update({"User-Agent": f"wppull/{__version__} (+https://tehkimguan.com)"})
    if user and app_password:
        s.auth = (user, app_password)
    return s


def fetch_all(base: str, kind: str, session: requests.Session) -> list:
    """Fetch every record of a WP collection, paginating 100 at a time."""
    items, page = [], 1
    while True:
        r = session.get(
            f"{base}/{kind}",
            params={"per_page": 100, "page": page, "_embed": 0},
            timeout=30,
        )
        # WP returns 400 (rest_post_invalid_page_number) when you page past the end.
        if r.status_code == 400:
            break
        r.raise_for_status()
        batch = r.json()
        if not isinstance(batch, list) or not batch:
            break
        items.extend(batch)
        total_pages = int(r.headers.get("X-WP-TotalPages", 0) or 0)
        if total_pages and page >= total_pages:
            break
        if len(batch) < 100:
            break
        page += 1
    return items


def fetch_term_map(base: str, kind: str, session: requests.Session) -> dict:
    """Build {term_id: name} for tags or categories. Best effort."""
    try:
        terms = fetch_all(base, kind, session)
    except requests.RequestException:
        return {}
    return {t["id"]: t.get("name", "") for t in terms if "id" in t}


def strip_tags(html: str) -> str:
    text = re.sub(r"<[^>]+>", "", html or "")
    text = (
        text.replace("&amp;", "&")
        .replace("&lt;", "<")
        .replace("&gt;", ">")
        .replace("&#8217;", "'")
        .replace("&#8211;", "-")
        .replace("&nbsp;", " ")
    )
    return re.sub(r"\s+", " ", text).strip()


def fm_value(s: str) -> str:
    """JSON-encode a string so it is always valid YAML scalar."""
    return json.dumps(s if s is not None else "", ensure_ascii=False)


def safe_filename(slug: str) -> str:
    name = re.sub(r"[^a-z0-9\-]", "-", (slug or "").lower()).strip("-")
    return name or "untitled"


def image_urls_in(html: str) -> list:
    return re.findall(r'<img[^>]+src="([^"]+)"', html or "")


def build_markdown(item: dict, tag_map: dict, cat_map: dict, strip_html: bool) -> str:
    title = strip_tags(item.get("title", {}).get("rendered", ""))
    excerpt = strip_tags(item.get("excerpt", {}).get("rendered", ""))
    date = (item.get("date") or "")[:10]
    tag_names = [tag_map.get(t, str(t)) for t in item.get("tags", [])]
    cat_names = [cat_map.get(c, str(c)) for c in item.get("categories", [])]
    all_tags = [t for t in (tag_names + cat_names) if t]

    body_html = item.get("content", {}).get("rendered", "")
    body = strip_tags(body_html) if strip_html else body_html

    lines = [
        "---",
        f"title: {fm_value(title)}",
        f"description: {fm_value(excerpt)}",
        f"publishedAt: {date}",
        f"tags: {json.dumps(all_tags, ensure_ascii=False)}",
        f"slug: {fm_value(item.get('slug', ''))}",
        "draft: false",
        "---",
        "",
        body,
        "",
    ]
    return "\n".join(lines)


# ── CLI ──────────────────────────────────────────────────────────────────────

@click.group()
@click.version_option(__version__, prog_name="wppull")
@click.option("--json", "json_out", is_flag=True, help="Print a JSON summary instead of human text.")
@click.option("--user", default=None, help="WordPress username (only if the REST API needs auth).")
@click.option("--app-password", default=None, help="WordPress Application Password (Users -> Profile).")
@click.pass_context
def main(ctx, json_out, user, app_password):
    """Pull WordPress content out through the REST API for a static-site migration."""
    ctx.ensure_object(dict)
    ctx.obj["json"] = json_out
    ctx.obj["session"] = make_session(user, app_password)


@main.command()
@click.argument("site")
@click.option("--out", default="src/content/blog", help="Output directory for Markdown files.")
@click.option("--type", "kinds", type=click.Choice(["posts", "pages", "both"]), default="both")
@click.option("--strip-html", is_flag=True, help="Strip HTML to plain text instead of keeping rendered HTML.")
@click.pass_context
def pull(ctx, site, out, kinds, strip_html):
    """Pull all posts and/or pages from SITE into Markdown files.

    SITE may be a domain (example.com) or a full URL.
    """
    session = ctx.obj["session"]
    base = api_base(site)
    out_dir = Path(out)
    out_dir.mkdir(parents=True, exist_ok=True)

    tag_map = fetch_term_map(base, "tags", session)
    cat_map = fetch_term_map(base, "categories", session)

    targets = ["posts", "pages"] if kinds == "both" else [kinds]
    written, media = [], set()

    for kind in targets:
        try:
            items = fetch_all(base, kind, session)
        except requests.RequestException as e:
            click.echo(f"  ! could not fetch /{kind}: {e}", err=True)
            continue
        for item in items:
            md = build_markdown(item, tag_map, cat_map, strip_html)
            fname = safe_filename(item.get("slug", "")) + ".md"
            (out_dir / fname).write_text(md, encoding="utf-8")
            written.append(str(out_dir / fname))
            for url in image_urls_in(item.get("content", {}).get("rendered", "")):
                media.add(url)

    manifest = out_dir.parent / "media-manifest.json"
    manifest.write_text(json.dumps(sorted(media), indent=2, ensure_ascii=False), encoding="utf-8")

    if ctx.obj["json"]:
        click.echo(json.dumps(
            {"site": base, "files_written": len(written), "media_referenced": len(media),
             "out_dir": str(out_dir), "media_manifest": str(manifest)},
            indent=2, ensure_ascii=False))
    else:
        click.echo(f"  wrote {len(written)} file(s) to {out_dir}")
        click.echo(f"  {len(media)} image URL(s) listed in {manifest}")
        click.echo("  next: ask kg-website-agent to convert the HTML bodies to clean Markdown")
        click.echo("        and download the media-manifest images into public/images/")


@main.command()
@click.argument("site")
@click.option("--download", default=None, help="Download every media file into this directory.")
@click.pass_context
def media(ctx, site, download):
    """List (or download) every media file on SITE."""
    session = ctx.obj["session"]
    base = api_base(site)
    try:
        items = fetch_all(base, "media", session)
    except requests.RequestException as e:
        click.echo(f"  ! could not fetch /media: {e}", err=True)
        sys.exit(1)

    records = [
        {"id": m.get("id"), "src": m.get("source_url"),
         "alt": strip_tags(m.get("alt_text", "")), "mime": m.get("mime_type")}
        for m in items
    ]

    if download:
        dest = Path(download)
        dest.mkdir(parents=True, exist_ok=True)
        ok = 0
        for rec in records:
            url = rec["src"]
            if not url:
                continue
            try:
                resp = session.get(url, timeout=60)
                resp.raise_for_status()
                (dest / os.path.basename(url.split("?")[0])).write_bytes(resp.content)
                ok += 1
            except requests.RequestException:
                click.echo(f"  ! failed: {url}", err=True)
        click.echo(f"  downloaded {ok}/{len(records)} file(s) to {dest}")
        return

    if ctx.obj["json"]:
        click.echo(json.dumps(records, indent=2, ensure_ascii=False))
    else:
        for rec in records:
            click.echo(f"  [{rec['id']}] {rec['src']}")
        click.echo(f"  {len(records)} media file(s)")


if __name__ == "__main__":
    main(obj={})
