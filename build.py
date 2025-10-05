#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Text-only, black&white static blog builder for GitHub Pages.
- Reads Markdown files from posts_src/
- Generates HTML into posts/
- Writes index.html, sitemap.xml, rss.xml, robots.txt at project root
Usage:
    pip install markdown
    python build.py
"""
import os, re, datetime, html
from pathlib import Path
try:
    import markdown  # pip install markdown
except ImportError:
    raise SystemExit("pip install markdown 필요: pip install markdown")

# --- Load config ---
from config import SITE_TITLE, AUTHOR, BASE_URL, INDEX_LIMIT, SITEMAP_FILENAME, RSS_FILENAME, ROBOTS_FILENAME

ROOT = Path(__file__).parent
SRC  = ROOT / "posts_src"
DST  = ROOT / "posts"
DST.mkdir(exist_ok=True)

# --- Helpers ---
def parse_post(md_path: Path):
    """Return dict with keys: title, date (YYYY-MM-DD), slug, html_body, rel_link"""
    text = md_path.read_text(encoding="utf-8")
    # Extract first non-empty lines for title & date
    lines = [l.rstrip() for l in text.splitlines()]
    nonempty = [l for l in lines if l.strip()]
    title = md_path.stem
    date = None
    # Title: first non-empty, strip leading '#'
    if nonempty:
        t0 = nonempty[0].lstrip("# ").strip()
        if t0:
            title = t0
    # Date: second non-empty if matches YYYY-MM-DD
    if len(nonempty) >= 2 and re.fullmatch(r"\d{4}-\d{2}-\d{2}", nonempty[1].strip()):
        date = nonempty[1].strip()
    else:
        date = datetime.date.today().isoformat()

    # Convert markdown to HTML
    html_body = markdown.markdown(text, extensions=["extra"])

    slug = md_path.stem
    rel_link = f"posts/{slug}.html"
    return {
        "title": title,
        "date": date,
        "slug": slug,
        "html_body": html_body,
        "rel_link": rel_link,
        "src": md_path.name,
    }

def render_post_html(title, date, body_html):
    # Minimal black&white single-file CSS
    return f"""<!doctype html>
