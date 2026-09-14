#!/usr/bin/env python3
"""Met à jour data/videos.json depuis YouTube, puis régénère docs/index.html.

Usage : python3 scripts/update.py [--full] [--details N] [--no-build] [--delay S]

Sans option : parcourt chaque chaîne de channels.json de la plus récente vidéo vers le passé
et s'arrête dès qu'une page ne contient plus rien de nouveau (incrémental). Les vidéos
nouvelles reçoivent une date approximative (déduite du "3 days ago" de la liste), puis leur
page est consultée pour obtenir la date de publication exacte, à concurrence de --details
vidéos par exécution (défaut 200, 0 pour désactiver) — les autres restent en "approx" et
seront précisées aux exécutions suivantes.

  --full      parcourt toute la playlist même si rien de nouveau (rattrapage, nouvelle chaîne)
  --details N nombre maximum de pages vidéo consultées pour obtenir la date exacte
  --no-build  ne régénère pas la page HTML
  --delay S   pause entre deux requêtes YouTube (défaut 0.5 s)

En GitHub Actions, écrit added=N et dated=N dans $GITHUB_OUTPUT.
"""
import argparse
import os
import sys
import time
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import youtube  # noqa: E402
from db import load_channels, load_db, save_db  # noqa: E402


def crawl(db, full, delay):
    by_id = {v["id"]: v for v in db["videos"]}
    today = date.today()
    added = 0
    for ch in load_channels():
        print(f"Chaîne {ch['name']} — playlist {ch['uploads_playlist']}")
        known = set() if full else {v["id"] for v in db["videos"] if v.get("channel_id") == ch["channel_id"]}
        for item in youtube.list_playlist(ch["uploads_playlist"], stop_at_ids=known, delay=delay):
            v = by_id.get(item["id"])
            if v is None:
                v = {
                    "id": item["id"],
                    "title": item["title"],
                    "channel": ch["name"],
                    "channel_id": ch["channel_id"],
                    "credits": item["credits"] if item["credits"] != ch["name"] else "",
                    "duration_sec": item["duration_sec"],
                    "views": item["views"],
                    "published": youtube.approx_date(item["age_days"], today) if item["age_days"] is not None else None,
                    "date_precision": "approx",
                }
                db["videos"].append(v)
                by_id[v["id"]] = v
                added += 1
            else:
                if item["title"]:
                    v["title"] = item["title"]
                if item["duration_sec"] and v.get("date_precision") != "exact":
                    v["duration_sec"] = item["duration_sec"]
                if item["views"] > (v.get("views") or 0):
                    v["views"] = item["views"]
    print(f"{added} nouvelle(s) vidéo(s)")
    return added


def fetch_details(db, limit, delay):
    todo = [v for v in db["videos"] if v.get("date_precision") != "exact"]
    todo.sort(key=lambda v: v.get("published") or "", reverse=True)
    todo = todo[:limit]
    if not todo:
        return 0
    print(f"Dates exactes : {len(todo)} vidéo(s) à consulter")
    done = 0
    failures = 0
    for i, v in enumerate(todo, 1):
        try:
            d = youtube.video_details(v["id"])
            failures = 0
        except Exception as e:  # noqa: BLE001
            print(f"  ! {v['id']} : {e}")
            failures += 1
            if failures >= 5:
                print("  5 échecs consécutifs : arrêt (relancer plus tard, ou avec --delay plus grand)")
                break
            continue
        if d["published"]:
            v["published"] = d["published"]
            v["date_precision"] = "exact"
            done += 1
        if d["duration_sec"]:
            v["duration_sec"] = d["duration_sec"]
        if d["views"] is not None:
            v["views"] = d["views"]
        if i % 25 == 0:
            print(f"  {i}/{len(todo)}")
            save_db(db)
        time.sleep(delay)
    print(f"{done} date(s) précisée(s)")
    return done


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--full", action="store_true")
    ap.add_argument("--details", type=int, default=200)
    ap.add_argument("--no-build", action="store_true")
    ap.add_argument("--delay", type=float, default=0.5)
    args = ap.parse_args()

    db = load_db()
    added = crawl(db, args.full, args.delay)
    db["updated"] = date.today().isoformat()
    save_db(db)
    dated = 0
    if args.details > 0:
        dated = fetch_details(db, args.details, args.delay)
        save_db(db)
    remaining = sum(1 for v in db["videos"] if v.get("date_precision") != "exact")
    print(f"{len(db['videos'])} vidéos en base, {remaining} avec date approximative")
    # En GitHub Actions : expose les compteurs pour décider s'il faut commiter la base
    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a", encoding="utf-8") as f:
            f.write(f"added={added}\ndated={dated}\n")
    if not args.no_build:
        import build
        build.main()


if __name__ == "__main__":
    main()
