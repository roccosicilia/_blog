#!/usr/bin/env python3
"""
Converte l'export XML di WordPress (WXR) in file Markdown per Jekyll/Minima.

Uso:
    python3 wp2jekyll.py                        # usa i valori della sezione CONFIG
    python3 wp2jekyll.py export.xml _posts      # sovrascrive XML_PATH e OUTPUT_DIR

Dipendenze:
    pip install markdownify beautifulsoup4
"""

import argparse
import html
import os
import re
import sys
import unicodedata
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from urllib.parse import unquote, urlparse
from zoneinfo import ZoneInfo

from bs4 import BeautifulSoup, NavigableString
from markdownify import markdownify

# ============================== CONFIG ==============================
XML_PATH = "roccosicilia.WordPress.2026-10-23.xml"                 # file XML esportato da WordPress
OUTPUT_DIR = "./"                   # cartella di destinazione dei .md
MANIFEST_PATH = "images_manifest.tsv"   # elenco immagini da scaricare/copiare

IMAGES_URL_PREFIX = "/assets/images-posts"   # percorso delle immagini nel sito
FORCE_IMAGE_EXT = None                  # es. ".webp" se hai convertito le immagini
FALLBACK_FIRST_IMAGE = False            # senza copertina usa la prima immagine del post

FULL_WIDTH_MIN = 600                    # >= 600px: immagine a tutta larghezza
SMALL_WIDTH_MIN = 150                   # sotto soglia: immagine float affiancata,
SMALL_WIDTH_MAX = 400                   # con larghezza compresa tra questi valori

DEFAULT_TZ = "Europe/Rome"              # usato solo se manca la data GMT nel post
INCLUDE_STATUSES = {"publish"}          # es. {"publish", "draft"}
OVERWRITE = True                        # sovrascrive i file gia' presenti
# ====================================================================

NS = {
    "content": "http://purl.org/rss/1.0/modules/content/",
    "excerpt": "http://wordpress.org/export/1.2/excerpt/",
    "dc": "http://purl.org/dc/elements/1.1/",
    "wp": "http://wordpress.org/export/1.2/",
}

BLOCK_START = re.compile(
    r"\s*<(p|div|ul|ol|li|h[1-6]|table|figure|blockquote|iframe|hr|video|audio|section)\b"
    r"|\s*XPREX\d+X",
    re.I,
)
IMG_EXT = (".jpg", ".jpeg", ".png", ".gif", ".webp", ".avif", ".svg")
SIZE_CLASSES = {"thumbnail": 150, "medium": 300, "medium_large": 768, "large": 1024}


# ----------------------------- utilita' ------------------------------
def txt(item, tag):
    el = item.find(tag, NS)
    return (el.text or "").strip() if el is not None and el.text else ""


def detect_namespaces(path):
    """Alcune versioni di WXR usano wp/1.0 o 1.1: legge quella dichiarata."""
    head = Path(path).read_text(encoding="utf-8", errors="replace")[:6000]
    m = re.search(r'xmlns:wp="([^"]+)"', head)
    if m:
        NS["wp"] = m.group(1)


