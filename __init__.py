# -*- coding: utf-8 -*-
"""
Planificateur d'études & Récompenses — module complémentaire pour Anki.

* Tu ajoutes tes examens (date + paquets) ; le module calcule combien de
  nouvelles cartes voir chaque jour pour les avoir toutes vues X jours avant
  l'examen, et peut régler automatiquement la limite du paquet.
* Système de motivation : XP, niveaux, séries de jours, badges, pièces et
  boutique de récompenses que tu choisis toi-même.
"""

import copy
import html
import json
import math
import os
import random
import re
import time
from datetime import date, datetime, timedelta

from aqt import gui_hooks, mw
from aqt.qt import (QAction, QDialog, QHBoxLayout, QLabel, QPushButton, QShortcut, Qt,
                    QTimer, QUrl, QVBoxLayout, QWidget)

try:
    from aqt.qt import QWebEnginePage, QWebEngineProfile, QWebEngineSettings, QWebEngineView
except ImportError:
    try:
        from PyQt6.QtWebEngineCore import QWebEnginePage, QWebEngineProfile, QWebEngineSettings
        from PyQt6.QtWebEngineWidgets import QWebEngineView
    except ImportError:
        QWebEngineView = None
from aqt.utils import tooltip
from aqt.webview import AnkiWebView

from . import shop
from . import village

try:
    from aqt.qt import qconnect
except ImportError:  # très vieilles versions
    def qconnect(signal, func):
        signal.connect(func)

try:
    from aqt.theme import theme_manager
except ImportError:
    theme_manager = None

ADDON_DIR = os.path.dirname(os.path.abspath(__file__))
USER_DIR = os.path.join(ADDON_DIR, "user_files")
WEB_FILE = os.path.join(ADDON_DIR, "web", "dashboard.html")
ADDON_MODULE = __name__


# ───────────────────────────────────────────── configuration

def conf():
    c = mw.addonManager.getConfig(ADDON_MODULE) or {}

    def g(key, default):
        try:
            return int(c.get(key, default))
        except (TypeError, ValueError):
            return default

    return {
        "buffer": g("marge_jours_defaut", 3),
        "default_goal": g("objectif_revisions_sans_examen", 100),
        "xp_rev": g("xp_par_revision", 2),
        "xp_new": g("xp_bonus_nouvelle_carte", 3),
        "bonus": g("bonus_objectif_atteint", 50),
        "notif_every": g("notification_toutes_les_n_cartes", 25),
        "video_price": max(1, g("prix_10_minutes_video", 300)),
        "coin_ease": {1: g("pieces_a_revoir", 1), 2: g("pieces_difficile", 3),
                      3: g("pieces_correct", 5), 4: g("pieces_facile", 5)},
        "coin_new": g("pieces_bonus_nouvelle_carte", 4),
        "coin_bonus": g("pieces_bonus_objectif", 100),
        "casino_ticket": g("casino_prix_billet", 100),
        "casino_bets": g("casino_mises_par_billet", 15),
        "casino_max": g("casino_mise_max", 300),
        "video_url": str(c.get("site_video", "https://www.youtube.com")) or "https://www.youtube.com",
        "city": str(c.get("ville_meteo", "Paris")) or "Paris",
        "rain_bonus": g("bonus_pluie_pourcent", 20),
    }


def video_packs(c):
    p = c["video_price"]
    return [{"minutes": 10, "cost": p}, {"minutes": 20, "cost": round(p * 1.85)},
            {"minutes": 45, "cost": round(p * 4)}]


def video_site_name(c):
    u = c["video_url"].lower()
    if "youtube" in u:
        return "YouTube"
    return u.split("//")[-1].split("/")[0].replace("www.", "")


# ───────────────────────────────────────────── données (un fichier par profil)

DEFAULT_REWARDS = [
    {"id": 1, "name": "Une pause café / pâtisserie", "cost": 200},
    {"id": 2, "name": "Un épisode de ma série", "cost": 300},
    {"id": 3, "name": "Une soirée sans étudier", "cost": 1000},
    {"id": 4, "name": "Un petit achat plaisir", "cost": 2000},
]

_state = None
_state_path = None


def _path():
    os.makedirs(USER_DIR, exist_ok=True)
    name = mw.pm.name if (mw.pm and mw.pm.name) else "profil"
    safe = "".join(ch if (ch.isalnum() or ch in "-_") else "_" for ch in name)
    return os.path.join(USER_DIR, f"donnees_{safe}.json")


def S():
    """Retourne l'état (chargé depuis le disque si nécessaire)."""
    global _state, _state_path
    p = _path()
    if _state is None or _state_path != p:
        st = {}
        migrate = False
        if os.path.exists(p):
            try:
                with open(p, encoding="utf-8") as f:
                    st = json.load(f)
            except Exception:
                try:
                    os.replace(p, p + ".corrompu.bak")
                except OSError:
                    pass
                st = {}
            migrate = bool(st) and "scale_v2" not in st
        base = {
            "exams": [], "xp": 0, "coins": 0, "days": {}, "badges": {},
            "rewards": copy.deepcopy(DEFAULT_REWARDS), "purchases": [],
            "next_id": 100, "best_streak": 0, "last_auto": None,
            "owned": {}, "equipped": {}, "mascot_name": "", "tickets": 0,
            "boost": {"cards": 0}, "highscores": {}, "games_played": 0,
            "pending": None, "jackpot": False, "video_seconds": 0, "scale_v2": True,
            "kb_lock": False, "type_on": True, "pad_size": 1,
            "chests": 0, "chests_opened": 0, "quests_done": 0, "pumpkins": 0,
            "boss": {"idx": 0, "hp": None}, "bosses_down": 0,
            "univ": {"levels": {}, "energy": 0, "cash": 0.0, "last": None, "collected": 0},
            "specimens": {}, "packs": 0, "alert_day": None, "sound_on": True, "sound_vol": 0.5,
            "weather": None, "weather_loc": None, "gear": {}, "cos_lv": {},
        }
        for k, v in base.items():
            st.setdefault(k, v)
        for cat, free in (("theme", "classique"), ("wallpaper", "aucun"),
                          ("effect", "gains"), ("mascot", "hibou"), ("box_theme", "classique"),
                          ("box_font", "systeme"), ("corr", "rouge"), ("display", "bois")):
            st["owned"].setdefault(cat, [])
            if free not in st["owned"][cat]:
                st["owned"][cat].append(free)
        if migrate:  # nouvelle échelle des pièces : tout est multiplié par 2
            st["coins"] = int(st.get("coins", 0)) * 2
            for r in st.get("rewards", []):
                r["cost"] = int(r.get("cost", 0)) * 2
            st["scale_v2"] = True
            st["scale_msg"] = True
        if "moderne" not in st["owned"]["theme"]:
            st["owned"]["theme"].append("moderne")
        eq = st["equipped"]
        if not st.get("theme_v2"):  # nouveau thème gratuit par défaut
            if eq.get("theme", "classique") == "classique":
                eq["theme"] = "moderne"
            st["theme_v2"] = True
        eq.setdefault("theme", "moderne")
        eq.setdefault("wallpaper", "aucun")
        eq.setdefault("effects", ["gains"])
        eq.setdefault("mascot", "hibou")
        eq.setdefault("box_theme", "classique")
        eq.setdefault("box_font", "systeme")
        eq.setdefault("corr", "rouge")
        eq.setdefault("display", "bois")
        eq.setdefault("accessory", "aucun")
        for ex in st.get("exams", []):
            ex["auto"] = True  # l'ajustement quotidien est toujours actif
        if "meteo" in st["owned"].setdefault("wallpaper", []):  # ancien fond météo plein écran, retiré
            st["owned"]["wallpaper"].remove("meteo")
        if eq.get("wallpaper") == "meteo":
            eq["wallpaper"] = "aucun"
        st["owned"].setdefault("accessory", [])
        if "aucun" not in st["owned"]["accessory"]:
            st["owned"]["accessory"].append("aucun")
        st.setdefault("wall_side", "right")
        if "tracks" not in st:  # passage à la boutique en lignes d'évolution : on garde tes acquis
            st["tracks"] = {cat: shop.track_from_owned(cat, st["owned"].get(cat, []), st.get("cos_lv", {}))
                            for cat, *_r in shop.TRACKS}
            for cat, *_r in shop.TRACKS:
                track_sync(st, cat, equip=True)
            migrate = True
        _state, _state_path = st, p
        if migrate:
            save()
    return _state


def save():
    if _state is None or not _state_path:
        return
    tmp = _state_path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(_state, f, ensure_ascii=False, indent=1)
    os.replace(tmp, _state_path)


def new_id(st):
    st["next_id"] = int(st.get("next_id", 100)) + 1
    return st["next_id"]


def find(items, id_):
    for it in items:
        if str(it.get("id")) == str(id_):
            return it
    return None


# ───────────────────────────────────────────── temps (respecte l'heure de bascule d'Anki)

def day_cutoff():
    for attr in ("day_cutoff", "dayCutoff"):
        try:
            v = getattr(mw.col.sched, attr)
            if v:
                return int(v)
        except Exception:
            pass
    now = datetime.now()
    nxt = now.replace(hour=4, minute=0, second=0, microsecond=0)
    if nxt <= now:
        nxt += timedelta(days=1)
    return int(nxt.timestamp())


def anki_today(cutoff):
    return datetime.fromtimestamp(cutoff - 86400).date()


# ───────────────────────────────────────────── paquets

def deck_exists(did):
    try:
        return bool(mw.col.decks.get(int(did), default=False))
    except Exception:
        return False


def deck_name(did):
    try:
        d = mw.col.decks.get(int(did), default=False)
        return d["name"] if d else None
    except Exception:
        return None


def dids_for(exam):
    out = set()
    for did in exam.get("decks", []):
        if deck_exists(did):
            out.update(int(x) for x in mw.col.decks.deck_and_child_ids(int(did)))
    return out


def _in(ids):
    return "(" + ",".join(str(int(i)) for i in ids) + ")"


def set_new_limit(did, n):
    """Règle la limite « Ce paquet » de nouvelles cartes/jour (Anki 2.1.55+, planificateur v3)."""
    try:
        deck = mw.col.decks.get(int(did), default=False)
        if not deck or deck.get("dyn"):
            return False
        new = None if n is None else int(n)
        if deck.get("newLimit") == new:
            return True  # rien à changer
        deck["newLimit"] = new
        mw.col.decks.save(deck)
        return True
    except Exception as e:
        print("planificateur_etudes: impossible de régler la limite:", e)
        return False


# Nouvelles cartes vues pour la première fois aujourd'hui
INTRO_SQL = (
    "select count(distinct r.cid) from revlog r where r.ease > 0 and r.id >= ? {extra} "
    "and not exists (select 1 from revlog r2 where r2.cid = r.cid and r2.ease > 0 and r2.id < ?)"
)


# ───────────────────────────────────────────── planification

