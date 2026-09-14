"""Accès à YouTube sans dépendance externe (stdlib uniquement).

Deux opérations :
- list_playlist() : parcourt une playlist page par page (100 vidéos par page) via la page HTML
  initiale puis l'API de continuation "browse" utilisée par le site lui-même. Renvoie les
  métadonnées visibles dans la liste (titre, durée, vues arrondies, date relative, crédits —
  la ligne « Google Cloud Tech and X » des vidéos en collaboration).
- video_details() : lit la page d'une vidéo pour obtenir la date de publication exacte,
  la durée en secondes et le nombre de vues exact.

La playlist "uploads" d'une chaîne a pour identifiant "UU" + identifiant de chaîne sans "UC".
"""
import json
import re
import time
import urllib.error
import urllib.request
from datetime import date, timedelta

USER_AGENT = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")
BROWSE_URL = "https://www.youtube.com/youtubei/v1/browse?prettyPrint=false"
PLAYLIST_URL = "https://www.youtube.com/playlist?list={}"
WATCH_URL = "https://www.youtube.com/watch?v={}"


def fetch(url, data=None, headers=None, retries=3):
    h = {"User-Agent": USER_AGENT, "Accept-Language": "en-US,en;q=0.9",
         "Cookie": "CONSENT=YES+1; SOCS=CAI"}
    if headers:
        h.update(headers)
    last_err = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, data=data, headers=h)
            return urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            last_err = e
            if e.code != 429:
                raise
            # YouTube limite le débit : attente longue et croissante avant de retenter
            time.sleep(20 * (attempt + 1))
        except Exception as e:  # noqa: BLE001 — réseau : on retente
            last_err = e
            time.sleep(2 * (attempt + 1))
    raise last_err


def _walk(obj, key, out):
    if isinstance(obj, dict):
        if key in obj:
            out.append(obj[key])
        for v in obj.values():
            _walk(v, key, out)
    elif isinstance(obj, list):
        for v in obj:
            _walk(v, key, out)


def _find_all(obj, key):
    out = []
    _walk(obj, key, out)
    return out


def _continuation_token(obj):
    for c in _find_all(obj, "continuationCommand"):
        if isinstance(c, dict) and "token" in c:
            return c["token"]
    return None


def duration_text_to_seconds(text):
    """'1:02:03' → 3723 ; '5:56' → 356 ; texte non numérique (LIVE, UPCOMING) → 0."""
    parts = text.strip().split(":")
    if not all(p.isdigit() for p in parts):
        return 0
    total = 0
    for p in parts:
        total = total * 60 + int(p)
    return total


def views_text_to_int(text):
    """'17K views' → 17000 ; '1.2M views' → 1200000 ; 'No views' → 0."""
    m = re.match(r"([\d.,]+)\s*([KMB]?)", text.strip(), re.I)
    if not m:
        return 0
    n = float(m.group(1).replace(",", ""))
    mult = {"": 1, "K": 1_000, "M": 1_000_000, "B": 1_000_000_000}[m.group(2).upper()]
    return int(n * mult)


def relative_date_to_days(text):
    """'3 days ago' → 3 ; 'Streamed 2 years ago' → 730 ; None si non reconnu."""
    t = re.sub(r"^(Streamed|Premiered)\s+", "", text.strip(), flags=re.I)
    if re.match(r"today|just now|\d+\s+(second|minute|hour)s?\s+ago", t, re.I):
        return 0
    if re.match(r"yesterday", t, re.I):
        return 1
    m = re.match(r"(\d+)\s+(day|week|month|year)s?\s+ago", t, re.I)
    if not m:
        return None
    return int(m.group(1)) * {"day": 1, "week": 7, "month": 30, "year": 365}[m.group(2).lower()]


def _parse_lockup(lockup):
    meta = lockup.get("metadata", {}).get("lockupMetadataViewModel", {})
    title = meta.get("title", {}).get("content", "")
    channel, views_text, date_text = "", "", ""
    rows = _find_all(meta, "metadataRows")
    parts_rows = []
    for row_list in rows:
        for row in row_list:
            parts_rows.append([p.get("text", {}).get("content", "") for p in row.get("metadataParts", [])])
    for parts in parts_rows:
        for p in parts:
            if re.search(r"views?$", p, re.I):
                views_text = p
            elif re.search(r"ago$|today|yesterday", p, re.I):
                date_text = p
            elif not channel:
                channel = p
    duration_text = ""
    for badge in _find_all(lockup, "thumbnailBadgeViewModel"):
        text = badge.get("text", "")
        if re.match(r"^[\d:]+$", text):
            duration_text = text
    return {
        "id": lockup.get("contentId", ""),
        "title": title,
        "credits": channel,
        "duration_sec": duration_text_to_seconds(duration_text),
        "views": views_text_to_int(views_text),
        "date_text": date_text,
        "age_days": relative_date_to_days(date_text) if date_text else None,
    }


def list_playlist(playlist_id, stop_at_ids=None, max_pages=None, delay=0.5, log=print):
    """Itère sur les vidéos d'une playlist, de la plus récente à la plus ancienne.

    stop_at_ids : ensemble d'identifiants déjà connus ; l'itération s'arrête dès qu'une page
    ne contient plus aucune vidéo nouvelle (mode incrémental).
    """
    html = fetch(PLAYLIST_URL.format(playlist_id))
    m = re.search(r"ytInitialData\s*=\s*(\{.*?\});\s*</script>", html, re.S)
    if not m:
        raise RuntimeError("ytInitialData introuvable dans la page playlist")
    data = json.loads(m.group(1))
    version = re.search(r'"INNERTUBE_CLIENT_VERSION":"([^"]+)"', html)
    client_version = version.group(1) if version else "2.20240101.00.00"
    stop_at_ids = stop_at_ids or set()
    page = 0
    while True:
        page += 1
        lockups = [l for l in _find_all(data, "lockupViewModel")
                   if l.get("contentType") == "LOCKUP_CONTENT_TYPE_VIDEO"]
        videos = [_parse_lockup(l) for l in lockups]
        videos = [v for v in videos if v["id"]]
        new = [v for v in videos if v["id"] not in stop_at_ids]
        log(f"  page {page} : {len(videos)} vidéos, {len(new)} nouvelles")
        for v in videos:
            yield v
        token = _continuation_token(data)
        if token is None or (stop_at_ids and not new) or (max_pages and page >= max_pages):
            return
        time.sleep(delay)
        body = json.dumps({
            "context": {"client": {"clientName": "WEB", "clientVersion": client_version,
                                   "hl": "en", "gl": "US"}},
            "continuation": token,
        }).encode()
        data = json.loads(fetch(BROWSE_URL, data=body, headers={
            "Content-Type": "application/json",
            "X-Youtube-Client-Name": "1",
            "X-Youtube-Client-Version": client_version,
        }))


def video_details(video_id):
    """Date de publication exacte (YYYY-MM-DD), durée et vues, lues sur la page de la vidéo."""
    html = fetch(WATCH_URL.format(video_id))

    def grab(key):
        m = re.search(r'"%s":\s*"([^"]*)"' % key, html)
        return m.group(1) if m else None

    published = grab("publishDate") or grab("uploadDate")
    length = grab("lengthSeconds")
    views = grab("viewCount")
    return {
        "published": published[:10] if published else None,
        "duration_sec": int(length) if length and length.isdigit() else None,
        "views": int(views) if views and views.isdigit() else None,
    }


def approx_date(age_days, reference=None):
    reference = reference or date.today()
    return (reference - timedelta(days=age_days)).isoformat()
