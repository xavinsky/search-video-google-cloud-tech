#!/usr/bin/env python3
"""Génère docs/index.html depuis data/videos.json et la taxonomie scripts/tags.py.

Usage : python3 scripts/build.py
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from db import ROOT, load_channels, load_db  # noqa: E402
from tags import GROUPS, MANUAL_OVERRIDES  # noqa: E402

TEMPLATE = ROOT / "templates" / "index.html"
OUTPUT = ROOT / "docs" / "index.html"

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
        print("Ajoute un motif dans GROUPS ou une entrée dans MANUAL_OVERRIDES (scripts/tags.py), puis relance.\n")

    used = {t for v in videos for t in v["tags"]}
    groups = [{"name": g, "tags": [t for t, _ in tags if t in used]} for g, tags in GROUPS]
    groups = [g for g in groups if g["tags"]]

    def to_js(obj):
        return json.dumps(obj, ensure_ascii=False).replace("</", "<\\/")

    out = (TEMPLATE.read_text(encoding="utf-8")
           .replace("__DATA_JSON__", to_js(videos))
           .replace("__GROUPS_JSON__", to_js(groups))
           .replace("__CHANNELS_JSON__", to_js(channels))
           .replace("__UPDATED__", db.get("updated") or ""))
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(out, encoding="utf-8")
    print(f"{len(videos)} vidéos — {len(used)} tags — écrit dans {OUTPUT.relative_to(ROOT)}")
    return len(unclassified)


if __name__ == "__main__":
    sys.exit(1 if main() else 0)