def exam_stats(ex, today, cutoff):
    db = mw.col.db
    try:
        ed = date.fromisoformat(ex["date"])
    except Exception:
        ed = today
    buffer = max(0, int(ex.get("buffer", 3)))
    deadline = ed - timedelta(days=buffer)
    r = {
        "id": ex["id"], "name": ex.get("name", "Examen"), "date": ed.isoformat(),
        "buffer": buffer, "deadline": deadline.isoformat(),
        "days_to_exam": (ed - today).days, "days_avail": (deadline - today).days + 1,
        "auto": bool(ex.get("auto")),
        "decks": [n for n in (deck_name(d) for d in ex.get("decks", [])) if n],
        "total": 0, "new_remaining": 0, "intro_today": 0, "reviews_today": 0,
        "due": 0, "target": 0, "seen_pct": 0, "met": True, "progress": 1.0,
        "status": "on", "advice": "",
    }
    if r["days_to_exam"] < 0:
        r.update(status="past", advice="Examen passé. Tu peux le supprimer de la liste.")
        return r
    dids = dids_for(ex)
    if not dids:
        r.update(status="nodeck", advice="Aucun paquet de cet examen n'existe (supprimé ?). Supprime l'examen et recrée-le.")
        return r

    ins = _in(dids)
    where = f"(did in {ins} or odid in {ins})"
    sub = f"select id from cards where {where}"
    start_ms = (cutoff - 86400) * 1000

    total = db.scalar(f"select count() from cards where {where}") or 0
    new_rem = db.scalar(f"select count() from cards where {where} and type = 0 and queue != -1") or 0
    due = db.scalar(
        f"select count() from cards where {where} and "
        "((queue in (2,3) and due <= ?) or (queue = 1 and due <= ?))",
        mw.col.sched.today, int(time.time()) + 1200,
    ) or 0
    intro = db.scalar(INTRO_SQL.format(extra=f"and r.cid in ({sub})"), start_ms, start_ms) or 0
    reviews = db.scalar(f"select count() from revlog where ease > 0 and id >= ? and cid in ({sub})", start_ms) or 0

    pool = new_rem + intro
    if new_rem == 0:
        status, target = "done", intro
        advice = "Toutes les nouvelles cartes sont vues 🎉 Phase révision : garde tes révisions dues à zéro chaque jour."
    elif r["days_avail"] >= 1:
        status, target = "on", math.ceil(pool / r["days_avail"])
        advice = (f"Rythme : {target} nouvelles cartes par jour pendant {r['days_avail']} jour(s), "
                  f"puis {buffer} jour(s) réservés aux révisions avant l'examen.")
    else:
        days = max(1, r["days_to_exam"])
        status, target = "late", math.ceil(pool / days)
        advice = (f"⚠️ La marge de {buffer} jour(s) est entamée : il reste {new_rem} nouvelles cartes "
                  f"à voir d'ici l'examen, soit {target} par jour.")

    # 🔥 mode tryhard : des nouvelles cartes en plus aujourd'hui pour alléger les jours suivants
    th = ex.get("tryhard") or {}
    extra = int(th.get("extra", 0)) if th.get("day") == today.isoformat() else 0
    days_left = r["days_avail"] if status == "on" else max(1, r["days_to_exam"])
    room = max(0, pool - max(intro, target))

    def _next(e):
        if days_left <= 1:
            return None
        return math.ceil(max(0, pool - max(intro, target + e)) / float(days_left - 1))

    options = []
    if status in ("on", "late") and room > 0:
        seen = set()
        for lab, e in (("½ journée", math.ceil(target / 2.0)), ("1 journée", target), ("2 journées", 2 * target)):
            e = min(room, max(1, e))
            if e in seen:
                continue
            seen.add(e)
            options.append({"label": lab, "extra": e, "next": _next(e)})
    # jours sans toucher à ce paquet sur la dernière semaine (depuis que tu as commencé à l'étudier)
    first = db.scalar(f"select min(id) from revlog where cid in ({sub})")
    start7 = (cutoff - 8 * 86400) * 1000
    window = 0 if not first else max(0, min(7, (start_ms - max(start7, int(first))) // 86400000 + (1 if first > start7 else 0)))
    studied = db.scalar(f"select count(distinct (id/1000 - ?)/86400) from revlog where id >= ? and id < ? and cid in ({sub})",
                        cutoff - 8 * 86400, start7, start_ms) or 0
    r.update(extra=extra, tryhard_done=bool(extra) and intro >= target + extra, tryhard_room=room,
             tryhard_options=options, next_target=_next(0), next_with_extra=_next(extra) if extra else None,
             days_left=days_left, missed7=max(0, int(window) - int(studied)))

    rev_done = max(0, reviews - intro)
    work = target + rev_done + due
    progress = (min(intro, target) + rev_done) / float(work) if work else 1.0
    r.update(
        total=total, new_remaining=new_rem, intro_today=intro, reviews_today=reviews,
        due=due, target=target, seen_pct=round(100 * (total - new_rem) / total) if total else 0,
        met=(intro >= target and due == 0), progress=progress,
        status=status, advice=advice,
    )
    return r


def today_status(cutoff, today):
    st = S()
    c = conf()
    db = mw.col.db
    start_ms = (cutoff - 86400) * 1000
    exams = sorted((exam_stats(e, today, cutoff) for e in st["exams"]),
                   key=lambda e: (e["date"], e["id"]))
    active = [e for e in exams if e["status"] in ("on", "late", "done")]
    rev_all = db.scalar("select count() from revlog where ease > 0 and id >= ?", start_ms) or 0
    intro_all = db.scalar(INTRO_SQL.format(extra=""), start_ms, start_ms) or 0
    coin_rev = 0
    eases = db.all("select ease, count() from revlog where ease > 0 and id >= ? group by ease", start_ms)
    for ease, n in eases:
        coin_rev += c["coin_ease"].get(min(4, int(ease)), 1) * int(n)
    if active:
        mode = "exams"
        met = all(e["met"] for e in active)
        pct = sum(e["progress"] for e in active) / len(active)
    else:
        mode = "default"
        goal = max(1, c["default_goal"])
        met = rev_all >= goal
        pct = min(1.0, rev_all / float(goal))
    return {"today": today, "cutoff": cutoff, "exams": exams, "active": active,
            "mode": mode, "met": met, "pct": pct, "rev_all": rev_all, "intro_all": intro_all,
            "coin_rev": coin_rev, "eases": [(int(e), int(n)) for e, n in eases]}


def apply_exam_limits(ex, today, cutoff, announce=False):
    s = exam_stats(ex, today, cutoff)
    if s["status"] in ("past", "nodeck"):
        return False
    decks = [int(d) for d in ex.get("decks", []) if deck_exists(d)]
    counts = {}
    for did in decks:
        ids = _in(mw.col.decks.deck_and_child_ids(did))
        counts[did] = mw.col.db.scalar(
            f"select count() from cards where (did in {ids} or odid in {ids}) and type = 0 and queue != -1") or 0
    tot = sum(counts.values())
    ok = True
    goal = s["target"] + int(s.get("extra", 0))
    for did in decks:
        share = math.ceil(goal * counts[did] / float(tot)) if tot else 0
        ok = set_new_limit(did, share) and ok
    ex["applied"] = True
    if announce:
        if ok:
            tooltip(f"✔ Limite réglée : {goal} nouvelles cartes aujourd'hui pour « {html.escape(s['name'])} »"
                    + (f" (dont {s['extra']} en mode tryhard 🔥)" if s.get("extra") else ""))
        else:
            tooltip("Impossible de régler la limite (Anki 2.1.55+ avec le planificateur v3 est requis).")
    return ok


def reset_exam_limits(ex):
    for did in ex.get("decks", []):
        if deck_exists(did):
            set_new_limit(int(did), None)
    ex["applied"] = False


def resync_limits(announce=False):
    """Recalcule les objectifs (ex. après avoir ajouté des cartes) et met à jour les limites des paquets."""
    if not mw.col:
        return []
    st = S()
    cutoff = day_cutoff()
    today = anki_today(cutoff)
    changed = []
    for ex in st["exams"]:
        s0 = exam_stats(ex, today, cutoff)
        if s0["status"] in ("past", "nodeck"):
            continue
        old = ex.get("last_target")
        if ex.get("auto"):
            apply_exam_limits(ex, today, cutoff)
        ex["last_target"] = s0["target"]
        if old is not None and old != s0["target"]:
            changed.append((s0["name"], old, s0["target"]))
    save()
    if announce:
        if changed:
            tooltip("🔄 Objectifs recalculés :<br>" + "<br>".join(
                f"« {html.escape(n)} » : {b} nouvelles cartes/jour (avant {a})" for n, a, b in changed), period=6000)
        else:
            tooltip("🔄 Objectifs à jour : rien n'a changé.")
    elif changed:
        tooltip("🔄 Tu as ajouté des cartes : objectif recalculé<br>" + "<br>".join(
            f"« {html.escape(n)} » : {b}/jour (avant {a})" for n, a, b in changed), period=5000)
    return changed


_resync_timer = None


def schedule_resync(*_):
    """Après un ajout de cartes : on attend un peu (tu en ajoutes souvent plusieurs d'affilée)."""
    global _resync_timer
    if _resync_timer is None:
        _resync_timer = QTimer(mw)
        _resync_timer.setSingleShot(True)
        qconnect(_resync_timer.timeout, lambda: (resync_limits(), refresh_main()))
    _resync_timer.start(2500)


def auto_apply_all(today, cutoff):
    for ex in S()["exams"]:
        try:
            ed = date.fromisoformat(ex["date"])
        except Exception:
            continue
        if ed < today:
            if ex.get("applied"):
                reset_exam_limits(ex)
        elif ex.get("auto"):
            apply_exam_limits(ex, today, cutoff)


# ───────────────────────────────────────────── récompenses

TITLES = ["Novice", "Curieux·se", "Apprenti·e", "Studieux·se", "Assidu·e", "Méthodique",
          "Érudit·e", "Expert·e", "Maître des cartes", "Sage", "Légende d'Anki"]


def lvl_threshold(n):
    return 150 * (n - 1) * n  # niv. 2 = 300 XP, niv. 5 = 3000 XP, niv. 10 = 13 500 XP


def level_reward(n):
    """Pièces offertes en atteignant le niveau n."""
    return 50 * n


def cur_mascot():
    try:
        return S()["equipped"].get("mascot", "hibou")
    except Exception:
        return "hibou"


def next_reward(level):
    nxt = level + 1
    key = cur_mascot()
    evo = shop.mascot_stage(nxt, key) > shop.mascot_stage(level, key)
    return {"level": nxt, "coins": level_reward(nxt), "evolves": evo}


def level_info(xp):
    n = 1
    while xp >= lvl_threshold(n + 1):
        n += 1
    cur, nxt = lvl_threshold(n), lvl_threshold(n + 1)
    return {"n": n, "title": TITLES[min(n, len(TITLES)) - 1], "xp": xp,
            "cur": xp - cur, "need": nxt - cur, "pct": (xp - cur) / float(nxt - cur)}


BADGES = [
    ("premier", "🎯", "Premier objectif", "Atteindre l'objectif du jour une première fois"),
    ("serie3", "🔥", "En feu", "3 jours d'objectif d'affilée"),
    ("serie7", "🌟", "Semaine parfaite", "7 jours d'objectif d'affilée"),
    ("serie30", "👑", "Inarrêtable", "30 jours d'objectif d'affilée"),
    ("cent", "💯", "Centurion", "100 révisions en une journée"),
    ("trois_cents", "⚡", "Marathon", "300 révisions en une journée"),
    ("mille", "📚", "Bibliothèque vivante", "1 000 révisions au total"),
    ("leve_tot", "🌅", "Lève-tôt", "Réviser avant 8 h"),
    ("pret", "✅", "Prêt·e à temps", "Voir toutes les cartes d'un examen avant la date limite"),
    ("niveau5", "🎓", "Niveau 5", "Atteindre le niveau 5"),
    ("niveau10", "🏆", "Niveau 10", "Atteindre le niveau 10"),
    ("recompense", "🎁", "Bien mérité", "Échanger ta première récompense"),
    ("joueur", "🕹️", "Joueur·se", "Jouer ta première partie dans la salle de jeux"),
    ("jackpot", "🎰", "Jackpot !", "Gagner le gros lot à la roue ou au grattage"),
    ("collection", "🎨", "Collectionneur·se", "Acheter 3 personnalisations"),
    ("evolution", "✨", "Forme finale", "Faire évoluer ta mascotte au dernier stade"),
    ("flambeur", "🎲", "Coup de poker", "Gagner au moins 10 fois ta mise au casino"),
    ("quetes", "🗺️", "Aventurier·e", "Accomplir 10 quêtes du jour"),
    ("coffre", "🎁", "Chasseur·se de trésor", "Ouvrir ton premier coffre de série"),
    ("citrouilles", "🎃", "Chasse aux citrouilles", "Trouver 20 citrouilles pendant Halloween (édition limitée)"),
    ("boss1", "⚔️", "Tueur·se de boss", "Vaincre ton premier boss de révision"),
    ("boss5", "🐲", "Légende de l'arène", "Vaincre 5 boss de révision"),
    ("recteur", "🏰", "Recteur·rice", "Construire les 8 bâtiments de ton université"),
    ("campus", "🎓", "Campus prestigieux", "Atteindre 20 niveaux de bâtiments au total"),
    ("naturaliste", "🔎", "Naturaliste", "Découvrir 12 spécimens différents"),
    ("forgeron", "🔨", "Forgeron·ne", "Équiper les 5 pièces de ton héros"),
    ("legende", "👑", "Héros légendaire", "Forger une pièce en matériau Légendaire"),
    ("collection", "🧬", "Collection complète", "Découvrir les 24 spécimens"),
]

MSG_MET = [
    "Objectif du jour atteint 🎉 Tout ce que tu fais maintenant, c'est du bonus.",
    "Mission accomplie pour aujourd'hui ✅ Ton futur toi te remercie.",
    "C'est dans la boîte 🎉 Profite de ta pause, tu l'as méritée.",
]
MSG_HALF = [
    "Plus de la moitié de faite 💪 Le plus dur est derrière toi.",
    "Tu es sur la bonne pente, continue comme ça 🚀",
]
MSG_STARTED = [
    "Bien parti·e ! Chaque carte compte.",
    "La machine est lancée, garde le rythme 🔁",
]
MSG_ZERO = [
    "Une session de 10 minutes suffit pour lancer la journée 🚀",
    "Commence par quelques cartes : le reste suit tout seul.",
    "Ta série t'attend 🔥 Une petite session ?",
]


def goal_message(status):
    rnd = random.Random(status["today"].toordinal())
    if status["met"]:
        msg = rnd.choice(MSG_MET)
    elif status["pct"] >= 0.5:
        msg = rnd.choice(MSG_HALF)
    elif status["pct"] > 0:
        msg = rnd.choice(MSG_STARTED)
    else:
        msg = rnd.choice(MSG_ZERO)
    nxt = next((e for e in status["active"] if not e["met"]), None)
    if nxt and not status["met"]:
        todo = []
        rest = max(0, nxt["target"] - nxt["intro_today"])
        if rest:
            todo.append(f"{rest} nouvelle(s) carte(s)")
        if nxt["due"]:
            todo.append(f"{nxt['due']} révision(s)")
        if todo:
            msg += (f" Pour « {nxt['name']} » (dans {nxt['days_to_exam']} j) : encore "
                    + " et ".join(todo) + " aujourd'hui.")
    return msg


def catalog(cat):
    if cat == "accessory":
        return shop.ACCESSORIES
    return {"theme": shop.THEMES, "wallpaper": shop.WALLPAPERS,
            "effect": shop.EFFECTS, "mascot": shop.MASCOTS, "box_theme": shop.BOX_THEMES,
            "box_font": shop.BOX_FONTS, "corr": shop.CORR_STYLES,
            "display": shop.DISPLAYS}.get(cat, {})


# ───────────────────────────────────────────── boutique : lignes d'évolution

def track_level(st, cat):
    return max(0, min(shop.track_max(cat), int(st.setdefault("tracks", {}).get(cat, shop.track_start(cat)))))


def track_sync(st, cat, equip=False):
    """Recopie le niveau de la ligne dans « possédé / niveaux / équipé » (utilisés par tout le reste du module)."""
    lv = track_level(st, cat)
    owned = st["owned"].setdefault(cat, [])
    cl = st.setdefault("cos_lv", {})
    unlocked = shop.track_unlocked(cat, lv)
    for k, pol in unlocked:
        if k not in owned:
            owned.append(k)
        if shop.track_polish(cat) > 1:
            cl[f"{cat}:{k}"] = pol
    if not equip or not unlocked:
        return
    eq = st["equipped"]
    if cat in shop.CUMULATIVE:
        fx = eq.setdefault("effects", [])
        for k, _p in unlocked:
            if k not in fx and k not in st.setdefault("fx_seen", []):
                fx.append(k)
        st["fx_seen"] = [k for k, _p in unlocked]
    else:
        eq[cat] = shop.track_current(cat, lv)[0]


def style_preview(cat, k):
    it = catalog(cat)[k]
    row = {"key": k, "name": it["name"], "desc": it.get("desc", "")}
    if cat == "theme":
        row["swatch"] = list(it["light"]) if it["light"] else None
    elif cat == "wallpaper":
        row["preview"] = None if it["image"] == "none" else {"image": it["image"], "size": it["size"], "color": it["color"]}
    elif cat == "mascot":
        row["stages"] = [e for e, _n in it["stages"]]
    elif cat == "box_theme":
        row["box"] = {"bg": it["bg"], "ink": it["ink"], "border": it["border"],
                      "lines": it.get("lines", "none"), "shadow": it.get("shadow", "none")}
    elif cat == "box_font":
        row["font"] = it["stack"]
    elif cat == "corr":
        row["corr"] = {"kind": it["kind"], "value": it["value"], "ink": it.get("ink", "#1d1d1f")}
    return row


def tracks_view(st, plv):
    eq = st["equipped"]
    out = []
    for cat, title, icon, styles, polish, off in shop.TRACKS:
        lv = track_level(st, cat)
        mx = shop.track_max(cat)
        P = shop.track_polish(cat)
        cur_key, cur_pol = shop.track_current(cat, lv)
        cur_idx = styles.index(cur_key) if cur_key else -1
        t = {"cat": cat, "title": title, "icon": icon, "level": lv, "max": mx, "polish": P,
             "cur": dict(style_preview(cat, cur_key), pol=cur_pol) if cur_key else None,
             "road": [{"key": k, "name": catalog(cat)[k]["name"],
                       "state": "done" if (i < cur_idx or (cat in shop.CUMULATIVE and i <= cur_idx)) else ("cur" if i == cur_idx else "next"),
                       "need": 1 + shop.STYLE_LEVEL_STEP * i} for i, k in enumerate(styles)],
             "next": None}
        if cat in shop.CUMULATIVE:
            ul = shop.track_unlocked(cat, lv)
            t["road"] = [dict(r, state="done" if i < len(ul) else "next") for i, r in enumerate(t["road"])]
            t["fx"] = [{"key": k, "name": catalog(cat)[k]["name"], "pol": p, "on": k in eq.get("effects", []),
                        "desc": shop.lv_desc(cat, k)[p - 1]} for k, p in ul]
        else:
            if cur_key and P > 1:
                t["cur"]["lv_desc"] = shop.lv_desc(cat, cur_key)
            t["worn"] = eq.get(cat) == cur_key
            if off:
                t["off"] = {"key": off, "on": eq.get(cat) == off,
                            "label": "le look d'origine d'Anki" if cat == "theme" else "aucun fond"}
            ev = [k for k in st["owned"].get(cat, []) if catalog(cat).get(k, {}).get("event")]
            t["event_on"] = next((catalog(cat)[k]["name"] for k in ev if eq.get(cat) == k), None)
        if lv < mx:
            nk, label, desc = shop.track_label(cat, lv + 1)
            need = shop.track_need(cat, lv + 1)
            t["next"] = {"level": lv + 1, "cost": shop.track_cost(cat, lv + 1), "need": need, "locked": plv < need,
                         "label": label, "desc": desc, "new_style": shop.track_step(cat, lv + 1)[1] == 1,
                         "prev": style_preview(cat, nk)}
        out.append(t)
    return out


def track_upgrade(st, cat, plv, free=False):
    """Monte la ligne d'un cran. Retourne (ok, message)."""
    lv = track_level(st, cat)
    if lv >= shop.track_max(cat):
        return False, "Niveau maximum déjà atteint."
    need = shop.track_need(cat, lv + 1)
    if plv < need:
        return False, f"Ce style se débloque au niveau {need}."
    cost = 0 if free else shop.track_cost(cat, lv + 1)
    if st["coins"] < cost:
        return False, f"Il te manque {cost - st['coins']} 🪙"
    st["coins"] = int(st["coins"]) - cost
    st["tracks"][cat] = lv + 1
    track_sync(st, cat, equip=True)
    _k, label, desc = shop.track_label(cat, lv + 1)
    return True, f"✨ {html.escape(shop.TRACK[cat][1])} niveau {lv + 1} : {html.escape(label)}" + (f"<br>{html.escape(desc)}" if desc else "")


def mascot_now(st):
    m = shop.mascot_info(st["equipped"].get("mascot", "hibou"),
                         level_info(st["xp"])["n"], st.get("mascot_name", ""))
    m["emoji"] = shop.with_accessory(m["emoji"], st["equipped"].get("accessory"))
    return m


# ───────────────────────────────────────────── événement d'Halloween

def event_state(today=None):
    today = today or anki_today(day_cutoff())
    y = today.year
    if date(y, 10, 1) <= today <= date(y, 11, 2):
        return "on"
    if date(y, 9, 22) <= today < date(y, 10, 1):
        return "soon"
    return None


def event_view(st):
    today = anki_today(day_cutoff())
    e = event_state(today)
    return {"state": e, "pumpkins": int(st.get("pumpkins", 0)),
            "days": (date(today.year, 10, 1) - today).days if e == "soon" else
                    ((date(today.year, 11, 2) - today).days if e == "on" else 0)}


# ───────────────────────────────────────────── quêtes du jour

QUEST_POOL = [
    ("rev", "Réviser {n} cartes", [(50, 100), (80, 150), (120, 220)]),
    ("new", "Découvrir {n} nouvelles cartes", [(15, 120), (30, 200)]),
    ("combo", "Enchaîner {n} bonnes réponses d'affilée", [(15, 150), (30, 250)]),
    ("early", "Réviser {n} cartes avant 10 h", [(20, 150)]),
    ("finish", "Terminer un paquet", [(1, 200)]),
    ("goal", "Atteindre ton objectif du jour", [(1, 150)]),
    ("accuracy", "90 % de bonnes réponses sur au moins {n} cartes", [(40, 180)]),
]


def quests_for(st, today):
    q = st.get("quests")
    if not q or q.get("day") != today.isoformat():
        rnd = random.Random(today.toordinal() * 7 + 13)
        lst = []
        for i, (k, label, opts) in enumerate(rnd.sample(QUEST_POOL, 3)):
            n, rew = rnd.choice(opts)
            lst.append({"id": i, "type": k, "n": n, "reward": rew, "label": label.format(n=n), "done": False})
        q = {"day": today.isoformat(), "list": lst}
        st["quests"] = q
    return q


def quest_eval(qt, status, st):
    """Retourne (progression, objectif, texte de progression)."""
    db = mw.col.db
    start_ms = (status["cutoff"] - 86400) * 1000
    t, n = qt["type"], qt["n"]
    if t == "rev":
        return status["rev_all"], n, f"{min(status['rev_all'], n)}/{n}"
    if t == "new":
        return status["intro_all"], n, f"{min(status['intro_all'], n)}/{n}"
    if t == "combo":
        best = cur = 0
        for (e,) in db.all("select ease from revlog where ease > 0 and id >= ? order by id", start_ms):
            cur = cur + 1 if e > 1 else 0
            best = max(best, cur)
        return best, n, f"meilleure série : {min(best, n)}/{n}"
    if t == "early":
        ten = int(datetime.combine(status["today"], datetime.min.time()).replace(hour=10).timestamp() * 1000)
        c = db.scalar("select count() from revlog where ease > 0 and id >= ? and id < ?", start_ms, ten) or 0
        return c, n, f"{min(c, n)}/{n}"
    if t == "finish":
        c = len(casino_state(st).get("finished", []))
        return c, 1, "fait" if c else "pas encore"
    if t == "goal":
        return (1 if status["met"] else 0), 1, f"{round(status['pct'] * 100)} %"
    if t == "accuracy":
        tot = status["rev_all"]
        good = db.scalar("select count() from revlog where ease > 1 and id >= ?", start_ms) or 0
        pct = round(100 * good / tot) if tot else 0
        ok = tot >= n and pct >= 90
        return (n if ok else min(tot, n - 1)), n, f"{tot} cartes, {pct} % réussies"
    return 0, 1, ""


def check_quests(st, status, d, msgs):
    q = quests_for(st, status["today"])
    done_any = False
    for qt in q["list"]:
        if qt["done"]:
            continue
        cur, target, _txt = quest_eval(qt, status, st)
        if cur >= target:
            qt["done"] = True
            st["coins"] = int(st["coins"]) + qt["reward"]
            d["coins"] = int(d.get("coins", 0)) + qt["reward"]
            st["quests_done"] = int(st.get("quests_done", 0)) + 1
            msgs.append(f"📜 Quête accomplie : {qt['label']} ! +{qt['reward']} 🪙")
            done_any = True
    return done_any


def quests_view(st, status):
    out = []
    for qt in quests_for(st, status["today"])["list"]:
        cur, target, txt = quest_eval(qt, status, st)
        out.append({"label": qt["label"], "reward": qt["reward"], "done": qt["done"],
                    "pct": 1.0 if qt["done"] else min(1.0, cur / float(target or 1)), "txt": txt})
    return out


# ───────────────────────────────────────────── coffres de série

CHEST_COINS = [(400, 35), (600, 30), (900, 20), (1500, 10), (3000, 5)]


def open_chest(st):
    if int(st.get("chests", 0)) <= 0:
        return None
    st["chests"] = int(st["chests"]) - 1
    st["chests_opened"] = int(st.get("chests_opened", 0)) + 1
    coins = CHEST_COINS[weighted(CHEST_COINS)][0]
    st["coins"] = int(st["coins"]) + coins
    loot = [{"icon": "🪙", "text": f"+{coins}", "big": coins >= 1500}]
    r = random.random()
    if r < .15:
        pool = [(cat, k, it) for cat in ("theme", "wallpaper", "effect", "box_theme", "box_font", "corr", "display")
                for k, it in catalog(cat).items()
                if 0 < it.get("price", 0) <= 2400 and not it.get("event") and k not in st["owned"].get(cat, [])]
        if pool:
            cat, k, it = random.choice(pool)
            st["owned"].setdefault(cat, []).append(k)
            loot.append({"icon": "✨", "text": f"Objet rare : {it['name']} (déjà dans ta collection !)", "big": True})
    elif r < .40:
        st["tickets"] = int(st.get("tickets", 0)) + 2
        loot.append({"icon": "🎫", "text": "2 tickets de jeu gratuits", "big": False})
    elif r < .60:
        st.setdefault("boost", {"cards": 0})
        st["boost"]["cards"] = int(st["boost"].get("cards", 0)) + 50
        loot.append({"icon": "⚡", "text": "Boost ×2 pour tes 50 prochaines cartes", "big": False})
    return loot


def chest_view(st, today):
    s = streak(st, today)
    return {"count": int(st.get("chests", 0)), "streak": s, "progress": s % 7, "next_in": 7 - (s % 7)}


# ───────────────────────────────────────────── calendrier de l'année

def calendar_view(st, cutoff, today):
    days_n = 371  # 53 semaines
    base = cutoff - days_n * 86400
    rows = dict(mw.col.db.all(
        "select (id/1000 - ?)/86400 as d, count() from revlog where ease > 0 and id >= ? group by d",
        base, base * 1000))
    cells = []
    for i in range(days_n):
        dd = today - timedelta(days=days_n - 1 - i)
        cells.append([dd.isoformat(), int(rows.get(i, 0)), 1 if st["days"].get(dd.isoformat(), {}).get("goal") else 0])
    return cells


# ───────────────────────────────────────────── boss de révision

BOSS_DMG = {1: 0, 2: 1, 3: 2, 4: 2}  # Correct et Facile font autant de dégâts


BOSS_HP_GROWTH = 1.3          # chaque boss a 30 % de PV de plus que le précédent
BOSS_COOLDOWN = 12            # au moins 12 cartes entre deux contre-attaques
BOSS_RANKS = ["", "enragé", "ancestral", "cosmique", "légendaire", "éternel"]
# contre-attaques préférées de chaque boss (dans l'ordre de art.BOSSES)
BOSS_SIGNATURE = [["fog", "theft"], ["timer", "theft"], ["regen", "timer"], ["quiz", "shield"]]
BOSS_ATTACK_NAMES = {
    "quiz": ("📝", "Interro surprise"), "fog": ("💤", "Sieste collante"), "theft": ("🫳", "Vol de pièces"),
    "shield": ("🛡️", "Carapace"), "regen": ("⏳", "Retour en arrière"), "timer": ("⏱️", "Chrono-défi"),
}


def boss_max_hp(idx):
    return int(round(600 * BOSS_HP_GROWTH ** idx / 10.0)) * 10


def boss_loot_preview(idx, st=None):
    mult = 1 + (gear_stats(st)["loot"] if st else 0)
    return {"coins": int((500 + 160 * idx) * mult), "xp": int((150 + 35 * idx) * mult)}


def boss_fx(st):
    return st.setdefault("boss", {"idx": 0, "hp": None}).setdefault("fx", {})


def boss_fx_view(fx):
    out = []
    if fx.get("shield"):
        out.append({"icon": "🛡️", "label": f"Carapace {int(fx['shield'])}", "bad": True})
    if fx.get("fog"):
        out.append({"icon": "💤", "label": f"Dégâts ÷2 · {fx['fog']} carte{'s' if fx['fog'] > 1 else ''}", "bad": True})
    if fx.get("stun"):
        out.append({"icon": "💫", "label": f"Étourdi : dégâts ×2 · {fx['stun']} carte{'s' if fx['stun'] > 1 else ''}", "bad": False})
    ch = fx.get("challenge")
    if ch:
        out.append({"icon": "⏳", "label": f"Défi : {ch['got']}/{ch['need']} bonnes réponses d'affilée", "bad": True})
    if fx.get("timer"):
        out.append({"icon": "⏱️", "label": f"Réponds juste en moins de {fx['timer']['secs']} s", "bad": True})
    if fx.get("quiz"):
        out.append({"icon": "📝", "label": "Interro surprise en attente", "bad": True})
    if fx.get("belly"):
        out.append({"icon": "💰", "label": f"{int(fx['belly'])} 🪙 à récupérer en le battant", "bad": False})
    return out


def boss_now(st):
    b = st.setdefault("boss", {"idx": 0, "hp": None})
    idx = int(b.get("idx", 0))
    mx = boss_max_hp(idx)
    if b.get("hp") is None:
        b["hp"] = mx
    b["hp"] = min(int(b["hp"]), mx)
    n = len(shop.art.BOSSES)
    kind = shop.art.BOSSES[idx % n]
    cycle = idx // n
    name = kind["name"] + (f" {BOSS_RANKS[min(cycle, len(BOSS_RANKS) - 1)]}" if cycle else "")
    art = kind["art"]
    if cycle:  # même boss, mais d'une autre couleur et plus menaçant à chaque tour
        art = (f'<span style="display:inline-block;filter:hue-rotate({70 * cycle}deg) saturate({1 + .25 * cycle:.2f}) '
               f'drop-shadow(0 0 {2 + 2 * cycle}px rgba(255,60,60,.6))">{art}</span>')
    fx = b.get("fx", {})
    return {"idx": idx, "level": idx + 1, "name": name, "art": art, "taunt": kind["taunt"], "kind": idx % n,
            "hp": int(b["hp"]), "max": mx, "loot": boss_loot_preview(idx, st), "rage": int(b["hp"]) <= mx * .3,
            "shield": int(fx.get("shield", 0)), "fx": boss_fx_view(fx),
            "attacks": [BOSS_ATTACK_NAMES[k] for k in BOSS_SIGNATURE[idx % n]]}


def boss_heal(st, amount):
    b = st["boss"]
    cur = boss_now(st)
    b["hp"] = min(cur["max"], cur["hp"] + int(amount))
    return b["hp"] - cur["hp"]


def boss_hit(st, dmg, d):
    """Inflige des dégâts (la carapace absorbe d'abord) ; renvoie le butin si le boss tombe."""
    if dmg <= 0:
        return None
    b = st.setdefault("boss", {"idx": 0, "hp": None})
    fx = b.setdefault("fx", {})
    if fx.get("shield"):
        absorbed = min(int(fx["shield"]), int(dmg))
        fx["shield"] = int(fx["shield"]) - absorbed
        dmg -= absorbed
        if dmg <= 0:
            return None
    cur = boss_now(st)
    b["hp"] = max(0, cur["hp"] - dmg)
    if b["hp"] > 0:
        return None
    loot = boss_loot_preview(cur["idx"], st)
    items = [f"+{loot['coins']} 🪙", f"+{loot['xp']} XP"]
    add_gain(st, loot["xp"], loot["coins"], d)
    belly = int(fx.get("belly", 0))
    if belly:  # il recrache ce qu'il t'a volé, avec les intérêts
        back = int(belly * 1.5)
        st["coins"] = int(st["coins"]) + back
        items.append(f"+{back} 🪙 récupérées dans son ventre")
    if random.random() < .25:
        plv = level_info(st["xp"])["n"]
        pool = [c for c, *_r in shop.TRACKS
                if track_level(st, c) < shop.track_max(c) and shop.track_need(c, track_level(st, c) + 1) <= plv]
        if pool:
            cat = random.choice(pool)
            track_upgrade(st, cat, plv, free=True)
            items.append(f"Niveau offert : {shop.TRACK[cat][1]}")
    st["bosses_down"] = int(st.get("bosses_down", 0)) + 1
    st["packs"] = int(st.get("packs", 0)) + 1
    items.append("un sachet de spécimen 🧬")
    b["idx"] = cur["idx"] + 1
    b["hp"] = None
    b["fx"] = {}
    b["calm"] = 0
    nxt = boss_now(st)
    return {"name": cur["name"], "art": cur["art"], "items": items, "next": nxt["name"], "next_level": nxt["level"]}


# ── interro surprise : une de TES cartes déjà apprises, en QCM

_CLOZE = re.compile(r"\{\{c(\d+)::(.*?)(?:::(.*?))?\}\}", re.S)


def _plain(t):
    t = re.sub(r"\[sound:[^\]]*\]", " ", t or "")
    t = re.sub(r"<img[^>]*>", " 🖼️ ", t, flags=re.I)
    t = re.sub(r"<(br|div|p|li)[^>]*>", " ", t, flags=re.I)
    t = re.sub(r"<[^>]+>", "", t)
    return re.sub(r"\s+", " ", html.unescape(t)).strip()


def _note_qa(flds):
    f = flds.split("\x1f")
    m = _CLOZE.search(f[0])
    if m:
        q = _CLOZE.sub(lambda x: "[ … ]" if x.start() == m.start() else x.group(2), f[0])
        return _plain(q), _plain(m.group(2))
    if len(f) < 2:
        return None
    return _plain(f[0]), _plain(f[1])


def boss_quiz(did):
    db = mw.col.db
    ids = list(mw.col.decks.deck_and_child_ids(int(did))) if did else []
    where = f"(c.did in {_in(ids)} or c.odid in {_in(ids)})" if ids else "1=1"
    rows = db.all(f"select n.id, n.mid, n.flds from cards c join notes n on n.id = c.nid "
                  f"where {where} and c.type = 2 order by random() limit 30")
    for nid, mid, flds in rows:
        qa = _note_qa(flds)
        if not qa:
            continue
        q, ans = qa
        if not q or not ans or q == ans or len(ans) > 140 or "🖼️" in ans:
            continue
        others = []
        for (f2,) in db.all(f"select n.flds from cards c join notes n on n.id = c.nid "
                            f"where {where} and n.mid = ? and n.id != ? order by random() limit 40", mid, nid):
            qa2 = _note_qa(f2)
            if qa2 and qa2[1] and qa2[1] != ans and qa2[1] not in others and len(qa2[1]) <= 140 and "🖼️" not in qa2[1]:
                others.append(qa2[1])
            if len(others) == 3:
                break
        if len(others) < 3:
            continue
        choices = others + [ans]
        random.shuffle(choices)
        return {"q": q[:280], "choices": choices, "ok": choices.index(ans), "answer": ans}
    return None


# ── contre-attaques

def boss_attack(st, did=None, force=None):
    """Le boss riposte. Renvoie ce qu'il faut afficher pendant les révisions."""
    cur = boss_now(st)
    fx = boss_fx(st)
    idx, mx = cur["idx"], cur["max"]
    sig = BOSS_SIGNATURE[cur["kind"]]
    weights = {"quiz": 3, "fog": 1, "theft": 1, "shield": 1, "regen": 1, "timer": 1}
    for k in sig:
        weights[k] += 3
    order = [force] if force else []
    pool = dict(weights)
    while pool:
        k = random.choices(list(pool), weights=list(pool.values()))[0]
        order.append(k)
        pool.pop(k)
    for kind in order:
        icon, title = BOSS_ATTACK_NAMES[kind]
        base = {"type": kind, "icon": icon, "title": title, "boss": cur["name"], "art": cur["art"]}
        if kind == "quiz":
            q = boss_quiz(did)
            if not q:
                continue
            reward, heal = int(mx * .08), int(mx * .05)
            fx["quiz"] = dict(q, reward=reward, heal=heal)
            return dict(base, q=q["q"], choices=q["choices"],
                        text=f"Bonne réponse : contre-attaque de {reward} dégâts. Mauvaise : il se soigne de {heal} PV.")
        if kind == "fog":
            n = 6 + min(idx, 8)
            fx["fog"] = int(fx.get("fog", 0)) + n
            return dict(base, text=f"« Allez, une petite pause… » Tes dégâts sont divisés par 2 pendant {n} cartes.")
        if kind == "theft":
            amt = min(60 + 25 * idx, int(st["coins"] * (.03 + .005 * min(idx, 10))))
            if amt < 15:
                continue
            st["coins"] = int(st["coins"]) - amt
            fx["belly"] = int(fx.get("belly", 0)) + amt
            return dict(base, text=f"Il t'a volé {amt} 🪙 ! Bats-le pour les récupérer (+50 % d'intérêts).")
        if kind == "shield":
            n = int(mx * (.08 + .01 * min(idx, 7)))
            fx["shield"] = int(fx.get("shield", 0)) + n
            return dict(base, text=f"Une carapace de {n} points absorbe tes prochains coups.")
        if kind == "regen":
            need = min(8, 4 + idx // 3)
            heal = int(mx * (.06 + .005 * min(idx, 10)))
            fx["challenge"] = {"need": need, "got": 0, "heal": heal}
            return dict(base, text=f"Il essaie de remonter le temps ! Enchaîne {need} bonnes réponses pour l'étourdir, "
                                   f"sinon il récupère {heal} PV au premier « À revoir ».")
        if kind == "timer":
            secs = max(5, 10 - idx // 2)
            fx["timer"] = {"secs": secs, "start": None}
            return dict(base, text=f"Réponds juste à la prochaine carte en moins de {secs} secondes "
                                   f"pour un coup critique. Trop lent : tu seras distrait 5 cartes.")
    return None


def boss_maybe_attack(st, ease, did):
    """Une petite chance de riposte après chaque carte (plus souvent quand il est enragé)."""
    b = st.setdefault("boss", {"idx": 0, "hp": None})
    fx = b.setdefault("fx", {})
    if fx.get("quiz") or fx.get("challenge") or fx.get("timer"):
        return None
    b["calm"] = int(b.get("calm", 0)) + 1
    if b["calm"] < BOSS_COOLDOWN:
        return None
    cur = boss_now(st)
    p = .025 + .004 * min(cur["idx"], 10)
    if cur["idx"] == 0:
        p /= 2
    if cur["rage"]:
        p *= 2
    if ease == 1:  # tu as trébuché : il en profite
        p *= 1.8
    if random.random() >= p:
        return None
    b["calm"] = 0
    return boss_attack(st, did)


def boss_resolve(st, ease, d):
    """Après une réponse : défi en cours, chrono… Renvoie un message de résultat (ou None)."""
    fx = boss_fx(st)
    mx = boss_now(st)["max"]
    ch = fx.get("challenge")
    if ch:
        if ease >= 2:
            ch["got"] += 1
            if ch["got"] >= ch["need"]:
                fx.pop("challenge")
                fx["stun"] = int(fx.get("stun", 0)) + 10
                return {"ok": True, "text": "💫 Défi réussi ! Le boss est étourdi : dégâts ×2 pendant 10 cartes."}
        else:
            fx.pop("challenge")
            healed = boss_heal(st, ch["heal"])
            return {"ok": False, "text": f"⏳ Raté… il remonte le temps et récupère {healed} PV."}
    tm = fx.get("timer")
    if tm and tm.get("start"):
        fx.pop("timer")
        took = time.time() - float(tm["start"])
        if ease >= 3 and took <= tm["secs"]:
            dmg = int(mx * .05)
            down = boss_hit(st, dmg, d)
            return {"ok": True, "text": f"⚡ Réponse éclair en {took:.1f} s : coup critique de {dmg} dégâts !", "down": down, "dmg": dmg}
        fx["fog"] = int(fx.get("fog", 0)) + 5
        return {"ok": False, "text": f"⏱️ Trop lent ({took:.0f} s) ou raté : tu es distrait, dégâts ÷2 pendant 5 cartes."}
    return None


def boss_answer_quiz(st, choice, d):
    fx = boss_fx(st)
    q = fx.pop("quiz", None)
    if not q:
        return None
    if int(choice) == int(q["ok"]):
        down = boss_hit(st, q["reward"], d)
        return {"ok": True, "good": q["ok"], "dmg": q["reward"], "down": down,
                "text": f"Exact ! Ta contre-attaque lui inflige {q['reward']} dégâts ⚔️"}
    healed = boss_heal(st, q["heal"])
    return {"ok": False, "good": q["ok"], "text": f"Raté… La bonne réponse était « {q['answer']} ». Il récupère {healed} PV."}


# ───────────────────────────────────────────── université

def univ_state(st):
    u = st.setdefault("univ", {"levels": {}, "energy": 0, "cash": 0.0, "last": None, "collected": 0})
    u.setdefault("levels", {})
    return u


def univ_rate(u):
    base = sum(rate * int(u["levels"].get(k, 0)) for k, _n, _c, rate, _l, _d in shop.UNIV)
    return base * (1 + .05 * int(u["levels"].get("hall", 0)))


def univ_storage(u):
    return 600 + 1000 * int(u["levels"].get("hall", 0))


def univ_cost(key, level):
    base = next(c for k, _n, c, *_r in shop.UNIV if k == key)
    return int(round(base * (1.8 ** level) / 10.0)) * 10


def univ_tick(st):
    """Fait tourner le campus depuis la dernière visite, tant qu'il reste de l'énergie."""
    u = univ_state(st)
    now = time.time()
    last = u.get("last") or now
    minutes = max(0.0, (now - last) / 60.0)
    run = min(minutes, float(u.get("energy", 0)))
    u["energy"] = max(0.0, float(u.get("energy", 0)) - run)
    u["cash"] = min(univ_storage(u), float(u.get("cash", 0)) + univ_rate(u) * run / 60.0)
    u["last"] = now
    return u


def univ_view(st):
    u = univ_tick(st)
    lvl = level_info(st["xp"])["n"]
    blds = []
    for k, name, _c, rate, need, desc in shop.UNIV:
        cur = int(u["levels"].get(k, 0))
        blds.append({"key": k, "name": name, "level": cur, "max": shop.UNIV_MAX, "desc": desc, "need": need,
                     "locked": lvl < need, "cost": univ_cost(k, cur) if cur < shop.UNIV_MAX else None,
                     "rate": rate, "art": shop.art.BUILDINGS_ART[k]})
    wx = weather_now(st)
    students = 40 * int(u["levels"].get("residence", 0)) + 10 * sum(int(v) for v in u["levels"].values())
    total = sum(int(v) for v in u["levels"].values())
    for b in blds:
        cur = b["level"]
        b["mat"] = village.MATS[cur]["name"] if cur else ("Terrain verrouillé" if b["locked"] else "Terrain à bâtir")
        b["big"] = village.building_svg(b["key"], cur)
        if cur < shop.UNIV_MAX:
            b["next_art"] = village.building_svg(b["key"], cur + 1)
            b["next_mat"] = village.MATS[cur + 1]["name"]
    need = {b["key"]: b["need"] for b in blds if b["locked"] and b["level"] == 0}
    scene = village.campus_svg({b["key"]: b["level"] for b in blds}, need, total,
                               autumn=date.today().month in (9, 10, 11), snow=wx["snow"])
    return {"buildings": blds, "scene": scene, "total": total, "total_max": shop.UNIV_MAX * len(shop.UNIV),
            "rate": round(univ_rate(u)), "energy": int(u["energy"]), "energy_cap": shop.UNIV_ENERGY_CAP,
            "cash": int(u["cash"]), "storage": univ_storage(u), "students": students, "plot": shop.art.PLOT,
            "per_card": shop.UNIV_MIN_PER_CARD, "collected": int(u.get("collected", 0)),
            "night": wx["night"], "phase": wx["phase"], "snow": wx["snow"]}


# ───────────────────────────────────────────── prévisions des examens

def exam_forecast(ex, es, today, cutoff):
    """Rythme réel des 7 derniers jours → date de fin prévue des nouvelles cartes."""
    out = {"pace": 0.0, "finish": None, "margin": None, "state": "none", "label": ""}
    if es["status"] in ("past", "nodeck"):
        return out
    if es["new_remaining"] == 0:
        out.update(state="done", label="Nouvelles cartes terminées ✅")
        return out
    dids = dids_for(ex)
    ins = _in(dids)
    start = (cutoff - 7 * 86400) * 1000
    n7 = mw.col.db.scalar(INTRO_SQL.format(extra=f"and r.cid in (select id from cards where did in {ins} or odid in {ins})"),
                          start, start) or 0
    pace = n7 / 7.0
    out["pace"] = round(pace, 1)
    deadline = date.fromisoformat(es["deadline"])
    if pace <= 0:
        out.update(state="unknown", label="Pas encore de rythme mesuré")
        return out
    days = math.ceil(es["new_remaining"] / pace)
    finish = today + timedelta(days=max(0, days - 1))
    margin = (deadline - finish).days
    out.update(finish=finish.isoformat(), margin=margin)
    if margin > 0:
        out.update(state="ahead", label=f"En avance de {margin} j")
    elif margin == 0:
        out.update(state="ontime", label="Pile dans les temps")
    else:
        out.update(state="late", label=f"En retard de {-margin} j")
    return out


def deck_new_limit(did):
    """Limite effective de nouvelles cartes/jour d'un paquet (réglage « ce paquet » ou options du paquet)."""
    d = mw.col.decks.get(int(did), default=False)
    if not d:
        return 0
    if d.get("newLimit") is not None:
        return int(d["newLimit"])
    try:
        return int(mw.col.decks.config_dict_for_deck_id(int(did))["new"]["perDay"])
    except Exception:
        return None


def exam_plan(ex, es):
    """État du plan pour aujourd'hui : bien réglé ? fait ? à faire ?"""
    if es["status"] in ("past", "nodeck"):
        return {"state": "none", "label": "", "fixable": False}
    if es["new_remaining"] == 0:
        return {"state": "finished", "label": "Nouvelles cartes terminées ✅", "fixable": False}
    limits = [deck_new_limit(d) for d in ex.get("decks", []) if deck_exists(d)]
    known = [x for x in limits if x is not None]
    total_limit = sum(known) if known else None
    left = max(0, es["target"] - es["intro_today"])
    if total_limit is not None and total_limit < es["target"] and left > 0:
        return {"state": "notset", "label": f"⚠️ Réglé à {total_limit}/j au lieu de {es['target']}",
                "fixable": True, "limit": total_limit}
    if left == 0:
        return {"state": "done", "label": "✅ Fait aujourd'hui", "fixable": False}
    if es["status"] == "late":
        return {"state": "late", "label": f"Marge entamée : encore {left} nouvelles aujourd'hui", "fixable": False}
    return {"state": "todo", "label": f"À faire : {left} nouvelles aujourd'hui", "fixable": False}


def planning_view(st):
    cutoff = day_cutoff()
    today = anki_today(cutoff)
    out = []
    for ex in sorted(st["exams"], key=lambda e: e.get("date", "")):
        es = exam_stats(ex, today, cutoff)
        if es["status"] == "nodeck":
            continue
        fc = exam_forecast(ex, es, today, cutoff)
        out.append(dict(es, forecast=fc, plan=exam_plan(ex, es)))
    return out


# ───────────────────────────────────────────── spécimens

def open_pack(st):
    if int(st.get("packs", 0)) <= 0:
        return None
    st["packs"] = int(st["packs"]) - 1
    i = weighted([(r[0], r[1]) for r in shop.RARITIES])
    rar, _w, dup_coins, color = shop.RARITIES[i]
    key, emoji, name, _r = random.choice([x for x in shop.SPECIMENS if x[3] == rar])
    col = st.setdefault("specimens", {})
    new = key not in col
    col[key] = int(col.get(key, 0)) + 1
    bonus = 0 if new else dup_coins
    if bonus:
        st["coins"] = int(st["coins"]) + bonus
    return {"key": key, "emoji": emoji, "name": name, "rarity": rar, "rarity_label": shop.RARITY_LABEL[rar],
            "color": color, "new": new, "bonus": bonus}


def collection_view(st):
    col = st.get("specimens", {})
    color = {r[0]: r[3] for r in shop.RARITIES}
    items = [{"key": k, "emoji": e, "name": n, "rarity": r, "rarity_label": shop.RARITY_LABEL[r], "color": color[r],
              "count": int(col.get(k, 0))} for k, e, n, r in shop.SPECIMENS]
    return {"items": items, "got": len(col), "total": len(shop.SPECIMENS), "packs": int(st.get("packs", 0))}


# ───────────────────────────────────────────── météo (Open-Meteo, gratuit, sans compte)

def weather_kind(code):
    code = int(code)
    if code == 0 or code == 1:
        return "clear"
    if code in (2, 3):
        return "clouds"
    if code in (45, 48):
        return "fog"
    if code in (71, 73, 75, 77, 85, 86):
        return "snow"
    if code >= 95:
        return "storm"
    if 51 <= code <= 82:
        return "rain"
    return "clouds"


WEATHER_LABEL = {"clear": ("☀️", "Ciel dégagé"), "clouds": ("⛅", "Nuageux"), "fog": ("🌫️", "Brouillard"),
                 "rain": ("🌧️", "Pluie"), "snow": ("❄️", "Neige"), "storm": ("⛈️", "Orage")}


def weather_city(st):
    return st.get("weather_city") or conf()["city"]


def fetch_weather(city, loc):
    import urllib.parse
    import urllib.request
    if not loc or loc.get("q") != city:
        url = "https://geocoding-api.open-meteo.com/v1/search?" + urllib.parse.urlencode(
            {"name": city, "count": 1, "language": "fr"})
        with urllib.request.urlopen(url, timeout=8) as r:
            g = json.load(r)
        res = (g.get("results") or [None])[0]
        if not res:
            raise ValueError("ville introuvable")
        loc = {"q": city, "lat": res["latitude"], "lon": res["longitude"], "name": res.get("name", city)}
    url = ("https://api.open-meteo.com/v1/forecast?" + urllib.parse.urlencode(
        {"latitude": loc["lat"], "longitude": loc["lon"], "current": "temperature_2m,weather_code",
         "daily": "sunrise,sunset", "timezone": "auto", "forecast_days": 1}))
    with urllib.request.urlopen(url, timeout=8) as r:
        w = json.load(r)
    cur = w.get("current", {})
    daily = w.get("daily", {})
    return loc, {"code": int(cur.get("weather_code", 0)), "kind": weather_kind(cur.get("weather_code", 0)),
                 "temp": round(float(cur.get("temperature_2m", 0))), "city": loc["name"],
                 "sunrise": (daily.get("sunrise") or [None])[0], "sunset": (daily.get("sunset") or [None])[0],
                 "ts": time.time()}


_weather_busy = False


def refresh_weather(force=False):
    """Met à jour la météo en arrière-plan (au plus toutes les 30 minutes)."""
    global _weather_busy
    if _weather_busy or not mw.col:
        return
    st = S()
    city = weather_city(st)
    w = st.get("weather") or {}
    loc = st.get("weather_loc")
    if not force and w.get("ts", 0) > time.time() - 1800 and loc and loc.get("q") == city:
        return
    _weather_busy = True

    def done(fut):
        global _weather_busy
        _weather_busy = False
        try:
            new_loc, new_w = fut.result()
        except Exception as e:
            print("planificateur_etudes: météo indisponible :", e)
            if force:
                tooltip("Météo indisponible pour le moment (connexion ou ville introuvable).")
            return
        st2 = S()
        st2["weather_loc"], st2["weather"] = new_loc, new_w
        save()
        refresh_main()
        if _dlg:
            _dlg.refresh()

    try:
        mw.taskman.run_in_background(lambda: fetch_weather(city, loc), done)
    except Exception:
        _weather_busy = False


def day_phase(st):
    """aube / jour / crépuscule / nuit, d'après le vrai lever et coucher du soleil."""
    now = datetime.now()
    w = st.get("weather") or {}
    try:
        rise = datetime.fromisoformat(w["sunrise"]).replace(year=now.year, month=now.month, day=now.day)
        sset = datetime.fromisoformat(w["sunset"]).replace(year=now.year, month=now.month, day=now.day)
    except Exception:
        rise = now.replace(hour=6, minute=45)
        sset = now.replace(hour=19, minute=0)
    m = timedelta(minutes=45)
    if rise - m <= now <= rise + m:
        return "dawn"
    if sset - m <= now <= sset + m:
        return "dusk"
    if rise + m < now < sset - m:
        return "day"
    return "night"


def weather_now(st):
    w = st.get("weather") or {}
    fresh = w.get("ts", 0) > time.time() - 3 * 3600
    kind = w.get("kind", "clear") if fresh else "clear"
    phase = day_phase(st)
    month = datetime.now().month
    emoji, label = WEATHER_LABEL.get(kind, ("⛅", ""))
    if kind == "clear" and phase == "night":
        emoji, label = "🌙", "Nuit claire"
    return {"kind": kind, "phase": phase, "temp": w.get("temp"), "city": w.get("city") or weather_city(st),
            "fresh": fresh, "emoji": emoji, "label": label,
            "rain_bonus": conf()["rain_bonus"] if fresh and kind in ("rain", "storm") else 0,
            "night": phase == "night", "snow": kind == "snow" or month in (12, 1, 2)}


# ───────────────────────────────────────────── niveaux des cosmétiques

def cos_level(st, cat, key):
    if key not in st["owned"].get(cat, []):
        return 0
    return max(1, int(st.setdefault("cos_lv", {}).get(f"{cat}:{key}", 1)))


def fx_levels(st):
    return {k: cos_level(st, "effect", k) for k in st["equipped"].get("effects", [])}


# ───────────────────────────────────────────── héros et forge

def gear_tier(st, slot):
    return max(0, min(6, int(st.setdefault("gear", {}).get(slot, 0))))


def gear_stats(st):
    v = {slot: vals[gear_tier(st, slot)] for slot, _n, _i, _s, vals, _d in shop.GEAR}
    return {"dmg": int(v["arme"]), "crit": .12 + v["casque"] / 100.0, "critmult": 2 + v["bouclier"],
            "loot": v["armure"] / 100.0, "coins": v["amulette"] / 100.0}


def boss_dmg_today(status, stats):
    return sum((BOSS_DMG.get(min(4, int(e)), 0) + (stats["dmg"] if int(e) >= 2 else 0)) * int(n)
               for e, n in status.get("eases", []))


def hero_view(st):
    lvl = level_info(st["xp"])["n"]
    stats = gear_stats(st)
    g = dict(st.get("gear", {}))
    slots = []
    for slot, name, icon, statname, vals, _d in shop.GEAR:
        t = gear_tier(st, slot)
        nxt = None
        if t < 6:
            mat, need, cost = shop.TIERS[t + 1]
            prev = dict(g, **{slot: t + 1})
            nxt = {"tier": t + 1, "mat": mat, "need": need, "cost": cost, "desc": shop.gear_desc(slot, t + 1),
                   "locked": lvl < need, "color": shop.TIER_COLORS[t + 1], "preview": shop.art.avatar_svg(prev)}
        slots.append({"slot": slot, "name": name, "icon": icon, "stat": statname, "tier": t,
                      "mat": shop.TIERS[t][0] if t else "Aucun", "color": shop.TIER_COLORS[t] if t else "#adb5bd",
                      "desc": shop.gear_desc(slot, t) if t else "Rien d'équipé", "next": nxt})
    b = boss_now(st)
    per_hit = (2 + stats["dmg"]) * (1 + stats["crit"] * (stats["critmult"] - 1))
    return {"avatar": shop.art.avatar_svg(g), "slots": slots, "stats": stats,
            "power": sum(gear_tier(st, x[0]) for x in shop.GEAR),
            "hits_left": math.ceil(b["hp"] / per_hit) if per_hit else None, "per_hit": round(per_hit, 1)}


def day_entry(st, today):
    return st["days"].setdefault(today.isoformat(), {"rev": 0, "intro": 0, "goal": False, "xp": 0})


def streak(st, today):
    s, d = 0, today
    if not st["days"].get(d.isoformat(), {}).get("goal"):
        d -= timedelta(days=1)
    while st["days"].get(d.isoformat(), {}).get("goal"):
        s += 1
        d -= timedelta(days=1)
    return s


def add_gain(st, xp, coins, d):
    st["xp"] = int(st["xp"]) + max(0, xp)
    st["coins"] = int(st["coins"]) + max(0, coins)
    d["xp"] = int(d.get("xp", 0)) + max(0, xp)
    d["coins"] = int(d.get("coins", 0)) + max(0, coins)


def add_xp(st, amount, d):
    if amount <= 0:
        return
    st["xp"] = int(st["xp"]) + amount
    st["coins"] = int(st["coins"]) + amount
    d["xp"] = int(d.get("xp", 0)) + amount


def check_badges(st, status, today, d, from_review=False):
    s = streak(st, today)
    total = sum(int(x.get("rev", 0)) for x in st["days"].values())
    lvl = level_info(st["xp"])["n"]
    cond = {
        "premier": any(x.get("goal") for x in st["days"].values()),
        "serie3": s >= 3, "serie7": s >= 7, "serie30": s >= 30,
        "cent": d["rev"] >= 100, "trois_cents": d["rev"] >= 300,
        "mille": total >= 1000,
        "leve_tot": from_review and datetime.now().hour < 8,
        "pret": bool(status) and any(
            e["status"] == "done" and e["total"] > 0 and today <= date.fromisoformat(e["deadline"])
            for e in status["exams"]),
        "niveau5": lvl >= 5, "niveau10": lvl >= 10,
        "recompense": bool(st["purchases"]),
        "joueur": st.get("games_played", 0) > 0,
        "jackpot": bool(st.get("jackpot")),
        "collection": sum(1 for cat, keys in st["owned"].items() for k in keys
                          if catalog(cat).get(k, {}).get("price", 0) > 0) >= 3,
        "evolution": shop.mascot_stage(lvl, st["equipped"].get("mascot", "hibou"))
                     == len(shop.mascot_levels(st["equipped"].get("mascot", "hibou"))) - 1,
        "flambeur": bool(st.get("big_win")),
        "quetes": int(st.get("quests_done", 0)) >= 10,
        "coffre": int(st.get("chests_opened", 0)) >= 1,
        "citrouilles": int(st.get("pumpkins", 0)) >= 20,
        "boss1": int(st.get("bosses_down", 0)) >= 1,
        "recteur": all(int(st.get("univ", {}).get("levels", {}).get(k, 0)) > 0 for k, *_r in shop.UNIV),
        "campus": sum(int(v) for v in st.get("univ", {}).get("levels", {}).values()) >= 20,
        "naturaliste": len(st.get("specimens", {})) >= 12,
        "forgeron": all(int(st.get("gear", {}).get(x[0], 0)) > 0 for x in shop.GEAR),
        "legende": any(int(v) >= 6 for v in st.get("gear", {}).values()),
        "collection": len(st.get("specimens", {})) >= len(shop.SPECIMENS),
        "boss5": int(st.get("bosses_down", 0)) >= 5,
    }
    unlocked = []
    for key, icon, name, _desc in BADGES:
        if cond.get(key) and key not in st["badges"]:
            st["badges"][key] = today.isoformat()
            unlocked.append((icon, name))
    return unlocked


LAST = {"xp": 0, "msgs": [], "celebrate": False, "boost": False, "pct": 0.0}
SESSION = {"xp": 0, "cards": 0, "hits": 0, "miss": 0, "last_talk": 0}


def process(show=True, from_review=False):
    """Distribue l'XP, vérifie l'objectif du jour et les badges. Retourne le statut du jour."""
    st = S()
    c = conf()
    cutoff = day_cutoff()
    today = anki_today(cutoff)
    if st.get("last_auto") != today.isoformat():
        auto_apply_all(today, cutoff)
        st["last_auto"] = today.isoformat()

    status = today_status(cutoff, today)
    d = day_entry(st, today)
    msgs = []
    celebrate = False
    lvl_before = int(st.get("last_level") or level_info(st["xp"])["n"])

    # XP pour les révisions (compte aussi celles faites sur mobile puis synchronisées)
    new_rev = status["rev_all"] - int(d["rev"])
    new_intro = status["intro_all"] - int(d["intro"])
    gain = max(0, new_rev) * c["xp_rev"] + max(0, new_intro) * c["xp_new"]
    coin_today = status["coin_rev"] + status["intro_all"] * c["coin_new"]
    if "coins_rev" not in d:  # jour déjà compté avec l'ancienne formule
        d["coins_rev"] = coin_today if int(d["rev"]) > 0 else 0
    gain_coins = max(0, coin_today - int(d["coins_rev"]))
    d["coins_rev"] = max(int(d["coins_rev"]), coin_today)
    rb = weather_now(st)["rain_bonus"]
    if rb and gain_coins:
        gain_coins = int(round(gain_coins * (1 + rb / 100.0)))
    amu = gear_stats(st)["coins"]
    if amu and gain_coins:
        gain_coins = int(round(gain_coins * (1 + amu)))
    dmg_today = boss_dmg_today(status, gear_stats(st))
    if "dmg" not in d:  # ce qui a été révisé avant l'arrivée du boss ne compte pas
        d["dmg"] = dmg_today if int(d["rev"]) > 0 else 0
    boss_dmg = max(0, dmg_today - int(d["dmg"]))
    d["dmg"] = max(int(d["dmg"]), dmg_today)
    bfx = boss_fx(st)
    if new_rev > 0:  # effets de la dernière contre-attaque
        if bfx.get("fog"):
            k = min(int(bfx["fog"]), new_rev)
            boss_dmg -= int(round(boss_dmg * .5 * k / new_rev))
            bfx["fog"] = int(bfx["fog"]) - k
        if bfx.get("stun"):
            k = min(int(bfx["stun"]), new_rev)
            boss_dmg += int(round(boss_dmg * k / new_rev))
            bfx["stun"] = int(bfx["stun"]) - k
    boss_down = boss_hit(st, boss_dmg, d)
    if boss_down:
        msgs.append(f"⚔️ {boss_down['name']} est vaincu ! Butin : " + ", ".join(boss_down["items"]))
        celebrate = True
    boosted = False
    boost = st.setdefault("boost", {"cards": 0})
    if boost.get("cards", 0) > 0 and new_rev > 0:
        k = min(int(boost["cards"]), new_rev)
        gain += k * c["xp_rev"] + (max(0, new_intro) * c["xp_new"] if k else 0)
        gain_coins += round(gain_coins * k / float(new_rev))
        boost["cards"] = int(boost["cards"]) - k
        boosted = True
        if boost["cards"] == 0:
            msgs.append("⏱️ Ton boost XP ×2 est terminé.")
    old_rev = int(d["rev"])
    mkey = st["equipped"].get("mascot", "hibou")
    stage_before = shop.mascot_stage(lvl_before, mkey)
    mascot_before = mascot_now(st)
    d["rev"] = max(old_rev, status["rev_all"])
    d["intro"] = max(int(d["intro"]), status["intro_all"])
    add_gain(st, gain, gain_coins, d)
    if new_rev > 0:  # chaque carte fait tourner le campus
        u = univ_tick(st)
        u["energy"] = min(shop.UNIV_ENERGY_CAP, float(u["energy"]) + shop.UNIV_MIN_PER_CARD * new_rev)

    n = c["notif_every"]
    if n > 0 and d["rev"] // n > old_rev // n and not (status["met"] and not d["goal"]):
        msgs.append(f"💪 {d['rev']} cartes aujourd'hui ! (+{d['xp']} XP, +{d.get('coins', 0)} 🪙)")

    if status["met"] and not d["goal"]:
        d["goal"] = True
        s = streak(st, today)
        bonus = c["bonus"] + min(10 * (s - 1), 100)
        cbonus = c["coin_bonus"] + min(20 * (s - 1), 200)
        add_gain(st, bonus, cbonus, d)
        gain_coins += cbonus
        if s > 0 and s % 7 == 0:
            st["chests"] = int(st.get("chests", 0)) + 1
            msgs.append(f"🎁 {s} jours d'affilée : tu gagnes un coffre de série ! Ouvre-le dans le planificateur.")
        st["best_streak"] = max(int(st.get("best_streak", 0)), s)
        msgs.append(f"<b style='font-size:120%'>🎉 Objectif du jour atteint !</b><br>+{bonus} XP, +{cbonus} 🪙 · 🔥 série de {s} jour(s)")
        celebrate = True

    for es in status["active"]:  # 🔥 tryhard terminé
        ex = find(st["exams"], es["id"])
        th = (ex or {}).get("tryhard") or {}
        if es.get("tryhard_done") and not th.get("done"):
            th["done"] = True
            bonus_xp, bonus_c = 2 * es["extra"], 3 * es["extra"]
            add_gain(st, bonus_xp, bonus_c, d)
            gain_coins += bonus_c
            nxt = es.get("next_with_extra")
            msgs.append(f"<b>🔥 Tryhard réussi sur « {html.escape(es['name'])} » !</b> +{es['extra']} cartes d'avance, "
                        f"+{bonus_xp} XP, +{bonus_c} 🪙" + (f"<br>Demain : {nxt} nouvelles cartes seulement." if nxt is not None else ""))
            celebrate = True

    if check_quests(st, status, d, msgs):
        celebrate = True
    if from_review and event_state(today) == "on" and new_rev > 0 and random.random() < .05:
        st["pumpkins"] = int(st.get("pumpkins", 0)) + 1
        st["coins"] = int(st["coins"]) + 25
        msgs.append(f"🎃 Tu as trouvé une citrouille ! +25 🪙 ({st['pumpkins']} au total)")
    lvl = level_info(st["xp"])
    levelup = None
    if lvl["n"] > lvl_before:
        lvl_coins = sum(level_reward(n) for n in range(lvl_before + 1, lvl["n"] + 1))
        st["coins"] = int(st["coins"]) + lvl_coins
        d["coins"] = int(d.get("coins", 0)) + lvl_coins
        m = mascot_now(st)
        evolved = shop.mascot_stage(lvl["n"], mkey) > stage_before
        levelup = {"level": lvl["n"], "title": lvl["title"], "from": mascot_before["emoji"],
                   "from_name": mascot_before["stage"], "to": m["emoji"], "stage": m["stage"],
                   "name": st.get("mascot_name", ""), "evolved": evolved, "coins": lvl_coins}
        msgs.append(f"⬆️ Niveau {lvl['n']} : {lvl['title']} ! +{lvl_coins} 🪙")
        celebrate = True
        if evolved:
            msgs.append(f"✨ Ta mascotte a évolué : {m['emoji']} {html.escape(m['stage'])} !")
    for icon, name in check_badges(st, status, today, d, from_review):
        msgs.append(f"🏅 Badge débloqué : {icon} {name}")
        celebrate = True

    st["last_level"] = lvl["n"]
    save()
    SESSION["xp"] += gain
    LAST.update(xp=gain, coins=gain_coins, msgs=msgs, celebrate=celebrate, boost=boosted,
                pct=status["pct"], levelup=levelup, boss_dmg=boss_dmg, boss_down=boss_down)
    if show and msgs:
        tooltip("<br>".join(msgs), period=5000)
    return status


# ───────────────────────────────────────────── tableau de bord

def build_view():
    check_finished_decks(announce=True)
    st = S()
    c = conf()
    status = process(show=False)
    today = status["today"]
    lvl = level_info(st["xp"])

    base = status["cutoff"] - 14 * 86400
    rows = dict(mw.col.db.all(
        "select (id/1000 - ?)/86400 as d, count() from revlog where ease > 0 and id >= ? group by d",
        base, base * 1000))
    hist = []
    for i in range(14):
        dd = today - timedelta(days=13 - i)
        hist.append({"label": dd.strftime("%d/%m"), "count": rows.get(i, 0),
                     "goal": bool(st["days"].get(dd.isoformat(), {}).get("goal"))})

    decks = [{"id": str(d.id), "name": d.name}
             for d in mw.col.decks.all_names_and_ids(include_filtered=False)]
    decks.sort(key=lambda x: x["name"].lower())

    return {
        "night": bool(theme_manager and theme_manager.night_mode),
        "today": today.isoformat(),
        "level": lvl, "coins": st["coins"], "streak": streak(st, today),
        "best_streak": st.get("best_streak", 0),
        "goal": {"met": status["met"], "pct": status["pct"], "message": goal_message(status),
                 "mode": status["mode"], "rev_all": status["rev_all"],
                 "intro_all": status["intro_all"], "default_goal": c["default_goal"]},
        "exams": status["exams"],
        "decks": decks,
        "default_buffer": c["buffer"],
        "rewards": st["rewards"],
        "purchases": list(reversed(st["purchases"][-5:])),
        "badges": [{"key": k, "icon": i, "name": n, "desc": ds, "date": st["badges"].get(k)}
                   for k, i, n, ds in BADGES],
        "history": hist,
        "theme": shop.THEMES.get(st["equipped"]["theme"], {}).get("light") and {
            "light": shop.THEMES[st["equipped"]["theme"]]["light"],
            "dark": shop.THEMES[st["equipped"]["theme"]]["dark"]},
        "mascot": mascot_now(st),
        "mascot_custom": st.get("mascot_name", ""),
        "tickets": st.get("tickets", 0),
        "boost_cards": st.get("boost", {}).get("cards", 0),
        "games": [dict(g, key=k, best=st["highscores"].get(k)) for k, g in shop.GAMES.items()],
        "shop": [dict(sec, items=[it for it in sec["items"] if it["event"]]) for sec in shop_view(st, lvl["n"])
                 if any(it["event"] for it in sec["items"])],
        "tracks": tracks_view(st, lvl["n"]),
        "wall_side": st.get("wall_side", "right"),
        "casino": casino_view(st, status),
        "quests": quests_view(st, status),
        "boss": dict(boss_now(st), down=int(st.get("bosses_down", 0))),
        "univ": univ_view(st),
        "hero": hero_view(st),
        "sound": {"on": bool(st.get("sound_on", True)), "vol": float(st.get("sound_vol", .5))},
        "weather": weather_now(st),
        "weather_city": weather_city(st),
        "planning": planning_view(st),
        "collection": collection_view(st),
        "mascot_html": mascot_now(st)["emoji"],
        "chest": chest_view(st, today),
        "event": event_view(st),
        "calendar": calendar_view(st, status["cutoff"], today),
        "chest_svg": [shop.art.CHEST, shop.art.CHEST_OPEN],
        "next": next_reward(lvl["n"]),
        "coin_rates": {"again": c["coin_ease"][1], "hard": c["coin_ease"][2], "good": c["coin_ease"][3],
                       "easy": c["coin_ease"][4], "new": c["coin_new"], "goal": c["coin_bonus"]},
        "video": {"seconds": int(st.get("video_seconds", 0)), "packs": video_packs(c),
                  "site": video_site_name(c)},
    }


def shop_view(st, level):
    eq = st["equipped"]
    out = []
    for cat, title, items in (("theme", "Thèmes de couleurs", shop.THEMES),
                              ("wallpaper", "Fonds d'écran des révisions", shop.WALLPAPERS),
                              ("effect", "Effets pendant les révisions", shop.EFFECTS),
                              ("mascot", "Mascottes", shop.MASCOTS),
                              ("box_theme", "Case de réponse : thèmes", shop.BOX_THEMES),
                              ("box_font", "Case de réponse : polices", shop.BOX_FONTS),
                              ("corr", "Couleur de tes corrections", shop.CORR_STYLES),
                              ("display", "Vitrine de badges (écran d'accueil)", shop.DISPLAYS),
                              ("accessory", "Accessoires de ta mascotte", shop.ACCESSORIES)):
        rows = []
        for k, it in items.items():
            if it.get("event") and event_state() != "on" and k not in st["owned"].get(cat, []):
                continue  # objet d'événement : visible seulement pendant l'événement
            if cat == "effect":
                on = k in eq.get("effects", [])
            else:
                on = eq.get(cat) == k
            row = {"key": k, "name": it["name"], "price": it["price"],
                   "owned": k in st["owned"].get(cat, []), "on": on, "desc": it.get("desc", "")}
            if cat in shop.UPG_CATS and not (cat == "wallpaper" and k == "aucun") and not (cat == "theme" and k == "classique"):
                lv = cos_level(st, cat, k)
                row["lv"] = lv
                row["lv_desc"] = shop.lv_desc(cat, k)
                row["upg_cost"] = shop.upgrade_cost(it["price"], lv + 1) if 0 < lv < shop.UPG_MAX else None
            if cat == "theme":
                row["swatch"] = list(it["light"]) if it["light"] else None
            elif cat == "wallpaper":
                row["preview"] = None if it["image"] == "none" else {
                    "image": it["image"], "size": it["size"], "color": it["color"]}
            elif cat == "mascot":
                row["stages"] = [e for e, _n in it["stages"]]
            elif cat == "box_theme":
                row["box"] = {"bg": it["bg"], "ink": it["ink"], "border": it["border"],
                              "lines": it.get("lines", "none"), "shadow": it.get("shadow", "none")}
            elif cat == "box_font":
                row["font"] = it["stack"]
            elif cat == "accessory":
                row["svg"] = it["svg"]
                row["event"] = bool(it.get("event"))
            elif cat == "corr":
                row["corr"] = {"kind": it["kind"], "value": it["value"], "ink": it.get("ink", "#1d1d1f")}
            row["event"] = bool(it.get("event"))
            rows.append(row)
        if cat == "accessory" and len(rows) <= 1:
            continue
        out.append({"cat": cat, "title": title, "items": rows})
    return out


def apply_prize(st, kind, value):
    if kind == "coins":
        st["coins"] = int(st["coins"]) + int(value)
        return f"+{value} 🪙" if value else "Pas de chance cette fois…"
    if kind == "boost":
        st.setdefault("boost", {"cards": 0})
        st["boost"]["cards"] = int(st["boost"].get("cards", 0)) + int(value)
        return f"Boost XP ×2 pour tes {value} prochaines cartes ⚡"
    if kind == "ticket":
        st["tickets"] = int(st.get("tickets", 0)) + int(value)
        return f"{value} ticket(s) de partie gratuite 🎫" if int(value) > 1 else "Un ticket de partie gratuite 🎫"
    if kind == "lot":  # un niveau gratuit sur une ligne de la boutique
        plv = level_info(st["xp"])["n"]
        pool = [cat for cat, *_r in shop.TRACKS
                if track_level(st, cat) < shop.track_max(cat) and shop.track_need(cat, track_level(st, cat) + 1) <= plv]
        if pool:
            cat = random.choice(pool)
            _ok, msg = track_upgrade(st, cat, plv, free=True)
            refresh_cosmetics()
            return "🎁 Lot surprise : niveau offert !<br>" + msg
        st["coins"] = int(st["coins"]) + 400
        return "🎁 Lot surprise : +400 🪙 (ta boutique est au maximum pour ton niveau !)"
    return ""


def claim_pending(st):
    p = st.get("pending")
    if not p:
        return None
    st["pending"] = None
    value = int(p.get("value") or 0)
    if p.get("casino"):
        ca = casino_state(st)
        stake = int(p.get("stake", 0))
        ca["net"] = int(ca.get("net", 0)) + value - stake
        ca["total"] = int(ca.get("total", 0)) + value - stake
        if value >= 10 * stake > 0:
            st["big_win"] = True
        st["coins"] = int(st["coins"]) + value
        return (f"🎰 +{value} 🪙" if value else f"🎰 Mise perdue (-{stake} 🪙)")
    msg = apply_prize(st, p["kind"], value)
    if p.get("jackpot"):
        st["jackpot"] = True
    return msg


# ───────────────────────────────────────────── casino

ROUGES = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
SLOT_SYMBOLS = ["🍒", "🍋", "🔔", "⭐", "💎", "7️⃣"]
# (résultat, multiplicateur, poids) : jeu équitable, en moyenne on récupère exactement sa mise
SLOT_TABLE = [("7️⃣", 50, 0.3), ("💎", 20, 0.7), ("⭐", 10, 1.5), ("🔔", 5, 3.0),
              ("🍒", 3, 3.5), ("🍋", 3, 3.5), ("pair", 2.5, 8.0), (None, 0, 79.5)]
PLINKO_MULTS = [51.17, 11.94, 4.26, 1.88, 1.11, 0.6, 0.29, 0.6, 1.11, 1.88, 4.26, 11.94, 51.17]  # équitable
MINES_OPTIONS = (3, 5, 10)


def mines_mult(m, k):
    """Multiplicateur équitable après k cases sûres avec m mines sur 25."""
    r = 1.0
    for i in range(k):
        r *= (25 - i) / float(25 - m - i)
    return r


ROULETTE_BETS = {"rouge": "Rouge", "noir": "Noir", "pair": "Pair", "impair": "Impair",
                 "manque": "1 à 18", "passe": "19 à 36"}


def casino_state(st):
    today = anki_today(day_cutoff()).isoformat()
    ca = st.setdefault("casino", {})
    if ca.get("day") != today:
        ca.update(day=today, bets=0, net=0, finished=[], finished_names=[])
    ca.setdefault("finished", [])
    ca.setdefault("finished_names", [])
    return ca


def check_finished_decks(announce=True):
    """Chaque paquet terminé aujourd'hui donne une entrée au casino."""
    if not mw.col:
        return
    st = S()
    ca = casino_state(st)
    c = conf()
    try:
        tree = mw.col.sched.deck_due_tree()
    except Exception:
        return
    start_ms = (day_cutoff() - 86400) * 1000
    won = []
    for node in getattr(tree, "children", []):
        did = int(getattr(node, "deck_id", 0))
        if not did or did in ca["finished"]:
            continue
        if getattr(node, "new_count", 1) or getattr(node, "learn_count", 1) or getattr(node, "review_count", 1):
            continue
        ids = _in(mw.col.decks.deck_and_child_ids(did))
        n = mw.col.db.scalar(
            f"select count() from revlog where ease > 0 and id >= ? and cid in "
            f"(select id from cards where did in {ids} or odid in {ids})", start_ms) or 0
        if n > 0:
            ca["finished"].append(did)
            ca["finished_names"].append(getattr(node, "name", "paquet"))
            ca["bets"] = int(ca.get("bets", 0)) + c["casino_bets"]
            st["packs"] = int(st.get("packs", 0)) + 1
            won.append(getattr(node, "name", "paquet"))
    if won:
        save()
        if announce:
            tooltip("🎟️ Paquet terminé : " + ", ".join(html.escape(w) for w in won) +
                    f"<br>Tu gagnes une entrée au casino ({c['casino_bets']} mises) 🎰 et un sachet de spécimen 🧬", period=6000)


def choice_ok_mines(choice):
    try:
        n = int(choice)
    except (TypeError, ValueError):
        return None
    return n if n in MINES_OPTIONS else None


def slot_spin():
    i = weighted([(r[0], r[2]) for r in SLOT_TABLE])
    sym, mult, _w = SLOT_TABLE[i]
    if sym == "pair":
        a, b = random.sample(SLOT_SYMBOLS, 2)
        reels = [a, a, b]
        random.shuffle(reels)
    elif sym:
        reels = [sym] * 3
    else:
        reels = random.sample(SLOT_SYMBOLS, 3)
    return reels, mult


def roulette_win(choice, n):
    if choice.startswith("num:"):
        try:
            return 36 if int(choice[4:]) == n else 0
        except ValueError:
            return 0
    ok = {"rouge": n in ROUGES, "noir": n not in ROUGES, "pair": n % 2 == 0, "impair": n % 2 == 1,
          "manque": n <= 18, "passe": n >= 19}.get(choice, False)
    return 2 if ok else 0


def casino_view(st, status):
    c = conf()
    ca = casino_state(st)
    return {"bets": int(ca.get("bets", 0)), "finished": list(ca.get("finished_names", [])),
            "net": int(ca.get("net", 0)), "total": int(ca.get("total", 0)),
            "ticket_bets": c["casino_bets"], "max": c["casino_max"], "roulette": ROULETTE_BETS,
            "mines": list(MINES_OPTIONS), "plinko": PLINKO_MULTS}


def weighted(options):
    total = sum(o[-1] for o in options)
    x = random.uniform(0, total)
    for i, o in enumerate(options):
        x -= o[-1]
        if x <= 0:
            return i
    return len(options) - 1


def scratch_grid(win_symbol):
    syms = list(shop.SCRATCH_SYMBOLS)
    grid = []
    if win_symbol:
        grid += [win_symbol] * 3
        others = [x for x in syms if x != win_symbol]
    else:
        others = syms
    counts = {}
    while len(grid) < 9:
        x = random.choice(others)
        if counts.get(x, 0) < 2:
            counts[x] = counts.get(x, 0) + 1
            grid.append(x)
    random.shuffle(grid)
    return grid


def refresh_cosmetics():
    try:
        mw.toolbar.draw()
    except Exception:
        pass
    refresh_main()


def study_exam(ex):
    decks = [int(d) for d in (ex or {}).get("decks", []) if deck_exists(d)]
    if decks:
        mw.col.decks.select(decks[0])
        mw.moveToState("overview")
    else:
        mw.moveToState("deckBrowser")


def refresh_main():
    try:
        if mw.state == "deckBrowser":
            mw.deckBrowser.refresh()
        elif mw.state == "overview":
            mw.overview.refresh()
    except Exception:
        pass


class Dashboard(QDialog):
    def __init__(self):
        super().__init__(mw)
        self.setWindowTitle("Planificateur d'études")
        self.resize(940, 800)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        try:
            self.web = AnkiWebView(parent=self, title="planificateur_etudes")
        except TypeError:
            self.web = AnkiWebView(self)
        self.web.set_bridge_command(self.on_bridge, self)
        allow_sound(self.web)
        lay.addWidget(self.web)
        with open(WEB_FILE, encoding="utf-8") as f:
            page = (f.read().replace("/*SFX*/", shop.SFX_JS).replace("/*CONFETTI*/", shop.CONFETTI_JS).replace("/*WALLCSS*/", shop.WALL_CSS)
                    .replace("/*COINSVG*/", shop.art.COIN))
        self.web.stdHtml(page, context=self)
        st = S()
        msg = claim_pending(st)
        if msg:
            save()
            tooltip("Gain de ta dernière partie : " + msg)
        self.refresh()
        qconnect(self.finished, self._closed)

    def refresh(self):
        try:
            view = build_view()
        except Exception as e:
            view = {"error": str(e)}
        self.web.eval("render(%s);" % json.dumps(view, ensure_ascii=False, default=str))

    def _closed(self, *_):
        global _dlg
        _dlg = None
        try:
            self.web.cleanup()
        except Exception:
            pass

    @staticmethod
    def _equip(st, cat, key, force_on=False):
        eq = st["equipped"]
        if cat == "effect":
            fx = eq.setdefault("effects", [])
            if key in fx and not force_on:
                fx.remove(key)
            elif key not in fx:
                fx.append(key)
        else:
            eq[cat] = key

    def on_bridge(self, cmd):
        try:
            m = json.loads(cmd)
        except Exception:
            return None
        a = m.get("a")
        st = S()
        cutoff = day_cutoff()
        today = anki_today(cutoff)

        if a == "addExam":
            try:
                d = date.fromisoformat(m["date"]).isoformat()
            except Exception:
                tooltip("Date invalide.")
                return None
            ex = {"id": new_id(st), "name": str(m.get("name", "Examen"))[:80] or "Examen",
                  "date": d, "buffer": max(0, min(60, int(m.get("buffer", 3)))),
                  "decks": [int(x) for x in m.get("decks", [])], "auto": True}
            st["exams"].append(ex)
            if ex["auto"]:
                apply_exam_limits(ex, today, cutoff)
            tooltip("📅 Examen ajouté, ton plan est prêt !")
        elif a == "delExam":
            ex = find(st["exams"], m.get("id"))
            if ex:
                if ex.get("applied"):
                    reset_exam_limits(ex)
                st["exams"].remove(ex)
        elif a == "toggleAuto":
            ex = find(st["exams"], m.get("id"))
            if ex:
                ex["auto"] = not ex.get("auto")
                if ex["auto"]:
                    apply_exam_limits(ex, today, cutoff, announce=True)
        elif a == "apply":
            ex = find(st["exams"], m.get("id"))
            if ex:
                apply_exam_limits(ex, today, cutoff, announce=True)
        elif a == "fixExam":
            ex = find(st["exams"], m.get("id"))
            if ex:
                ex["auto"] = True
                apply_exam_limits(ex, today, cutoff, announce=True)
                refresh_main()
        elif a == "resetLimit":
            ex = find(st["exams"], m.get("id"))
            if ex:
                reset_exam_limits(ex)
                ex["auto"] = False
                tooltip("Limite du paquet remise selon ses options normales.")
        elif a == "study":
            ex = find(st["exams"], m["id"]) if m.get("id") else None
            if ex is None:
                status = today_status(cutoff, today)
                nxt = next((e for e in status["active"] if not e["met"]), None) or \
                    (status["active"][0] if status["active"] else None)
                ex = find(st["exams"], nxt["id"]) if nxt else None
            save()
            self.close()
            study_exam(ex)
            return None
        elif a == "play":
            key = m.get("game")
            g = shop.GAMES.get(key)
            if not g:
                return None
            if st.get("pending"):
                claim_pending(st)
            if int(st.get("tickets", 0)) > 0:
                st["tickets"] = int(st["tickets"]) - 1
                tooltip("🎫 Ticket gratuit utilisé")
            elif st["coins"] >= g["price"]:
                st["coins"] = int(st["coins"]) - g["price"]
            else:
                tooltip(f"Il te manque {g['price'] - st['coins']} 🪙 pour jouer. Au boulot 😉")
                return None
            st["games_played"] = int(st.get("games_played", 0)) + 1
            token = str(random.randint(10 ** 8, 10 ** 9))
            payload = {"game": key, "token": token}
            if key == "roue":
                i = weighted(shop.WHEEL)
                label, kind, value, _w = shop.WHEEL[i]
                st["pending"] = {"token": token, "kind": kind, "value": value,
                                 "jackpot": value >= 500}
                payload.update(index=i, labels=[w[0] for w in shop.WHEEL], label=label)
            elif key == "grattage":
                i = weighted(shop.SCRATCH)
                sym, kind, value, _w = shop.SCRATCH[i]
                if sym:
                    st["pending"] = {"token": token, "kind": kind, "value": value,
                                     "jackpot": value >= 500}
                    label = f"3 × {sym} : " + ({"coins": f"+{value} 🪙",
                                               "boost": f"boost XP ×2 ({value} cartes)",
                                               "ticket": f"{value} tickets de jeu gratuits",
                                               "lot": "un lot surprise de la boutique !"}[kind])
                else:
                    label = "Perdu… Retente ta chance !"
                payload.update(grid=scratch_grid(sym), win=sym, label=label)
            save()
            self.refresh()
            self.web.eval("startGame(%s);" % json.dumps(payload, ensure_ascii=False))
            refresh_main()
            return None
        elif a == "claim":
            p = st.get("pending")
            if p and p.get("token") == m.get("token"):
                msg = claim_pending(st)
                msgs = [msg] if msg and not p.get("casino") else []  # le casino affiche lui-même le résultat
                for icon, name in check_badges(st, None, today, day_entry(st, today)):
                    msgs.append(f"🏅 Badge débloqué : {icon} {name}")
                if msgs:
                    tooltip("<br>".join(msgs), period=4000)
        elif a == "score":
            key = m.get("game")
            try:
                score = max(0, int(m.get("score", 0)))
            except (TypeError, ValueError):
                score = 0
            if key in shop.GAMES:
                best = int(st["highscores"].get(key) or 0)
                if score > best:
                    st["highscores"][key] = score
                    if score > 0:
                        bonus = shop.GAMES[key]["price"] * shop.RECORD_MULT
                        add_gain(st, shop.RECORD_XP, bonus, day_entry(st, today))
                        tooltip(f"🏆 Nouveau record : {score} ! +{bonus} 🪙 et +{shop.RECORD_XP} XP")
                        self.web.eval("planifConfetti();")
                        process(show=True)  # montée de niveau éventuelle
        elif a == "buyItem":
            cat, key = m.get("cat"), m.get("key")
            it = catalog(cat).get(key)
            if it and it.get("event") and event_state() != "on":
                tooltip("Cet objet n'est disponible que pendant l'événement.")
                return None
            if it and key not in st["owned"].setdefault(cat, []):
                if st["coins"] < it["price"]:
                    tooltip(f"Il te manque {it['price'] - st['coins']} 🪙")
                    return None
                st["coins"] = int(st["coins"]) - it["price"]
                st["owned"][cat].append(key)
                self._equip(st, cat, key, force_on=True)
                msgs = [f"✨ {html.escape(it['name'])} débloqué et activé !"]
                for icon, name in check_badges(st, None, today, day_entry(st, today)):
                    msgs.append(f"🏅 Badge débloqué : {icon} {name}")
                tooltip("<br>".join(msgs), period=4000)
                self.web.eval("planifConfetti();")
                refresh_cosmetics()
        elif a == "equip":
            cat, key = m.get("cat"), m.get("key")
            if key in st["owned"].get(cat, []):
                self._equip(st, cat, key)
                refresh_cosmetics()
        elif a == "buyTime":
            c = conf()
            pack = next((pk for pk in video_packs(c) if pk["minutes"] == int(m.get("minutes", 0))), None)
            if pack:
                if st["coins"] < pack["cost"]:
                    tooltip(f"Il te manque {pack['cost'] - st['coins']} 🪙")
                    return None
                st["coins"] = int(st["coins"]) - pack["cost"]
                st["video_seconds"] = int(st.get("video_seconds", 0)) + pack["minutes"] * 60
                tooltip(f"📺 +{pack['minutes']} min de {video_site_name(c)} ajoutées !")
        elif a == "openVideo":
            save()
            open_video()
        elif a == "casinoTicket":
            c = conf()
            status = today_status(cutoff, today)
            if not status["met"]:
                tooltip("🔒 Le casino ouvre quand ton objectif du jour est atteint.")
                return None
            if st["coins"] < c["casino_ticket"]:
                tooltip(f"Il te manque {c['casino_ticket'] - st['coins']} 🪙 pour le billet.")
                return None
            st["coins"] = int(st["coins"]) - c["casino_ticket"]
            ca = casino_state(st)
            ca["bets"] = int(ca.get("bets", 0)) + c["casino_bets"]
            tooltip(f"🎟️ Billet validé : {c['casino_bets']} mises pour aujourd'hui. Bonne chance !")
        elif a == "casinoBet":
            c = conf()
            ca = casino_state(st)
            game = m.get("game")
            try:
                stake = int(m.get("stake", 0))
            except (TypeError, ValueError):
                stake = 0
            if st.get("pending"):
                claim_pending(st)
            if int(ca.get("bets", 0)) <= 0:
                tooltip("🎟️ Il te faut un billet d'entrée pour miser.")
                return None
            if stake < 1 or stake > c["casino_max"]:
                tooltip(f"La mise doit être entre 1 et {c['casino_max']} 🪙.")
                return None
            if stake > st["coins"]:
                tooltip("Tu n'as pas assez de pièces pour cette mise.")
                return None
            if game not in ("slots", "roulette", "fusee", "mines", "plinko"):
                return None
            if game == "mines" and choice_ok_mines(m.get("choice")) is None:
                tooltip("Choisis le nombre de mines.")
                return None
            choice = str(m.get("choice", ""))
            if game == "roulette" and not (choice in ROULETTE_BETS or
                                           (choice.startswith("num:") and choice[4:].isdigit()
                                            and 1 <= int(choice[4:]) <= 36)):
                tooltip("Choisis sur quoi miser.")
                return None
            st["coins"] = int(st["coins"]) - stake
            ca["bets"] = int(ca["bets"]) - 1
            token = str(random.randint(10 ** 8, 10 ** 9))
            payload = {"game": game, "token": token, "stake": stake, "choice": choice}
            pend = {"token": token, "kind": "coins", "value": 0, "casino": True, "stake": stake}
            if game == "slots":
                reels, mult = slot_spin()
                pend["value"] = int(stake * mult)
                payload.update(reels=reels, mult=mult, payout=pend["value"], symbols=SLOT_SYMBOLS)
            elif game == "roulette":
                n = random.randint(1, 36)  # pas de zéro : aucun avantage pour la maison
                mult = roulette_win(choice, n)
                pend["value"] = stake * mult
                payload.update(number=n, red=n in ROUGES, mult=mult, payout=pend["value"],
                               label=ROULETTE_BETS.get(choice) or ("n° " + choice[4:]))
            elif game == "mines":
                nm = choice_ok_mines(choice)
                pend.update(mines=random.sample(range(25), nm), m=nm, picked=[])
                payload.update(mines=nm, next=round(mines_mult(nm, 1), 2))
            elif game == "plinko":
                path = [random.randint(0, 1) for _ in range(12)]
                k = sum(path)
                mult = PLINKO_MULTS[k]
                pend["value"] = int(stake * mult)
                payload.update(path=path, slot=k, mult=mult, payout=pend["value"], mults=PLINKO_MULTS)
            else:
                u = random.random()
                crash = max(1.0, math.floor(100 / (1 - u)) / 100.0)  # équitable : P(≥ m) = 1/m
                crash = min(crash, 1000.0)
                pend.update(crash=crash, value=0)
                payload.update(crash=crash)
            st["pending"] = pend
            save()
            self.refresh()
            self.web.eval("startGame(%s);" % json.dumps(payload, ensure_ascii=False))
            return None
        elif a in ("minesPick", "minesCash"):
            p = st.get("pending")
            if not (p and p.get("token") == m.get("token") and "mines" in p):
                return None
            if a == "minesPick":
                try:
                    idx = int(m.get("idx"))
                except (TypeError, ValueError):
                    return None
                if not 0 <= idx < 25 or idx in p["picked"]:
                    return None
                if idx in p["mines"]:
                    p["value"] = 0
                    claim_pending(st)
                    save()
                    self.web.eval("minesBoom(%d,%s);" % (idx, json.dumps(p["mines"])))
                    self.refresh()
                    return None
                p["picked"].append(idx)
                k = len(p["picked"])
                mult = mines_mult(p["m"], k)
                pay = int(p["stake"] * mult)
                if k >= 25 - p["m"]:  # toutes les cases sûres trouvées : on encaisse
                    a = "minesCash"
                else:
                    save()
                    self.web.eval("minesSafe(%d,%.2f,%.2f,%d);" % (idx, mult, mines_mult(p["m"], k + 1), pay))
                    return None
            if a == "minesCash":
                k = len(p["picked"])
                if k == 0:
                    return None
                mult = mines_mult(p["m"], k)
                p["value"] = int(p["stake"] * mult)
                mines = p["mines"]
                claim_pending(st)
                badges = [f"🏅 Badge débloqué : {icon} {name}" for icon, name in check_badges(st, None, today, day_entry(st, today))]
                save()
                self.web.eval("minesCashed(%d,%.2f,%s);" % (int(p["value"]), mult, json.dumps(mines)))
                if badges:
                    tooltip("<br>".join(badges), period=3000)
                self.refresh()
                return None
        elif a == "casinoCashout":
            p = st.get("pending")
            if p and p.get("token") == m.get("token") and "crash" in p:
                try:
                    mult = float(m.get("m", 0))
                except (TypeError, ValueError):
                    mult = 0
                p["value"] = int(p["stake"] * mult) if 1.0 <= mult <= p["crash"] + 1e-9 else 0
                claim_pending(st)
                badges = [f"🏅 Badge débloqué : {icon} {name}" for icon, name in check_badges(st, None, today, day_entry(st, today))]
                if badges:
                    tooltip("<br>".join(badges), period=3000)
        elif a == "minesCancel":
            # table quittée avant d'avoir retourné une case : mise et billet rendus
            p = st.get("pending")
            if p and p.get("token") == m.get("token") and "mines" in p and not p.get("picked"):
                p["value"] = int(p["stake"])
                claim_pending(st)
                ca = casino_state(st)
                ca["bets"] = int(ca.get("bets", 0)) + 1
        elif a == "openChest":
            loot = open_chest(st)
            if loot:
                msgs = []
                for icon, name in check_badges(st, None, today, day_entry(st, today)):
                    msgs.append(f"🏅 Badge débloqué : {icon} {name}")
                save()
                self.web.eval("startGame(%s);" % json.dumps({"game": "chest", "loot": loot}, ensure_ascii=False))
                if msgs:
                    QTimer.singleShot(3500, lambda: tooltip("<br>".join(msgs), period=4000))
                return None
        elif a == "refresh":
            pass
        elif a == "setCity":
            city = str(m.get("city", "")).strip()[:60]
            if city:
                st["weather_city"] = city
                save()
                refresh_weather(force=True)
                tooltip(f"📍 Météo réglée sur {html.escape(city)}…")
        elif a == "sound":
            if "on" in m:
                st["sound_on"] = bool(m["on"])
            if "vol" in m:
                try:
                    st["sound_vol"] = max(0.0, min(1.0, float(m["vol"])))
                    st["sound_on"] = True
                except (TypeError, ValueError):
                    pass
        elif a == "univBuild":
            key = m.get("key")
            u = univ_tick(st)
            b = next((x for x in shop.UNIV if x[0] == key), None)
            if b:
                cur = int(u["levels"].get(key, 0))
                if level_info(st["xp"])["n"] < b[4]:
                    tooltip(f"Débloqué au niveau {b[4]}.")
                    return None
                if cur >= shop.UNIV_MAX:
                    return None
                cost = univ_cost(key, cur)
                if st["coins"] < cost:
                    tooltip(f"Il te manque {cost - st['coins']} 🪙")
                    return None
                st["coins"] = int(st["coins"]) - cost
                u["levels"][key] = cur + 1
                msgs = [f"🏗️ {b[1]} {'construite' if cur == 0 else 'améliorée'} (niveau {cur + 1}) !"]
                for icon, name in check_badges(st, None, today, day_entry(st, today)):
                    msgs.append(f"🏅 Badge débloqué : {icon} {name}")
                tooltip("<br>".join(msgs), period=4000)
                self.web.eval("planifConfetti();")
        elif a == "univCollect":
            u = univ_tick(st)
            got = int(u["cash"])
            if got > 0:
                u["cash"] = float(u["cash"]) - got
                u["collected"] = int(u.get("collected", 0)) + got
                st["coins"] = int(st["coins"]) + got
                tooltip(f"💰 Tu récoltes {got} 🪙 de ton université !")
        elif a == "openPack":
            res = open_pack(st)
            if res:
                msgs = []
                for icon, name in check_badges(st, None, today, day_entry(st, today)):
                    msgs.append(f"🏅 Badge débloqué : {icon} {name}")
                save()
                self.web.eval("startGame(%s);" % json.dumps({"game": "pack", "res": res}, ensure_ascii=False))
                if msgs:
                    QTimer.singleShot(3000, lambda: tooltip("<br>".join(msgs), period=4000))
                return None
        elif a == "resync":
            resync_limits(announce=True)
        elif a == "tryhard":
            ex = find(st["exams"], m.get("id"))
            if ex:
                es = exam_stats(ex, today, cutoff)
                n = max(0, min(int(es.get("tryhard_room", 0)), int(m.get("extra", 0) or 0)))
                ex["tryhard"] = {"day": today.isoformat(), "extra": n, "done": False}
                ex["auto"] = True
                apply_exam_limits(ex, today, cutoff)
                if n:
                    es = exam_stats(ex, today, cutoff)
                    tooltip(f"🔥 Mode tryhard : +{n} nouvelles cartes aujourd'hui pour « {html.escape(es['name'])} »"
                            + (f"<br>Si tu les fais, demain ce sera {es['next_with_extra']}/jour au lieu de {es['next_target']}."
                               if es.get("next_with_extra") is not None else ""), period=5000)
                else:
                    tooltip("Mode tryhard annulé : retour à l'objectif normal.")
                refresh_main()
        elif a == "trackUp":
            cat = m.get("cat")
            if cat in shop.TRACK:
                ok, msg = track_upgrade(st, cat, level_info(st["xp"])["n"])
                if not ok:
                    tooltip(msg)
                    return None
                msgs = [msg]
                for icon, name in check_badges(st, None, today, day_entry(st, today)):
                    msgs.append(f"🏅 Badge débloqué : {icon} {name}")
                tooltip("<br>".join(msgs), period=4500)
                self.web.eval("planifConfetti(2);")
                refresh_cosmetics()
        elif a == "trackEquip":
            cat = m.get("cat")
            if cat in shop.TRACK and cat not in shop.CUMULATIVE:
                k = shop.track_current(cat, track_level(st, cat))[0]
                if k:
                    st["equipped"][cat] = k
                    refresh_cosmetics()
        elif a == "upgradeItem":
            cat, key = m.get("cat"), m.get("key")
            it = catalog(cat).get(key)
            lv = cos_level(st, cat, key)
            if it and cat in shop.UPG_CATS and 0 < lv < shop.UPG_MAX:
                cost = shop.upgrade_cost(it["price"], lv + 1)
                if st["coins"] < cost:
                    tooltip(f"Il te manque {cost - st['coins']} 🪙")
                    return None
                st["coins"] = int(st["coins"]) - cost
                st.setdefault("cos_lv", {})[f"{cat}:{key}"] = lv + 1
                tooltip(f"✨ {html.escape(it['name'])} passe au niveau {lv + 1} ! {html.escape(shop.lv_desc(cat, key)[lv])}", period=4500)
                self.web.eval("planifConfetti(%d);" % (lv + 1))
                refresh_cosmetics()
        elif a == "forge":
            slot = m.get("slot")
            if slot in [x[0] for x in shop.GEAR]:
                t = gear_tier(st, slot)
                if t >= 6:
                    return None
                mat, need, cost = shop.TIERS[t + 1]
                if level_info(st["xp"])["n"] < need:
                    tooltip(f"Matériau {mat} débloqué au niveau {need}.")
                    return None
                if st["coins"] < cost:
                    tooltip(f"Il te manque {cost - st['coins']} 🪙")
                    return None
                st["coins"] = int(st["coins"]) - cost
                st["gear"][slot] = t + 1
                status = today_status(cutoff, today)  # pas de dégâts rétroactifs sur les cartes déjà faites
                day_entry(st, today)["dmg"] = boss_dmg_today(status, gear_stats(st))
                name = next(x[1] for x in shop.GEAR if x[0] == slot)
                msgs = [f"🔨 {name} en {mat} forgé(e) ! {shop.gear_desc(slot, t + 1)}"]
                for icon, bname in check_badges(st, None, today, day_entry(st, today)):
                    msgs.append(f"🏅 Badge débloqué : {icon} {bname}")
                tooltip("<br>".join(msgs), period=4500)
                self.web.eval("forgeFx();")
        elif a == "wallSide":
            if m.get("side") in ("left", "right", "off"):
                st["wall_side"] = m["side"]
                refresh_main()
        elif a == "renameMascot":
            st["mascot_name"] = str(m.get("name", "")).strip()[:24]
        elif a == "addReward":
            name = str(m.get("name", "")).strip()[:80]
            try:
                cost = max(1, int(m.get("cost", 100)))
            except (TypeError, ValueError):
                cost = 100
            if name:
                st["rewards"].append({"id": new_id(st), "name": name, "cost": cost})
        elif a == "delReward":
            r = find(st["rewards"], m.get("id"))
            if r:
                st["rewards"].remove(r)
        elif a == "buy":
            r = find(st["rewards"], m.get("id"))
            if r and st["coins"] >= r["cost"]:
                st["coins"] -= r["cost"]
                st["purchases"].append({"name": r["name"], "cost": r["cost"], "date": today.isoformat()})
                msgs = [f"🎁 Profite bien : {html.escape(r['name'])} !"]
                for icon, name in check_badges(st, None, today, day_entry(st, today)):
                    msgs.append(f"🏅 Badge débloqué : {icon} {name}")
                tooltip("<br>".join(msgs), period=4000)

        save()
        self.refresh()
        refresh_main()
        return None


# ───────────────────────────────────────────── récompense vidéo (YouTube)

_video_profile = None
_video = None
CHROME_UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
             "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")


def video_profile():
    global _video_profile
    if _video_profile is None:
        _video_profile = QWebEngineProfile("planif_video", mw)  # garde tes cookies d'une fois à l'autre
        _video_profile.setHttpUserAgent(CHROME_UA)
        try:
            _video_profile.settings().setAttribute(
                QWebEngineSettings.WebAttribute.FullScreenSupportEnabled, True)
        except Exception:
            pass
    return _video_profile


def fmt_time(sec):
    sec = max(0, int(sec))
    return f"{sec // 60:02d}:{sec % 60:02d}"


class VideoWindow(QDialog):
    def __init__(self):
        super().__init__(mw)
        c = conf()
        self.site = video_site_name(c)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.setWindowTitle(f"{self.site} — récompense")
        self.resize(1120, 740)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)
        self.top = QWidget(self)
        bar = QHBoxLayout(self.top)
        bar.setContentsMargins(12, 6, 12, 6)
        self.label = QLabel()
        self.label.setStyleSheet("font-size:15px;font-weight:600")
        bar.addWidget(self.label)
        bar.addStretch()
        self.more = QPushButton()
        qconnect(self.more.clicked, self.buy_more)
        bar.addWidget(self.more)
        pause = QPushButton("⏸ Pause (je garde mon temps)")
        qconnect(pause.clicked, self.close)
        bar.addWidget(pause)
        lay.addWidget(self.top)
        self.view = QWebEngineView(self)
        page = QWebEnginePage(video_profile(), self.view)
        self.view.setPage(page)
        try:
            page.fullScreenRequested.connect(self.on_fullscreen)
        except Exception:
            pass
        lay.addWidget(self.view, 1)
        self.view.setUrl(QUrl(c["video_url"]))
        self.over = False
        self.timer = QTimer(self)
        qconnect(self.timer.timeout, self.tick)
        self.timer.start(1000)
        self.tick(initial=True)

    def on_fullscreen(self, req):
        req.accept()
        if req.toggleOn():
            self.top.hide()
            self.showFullScreen()
        else:
            self.top.show()
            self.showNormal()

    def buy_more(self):
        st = S()
        c = conf()
        if st["coins"] >= c["video_price"]:
            st["coins"] = int(st["coins"]) - c["video_price"]
            st["video_seconds"] = int(st.get("video_seconds", 0)) + 600
            save()
            self.tick(initial=True)
            if _dlg:
                _dlg.refresh()

    def tick(self, initial=False):
        st = S()
        c = conf()
        if not initial and not self.over:
            st["video_seconds"] = max(0, int(st.get("video_seconds", 0)) - 1)
        left = int(st.get("video_seconds", 0))
        self.label.setText(f"📺 Temps restant : {fmt_time(left)}")
        self.more.setText(f"+10 min ({c['video_price']} 🪙)")
        self.more.setEnabled(st["coins"] >= c["video_price"])
        if not initial and left == 60:
            tooltip("⏱️ Plus qu'une minute de vidéo !", parent=self, period=4000)
        if left % 15 == 0:
            save()
        if left <= 0 and not self.over:
            self.over = True
            self.timer.stop()
            save()
            if self.isFullScreen():
                self.showNormal()
                self.top.show()
            self.view.setHtml(
                "<body style='font-family:system-ui;display:flex;align-items:center;justify-content:center;"
                "height:95vh;background:#152024;color:#fff;text-align:center'><div>"
                "<div style='font-size:60px'>⏰</div><h1>Temps écoulé !</h1>"
                "<p style='font-size:18px'>Retourne réviser quelques cartes pour gagner plus de temps 💪</p></div></body>")
            QTimer.singleShot(5000, self.close)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key.Key_Escape:  # Échap ne ferme pas la fenêtre (utile en plein écran)
            if self.isFullScreen():
                try:
                    self.view.page().triggerAction(QWebEnginePage.WebAction.ExitFullScreen)
                except Exception:
                    self.showNormal()
                    self.top.show()
            return
        super().keyPressEvent(e)

    def closeEvent(self, e):
        global _video
        self.timer.stop()
        save()
        try:
            self.view.setHtml("")  # coupe le son tout de suite
        except Exception:
            pass
        _video = None
        if _dlg:
            _dlg.refresh()
        super().closeEvent(e)


def open_video():
    global _video
    if QWebEngineView is None:
        tooltip("Ta version d'Anki ne permet pas d'ouvrir une page web ici.")
        return
    if int(S().get("video_seconds", 0)) <= 0:
        tooltip("Tu n'as plus de temps vidéo. Achètes-en dans la Salle de jeux 😉")
        return
    if _video is None:
        _video = VideoWindow()
    _video.show()
    _video.raise_()
    _video.activateWindow()


_dlg = None


def open_dashboard(*_, tab=None):
    global _dlg
    if not mw.col:
        return
    if _dlg is None:
        _dlg = Dashboard()
    else:
        _dlg.refresh()
    if tab:
        _dlg.web.eval("if(window.setTab)setTab(%s);" % json.dumps(tab))
    _dlg.show()
    _dlg.raise_()
    _dlg.activateWindow()


# ───────────────────────────────────────────── intégration à Anki

def summary_html():
    st = S()
    status = process(show=True)
    today = status["today"]
    lvl = level_info(st["xp"])
    s = streak(st, today)
    pct = round(100 * status["pct"])
    color = "#1f9e6e" if status["met"] else "#4f63d8"
    if status["met"]:
        line = "✅ Objectif du jour atteint, bravo !"
    else:
        line = f"Objectif du jour : {pct} %"
        nxt = next((e for e in status["active"] if not e["met"]), None)
        if nxt:
            line += (f" · 📅 {html.escape(nxt['name'])} dans {nxt['days_to_exam']} j : "
                     f"{nxt['intro_today']}/{nxt['target']} nouvelles, {nxt['due']} révisions dues")
    return f"""
<div id="planif-summary" style="max-width:560px;margin:18px auto 14px;padding:14px 18px;border-radius:16px;
            border:1px solid var(--planif-line,rgba(128,128,128,.3));background:var(--planif-surface,transparent);text-align:left">
  <div style="display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap">
    <b><span style="font-size:22px;vertical-align:middle">{mascot_now(st)['emoji']}</span> &nbsp;🔥 {s} j &nbsp; Niv. {lvl['n']} {html.escape(lvl['title'])} &nbsp; 🪙 {st['coins']}</b>
    <button onclick="pycmd('planif:open');return false;">Ouvrir le planificateur</button>
  </div>
  <div style="height:8px;background:rgba(128,128,128,.25);border-radius:6px;margin:10px 0 6px;overflow:hidden">
    <div style="height:100%;width:{pct}%;background:{color}"></div>
  </div>
  <div style="font-size:90%">{line}</div>
</div>"""


def wall_for_home():
    st = S()
    today = anki_today(day_cutoff()).isoformat()
    badges = [{"icon": i, "name": n, "desc": ds, "date": st["badges"].get(k)} for k, i, n, ds in BADGES]
    exams = [e for e in planning_view(st) if e["status"] in ("on", "late", "done")][:4]
    return shop.wall_html(badges, st["equipped"].get("display", "bois"), st.get("wall_side", "right"), today, exams,
                          cos_level(st, "display", st["equipped"].get("display", "bois")))


def on_deck_browser(deck_browser, content):
    try:
        # le résumé passe juste sous la liste des paquets (avant les statistiques d'Anki)
        content.stats = summary_html().replace("🪙", shop.art.COIN) + content.stats + wall_for_home()
    except Exception as e:
        print("planificateur_etudes:", e)


def on_js_message(handled, message, context):
    if message == "planif:open":
        open_dashboard()
        return (True, None)
    if message == "planif:open:badges":
        open_dashboard(tab="badges")
        return (True, None)
    if message.startswith("planif:fix:"):
        try:
            st = S()
            ex = find(st["exams"], message.rsplit(":", 1)[1])
            if ex:
                cutoff = day_cutoff()
                ex["auto"] = True
                apply_exam_limits(ex, anki_today(cutoff), cutoff, announce=True)
                save()
                refresh_main()
        except Exception as e:
            print("planificateur_etudes:", e)
        return (True, None)
    if message == "planif:open:planning":
        open_dashboard(tab="planning")
        return (True, None)
    if message in ("planif:undo", "planif:key:undo"):
        if S().get("type_on") and mw.state == "review":
            undo_last()
        return (True, None)
    if message.startswith("planif:quiz:"):
        try:
            st = S()
            d = day_entry(st, anki_today(day_cutoff()))
            res = boss_answer_quiz(st, int(message.rsplit(":", 1)[1]), d)
            save()
            if res and mw.reviewer and mw.reviewer.web:
                bd = boss_now(st)
                bd.update(dmg=res.get("dmg", 0), crit=bool(res.get("ok")), down=res.get("down"),
                          hero=shop.art.avatar_svg(st.get("gear", {})))
                bd.pop("taunt", None)
                mw.reviewer.web.eval("if(window.planifBossResult)planifBossResult(%s);" % json.dumps(res, ensure_ascii=False, default=str))
                mw.reviewer.web.eval("if(window.planifBoss)planifBoss(%s);" % json.dumps(bd, ensure_ascii=False))
        except Exception as e:
            print("planificateur_etudes:", e)
        return (True, None)
    if message == "planif:lock":
        toggle_kb_lock()
        return (True, None)
    if message.startswith("planif:type:"):
        st = S()
        st["type_on"] = message.endswith(":on")
        save()
        apply_kb_lock()
        push_reviewer_state(focus=True)
        return (True, None)
    if message == "planif:reveal" or message == "planif:key:reveal":
        if S().get("type_on"):
            reveal_answer()
        return (True, None)
    if message.startswith("planif:ease:") or (message.startswith("planif:key:") and message[-1] in "1234"):
        if S().get("type_on"):
            answer_with(int(message[-1]))
        return (True, None)
    if message == "planif:key:focus":
        if S().get("type_on") and mw.reviewer and mw.reviewer.web:
            mw.reviewer.web.setFocus()
            mw.reviewer.web.eval("if(window.planifTypeFocus)planifTypeFocus();")
        return (True, None)
    if message.startswith("planif:padsize:"):
        try:
            S()["pad_size"] = int(message.rsplit(":", 1)[1])
            save()
        except ValueError:
            pass
        return (True, None)
    return handled


def hud_data():
    st = S()
    lv = level_info(st["xp"])
    m = mascot_now(st)
    nr = next_reward(lv["n"])
    nxt = {"level": nr["level"], "coins": nr["coins"]}
    if nr["evolves"]:
        nxt["evo"] = shop.mascot_info(st["equipped"].get("mascot", "hibou"), nr["level"])["emoji"]
    wx = weather_now(st)
    return {"mascot": m["emoji"], "mname": st.get("mascot_name") or m["stage"],
            "fxlv": fx_levels(st), "hero": shop.art.avatar_svg(st.get("gear", {})),
            "wx": {"kind": wx["kind"] if wx["fresh"] else None, "phase": wx["phase"],
                   "temp": (st.get("weather") or {}).get("temp") if wx["fresh"] else None},
            "level": lv["n"], "xp_cur": lv["cur"], "xp_need": lv["need"], "next": nxt,
            "coins": st["coins"], "session_xp": SESSION["xp"], "pct": LAST.get("pct", 0),
            "effects": list(st["equipped"].get("effects", []))}


# ───────────────────────────────────────────── ce que dit la mascotte

def _pick(options):
    return random.choice(options)


CAT_LABEL = {"theme": "le thème", "wallpaper": "le fond d'écran", "effect": "l'effet", "mascot": "la mascotte",
             "box_theme": "la case", "box_font": "la police", "corr": "la couleur de correction",
             "display": "la vitrine"}


def cheapest_goal(st):
    """Prochaine amélioration à viser : la moins chère hors de portée, sinon la plus chère abordable."""
    out_reach, affordable = None, None
    plv = level_info(st["xp"])["n"]
    for cat, *_r in shop.TRACKS:
        lv = track_level(st, cat)
        if lv >= shop.track_max(cat) or shop.track_need(cat, lv + 1) > plv:
            continue
        cost = shop.track_cost(cat, lv + 1)
        item = (cost, f"{CAT_LABEL[cat]} au niveau {lv + 1} ({shop.track_label(cat, lv + 1)[1]})")
        if cost > st["coins"]:
            if out_reach is None or cost < out_reach[0]:
                out_reach = item
        elif affordable is None or cost > affordable[0]:
            affordable = item
    return out_reach or affordable


def companion_line(st, status, ease, d):
    today = status["today"].isoformat()
    if ease == 1:
        SESSION["miss"] += 1
        SESSION["hits"] = 0
    else:
        SESSION["hits"] += 1
        SESSION["miss"] = 0
    if SESSION["miss"] == 3:
        return _pick(["Pas grave ! C'est en se trompant qu'on retient le mieux 💡",
                      "Ces cartes résistent, mais elles vont finir par céder 😤",
                      "Respire un coup, on continue ensemble 🌿"])
    if SESSION["hits"] in (10, 25, 50, 100):
        return f"{SESSION['hits']} bonnes réponses d'affilée ! Tu es en feu 🔥"
    best = max((int(x.get("rev", 0)) for k, x in st["days"].items() if k != today), default=0)
    if best >= 20 and int(d["rev"]) > best and not d.get("record_said"):
        d["record_said"] = True
        return f"Nouveau record : {d['rev']} cartes en une journée ! Je suis fier de toi 🏆"
    if SESSION["cards"] - SESSION["last_talk"] < 9:
        return None
    SESSION["last_talk"] = SESSION["cards"]
    c = []
    nxt = next((e for e in status["active"] if not e["met"]), None)
    if nxt:
        rest = max(0, nxt["target"] - nxt["intro_today"]) + nxt["due"]
        if 0 < rest <= 25:
            c.append(f"Plus que {rest} cartes et c'est bouclé pour « {nxt['name']} » aujourd'hui !")
        if nxt["days_to_exam"] > 0:
            c.append(f"« {nxt['name']} » dans {nxt['days_to_exam']} jours, et tu as déjà vu "
                     f"{nxt['seen_pct']} % du paquet 💪")
    elif status["met"]:
        c.append("L'objectif du jour est atteint : tout ce qu'on fait là, c'est du bonus ✨")
    s = streak(st, status["today"])
    if s >= 2:
        c.append(f"{s} jours d'affilée ensemble, on ne casse pas la série 🔥")
    lv = level_info(st["xp"])
    nr = next_reward(lv["n"])
    need = lv["need"] - lv["cur"]
    if nr["evolves"]:
        c.append(f"Encore {need} XP et j'évolue ! J'ai trop hâte ✨")
    else:
        c.append(f"Encore {need} XP pour le niveau {nr['level']}, et {nr['coins']} 🪙 à la clé !")
    c.append(f"Déjà {SESSION['cards']} cartes cette session, belle concentration 🧠")
    goal = cheapest_goal(st)
    if goal:
        price, name = goal
        if st["coins"] >= price:
            c.append(f"Avec tes {st['coins']} 🪙, tu pourrais t'offrir {name} 😏")
        else:
            c.append(f"Plus que {price - st['coins']} 🪙 pour {name} 👀")
    if event_state(status["today"]) == "on":
        c += ["Joyeux Halloween ! 🎃 Chaque bonne réponse peut cacher une citrouille…",
              "Même les fantômes révisent leurs cartes 👻",
              f"Déjà {st.get('pumpkins', 0)} citrouilles trouvées, continue la chasse 🎃"]
    wx = weather_now(st)
    if wx["fresh"]:
        city = wx["city"]
        if wx["rain_bonus"]:
            c.append(f"Il pleut à {city} ☔ : +{wx['rain_bonus']} % de pièces, temps idéal pour réviser !")
        elif wx["kind"] == "snow":
            c.append(f"Il neige à {city} ❄️ : reste au chaud avec tes cartes.")
        elif wx["kind"] == "clear" and wx["phase"] == "day":
            c.append(f"Grand soleil à {city} ☀️ : une petite pause dehors après ta session ?")
        elif wx["phase"] == "dusk":
            c.append("Le soleil se couche 🌇 : belle lumière pour une dernière série de cartes.")
    bnow = boss_now(st)
    if bnow["hp"] <= bnow["max"] * .15:
        c.append(f"{bnow['name']} n'a plus que {bnow['hp']} PV, on l'achève ! ⚔️")
    elif bnow["hp"] >= bnow["max"] * .9:
        c.append(f"Un nouveau boss nous attend : {bnow['name']} ({bnow['max']} PV). À l'attaque ! ⚔️")
    q = st.get("quests", {})
    if q.get("day") == today:
        left = [x for x in q.get("list", []) if not x["done"]]
        if left:
            c.append(f"Quête du jour : « {left[0]['label']} », {left[0]['reward']} 🪙 à la clé 📜")
    h = datetime.now().hour
    if h >= 23 or h < 5:
        c.append("Il se fait tard… Le sommeil aide à fixer tout ça, pense à dormir 😴")
    elif h < 9:
        c.append("Réviser dès le matin, respect 🌅")
    if int(d["rev"]) >= 100:
        c.append(f"{d['rev']} cartes aujourd'hui, ton cerveau travaille dur 🧠💪")
    return _pick(c) if c else None


def on_answer(reviewer, card, ease):
    try:
        st = S()
        SESSION["cards"] += 1
        status = process(show=False, from_review=True)
        dday = day_entry(st, status["today"])
        if LAST["msgs"]:
            talk = " ".join(re.sub(r"<[^>]+>", " ", mm) for mm in LAST["msgs"])
            talk = re.sub(r"\s+", " ", talk).strip()
            companion_line(st, status, int(ease), dday)  # met à jour les séries
        else:
            talk = companion_line(st, status, int(ease), dday)
        d = hud_data()
        d.update(xp=LAST["xp"], gain_coins=LAST.get("coins", 0), ease=int(ease), talk=talk,
                 celebrate=LAST["celebrate"], boost=LAST["boost"])
        reviewer.web.eval("if(window.planifGain)planifGain(%s);" % json.dumps(d, ensure_ascii=False))
        # boss : coup critique de temps en temps (×2)
        dmg, crit, down = int(LAST.get("boss_dmg") or 0), False, LAST.get("boss_down")
        gs = gear_stats(st)
        if dmg > 0 and not down and int(ease) >= 3 and random.random() < gs["crit"]:
            crit = True
            extra = int(round(dmg * (gs["critmult"] - 1)))
            down = boss_hit(st, extra, dday)
            dmg += extra
            save()
        result = attack = None
        if not down:
            result = boss_resolve(st, int(ease), dday)
            if result and result.get("down"):
                down = result["down"]
            if result and result.get("dmg"):
                dmg += result["dmg"]
                crit = True
            if not down:
                attack = boss_maybe_attack(st, int(ease), card.odid or card.did)
            save()
        bd = boss_now(st)
        bd.update(dmg=dmg, crit=crit, down=down, hero=shop.art.avatar_svg(st.get("gear", {})))
        bd.pop("taunt", None)
        reviewer.web.eval("if(window.planifBoss)planifBoss(%s);" % json.dumps(bd, ensure_ascii=False))
        if result:
            reviewer.web.eval("if(window.planifBossResult)planifBossResult(%s);" % json.dumps(result, ensure_ascii=False, default=str))
        if attack:
            reviewer.web.eval("if(window.planifBossAttack)planifBossAttack(%s);" % json.dumps(attack, ensure_ascii=False))
        if LAST.get("levelup"):
            reviewer.web.eval("if(window.planifLevelUp)planifLevelUp(%s);"
                              % json.dumps(LAST["levelup"], ensure_ascii=False))
    except Exception as e:
        print("planificateur_etudes:", e)


_KB_DISABLED = []
_KB_ACTIONS = []  # (action du menu, ses raccourcis d'origine)
KEEP_SHORTCUTS = {"Ctrl+Q", "Meta+Q"}  # on garde « Quitter »


def apply_kb_lock():
    """Désactive les raccourcis clavier d'Anki pendant les révisions si le cadenas est fermé."""
    global _KB_DISABLED, _KB_ACTIONS
    try:
        st = S()
        locked = mw.state == "review" and bool(st.get("kb_lock") or st.get("type_on"))
    except Exception:
        locked = False
    if locked:
        for qs in mw.findChildren(QShortcut):
            try:
                if qs.isEnabled():
                    qs.setEnabled(False)
                    _KB_DISABLED.append(qs)
            except RuntimeError:
                pass
        # raccourcis des menus (ex. F = créer un paquet filtré, Ctrl+Z = annuler)
        for act in mw.findChildren(QAction):
            try:
                seqs = list(act.shortcuts())
                if seqs and not any(k.toString() in KEEP_SHORTCUTS for k in seqs):
                    _KB_ACTIONS.append((act, seqs))
                    act.setShortcuts([])
            except RuntimeError:
                pass
    else:
        for act, seqs in _KB_ACTIONS:
            try:
                act.setShortcuts(seqs)
            except RuntimeError:
                pass
        _KB_ACTIONS = []
        for qs in _KB_DISABLED:
            try:
                qs.setEnabled(True)
            except RuntimeError:  # raccourci déjà supprimé par Anki
                pass
        _KB_DISABLED = []


def toggle_kb_lock():
    st = S()
    st["kb_lock"] = not st.get("kb_lock")
    save()
    apply_kb_lock()
    if mw.reviewer and mw.reviewer.web:
        mw.reviewer.web.eval("if(window.planifLock)planifLock(%s);" % ("true" if st["kb_lock"] else "false"))


def allow_sound(web):
    try:
        web.settings().setAttribute(QWebEngineSettings.WebAttribute.PlaybackRequiresUserGesture, False)
    except Exception:
        pass


def push_reviewer_state(focus=False):
    """Affiche/masque la zone de réponse et le cadenas selon les réglages."""
    if not (mw.reviewer and mw.reviewer.web):
        return
    st = S()
    web = mw.reviewer.web
    allow_sound(web)
    web.eval("if(window.sfxSet)sfxSet(%s,%.2f);" % ("true" if st.get("sound_on", True) else "false", float(st.get("sound_vol", .5))))
    web.eval("if(window.planifLock)planifLock(%s);" % ("true" if st.get("kb_lock") else "false"))
    web.eval("if(window.planifType)planifType(%s,%d,%s);"
             % ("true" if st.get("type_on") else "false", int(st.get("pad_size", 1)),
                json.dumps(dict(shop.box_style(st["equipped"]), lv=cos_level(st, "box_theme", st["equipped"].get("box_theme"))),
                           ensure_ascii=False)))
    if focus and st.get("type_on") and getattr(mw.reviewer, "state", "") == "question":
        web.setFocus()
        web.eval("if(window.planifTypeFocus)planifTypeFocus();")


def undo_last():
    try:
        if hasattr(mw, "undo"):
            mw.undo()
        else:
            mw.onUndo()
    except Exception as e:
        print("planificateur_etudes:", e)
        return

    def toast():
        if mw.state == "review" and mw.reviewer and mw.reviewer.web:
            mw.reviewer.web.eval("if(window.planifToast)planifToast('↩️ Note précédente annulée : tu peux répondre à nouveau');")
    QTimer.singleShot(350, toast)


def reveal_answer():
    r = mw.reviewer
    if r and getattr(r, "state", "") == "question":
        try:
            r._showAnswer()
        except AttributeError:
            r.onEnterKey()


def answer_with(ease):
    r = mw.reviewer
    if r and getattr(r, "state", "") == "answer" and 1 <= ease <= 4:
        try:
            r._answerCard(ease)
        except Exception as e:
            print("planificateur_etudes:", e)


def on_show_answer(card):
    try:
        if mw.reviewer and mw.reviewer.web:
            mw.reviewer.web.eval("if(window.planifTypeAnswer)planifTypeAnswer();")
            mw.reviewer.web.setFocus()  # pour que 1-4 arrivent bien au module
    except Exception as e:
        print("planificateur_etudes:", e)


def on_show_question(card):
    try:
        apply_kb_lock()
        if mw.reviewer and mw.reviewer.web:
            push_reviewer_state()
            mw.reviewer.web.eval("if(window.planifTypeQuestion)planifTypeQuestion();")
            st = S()
            bfx = boss_fx(st)
            if bfx.get("timer") and not bfx["timer"].get("start"):
                bfx["timer"]["start"] = time.time()
                mw.reviewer.web.eval("if(window.planifBossTimer)planifBossTimer(%d);" % int(bfx["timer"]["secs"]))
            bd = boss_now(st)
            bd.update(dmg=0, crit=False, down=None, hero=shop.art.avatar_svg(st.get("gear", {})))
            bd.pop("taunt", None)
            mw.reviewer.web.eval("if(window.planifBoss)planifBoss(%s);" % json.dumps(bd, ensure_ascii=False))
            q = bfx.get("quiz")
            if q:  # interro restée sans réponse : elle revient
                icon, title = BOSS_ATTACK_NAMES["quiz"]
                mw.reviewer.web.eval("if(window.planifBossAttack)planifBossAttack(%s);" % json.dumps(
                    {"type": "quiz", "icon": icon, "title": title, "boss": bd["name"], "art": bd["art"], "q": q["q"],
                     "choices": q["choices"], "text": "Tu n'y échapperas pas : réponds à l'interro !"}, ensure_ascii=False))
            if S().get("type_on"):
                mw.reviewer.web.setFocus()
            mw.reviewer.web.eval("if(window.planifHUD)planifHUD(%s);" % json.dumps(hud_data(), ensure_ascii=False))
    except Exception as e:
        print("planificateur_etudes:", e)


def on_state_change(new_state, old_state):
    QTimer.singleShot(0, apply_kb_lock)
    if new_state in ("overview", "deckBrowser") and old_state == "review":
        QTimer.singleShot(300, lambda: check_finished_decks(announce=True))
    if new_state in ("review", "deckBrowser"):
        refresh_weather()
    if new_state == "deckBrowser" and old_state != "deckBrowser":
        QTimer.singleShot(150, lambda: resync_limits() and refresh_main())
    if new_state == "review" and old_state != "review":
        SESSION.update(xp=0, cards=0, hits=0, miss=0, last_talk=0)
        try:
            process(show=False)
        except Exception:
            pass


THEMED_CONTEXTS = ("DeckBrowser", "Overview", "Toolbar", "TopToolbar", "BottomBar",
                   "BottomToolbar", "DeckBrowserBottomBar", "OverviewBottomBar", "ReviewerBottomBar")


def on_webview_content(web_content, context):
    try:
        if not (mw.col and mw.pm and mw.pm.name):
            return
        name = type(context).__name__
        st = S()
        eq = st["equipped"]
        if name in THEMED_CONTEXTS or name.endswith("BottomBar") or name.endswith("Toolbar"):
            css = shop.theme_css(eq.get("theme"), cos_level(st, "theme", eq.get("theme")))
            if css:
                web_content.head += "<style>" + css + "</style>"
            if name == "ReviewerBottomBar":
                web_content.head += "<script>" + shop.BOTTOMBAR_JS + "</script>"
        elif name == "Reviewer":
            web_content.head += ("<style>" + shop.wallpaper_css(eq.get("wallpaper"), None, cos_level(st, "wallpaper", eq.get("wallpaper"))) + shop.REVIEWER_CSS +
                                 "</style><script>" + shop.REVIEWER_JS + "</script>")
    except Exception as e:
        print("planificateur_etudes:", e)


def startup():
    if not mw.col:
        return
    try:
        st = S()
        if st.pop("scale_msg", False):
            save()
            QTimer.singleShot(7000, lambda: tooltip(
                "💰 Nouvelle échelle des pièces : tu gagnes plus quand tu réussis, et les prix ont doublé.<br>"
                "Tes pièces et tes récompenses perso ont été doublées aussi : tu ne perds rien !", period=8000))
        refresh_weather()
        resync_limits()  # à chaque ouverture d'Anki
        status = process(show=False)
        today_iso = status["today"].isoformat()
        if st.get("alert_day") != today_iso:
            late = [e for e in planning_view(st) if e["plan"]["state"] in ("notset", "late")]
            if late:
                st["alert_day"] = today_iso
                save()
                lines = []
                for e in late[:3]:
                    if e["plan"]["state"] == "notset":
                        lines.append(f"⚠️ « {html.escape(e['name'])} » : ton paquet n'est pas réglé sur {e['target']} "
                                     f"nouvelles/jour. Clique sur « Corriger » dans le calendrier de l'accueil.")
                    else:
                        lines.append(f"⚠️ « {html.escape(e['name'])} » : ta marge de révision est entamée, "
                                     f"vise {e['target']} nouvelles cartes/jour jusqu'à l'examen.")
                QTimer.singleShot(2500, lambda: tooltip("<br>".join(lines), period=9000))
                return
        if not status["met"]:
            nxt = next((e for e in status["active"] if not e["met"]), None)
            if nxt:
                tooltip(f"📅 « {html.escape(nxt['name'])} » dans {nxt['days_to_exam']} jour(s).<br>"
                        f"Aujourd'hui : {max(0, nxt['target'] - nxt['intro_today'])} nouvelles cartes "
                        f"+ {nxt['due']} révisions.", period=6000)
        refresh_main()
    except Exception as e:
        print("planificateur_etudes:", e)


def on_profile_open():
    global _state
    _state = None
    QTimer.singleShot(1200, startup)


def on_profile_close():
    global _state
    try:
        save()
    except Exception:
        pass
    _state = None


def on_sync_done():
    try:
        resync_limits()
        process(show=True)
        refresh_main()
    except Exception as e:
        print("planificateur_etudes:", e)


def on_toolbar(links, toolbar):
    try:
        links.append(toolbar.create_link("planif", "🔥 Objectifs", open_dashboard,
                                         tip="Planificateur d'études", id="planif"))
    except Exception:
        pass


action = QAction("Planificateur d'études 🔥", mw)
qconnect(action.triggered, open_dashboard)
mw.form.menuTools.addAction(action)

gui_hooks.deck_browser_will_render_content.append(on_deck_browser)
gui_hooks.webview_did_receive_js_message.append(on_js_message)
gui_hooks.reviewer_did_answer_card.append(on_answer)
gui_hooks.profile_did_open.append(on_profile_open)
gui_hooks.profile_will_close.append(on_profile_close)
gui_hooks.top_toolbar_did_init_links.append(on_toolbar)
gui_hooks.webview_will_set_content.append(on_webview_content)
gui_hooks.reviewer_did_show_question.append(on_show_question)
gui_hooks.reviewer_did_show_answer.append(on_show_answer)
gui_hooks.state_did_change.append(on_state_change)
try:
    gui_hooks.add_cards_did_add_note.append(schedule_resync)
except AttributeError:
    pass
try:
    gui_hooks.sync_did_finish.append(on_sync_done)
except AttributeError:
    pass
