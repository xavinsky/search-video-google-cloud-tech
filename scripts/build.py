#!/usr/bin/env python3
"""Génère docs/index.html et docs/sitemap.xml depuis data/videos.json et la taxonomie scripts/tags.py.

Usage : python3 scripts/build.py
"""
import html
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from db import ROOT, load_channels, load_db  # noqa: E402
from tags import GROUPS, MANUAL_OVERRIDES  # noqa: E402

TEMPLATE = ROOT / "templates" / "index.html"
OUTPUT = ROOT / "docs" / "index.html"
SITEMAP = ROOT / "docs" / "sitemap.xml"

# Le site est servi sous ce chemin du domaine tekio.org (GitHub Pages, domaine personnalisé).
SITE_URL = "https://tekio.org/search-video-google-cloud-tech/"
SITE_NAME = "Vidéos Google Cloud Tech, recherche par technologie"

COMPILED = [(group, [(tag, re.compile(pat, re.I)) for tag, pat in tags]) for group, tags in GROUPS]


def tag_video(title):
    found = []
    for _group, tags in COMPILED:
        for tag, rx in tags:
            if rx.search(title):
                found.append(tag)
    if not found and title in MANUAL_OVERRIDES:
        found = list(MANUAL_OVERRIDES[title])
    return found


def write_sitemap(urls, lastmod):
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for url in urls:
        lines.append("  <url>")
        lines.append(f"    <loc>{html.escape(url)}</loc>")
        if lastmod:
            lines.append(f"    <lastmod>{lastmod}</lastmod>")
        lines.append("  </url>")
    lines.append("</urlset>")
    SITEMAP.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    db = load_db()
    channels = load_channels()
    videos, unclassified = [], []
    for v in db["videos"]:
        tags = tag_video(v["title"])
        if not tags:
            unclassified.append(v["title"])
        videos.append({
            "id": v["id"],
            "url": f"https://www.youtube.com/watch?v={v['id']}",
            "title": v["title"],
            "channel": v.get("channel", ""),
            "credits": v.get("credits") or "",
            "durationSec": v.get("duration_sec") or 0,
            "views": v.get("views") or 0,
            "published": v.get("published"),
            "approx": v.get("date_precision") != "exact",
            "tags": tags,
        })

    if unclassified:
        print(f"\n⚠️  {len(unclassified)} vidéo(s) sans aucun tag — à classer (pas de fourre-tout !) :")
        for t in unclassified:
            print("  -", t)
            if os.environ.get("GITHUB_ACTIONS"):
                print(f"::warning title=Vidéo non classée::{t}")
        print("Ajoute un motif dans GROUPS ou une entrée dans MANUAL_OVERRIDES (scripts/tags.py), puis relance.\n")

    used = {t for v in videos for t in v["tags"]}
    groups = [{"name": g, "tags": [t for t, _ in tags if t in used]} for g, tags in GROUPS]
    groups = [g for g in groups if g["tags"]]

    def to_js(obj):
        return json.dumps(obj, ensure_ascii=False).replace("</", "<\\/")

    updated = db.get("updated") or ""
    title = f"{SITE_NAME} | tekio.org"
    description = (f"Recherche dans {len(videos)} vidéos de la chaîne YouTube Google Cloud Tech, "
                   "taguées par technologie : BigQuery, GKE, Vertex AI, ADK...")
    assert len(description) <= 160, description
    jsonld = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": SITE_NAME,
        "url": SITE_URL,
        "description": description,
        "inLanguage": "fr",
        "isPartOf": {"@type": "WebSite", "name": "tekio.org", "url": "https://tekio.org/"},
    }
    if updated:
        jsonld["dateModified"] = updated

    out = (TEMPLATE.read_text(encoding="utf-8")
           .replace("__TITLE__", html.escape(title))
           .replace("__DESCRIPTION__", html.escape(description))
           .replace("__CANONICAL__", SITE_URL)
           .replace("__JSONLD__", to_js(jsonld))
           .replace("__DATA_JSON__", to_js(videos))
           .replace("__GROUPS_JSON__", to_js(groups))
           .replace("__CHANNELS_JSON__", to_js(channels))
           .replace("__UPDATED__", updated))
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(out, encoding="utf-8")
    write_sitemap([SITE_URL], updated)
    print(f"{len(videos)} vidéos — {len(used)} tags — écrit dans {OUTPUT.relative_to(ROOT)}")
    return len(unclassified)


if __name__ == "__main__":
    main()