def slugify(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def yaml_escape(s):
    return s.replace("\\", "\\\\").replace('"', '\\"')


def format_date(local_s, gmt_s):
    """Data nel formato Jekyll con offset: l'offset e' ricavato da post_date - post_date_gmt."""
    local = datetime.strptime(local_s, "%Y-%m-%d %H:%M:%S")
    if gmt_s and not gmt_s.startswith("0000"):
        offset = local - datetime.strptime(gmt_s, "%Y-%m-%d %H:%M:%S")
    else:
        offset = local.replace(tzinfo=ZoneInfo(DEFAULT_TZ)).utcoffset()
    minutes = int(offset.total_seconds() // 60)
    sign = "+" if minutes >= 0 else "-"
    minutes = abs(minutes)
    return local, f"{local:%Y-%m-%d %H:%M:%S} {sign}{minutes // 60:02d}{minutes % 60:02d}"


# ----------------------------- immagini ------------------------------
class ImageRegistry:
    """Tiene traccia delle immagini locali e segnala collisioni di nome."""

    def __init__(self):
        self.files = {}  # nome locale -> url originale

    def register(self, url):
        path = unquote(urlparse(url).path)
        name = os.path.basename(path).replace(" ", "-")
        name = re.sub(r"-\d+x\d+(?=\.[A-Za-z0-9]+$)", "", name)  # rimuove -300x200
        if FORCE_IMAGE_EXT:
            name = os.path.splitext(name)[0] + FORCE_IMAGE_EXT
        known = self.files.get(name)
        if known and known != url and re.sub(r"-\d+x\d+(?=\.)", "", known) != re.sub(r"-\d+x\d+(?=\.)", "", url):
            print(f"  ! collisione nome immagine '{name}': {known} <> {url}", file=sys.stderr)
        self.files.setdefault(name, url)
        return name


def detect_width(img, src):
    """Larghezza stimata: attributo width, suffisso -WxH, classe size-*."""
    w = img.get("width", "")
    if str(w).isdigit():
        return int(w)
    m = re.search(r"-(\d+)x\d+\.[A-Za-z0-9]+(?:\?.*)?$", src)
    if m:
        return int(m.group(1))
    for cls in img.get("class", []):
        m = re.match(r"size-(.+)", cls)
        if m and m.group(1) in SIZE_CLASSES:
            return SIZE_CLASSES[m.group(1)]
    return None


def build_img(src_expr, alt, width, align):
    if width is None or width >= FULL_WIDTH_MIN:
        style = ("float: left; width: 100%; max-width: 100%; margin-right: 20px; "
                 "margin-bottom: 10px; border-radius: 4px;")
    else:
        w = max(SMALL_WIDTH_MIN, min(width, SMALL_WIDTH_MAX))
        if align == "right":
            style = (f"float: right; width: {w}px; max-width: 100%; margin-left: 20px; "
                     "margin-bottom: 10px; border-radius: 4px;")
        else:
            style = (f"float: left; width: {w}px; max-width: 100%; margin-right: 20px; "
                     "margin-bottom: 10px; border-radius: 4px;")
    return f'<img src="{src_expr}" alt="{html.escape(alt, quote=True)}" style="{style}" />'


# ----------------------------- contenuto -----------------------------
def autop(text):
    """Versione minimale di wpautop: i post classici non hanno <p>, solo righe vuote."""
    pres = {}

    def stash_pre(m):
        key = f"XPREX{len(pres)}X"
        pres[key] = m.group(0)
        return f"\n\n{key}\n\n"

    text = re.sub(r"<pre\b.*?</pre>", stash_pre, text, flags=re.S | re.I)
    chunks = [c for c in re.split(r"\n\s*\n", text) if c.strip()]
    out = []
    for c in chunks:
        if BLOCK_START.match(c):
            out.append(c)
        else:
            out.append("<p>" + c.strip().replace("\n", "<br>\n") + "</p>")
    text = "\n\n".join(out)
    for key, val in pres.items():
        text = text.replace(key, val)
    return text


def convert_content(raw, images, is_local):
    """Restituisce (markdown, nome_prima_immagine_locale)."""
    text = raw.replace("\r\n", "\n")
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)             # commenti Gutenberg
    text = re.sub(r"\[/?caption[^\]]*\]", "", text)                # shortcode caption
    text = re.sub(r"\[embed\](.*?)\[/embed\]", r"\n\n\1\n\n", text, flags=re.S)
    text = autop(text)

    soup = BeautifulSoup(text, "html.parser")
    stash = {}
    first_image = None

    def keep(raw_html):
        key = f"XRAWX{len(stash)}X"
        stash[key] = raw_html
        return NavigableString(f"\n\n{key}\n\n")

    # iframe, video, audio: restano HTML cosi' come sono
    for tag in soup.find_all(["iframe", "video", "audio"]):
        tag.replace_with(keep(str(tag)))

    for img in soup.find_all("img"):
        src = img.get("src") or img.get("data-src") or ""
        if not src:
            img.decompose()
            continue
        width = detect_width(img, src)
        align = "right" if "alignright" in img.get("class", []) else "left"
        alt = (img.get("alt") or "").strip()

        if is_local(src):
            name = images.register(src)
            src_expr = f"{{{{ '{IMAGES_URL_PREFIX}/{name}' | relative_url }}}}"
            first_image = first_image or name
            alt = alt or os.path.splitext(name)[0].replace("-", " ")
        else:
            src_expr = src
            alt = alt or "immagine"

        # <a href="immagine.jpg"><img></a> -> solo l'immagine
        target = img
        parent = img.parent
        if parent is not None and parent.name == "a":
            href = (parent.get("href") or "").lower().split("?")[0]
            only_child = len([c for c in parent.contents
                              if not (isinstance(c, NavigableString) and not c.strip())]) == 1
            if only_child and (href.endswith(IMG_EXT) or "/wp-content/uploads/" in href):
                target = parent
        target.replace_with(keep(build_img(src_expr, alt, width, align)))

    md = markdownify(
        str(soup),
        heading_style="ATX",
        bullets="-",
        code_language="",
        escape_underscores=False,
        escape_asterisks=False,
    )
    md = re.sub(r"\n{3,}", "\n\n", md).strip()

    # Jekyll interpreta Liquid anche nei blocchi di codice: neutralizza {{ e {%
    md = re.sub(r"\{\{|\{%", lambda m: '{{ "%s" }}' % m.group(0), md)

    # solo dopo l'escape rimette immagini e iframe (che contengono Liquid voluto)
    for key, val in stash.items():
        md = md.replace(key, val)
    return md, first_image


# ------------------------------ main ---------------------------------
def main():
    ap = argparse.ArgumentParser(description="WordPress XML -> post Jekyll")
    ap.add_argument("xml", nargs="?", default=XML_PATH)
    ap.add_argument("out", nargs="?", default=OUTPUT_DIR)
    args = ap.parse_args()

    detect_namespaces(args.xml)
    channel = ET.parse(args.xml).getroot().find("channel")
    items = channel.findall("item")

    # host del sito originale: serve a distinguere immagini locali da esterne
    hosts = set()
    for tag in ("wp:base_blog_url", "wp:base_site_url", "link"):
        el = channel.find(tag, NS)
        if el is not None and el.text:
            hosts.add(urlparse(el.text.strip()).netloc)

    def is_local(url):
        p = urlparse(url)
        return (not p.netloc) or p.netloc in hosts or "/wp-content/uploads/" in p.path

    # id allegato -> url (per le immagini di copertina)
    attachments = {}
    for it in items:
        if txt(it, "wp:post_type") == "attachment":
            attachments[txt(it, "wp:post_id")] = txt(it, "wp:attachment_url") or txt(it, "guid")

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    images = ImageRegistry()
    used_names, written, skipped = set(), 0, 0

    for it in items:
        if txt(it, "wp:post_type") != "post" or txt(it, "wp:status") not in INCLUDE_STATUSES:
            continue

        title = html.unescape(txt(it, "title")) or "Senza titolo"
        local_s, gmt_s = txt(it, "wp:post_date"), txt(it, "wp:post_date_gmt")
        if not local_s or local_s.startswith("0000"):
            print(f"  ! salto '{title}': data mancante", file=sys.stderr)
            continue
        local_dt, date_str = format_date(local_s, gmt_s)

        # categorie: slug originali di WordPress, senza modifiche
        cats = [unquote(c.get("nicename", "")) for c in it.findall("category")
                if c.get("domain") == "category" and c.get("nicename")]

        # copertina dalla featured image
        thumb_id = ""
        for meta in it.findall("wp:postmeta", NS):
            if txt(meta, "wp:meta_key") == "_thumbnail_id":
                thumb_id = txt(meta, "wp:meta_value")
        cover = ""
        if thumb_id and attachments.get(thumb_id):
            cover = f"{IMAGES_URL_PREFIX}/{images.register(attachments[thumb_id])}"

        body, first_image = convert_content(txt_raw(it), images, is_local)
        if not cover and FALLBACK_FIRST_IMAGE and first_image:
            cover = f"{IMAGES_URL_PREFIX}/{first_image}"

        slug = slugify(unquote(txt(it, "wp:post_name"))) or slugify(title) or f"post-{txt(it, 'wp:post_id')}"
        filename = f"{local_dt:%Y-%m-%d}-{slug}.md"
        n = 2
        while filename in used_names:
            filename = f"{local_dt:%Y-%m-%d}-{slug}-{n}.md"
            n += 1
        used_names.add(filename)

        dest = out_dir / filename
        if dest.exists() and not OVERWRITE:
            skipped += 1
            continue

        front = [
            "---",
            "layout:     post",
            f'title:      "{yaml_escape(title)}"',
            f"date:       {date_str}",
            f"categories: [{', '.join(cats)}]",
            f"image:      {cover}".rstrip(),
            "---",
        ]
        dest.write_text("\n".join(front) + "\n" + body + "\n", encoding="utf-8")
        written += 1

    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        for name, url in sorted(images.files.items()):
            f.write(f"{name}\t{url}\n")

    print(f"Post scritti: {written}  (saltati: {skipped})  -> {out_dir}")
    print(f"Immagini referenziate: {len(images.files)}  -> {MANIFEST_PATH}")


def txt_raw(item):
    el = item.find("content:encoded", NS)
    return el.text or "" if el is not None else ""


if __name__ == "__main__":
    main()