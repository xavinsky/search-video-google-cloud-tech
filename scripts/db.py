"""Lecture/écriture de la base de vidéos data/videos.json."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data" / "videos.json"
CHANNELS_PATH = ROOT / "channels.json"


def load_channels():
    return json.loads(CHANNELS_PATH.read_text(encoding="utf-8"))


def load_db():
    if not DB_PATH.exists():
        return {"updated": None, "videos": []}
    return json.loads(DB_PATH.read_text(encoding="utf-8"))


def save_db(db):
    db["videos"].sort(key=lambda v: (v.get("published") or "", v["id"]), reverse=True)
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    DB_PATH.write_text(json.dumps(db, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