<html lang="ko"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(title)} - {html.escape(SITE_TITLE)}">
<style>
:root {{ color-scheme: light dark; }}
* {{ box-sizing: border-box; }}
body {{ margin:0; font-family:-apple-system,system-ui,"Apple SD Gothic Neo","Malgun Gothic",sans-serif; }}
.wrap {{ max-width:720px; margin:0 auto; padding:48px 20px; }}
a {{ color:black; text-decoration:none; border-bottom:1px solid #ccc; }}
a:hover {{ border-bottom-color:black; }}
header a {{ border-bottom:1px solid #ccc; }}
article h1 {{ font-size:1.8rem; margin:0 0 8px; }}
article p, article li {{ line-height:1.8; }}
time {{ color:#666; }}
footer {{ margin-top:40px; color:#777; font-size:0.9rem; }}
code, pre {{ font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
pre {{ overflow:auto; padding:12px; border:1px solid #ddd; }}
hr {{ border:0; border-top:1px solid #ddd; }}
</style>
</head><body>
<div class="wrap">
  <header><a href="../index.html">← 글 목록</a></header>
  <article>
    <h1>{html.escape(title)}</h1>
    <time datetime="{html.escape(date)}">{html.escape(date)}</time>
    {body_html}
  </article>
  <footer>© {datetime.date.today().year} {html.escape(AUTHOR)}</footer>
</div>
</body></html>"""

def render_index(posts_meta):
    items = []
    for p in posts_meta:
        items.append(f'<li><a href="{p["rel_link"]}">{html.escape(p["title"])}</a><br><time datetime="{p["date"]}">{p["date"]}</time></li>')
    items_html = "\n    ".join(items)
    return f"""<!doctype html>
<html lang="ko"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(SITE_TITLE)}</title>
<meta name="description" content="{html.escape(SITE_TITLE)} - 텍스트 전용 흑백 블로그">
<style>
:root {{ color-scheme: light dark; }}
* {{ box-sizing: border-box; }}
body {{ margin:0; font-family:-apple-system,system-ui,"Apple SD Gothic Neo","Malgun Gothic",sans-serif; }}
.wrap {{ max-width:720px; margin:0 auto; padding:48px 20px; }}
header h1 {{ font-size:1.6rem; margin:0 0 4px; }}
header p {{ color:#555; margin:0 0 24px; line-height:1.6; }}
a {{ color:black; text-decoration:none; border-bottom:1px solid #ccc; }}
a:hover {{ border-bottom-color:black; }}
ul {{ list-style:none; padding:0; margin:0; }}
li {{ padding:14px 0; border-top:1px solid #ddd; }}
time {{ color:#666; font-size:0.9rem; }}
footer {{ margin-top:40px; color:#777; font-size:0.9rem; }}
</style>
</head><body>
<div class="wrap">
  <header>
    <h1>{html.escape(SITE_TITLE)}</h1>
    <p>흑백 · 텍스트만 · 초경량 블로그</p>
  </header>
  <main>
    <ul>
      {items_html}
    </ul>
  </main>
  <footer>
    <a href="{SITEMAP_FILENAME}">Sitemap</a> · <a href="{RSS_FILENAME}">RSS</a>
  </footer>
</div>
</body></html>"""

def write_file(path: Path, content: str):
    path.write_text(content, encoding="utf-8")

def generate_sitemap(posts_meta):
    urls = [f"""  <url><loc>{BASE_URL}/</loc></url>"""]
    for p in posts_meta:
        urls.append(f"""  <url><loc>{BASE_URL}/{p["rel_link"]}</loc></url>""")
    body = "\n".join(urls)
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{body}
</urlset>
"""

def rfc822_date(d: str):
    y, m, dd = map(int, d.split("-"))
    dt = datetime.date(y, m, dd)
    dt2 = datetime.datetime(dt.year, dt.month, dt.day, 12, 0, 0)
    return dt2.strftime("%a, %d %b %Y %H:%M:%S +0900")

def generate_rss(posts_meta):
    items = []
    for p in posts_meta:
        items.append(f"""  <item>
    <title>{html.escape(p["title"])}</title>
    <link>{BASE_URL}/{p["rel_link"]}</link>
    <guid>{BASE_URL}/{p["rel_link"]}</guid>
    <pubDate>{rfc822_date(p["date"])}</pubDate>
    <description>{html.escape(p["title"])} - {html.escape(SITE_TITLE)}</description>
  </item>""")
    items_html = "\n".join(items)
    return f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
  <channel>
    <title>{html.escape(SITE_TITLE)}</title>
    <link>{BASE_URL}/</link>
    <description>{html.escape(SITE_TITLE)} RSS</description>
    <language>ko</language>
{items_html}
  </channel>
</rss>
"""

def generate_robots():
    return f"""User-agent: *
Allow: /
Sitemap: {BASE_URL}/{SITEMAP_FILENAME}
"""

def main():
    posts_meta = []
    for md in sorted(SRC.glob("*.md")):
        p = parse_post(md)
        out = DST / f"{p['slug']}.html"
        out.write_text(render_post_html(p["title"], p["date"], p["html_body"]), encoding="utf-8")
        posts_meta.append(p)

    posts_meta.sort(key=lambda x: x["date"], reverse=True)
    posts_meta_view = posts_meta[:INDEX_LIMIT] if INDEX_LIMIT else posts_meta

    (ROOT / "index.html").write_text(render_index(posts_meta_view), encoding="utf-8")
    (ROOT / SITEMAP_FILENAME).write_text(generate_sitemap(posts_meta), encoding="utf-8")
    (ROOT / RSS_FILENAME).write_text(generate_rss(posts_meta), encoding="utf-8")
    (ROOT / ROBOTS_FILENAME).write_text(generate_robots(), encoding="utf-8")

    print(f"빌드 완료: 글 {len(posts_meta)}개, index/sitemap/rss/robots 생성.")

if __name__ == "__main__":
    main()
