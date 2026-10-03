# -*- coding: utf-8 -*-
"""Catalogue de la boutique et code injecté dans les écrans d'Anki."""

try:
    from . import art
except ImportError:  # chargé hors d'Anki (tests)
    import art

# ───────────────────────────────────────────── thèmes de couleurs (tout Anki)
# (fond, surface, accent) pour le mode clair puis le mode sombre
THEMES = {
    "moderne": {"name": "Moderne", "price": 0,
                "light": ("#eef2f0", "#ffffff", "#4f63d8", "#7a5cff"), "dark": ("#152024", "#1d2b30", "#8193ff", "#b197fc")},
    "classique": {"name": "Anki d'origine", "price": 0, "light": None, "dark": None},
    "menthe": {"name": "Menthe", "price": 600,
               "light": ("#e6f4ee", "#f7fcfa", "#1f9e6e"), "dark": ("#122019", "#1a2e26", "#3cc68f")},
    "lavande": {"name": "Lavande", "price": 600,
                "light": ("#efebfa", "#faf8ff", "#7a5cd6"), "dark": ("#1b1728", "#262036", "#a88fff")},
    "ocean": {"name": "Océan", "price": 800,
              "light": ("#e4f0f9", "#f6fbff", "#1f7fbf"), "dark": ("#0e1b27", "#152838", "#4fb0ef")},
    "sakura": {"name": "Sakura", "price": 800,
               "light": ("#fbecf0", "#fff8fa", "#d6557a"), "dark": ("#26161b", "#342027", "#ff8fae")},
    "or": {"name": "Nuit dorée", "price": 1200,
           "light": ("#f6f0e0", "#fffcf3", "#a87a06"), "dark": ("#15130c", "#221f14", "#e9b949")},
    "halloween": {"name": "Nuit d'Halloween 🎃", "price": 800, "event": "halloween",
                  "light": ("#fbeee0", "#fff7ef", "#e8590c"), "dark": ("#1a1024", "#261733", "#ff8c1a")},
    "neon": {"name": "Arcade néon", "price": 1600,
             "light": ("#efeefe", "#fbfbff", "#d4009e"), "dark": ("#0c0a1d", "#16132e", "#ff3cc7")},
}

# ───────────────────────────────────────────── fonds d'écran (pendant les révisions)
WALLPAPERS = {
    "aucun": {"name": "Aucun", "price": 0, "image": "none", "size": "auto", "color": "transparent"},
    "bonbon": {"name": "Bonbon", "price": 500, "color": "#f3e8ff", "size": "auto",
               "image": "linear-gradient(135deg,#ffd6e8,#d6e4ff 50%,#d6fff1)"},
    "cahier": {"name": "Cahier quadrillé", "price": 500, "color": "#fbfcfe", "size": "24px 24px, 24px 24px",
               "image": "linear-gradient(#cfe0f5 1px,transparent 1px),linear-gradient(90deg,#cfe0f5 1px,transparent 1px)"},
    "ocean": {"name": "Océan", "price": 800, "color": "#3fa7d6", "size": "auto",
              "image": "linear-gradient(180deg,#b9f3ff,#3fa7d6 60%,#1d4e89)"},
    "foret": {"name": "Forêt", "price": 800, "color": "#8cc084", "size": "auto",
              "image": "radial-gradient(ellipse at 20% 110%,#2f6b3f 0,transparent 55%),"
                       "radial-gradient(ellipse at 85% 105%,#3d7a4a 0,transparent 50%),"
                       "linear-gradient(180deg,#e3f6dc,#9fcf95 65%,#4f8a58)"},
    "coucher": {"name": "Coucher de soleil", "price": 1000, "color": "#ff6f91", "size": "auto",
                "image": "linear-gradient(160deg,#ffb36b,#ff6f91 50%,#7b5cff)"},
    "aurore": {"name": "Aurore boréale", "price": 1400, "color": "#132248", "size": "auto",
               "image": "radial-gradient(ellipse at 20% 0%,#5ee7b3 0,transparent 50%),"
                        "radial-gradient(ellipse at 80% 10%,#6a7bff 0,transparent 55%),"
                        "linear-gradient(180deg,#0f1b3d,#1b2f5c)"},
    "hantee": {"name": "Forêt hantée 🦇", "price": 900, "event": "halloween", "color": "#2a1640",
               "size": "420px 320px, 100% 100%, 100% 100%, 100% 100%",
               "image": "url('data:image/svg+xml," + __import__("urllib.parse").parse.quote(art.HAUNTED_SVG) + "'),"
                        "radial-gradient(circle at 82% 16%,#fff3c4 0,#ffd66b 5%,rgba(255,200,90,.25) 9%,transparent 16%),"
                        "radial-gradient(ellipse at 50% 120%,#ff8c1a55 0,transparent 55%),"
                        "linear-gradient(180deg,#1a0f2e,#3b1f5c 60%,#5a2a4a)"},
    "etoiles": {"name": "Nuit étoilée", "price": 1800, "color": "#0b1030",
                "size": "230px 230px, 170px 170px, 300px 300px, 100% 100%",
                "image": "radial-gradient(1.6px 1.6px at 30px 40px,#fff,transparent),"
                         "radial-gradient(1.2px 1.2px at 90px 120px,#dfe7ff,transparent),"
                         "radial-gradient(2px 2px at 200px 70px,#fff6d6,transparent),"
                         "linear-gradient(180deg,#0b1030,#27205a)"},
}

# ───────────────────────────────────────────── effets pendant les révisions
EFFECTS = {
    "gains": {"name": "Gains en direct", "price": 0,
              "desc": "+XP et +pièces qui s'envolent à chaque carte, avec une barre d'infos en bas à droite."},
    "etincelles": {"name": "Étincelles", "price": 500,
                   "desc": "Une gerbe d'étincelles quand tu réponds Correct ou Facile."},
    "combo": {"name": "Compteur de combo", "price": 700,
              "desc": "Affiche combien de cartes tu réussis d'affilée."},
    "confettis": {"name": "Confettis", "price": 1000,
                  "desc": "Pluie de confettis pour l'objectif du jour, un nouveau niveau ou un badge."},
}

# ───────────────────────────────────────────── mascottes (évoluent avec le niveau)
STAGE_LEVELS = [1, 3, 6, 10]
MASCOTS = {
    "hibou": {"name": "Hibou", "price": 0, "levels": art.MASCOT_LEVELS, "stages": art.HIBOU_STAGES,
              "desc": "De l'œuf moucheté au grand-duc de minuit."},
    "plante": {"name": "Plante", "price": 1000, "levels": art.MASCOT_LEVELS, "stages": art.PLANTE_STAGES,
               "desc": "Une graine endormie qui devient un arbre en fleurs."},
    "chat": {"name": "Chat", "price": 1400, "levels": art.MASCOT_LEVELS, "stages": art.CHAT_STAGES,
             "desc": "Du chaton au panier jusqu'au roi lion."},
    "dragon": {"name": "Dragon", "price": 2400, "levels": art.MASCOT_LEVELS, "stages": art.DRAGON_STAGES,
               "desc": "De l'œuf écaillé au dragon ancestral couronné."},
    "chouette": {"name": "Chouette savante", "price": 3200, "levels": art.CHOUETTE_LEVELS,
                 "stages": art.CHOUETTE_STAGES, "desc": "Elle finit diplômée, avec toque et aura dorée."},
}


# ───────────────────────────────────────────── case de réponse : thèmes, polices, corrections
BOX_THEMES = {
    "classique": {"name": "Classique", "price": 0, "bg": "transparent", "ink": "inherit",
                  "border": "rgba(128,128,128,.35)"},
    "cahier": {"name": "Cahier d'écolier", "price": 400, "bg": "#fdfdf8", "ink": "#1d2a4a", "border": "#bcd3ee",
               "pl": "52px",
               "lines": "linear-gradient(90deg,transparent 38px,#f2a3a3 38px,#f2a3a3 40px,transparent 40px),"
                        "repeating-linear-gradient(transparent 0,transparent 27px,#bcd3ee 27px,#bcd3ee 28px)"},
    "postit": {"name": "Post-it", "price": 500, "bg": "#fff6a8", "ink": "#3b3000", "border": "#e8d65a",
               "shadow": "0 6px 14px rgba(120,100,0,.18)"},
    "tableau": {"name": "Tableau noir", "price": 800, "bg": "#23402f", "ink": "#f4f1e8", "border": "#7a5230",
                "shadow": "inset 0 0 0 4px #7a5230"},
    "terminal": {"name": "Terminal", "price": 800, "bg": "#0c0f0c", "ink": "#33ff66", "border": "#1f3d25"},
    "parchemin": {"name": "Parchemin", "price": 1000, "bg": "#f3e5c0", "ink": "#4a3317", "border": "#c9a86a",
                  "lines": "radial-gradient(ellipse at center,transparent 55%,rgba(150,110,40,.25) 100%)"},
    "nuit": {"name": "Nuit bleue", "price": 1000, "bg": "#111a33", "ink": "#dfe7ff", "border": "#3b4f8f",
             "lines": "radial-gradient(1px 1px at 20% 30%,#fff,transparent),radial-gradient(1px 1px at 70% 60%,#cfe0ff,transparent),"
                      "radial-gradient(1.5px 1.5px at 85% 20%,#fff,transparent)"},
    "neon": {"name": "Néon", "price": 1400, "bg": "#0d0b1f", "ink": "#ffd6f5", "border": "#ff3cc7",
             "shadow": "0 0 14px rgba(255,60,199,.55)"},
}
BOX_FONTS = {
    "systeme": {"name": "Système", "price": 0, "stack": "system-ui,-apple-system,'Segoe UI',sans-serif"},
    "georgia": {"name": "Georgia", "price": 300, "stack": "Georgia,'Times New Roman',serif"},
    "machine": {"name": "Machine à écrire", "price": 400, "stack": "'American Typewriter','Courier New',monospace"},
    "code": {"name": "Code", "price": 400, "stack": "Menlo,Monaco,Consolas,monospace"},
    "manuscrite": {"name": "Manuscrite", "price": 600, "stack": "'Bradley Hand','Segoe Print',cursive"},
    "craie": {"name": "Craie", "price": 600, "stack": "'Chalkboard SE',Chalkboard,'Comic Sans MS',cursive"},
    "marqueur": {"name": "Marqueur", "price": 700, "stack": "'Marker Felt','Segoe Print',fantasy"},
    "calligraphie": {"name": "Calligraphie", "price": 800, "stack": "'Apple Chancery','Snell Roundhand','Palatino',cursive"},
}
CORR_STYLES = {
    "rouge": {"name": "Rouge", "price": 0, "kind": "color", "value": "#e03131"},
    "vert": {"name": "Vert", "price": 300, "kind": "color", "value": "#1f9e6e"},
    "bleu": {"name": "Bleu", "price": 300, "kind": "color", "value": "#2f6fe4"},
    "orange": {"name": "Orange", "price": 300, "kind": "color", "value": "#f08c00"},
    "violet": {"name": "Violet", "price": 400, "kind": "color", "value": "#9c36b5"},
    "rose": {"name": "Rose fluo", "price": 500, "kind": "color", "value": "#ff3cc7"},
    "or": {"name": "Or", "price": 700, "kind": "color", "value": "#d4a017"},
    "surligneur": {"name": "Surligneur jaune", "price": 800, "kind": "highlight", "value": "#fff08a", "ink": "#1d1d1f"},
}


# ───────────────────────────────────────────── accessoires de la mascotte
ACCESSORIES = {
    "aucun": {"name": "Aucun", "price": 0, "svg": ""},
    "sorciere": {"name": "Chapeau de sorcière 🎃", "price": 600, "event": "halloween", "svg": art.WITCH_HAT,
                 "desc": "Édition limitée Halloween, à garder pour toujours."},
}


def with_accessory(mascot_html, key):
    a = ACCESSORIES.get(key or "aucun")
    if not a or not a["svg"]:
        return mascot_html
    return ('<span style="position:relative;display:inline-block;line-height:1">' + mascot_html +
            '<span style="position:absolute;left:50%;top:-.34em;transform:translateX(-50%) rotate(-10deg);'
            'font-size:.5em;line-height:0;pointer-events:none">' + a["svg"] + '</span></span>')


def box_style(eq):
    t = BOX_THEMES.get(eq.get("box_theme")) or BOX_THEMES["classique"]
    f = BOX_FONTS.get(eq.get("box_font")) or BOX_FONTS["systeme"]
    c = CORR_STYLES.get(eq.get("corr")) or CORR_STYLES["rouge"]
    return {"bg": t["bg"], "ink": t["ink"], "border": t["border"], "lines": t.get("lines", "none"),
            "pl": t.get("pl", "12px"), "shadow": t.get("shadow", "none"), "font": f["stack"],
            "corr": {"kind": c["kind"], "value": c["value"], "ink": c.get("ink", "#1d1d1f")}}


def mascot_levels(key):
    return (MASCOTS.get(key) or MASCOTS["hibou"]).get("levels", STAGE_LEVELS)


def mascot_stage(level, key="hibou"):
    return max(i for i, lv in enumerate(mascot_levels(key)) if level >= lv)


def mascot_info(key, level, custom_name=""):
    m = MASCOTS.get(key) or MASCOTS["hibou"]
    levels = mascot_levels(key)
    i = mascot_stage(level, key)
    emoji, stage = m["stages"][i]
    nxt = levels[i + 1] if i + 1 < len(levels) else None
    return {"emoji": emoji, "stage": stage, "stage_index": i, "species": m["name"],
            "name": custom_name or stage, "next_level": nxt}


# ───────────────────────────────────────────── salle de jeux (payer chaque partie)
GAMES = {
    "roue": {"name": "Roue de la fortune", "icon": "🎡", "price": 120, "kind": "chance",
             "desc": "Fais tourner la roue : pièces, jackpot, boost d'XP ou ticket gratuit."},
    "grattage": {"name": "Carte à gratter", "icon": "🎟️", "price": 80, "kind": "chance",
                 "desc": "Trois symboles identiques et tu gagnes : pièces, tickets, boost… ou un lot surprise 🎁 de la boutique !"},
    "serpent": {"name": "Serpent", "icon": "🐍", "price": 60, "kind": "arcade",
                "desc": "Mange un max de pommes sans te mordre la queue. Bats ton record : partie remboursée deux fois + 40 XP !"},
    "briques": {"name": "Casse-briques", "icon": "🧱", "price": 60, "kind": "arcade",
                "desc": "Casse toutes les briques avec ta balle. Bats ton record : partie remboursée deux fois + 40 XP !"},
}
RECORD_MULT = 2   # battre son record rapporte 2 × le prix de la partie
RECORD_XP = 40
RECORD_BONUS = 30

# (étiquette, type, valeur, poids) — gain moyen inférieur au prix : la roue reste une dépense
WHEEL = [
    ("Raté", "coins", 0, 20),
    ("40 🪙", "coins", 40, 20),
    ("80 🪙", "coins", 80, 18),
    ("120 🪙", "coins", 120, 15),
    ("200 🪙", "coins", 200, 10),
    ("JACKPOT 500 🪙", "coins", 500, 3),
    ("Boost ×2", "boost", 30, 8),
    ("Ticket gratuit", "ticket", 1, 6),
]
# (symbole, type, valeur, poids) ; None = perdu
SCRATCH = [
    (None, None, 0, 45),
    ("🍀", "coins", 100, 20),
    ("🪙", "coins", 180, 12),
    ("💎", "coins", 600, 3),
    ("⭐", "boost", 30, 8),
    ("🎫", "ticket", 2, 7),
    ("🎁", "lot", 1, 5),
]
SCRATCH_SYMBOLS = ["🍀", "🪙", "💎", "⭐", "🎫", "🎁", "🍒", "🔔"]


# ───────────────────────────────────────────── CSS injecté

def _rgba(hexc, a):
    h = hexc.lstrip("#")
    return f"rgba({int(h[0:2], 16)},{int(h[2:4], 16)},{int(h[4:6], 16)},{a})"


# Habillage moderne commun à tous les thèmes (sauf « Anki d'origine »)
SKIN_CSS = r"""
body{font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
/* écran des paquets */
center>table,#decktree{border-collapse:separate!important;border-spacing:0 7px!important;margin-top:10px}
tr.deck td{background:var(--planif-surface)!important;padding-top:9px!important;padding-bottom:9px!important;
  border-top:1px solid var(--planif-line);border-bottom:1px solid var(--planif-line);transition:background .15s}
tr.deck td:first-child{border-left:1px solid var(--planif-line);border-radius:12px 0 0 12px;padding-left:14px!important}
tr.deck td:last-child{border-right:1px solid var(--planif-line);border-radius:0 12px 12px 0;padding-right:10px!important}
tr.deck:hover td,tr.deck.current td{background:var(--planif-soft)!important}
tr.deck.current td:first-child{box-shadow:inset 4px 0 0 var(--planif-accent)}
a.deck{font-weight:600;color:var(--fg)!important;text-decoration:none!important}
a.deck:hover{color:var(--planif-accent)!important}
a.collapse{color:var(--fg-subtle,#888)!important;text-decoration:none!important}
th{font-weight:600;font-size:12.5px;opacity:.7;padding-bottom:2px}
.new-count,.learn-count,.review-count{display:inline-block;min-width:24px;padding:2px 9px;border-radius:999px;
  font-weight:700;font-size:13px;text-align:center;text-decoration:none!important}
.new-count{color:#2f6fe4!important;background:rgba(47,111,228,.13)}
.learn-count{color:#e8590c!important;background:rgba(232,89,12,.13)}
.review-count{color:#1f9e6e!important;background:rgba(31,158,110,.14)}
.zero-count{opacity:.45;background:transparent!important;font-weight:500;color:inherit!important}
.nightMode .new-count,.night-mode .new-count{color:#74a9ff!important;background:rgba(116,169,255,.15)}
.nightMode .learn-count,.night-mode .learn-count{color:#ff9a5c!important;background:rgba(255,154,92,.15)}
.nightMode .review-count,.night-mode .review-count{color:#4cd69c!important;background:rgba(76,214,156,.15)}
.nightMode .zero-count,.night-mode .zero-count{color:inherit!important;background:transparent!important}
.gears{opacity:.45;transition:opacity .15s} tr.deck:hover .gears{opacity:.95}
/* boutons */
button{border-radius:10px!important;border:1px solid var(--planif-line)!important;background:var(--planif-surface)!important;
  background-image:none!important;color:var(--fg)!important;font-weight:600;box-shadow:0 1px 3px rgba(0,0,0,.07)!important;padding:5px 14px;
  transition:border-color .15s,background .15s,transform .1s}
button:hover{border-color:var(--planif-accent)!important;background:var(--planif-soft)!important}
button:active{transform:translateY(1px)}
#study,button#study,#ansbut,button#ansbut{background:linear-gradient(135deg,var(--planif-accent),var(--planif-accent2))!important;
  color:#fff!important;border:none!important;border-radius:14px!important;box-shadow:0 6px 16px var(--planif-soft)!important}
#study{padding:10px 30px!important;font-size:16px!important}
#study:hover,#ansbut:hover{filter:brightness(1.08)}
/* boutons de réponse colorés */
button[data-ease="1"],button[onclick*="ease1"]{color:#e03131!important;border:1.5px solid rgba(224,49,49,.55)!important;background:rgba(224,49,49,.09)!important}
button[data-ease="2"],button[onclick*="ease2"]{color:#e8590c!important;border:1.5px solid rgba(232,89,12,.55)!important;background:rgba(232,89,12,.09)!important}
button[data-ease="3"],button[onclick*="ease3"]{color:#1f9e6e!important;border:1.5px solid rgba(31,158,110,.55)!important;background:rgba(31,158,110,.1)!important}
button[data-ease="4"],button[onclick*="ease4"]{color:#2f6fe4!important;border:1.5px solid rgba(47,111,228,.55)!important;background:rgba(47,111,228,.09)!important}
button[data-ease]:hover,button[onclick*="ease"]:hover{filter:brightness(1.05);transform:translateY(-1px)}
.nightMode button[data-ease="1"],.night-mode button[data-ease="1"]{color:#ff6b6b!important}
.nightMode button[data-ease="2"],.night-mode button[data-ease="2"]{color:#ff9a5c!important}
.nightMode button[data-ease="3"],.night-mode button[data-ease="3"]{color:#4cd69c!important}
.nightMode button[data-ease="4"],.night-mode button[data-ease="4"]{color:#74a9ff!important}
/* barre du haut */
.hitem{border-radius:999px;padding:4px 12px!important;font-weight:600;text-decoration:none!important;color:var(--fg)!important;transition:background .15s}
.hitem:hover{background:var(--planif-soft)!important;color:var(--planif-accent)!important}
/* aperçu d'un paquet */
h3{font-weight:700;letter-spacing:.2px}
"""


def theme_css(key, lv=1):
    """Le thème ne repeint plus les fonds d'Anki (sinon ils ne se raccordent pas avec la fenêtre) :
    il garde les couleurs natives et n'ajoute que le style et les couleurs d'accent."""
    t = THEMES.get(key)
    if not t or not t["light"]:
        return ""
    L, D = t["light"], t["dark"]
    acc_l, acc_d = L[2], D[2]
    acc2_l = L[3] if len(L) > 3 else acc_l
    acc2_d = D[3] if len(D) > 3 else acc_d
    if key == "moderne":
        surf_l, surf_d = "rgba(255,255,255,.75)", "rgba(255,255,255,.045)"
    else:
        surf_l, surf_d = _rgba(acc_l, .07), _rgba(acc_d, .10)

    def block(sel, acc, acc2, surf, line):
        return (f"{sel}{{--planif-accent:{acc};--planif-accent2:{acc2};--planif-surface:{surf};"
                f"--planif-soft:{_rgba(acc, .16)};--planif-line:{line}}}\n")

    css = block(":root,html,body", acc_l, acc2_l, surf_l, "rgba(20,30,40,.09)")
    css += block("html.night-mode,html.nightMode,.night-mode body,.nightMode body,"
                 "body.nightMode,body.night-mode,body.night_mode", acc_d, acc2_d, surf_d, "rgba(255,255,255,.08)")
    return css + SKIN_CSS + (SKIN_L2 if lv >= 2 else "") + (SKIN_L3 if lv >= 3 else "")


SKY = {
    "dawn": "linear-gradient(180deg,#6d7fd6 0%,#f7a4a0 55%,#ffd8a8 100%)",
    "day": "linear-gradient(180deg,#3d9bf0 0%,#8fcbfa 60%,#e3f2ff 100%)",
    "dusk": "linear-gradient(180deg,#2f2468 0%,#c2557a 45%,#ff9f5a 75%,#ffd08a 100%)",
    "night": "linear-gradient(180deg,#050920 0%,#141a45 60%,#2a2360 100%)",
}
SKY_DULL = {  # ciel couvert / pluie / neige / brouillard
    "dawn": "linear-gradient(180deg,#7c7f99,#b9a3a3 60%,#d6c7bd)",
    "day": "linear-gradient(180deg,#6f7f8f,#a3b0bd 60%,#d5dbe1)",
    "dusk": "linear-gradient(180deg,#3a3350,#7d5a6e 55%,#b88e7e)",
    "night": "linear-gradient(180deg,#0a0e1c,#1d2433 60%,#2c3140)",
}


def live_sky(wx):
    kind, phase = (wx or {}).get("kind", "clear"), (wx or {}).get("phase", "day")
    sky = SKY[phase] if kind in ("clear", "clouds") else SKY_DULL[phase]
    if kind == "snow":
        sky = sky.replace("#d5dbe1", "#f1f5f9").replace("#a3b0bd", "#c9d3dd")
    orb = ""
    if kind in ("clear", "clouds"):
        if phase == "day":
            orb = "radial-gradient(circle at 86% 12%,rgba(255,236,150,.8) 0,rgba(255,224,102,.35) 3%,transparent 9%),"
        elif phase in ("dawn", "dusk"):
            orb = "radial-gradient(circle at 80% 84%,rgba(255,200,120,.7) 0,rgba(255,169,77,.25) 5%,transparent 13%),"
        else:
            orb = "radial-gradient(circle at 84% 14%,rgba(255,253,240,.75) 0,rgba(241,243,245,.5) 1.8%,rgba(255,255,255,.08) 4%,transparent 8%),"
    return orb + sky


VEIL_LIGHT = "linear-gradient(rgba(248,249,251,.58),rgba(248,249,251,.58)),"
VEIL_DARK = "linear-gradient(rgba(24,26,32,.6),rgba(24,26,32,.6)),"


def wallpaper_css(key, wx=None, lv=1):
    w = WALLPAPERS.get(key)
    if not w or w["image"] == "none":
        return ""
    if lv >= 2 and not w.get("live"):
        import urllib.parse as _u
        extra_img, extra_size = "", ""
        if lv >= 3:
            extra_img += "url('data:image/svg+xml," + _u.quote(DUST_SVG) + "'),"
            extra_size += "300px 300px, "
        extra_img += "radial-gradient(ellipse at center,transparent 50%,rgba(0,0,0,.28) 100%),"
        extra_size += "100% 100%, "
        w = dict(w, image=extra_img + w["image"], size=extra_size + w["size"])
    if w.get("live"):
        sky = live_sky(wx)
        return (
            f"html{{background-color:#e9ecef!important;background-image:{VEIL_LIGHT}{sky}!important;"
            "background-size:100% 100%!important;background-attachment:fixed!important;min-height:100%}\n"
            f"html.night-mode,html.nightMode{{background-color:#1c1e24!important;background-image:{VEIL_DARK}{sky}!important}}\n"
            "#qa{position:relative;z-index:1}\n"
            "html body,html body.card{background:transparent!important}\n"
            "#qa{background:rgba(255,255,255,.9);color:#1d1d1f;border-radius:18px;padding:22px 26px;"
            "margin:26px auto 80px;max-width:880px;box-shadow:0 6px 24px rgba(0,0,0,.08)}\n"
            ".nightMode #qa,.night-mode #qa,body.nightMode #qa,body.night_mode #qa"
            "{background:rgba(30,32,40,.9);color:#eceef3}\n")
    image, size = w["image"], w["size"]
    return (
        f"html{{background-color:{w['color']}!important;background-image:{image}!important;"
        f"background-size:{size}!important;background-attachment:fixed!important;min-height:100%}}\n"
        "#qa{position:relative;z-index:1}\n"
        "html body,html body.card{background:transparent!important}\n"
        "#qa{background:rgba(255,255,255,.9);color:#1d1d1f;border-radius:18px;padding:22px 26px;"
        "margin:26px auto 80px;max-width:880px;box-shadow:0 12px 40px rgba(0,0,0,.18)}\n"
        ".nightMode #qa,.night-mode #qa,body.nightMode #qa,body.night_mode #qa"
        "{background:rgba(24,26,32,.9);color:#eceef3}\n"
    )


SFX_JS = r"""
/* ───── bruitages synthétisés (aucun fichier audio) ───── */
var PSFX={on:true,vol:.5,ctx:null,last:{}};
function sfxSet(on,vol){PSFX.on=!!on;if(vol!=null)PSFX.vol=Math.max(0,Math.min(1,vol));}
function sfxCtx(){
  if(!PSFX.ctx){try{PSFX.ctx=new (window.AudioContext||window.webkitAudioContext)();}catch(e){return null;}}
  if(PSFX.ctx.state==='suspended'){try{PSFX.ctx.resume();}catch(e){}}
  return PSFX.ctx;
}
function sfxTone(f,dur,type,v,delay,f2){
  var c=sfxCtx();if(!c)return;var t=c.currentTime+(delay||0);
  var o=c.createOscillator(),g=c.createGain();o.type=type||'sine';o.frequency.setValueAtTime(f,t);
  if(f2)o.frequency.exponentialRampToValueAtTime(f2,t+dur);
  var vv=(v||.2)*PSFX.vol;g.gain.setValueAtTime(.0001,t);g.gain.exponentialRampToValueAtTime(vv,t+.008);
  g.gain.exponentialRampToValueAtTime(.0001,t+dur);o.connect(g);g.connect(c.destination);o.start(t);o.stop(t+dur+.02);
}
function sfxNoise(dur,v,delay,freq,q){
  var c=sfxCtx();if(!c)return;var t=c.currentTime+(delay||0),n=Math.floor(c.sampleRate*dur);
  var b=c.createBuffer(1,n,c.sampleRate),d=b.getChannelData(0);for(var i=0;i<n;i++)d[i]=(Math.random()*2-1)*(1-i/n);
  var s=c.createBufferSource();s.buffer=b;var fl=c.createBiquadFilter();fl.type='bandpass';fl.frequency.value=freq||1200;fl.Q.value=q||.8;
  var g=c.createGain();g.gain.value=(v||.3)*PSFX.vol;s.connect(fl);fl.connect(g);g.connect(c.destination);s.start(t);
}
function sfx(name,arg){
  if(!PSFX.on||PSFX.vol<=0)return;
  var now=Date.now();if(name==='tick'&&PSFX.last.tick&&now-PSFX.last.tick<35)return;PSFX.last[name]=now;
  switch(name){
    case 'click':sfxTone(620,.05,'triangle',.12);break;
    case 'tick':sfxTone(arg||1700,.025,'square',.05);break;
    case 'coin':sfxTone(1320,.07,'square',.07);sfxTone(1980,.16,'square',.06,.06);break;
    case 'coins':for(var i=0;i<5;i++){sfxTone(1500+i*140,.06,'square',.05,i*.06);}break;
    case 'xp':sfxTone(700,.09,'sine',.12);sfxTone(1050,.12,'sine',.1,.05);break;
    case 'soft':sfxTone(520,.08,'sine',.07);break;
    case 'miss':sfxTone(300,.12,'triangle',.08,0,220);break;
    case 'gem':sfxTone(1900,.1,'sine',.16);sfxTone(2850,.22,'sine',.12,.07);break;
    case 'win':[523,659,784,1047].forEach(function(f,i){sfxTone(f,.16,'triangle',.14,i*.08);});break;
    case 'big':[523,659,784,1047,784,1047,1319].forEach(function(f,i){sfxTone(f,.2,'triangle',.15,i*.09);});
      sfxNoise(.5,.08,.5,6000,.5);break;
    case 'lose':[440,370,311,262].forEach(function(f,i){sfxTone(f,.18,'triangle',.12,i*.11);});break;
    case 'boom':sfxNoise(.7,.5,0,300,.4);sfxTone(110,.5,'sine',.3,0,40);break;
    case 'hit':sfxNoise(.12,.25,0,700,1);sfxTone(160,.12,'square',.08,0,90);break;
    case 'crit':sfxNoise(.18,.35,0,1400,.8);sfxTone(220,.2,'sawtooth',.1,0,70);sfxTone(1400,.15,'square',.07,.05);break;
    case 'sparkle':for(var j=0;j<6;j++){sfxTone(2000+Math.random()*1800,.08,'sine',.05,j*.045);}break;
    case 'level':[392,523,659,784,1047].forEach(function(f,i){sfxTone(f,.22,'triangle',.15,i*.1);});
      sfxTone(1047,.6,'sine',.1,.55);sfxNoise(.6,.06,.5,7000,.5);break;
    case 'shake':for(var k=0;k<6;k++){sfxNoise(.05,.12,k*.2,900,2);}break;
    case 'pop':sfxTone(880,.06,'sine',.08,0,1320);break;
    case 'scratch':sfxNoise(.06,.05,0,3500,1.5);break;
  }
}
var PSFX_ROCKET=null;
function sfxRocket(on,mult){
  var c=sfxCtx();if(!c)return;
  if(!on){if(PSFX_ROCKET){try{PSFX_ROCKET.g.gain.setTargetAtTime(.0001,c.currentTime,.05);PSFX_ROCKET.o.stop(c.currentTime+.3);}catch(e){}PSFX_ROCKET=null;}return;}
  if(!PSFX.on)return;
  if(!PSFX_ROCKET){var o=c.createOscillator(),g=c.createGain();o.type='sawtooth';g.gain.value=.03*PSFX.vol;
    var fl=c.createBiquadFilter();fl.type='lowpass';fl.frequency.value=1200;o.connect(fl);fl.connect(g);g.connect(c.destination);o.start();PSFX_ROCKET={o:o,g:g};}
  PSFX_ROCKET.o.frequency.setTargetAtTime(160+Math.min(mult,20)*55,c.currentTime,.05);
}
"""

CONFETTI_JS = r"""
function planifFireworks(){
  var cv=document.createElement('canvas');cv.style.cssText='position:fixed;inset:0;width:100%;height:100%;pointer-events:none;z-index:99998';
  document.body.appendChild(cv);var W=cv.width=innerWidth,H=cv.height=innerHeight,ctx=cv.getContext('2d'),P=[],t0=performance.now();
  var cols=['#ffd43b','#ff6b9d','#4dabf7','#69db7c','#b197fc','#ff922b'];
  [[.25,.3,300],[.72,.22,700],[.5,.4,1100]].forEach(function(b){setTimeout(function(){if(window.sfx)sfx('boom');
    var c=cols[Math.floor(Math.random()*cols.length)];for(var i=0;i<70;i++){var a=Math.random()*6.28,v=2+Math.random()*5;
    P.push({x:W*b[0],y:H*b[1],vx:Math.cos(a)*v,vy:Math.sin(a)*v,l:1,c:c});}},b[2]);});
  (function f(t){ctx.clearRect(0,0,W,H);
    P.forEach(function(p){p.x+=p.vx;p.y+=p.vy;p.vy+=.06;p.vx*=.985;p.l-=.012;if(p.l>0){ctx.globalAlpha=p.l;ctx.fillStyle=p.c;
      ctx.beginPath();ctx.arc(p.x,p.y,2.4,0,6.29);ctx.fill();}});ctx.globalAlpha=1;
    if(t-t0<3200)requestAnimationFrame(f);else cv.remove();})(t0);
}
function planifConfetti(lv){
  lv=lv||1;
  if(window.sfx)sfx(lv>=3?'big':'win');
  if(lv>=3)planifFireworks();
  var cv=document.createElement('canvas');
  cv.style.cssText='position:fixed;inset:0;width:100%;height:100%;pointer-events:none;z-index:99999';
  document.body.appendChild(cv);
  var W=cv.width=innerWidth,H=cv.height=innerHeight,ctx=cv.getContext('2d');
  var cols=['#ff5e7e','#ffc93c','#3cc68f','#4fb0ef','#a88fff','#ff8f3c'];
  var N=lv>=2?320:160,P=[];for(var i=0;i<N;i++)P.push({x:W/2+(Math.random()-.5)*W*.3,y:H*.35,vx:(Math.random()-.5)*(lv>=2?18:14),
    vy:-Math.random()*13-4,r:Math.random()*6+4,c:cols[i%cols.length],a:Math.random()*6,va:(Math.random()-.5)*.3,s:lv>=2&&i%4===0});
  var t0=performance.now();
  (function f(t){ctx.clearRect(0,0,W,H);var k=(t-t0)/2600;
    P.forEach(function(p){p.vy+=.35;p.vx*=.99;p.x+=p.vx;p.y+=p.vy;p.a+=p.va;
      ctx.save();ctx.globalAlpha=Math.max(0,1-k);ctx.translate(p.x,p.y);ctx.rotate(p.a);
      ctx.fillStyle=p.c;if(p.s){ctx.beginPath();for(var q=0;q<10;q++){var rr=q%2?p.r*.45:p.r,aa=q*Math.PI/5;ctx.lineTo(Math.cos(aa)*rr,Math.sin(aa)*rr);}
      ctx.fill();}else ctx.fillRect(-p.r/2,-p.r/4,p.r,p.r/2);ctx.restore();});
    if(k<1)requestAnimationFrame(f);else cv.remove();})(t0);
}
"""

REVIEWER_CSS = r"""
:root{--pf-card:rgba(255,255,255,.96);--pf-ink:#1d1d1f;--pf-soft:rgba(128,128,128,.14);--pf-line:rgba(128,128,128,.22);
  --pf-shadow:0 4px 16px rgba(0,0,0,.11);--pf-accent:#6b4dff;--pf-gold:#c98a00;--pf-red:#d6336c;--pf-green:#2b8a3e}
.nightMode,.night-mode,body.night_mode{--pf-card:rgba(30,32,40,.96);--pf-ink:#eceef3;--pf-shadow:0 4px 16px rgba(0,0,0,.35);
  --pf-accent:#9d86ff;--pf-gold:#f2b93b;--pf-red:#ff7a9c;--pf-green:#5fd38a}
#planif-hud{position:fixed;bottom:12px;right:12px;z-index:9999;display:flex;align-items:center;gap:12px;
  padding:7px 14px 7px 10px;border-radius:14px;background:var(--pf-card);color:var(--pf-ink);
  font:600 12.5px/1.2 system-ui,sans-serif;box-shadow:var(--pf-shadow);pointer-events:none}
#planif-hud .m{font-size:26px;display:inline-block}
#planif-hud .wxb{position:relative;flex:none;width:50px;height:50px;border-radius:14px;overflow:hidden;display:flex;align-items:center;
  justify-content:center;background:linear-gradient(180deg,#8fcbfa,#d7ecff);box-shadow:inset 0 0 0 1px rgba(0,0,0,.06)}
#planif-hud .wxb .m{font-size:30px;position:relative;z-index:2;margin-top:6px}
#planif-hud .wxb.p-night{background:linear-gradient(180deg,#141a45,#2a2360)}
#planif-hud .wxb.p-dusk{background:linear-gradient(180deg,#7d4c8a,#ff9f6a)} #planif-hud .wxb.p-dawn{background:linear-gradient(180deg,#9aa7e8,#ffd1b0)}
#planif-hud .wxb.k-rain,#planif-hud .wxb.k-storm{background:linear-gradient(180deg,#7d8b99,#b8c3cd)}
#planif-hud .wxb.k-rain.p-night,#planif-hud .wxb.k-storm.p-night{background:linear-gradient(180deg,#1d2433,#3a4456)}
#planif-hud .wxb.k-snow{background:linear-gradient(180deg,#c9d6e3,#f1f5f9)} #planif-hud .wxb.k-fog{background:linear-gradient(180deg,#b7bec6,#dde1e5)}
#planif-hud .wxb.k-clouds{background:linear-gradient(180deg,#a9bccf,#dfe8f0)}
#planif-hud .wxfx i{position:absolute;font-style:normal;pointer-events:none;will-change:transform}
#planif-hud .wxfx .d{width:2px;height:7px;border-radius:2px;background:rgba(255,255,255,.85);top:-8px;animation:wxRain 1s linear infinite}
#planif-hud .wxfx .d:nth-child(1){left:8px;animation-delay:-.2s}#planif-hud .wxfx .d:nth-child(2){left:20px;animation-delay:-.6s}
#planif-hud .wxfx .d:nth-child(3){left:33px;animation-delay:-.4s}#planif-hud .wxfx .d:nth-child(4){left:43px;animation-delay:-.8s}
@keyframes wxRain{to{transform:translate(-4px,62px)}}
#planif-hud .wxfx .f{color:#fff;font-size:9px;top:-10px;animation:wxSnow 3s linear infinite;text-shadow:0 0 2px rgba(80,110,150,.6)}
#planif-hud .wxfx .f:nth-child(1){left:6px}#planif-hud .wxfx .f:nth-child(2){left:22px;animation-delay:-1s}#planif-hud .wxfx .f:nth-child(3){left:38px;animation-delay:-2s}
@keyframes wxSnow{to{transform:translate(3px,64px) rotate(120deg)}}
#planif-hud .wxfx .bolt{font-size:12px;right:2px;top:1px;animation:wxBolt 4s steps(1) infinite}
@keyframes wxBolt{0%,86%{opacity:0}88%,92%{opacity:1}90%{opacity:.2}}
#planif-hud .wxfx .sun{font-size:13px;right:2px;top:1px;animation:wxSpin 12s linear infinite}
@keyframes wxSpin{to{transform:rotate(360deg)}}
#planif-hud .wxfx .moon{font-size:11px;right:3px;top:2px}
#planif-hud .wxfx .st{width:2px;height:2px;border-radius:50%;background:#fff;animation:wxTw 2.4s ease-in-out infinite}
#planif-hud .wxfx .st:nth-of-type(odd){left:7px;top:6px}#planif-hud .wxfx .st:nth-of-type(even){left:17px;top:12px;animation-delay:-1.2s}
@keyframes wxTw{50%{opacity:.2}}
#planif-hud .wxfx .cl{font-size:14px;top:1px;left:-14px;animation:wxDrift 9s linear infinite;opacity:.9}
@keyframes wxDrift{to{transform:translateX(70px)}}
#planif-hud .wxfx .fog{left:0;right:0;top:26px;height:10px;background:rgba(255,255,255,.55);border-radius:6px;animation:wxFog 5s ease-in-out infinite alternate}
@keyframes wxFog{to{transform:translateX(8px)}}
#planif-hud .wxacc span{position:absolute;z-index:3;pointer-events:none;line-height:1}
#planif-hud .wxacc .umb{font-size:20px;top:1px;left:50%;transform:translateX(-50%) rotate(-12deg)}
#planif-hud .wxacc .scarf{font-size:13px;bottom:4px;left:50%;transform:translateX(-50%)}
#planif-hud .wxacc .shades{font-size:12px;top:22px;left:50%;transform:translateX(-50%)}
#planif-hud .wxacc .zz{font:800 9px system-ui;color:#c9d2ff;top:9px;right:7px;animation:wxTw 2s ease-in-out infinite}
#planif-hud .wxt{position:absolute;z-index:4;bottom:1px;right:3px;font:800 9.5px system-ui;color:#fff;text-shadow:0 1px 2px rgba(0,0,0,.55)}
@media (prefers-reduced-motion:reduce){#planif-hud .wxfx i{animation:none}}
#planif-hud .lv{display:flex;flex-direction:column;gap:4px;min-width:150px}
#planif-hud .tp{display:flex;justify-content:space-between;gap:8px}
#planif-hud .tp span{font-weight:500;opacity:.75}
#planif-hud .xb{height:8px;border-radius:8px;background:rgba(128,128,128,.25);overflow:hidden}
#planif-hud .xb div{height:100%;border-radius:8px;background:linear-gradient(90deg,#7a5cff,#4fb0ef);transition:width .6s cubic-bezier(.3,1.3,.5,1)}
#planif-hud .xb.bump{animation:phGlow .6s}
@keyframes phGlow{40%{box-shadow:0 0 0 3px rgba(122,92,255,.35)}}
#planif-hud .nx{font-weight:500;opacity:.85;white-space:nowrap}
#planif-hud .nx .big{font-size:18px;vertical-align:-2px}
#planif-hud .nx b{color:#d99a0b}
#planif-hud .co{font-size:14px;font-weight:800;color:#c98a00;white-space:nowrap}
#planif-hud .co.bump{animation:pfBounce .45s}
#planif-hud .gl{font-weight:500;opacity:.7;white-space:nowrap}
.planif-fly{position:fixed;z-index:10001;pointer-events:none;line-height:1;font-size:34px;filter:drop-shadow(0 4px 8px rgba(0,0,0,.28))}
.planif-fly.mini{font-size:20px}
.planif-lbl{position:fixed;z-index:10000;pointer-events:none;transform:translate(-50%,0);white-space:nowrap;
  font:800 18px system-ui,sans-serif;padding:3px 10px;border-radius:999px;box-shadow:0 4px 12px rgba(0,0,0,.15);
  animation:plLbl 2.3s ease forwards}
.planif-lbl.xp{background:linear-gradient(90deg,#7a5cff,#4fb0ef);color:#fff}
.planif-lbl.coin{background:#fff3c4;color:#8a5a00;border:2px solid #f2b93b}
.planif-lbl.coin.win{font-size:21px;background:linear-gradient(180deg,#ffe27a,#f5b000);color:#5a3a00;border-color:#fff3c4}
.planif-lbl.coin.miss{font-size:15px}
.planif-lbl.shine{box-shadow:0 0 16px rgba(255,200,60,.8),0 4px 12px rgba(0,0,0,.15)}
#planif-hud .co.sparkle{animation:coSpark 1.2s ease-out}
/* tickets : petites languettes qui sortent de derrière un panneau (gains, combo, boss, chrono) */
.planif-tab{position:fixed;z-index:9997;pointer-events:none;display:flex;align-items:center;gap:7px;overflow:hidden;
  padding:5px 11px 10px;border-radius:11px 11px 0 0;background:var(--pf-card);color:var(--pf-ink);
  font:700 12.5px/1.25 system-ui,sans-serif;font-variant-numeric:tabular-nums;box-shadow:0 -3px 12px rgba(0,0,0,.08);
  transform:translateY(100%);opacity:0}
.planif-tab.free{border-radius:11px;padding-bottom:6px;box-shadow:var(--pf-shadow)}
.planif-tab.on{transform:translateY(5px);opacity:1;transition:transform .5s cubic-bezier(.2,1.3,.35,1),opacity .2s}
.planif-tab.free.on{transform:none}
.planif-tab.out{transform:translateY(100%);opacity:0;transition:transform .32s cubic-bezier(.6,0,.85,.25),opacity .2s .12s}
.planif-tab.pop b,.planif-tab.pop>span{display:inline-block;animation:tkPop .32s}
@keyframes tkPop{40%{transform:scale(1.2)}}
.planif-tab .sh{position:absolute;inset:0;background:linear-gradient(100deg,transparent 40%,rgba(255,255,255,.6) 50%,transparent 60%);transform:translateX(-120%)}
.planif-tab.on .sh{animation:tkShine 1s .3s ease-out}
@keyframes tkShine{to{transform:translateX(120%)}}
#planif-tk{z-index:9998}
#planif-tk .x{color:var(--pf-accent)} #planif-tk .x b{background:linear-gradient(90deg,#7a5cff,#3fa6ec);-webkit-background-clip:text;background-clip:text;color:transparent}
#planif-tk .c{display:inline-flex;align-items:center;gap:3px;color:var(--pf-gold)}
#planif-tk .sep{width:1px;height:12px;background:var(--pf-line)}
#planif-tk .bo{font-size:9.5px;padding:2px 4px;border-radius:5px;background:#7a5cff;color:#fff}
#planif-tk.miss.on{opacity:.75}
#planif-tk.lv2{box-shadow:0 -3px 12px rgba(245,183,0,.28)}
#planif-combo{z-index:9998;color:#e8590c;font-weight:800}
/* boss : attaques et résultats, accrochés au panneau du boss */
#planif-btk{align-items:flex-start;max-width:262px;font-weight:600}
#planif-btk .ba{font-size:18px;line-height:1.1}
#planif-btk b{display:block;color:var(--pf-red);font-weight:800}
#planif-btk small{display:block;font-size:11.5px;font-weight:500;opacity:.85}
#planif-btk.res-ok b{color:var(--pf-green)} #planif-btk.res-ko b{color:#e8590c}
#planif-btk::before{content:'';position:absolute;left:0;top:0;bottom:0;width:3px;background:var(--pf-red)}
#planif-btk.res-ok::before{background:var(--pf-green)} #planif-btk.res-ko::before{background:#e8590c}
#planif-btm{gap:5px;font-size:13px;color:#e8590c}
#planif-btm b{font-size:15px;min-width:18px;text-align:right}
#planif-btm small{font-weight:600;opacity:.7}
#planif-btm .tb{position:absolute;left:0;right:0;bottom:5px;height:2px;background:var(--pf-soft)}
#planif-btm .tb i{display:block;height:100%;width:100%;background:#e8590c}
#planif-btm.hurry{color:var(--pf-red)} #planif-btm.hurry .tb i{background:var(--pf-red)}
#planif-btm.hurry b{animation:tkPop .5s}
#planif-btm.over{color:#868e96}
@media (prefers-reduced-motion:reduce){.planif-tab.on,.planif-tab.out{transition:opacity .2s}.planif-tab .sh,#planif-hud .xb::after{display:none}}
#planif-hud .xb{position:relative}
#planif-hud .xb::after{content:'';position:absolute;inset:0;background:linear-gradient(100deg,transparent 35%,rgba(255,255,255,.6) 50%,transparent 65%);transform:translateX(-110%)}
#planif-hud .xb.sweep::after{animation:xbSweep .85s ease-out}
@keyframes xbSweep{to{transform:translateX(110%)}}
@media (prefers-reduced-motion:reduce){#planif-tk.on,#planif-tk.out{transition:opacity .2s}#planif-tk .sh,#planif-hud .xb::after{display:none}}
@keyframes coSpark{0%,100%{text-shadow:none}30%{text-shadow:0 0 12px #ffd43b,0 0 24px #ff922b}}
@keyframes plLbl{0%{opacity:0;transform:translate(-50%,8px) scale(.7)}10%{opacity:1;transform:translate(-50%,0) scale(1.08)}
  18%{transform:translate(-50%,0) scale(1)}75%{opacity:1;transform:translate(-50%,-6px)}100%{opacity:0;transform:translate(-50%,-16px)}}
#planif-buddy{position:fixed;left:50%;bottom:62px;z-index:9996;display:flex;align-items:flex-end;gap:6px;pointer-events:none;
  transform:translate(-50%,40px) scale(.85);opacity:0;visibility:hidden;
  transition:transform .5s cubic-bezier(.2,1.35,.4,1),opacity .35s ease,visibility 0s linear .5s}
#planif-buddy.on{transform:translate(-50%,0);opacity:1;visibility:visible;transition:transform .5s cubic-bezier(.2,1.35,.4,1),opacity .3s ease,visibility 0s}
.planif-pad-on #planif-buddy{bottom:calc(var(--planif-pad-h) + 62px)}
#planif-buddy .bm{font-size:56px;line-height:1;filter:drop-shadow(0 6px 10px rgba(0,0,0,.25))}
#planif-buddy.on .bm{animation:pbBob 1.8s ease-in-out infinite}
@keyframes pbBob{50%{transform:translateY(-6px) rotate(-4deg)}}
#planif-buddy .bb{position:relative;max-width:340px;min-width:120px;background:var(--pf-card);color:var(--pf-ink);border-radius:14px;padding:9px 14px 10px;
  font:14px/1.4 system-ui,sans-serif;box-shadow:var(--pf-shadow);margin-bottom:28px;text-align:left}
#planif-buddy .bb::before{content:'';position:absolute;left:-8px;bottom:14px;border-style:solid;border-width:8px 10px 8px 0;
  border-color:transparent #fff transparent transparent}
#planif-buddy .nm{display:block;font-weight:700;font-size:11.5px;color:var(--pf-accent);margin-bottom:2px}
.nightMode #planif-buddy .bb,.night-mode #planif-buddy .bb,body.night_mode #planif-buddy .bb{background:#2a2d38;color:#eceef3}
.nightMode #planif-buddy .bb::before,.night-mode #planif-buddy .bb::before,body.night_mode #planif-buddy .bb::before{border-right-color:#2a2d38}
.planif-bounce{animation:pfBounce .5s}
@keyframes pfBounce{30%{transform:translateY(-8px) scale(1.15)}60%{transform:translateY(0) scale(.95)}}
.planif-float{position:fixed;left:50%;bottom:70px;transform:translateX(-50%);z-index:9999;pointer-events:none;
  font:800 20px system-ui,sans-serif;color:#e0a100;text-shadow:0 2px 6px rgba(0,0,0,.25);animation:pfUp 1.3s ease-out forwards}
.planif-float.win{font-size:24px;color:#f5b000}
.planif-float.miss{font-size:16px;color:#8a94a6}
@keyframes pfUp{from{opacity:0;transform:translate(-50%,10px)}15%{opacity:1}to{opacity:0;transform:translate(-50%,-70px)}}
#planif-toast{position:fixed;bottom:88px;left:50%;transform:translate(-50%,14px);z-index:9999;pointer-events:none;
  background:var(--pf-card);color:var(--pf-ink);border-radius:12px;padding:7px 14px;font:600 12.5px/1.4 system-ui,sans-serif;
  text-align:center;max-width:min(520px,56vw);box-shadow:var(--pf-shadow);opacity:0;
  transition:transform .45s cubic-bezier(.2,1.3,.35,1),opacity .2s}
#planif-toast.on{opacity:1;transform:translate(-50%,0)}
.planif-pad-on #planif-toast{bottom:calc(var(--planif-pad-h) + 88px)}
.planif-combo-big{position:fixed;left:50%;top:38%;transform:translate(-50%,-50%);z-index:10003;pointer-events:none;
  font:900 44px system-ui,sans-serif;color:#ffb020;text-shadow:0 3px 0 #c2410c;animation:comboBig 1.6s ease-out forwards}
@keyframes comboBig{0%{opacity:0;transform:translate(-50%,-50%) scale(.3) rotate(-8deg)}20%{opacity:1;transform:translate(-50%,-50%) scale(1.15) rotate(3deg)}
  70%{opacity:1;transform:translate(-50%,-50%) scale(1)}100%{opacity:0;transform:translate(-50%,-70%) scale(1)}}
#planif-bubble{position:fixed;bottom:60px;right:14px;z-index:9999;pointer-events:none;max-width:230px;
  background:var(--pf-card);color:var(--pf-ink);border-radius:14px 14px 4px 14px;padding:8px 12px;font:13px/1.4 system-ui,sans-serif;
  box-shadow:var(--pf-shadow);opacity:0;transition:opacity .3s}
#planif-bubble.on{opacity:1}
.planif-spark{position:fixed;width:9px;height:9px;border-radius:50%;pointer-events:none;z-index:9998}
.planif-spark.star{width:auto;height:auto;border-radius:0;font-size:22px;line-height:1;filter:drop-shadow(0 0 6px rgba(255,210,80,.9))}
.planif-ring.rainbow{border:6px solid transparent;background:conic-gradient(#ff6b9d,#ffd43b,#69db7c,#4dabf7,#b197fc,#ff6b9d) border-box;
  -webkit-mask:linear-gradient(#000 0 0) padding-box,linear-gradient(#000 0 0);-webkit-mask-composite:xor;mask-composite:exclude;box-shadow:none}
.planif-glow{position:fixed;inset:0;pointer-events:none;z-index:9996;background:radial-gradient(circle at 50% 70%,rgba(255,230,140,.55),transparent 60%)}
.planif-shoot{position:fixed;pointer-events:none;z-index:9998;font-size:26px;color:#ffe066;text-shadow:0 0 10px #ffd43b,0 0 20px #ff922b}
.planif-ring{position:fixed;width:260px;height:260px;border-radius:50%;pointer-events:none;z-index:9997;
  border:5px solid rgba(255,212,59,.85);box-shadow:0 0 30px rgba(255,212,59,.6),inset 0 0 30px rgba(255,212,59,.45)}
#planif-tools{position:fixed;bottom:12px;left:12px;z-index:10000;display:flex;gap:8px}
#planif-tools button{font:600 12.5px system-ui,sans-serif;
  padding:7px 13px;border-radius:12px;border:1px solid var(--pf-line);background:var(--pf-card);
  color:var(--pf-ink);cursor:pointer;opacity:.75;box-shadow:var(--pf-shadow);transition:opacity .2s}
#planif-tools button:hover{opacity:1}
.nightMode #planif-tools button,.night-mode #planif-tools button,body.night_mode #planif-tools button{background:rgba(30,32,40,.92);color:#eceef3}
#planif-tools #planif-lock.on{background:#d2463a;border-color:#d2463a;color:#fff;opacity:1}
#planif-tools #planif-typebtn.on{background:#4f63d8;border-color:#4f63d8;color:#fff;opacity:1}
/* zone de réponse tapée */
:root{--planif-pad-h:32vh}
#planif-pad{display:none;position:fixed;left:0;right:0;bottom:0;height:var(--planif-pad-h);z-index:9990;flex-direction:column;
  background:rgba(250,251,253,.97);color:#1d1d1f;border-top:2px solid rgba(79,99,216,.35);box-shadow:0 -6px 24px rgba(0,0,0,.12)}
.nightMode #planif-pad,.night-mode #planif-pad,body.night_mode #planif-pad{background:rgba(28,30,38,.97);color:#eceef3}
.planif-pad-on #planif-pad{display:flex}
#planif-pad .bar{display:flex;gap:6px;align-items:center;padding:6px 12px;font:13px system-ui,sans-serif;flex:none}
#planif-pad .bar button{font:600 13px system-ui,sans-serif;padding:4px 10px;border-radius:8px;border:1px solid rgba(128,128,128,.4);
  background:transparent;color:inherit;cursor:pointer}
#planif-pad .bar .sp{flex:1}
#planif-pad .hint b{display:inline-block;padding:0 6px;border-radius:5px;border:1px solid rgba(128,128,128,.45);margin:0 2px}
#planif-pad .hint.ans{color:#1f9e6e}
#planif-ta{flex:1;min-height:0;overflow:auto;margin:0 12px 12px;border:1.5px solid var(--pp-border,rgba(128,128,128,.35));
  border-radius:10px;padding:8px 12px 8px var(--pp-pl,12px);font-size:17px;line-height:28px;
  font-family:var(--pp-font,system-ui,sans-serif);color:var(--pp-ink,inherit);background-color:var(--pp-bg,transparent);
  background-image:var(--pp-lines,none);background-attachment:local;background-position:0 8px;
  box-shadow:var(--pp-shadow,none);outline:none;white-space:pre-wrap;overflow-wrap:break-word;text-align:left;cursor:text}
#planif-ta:focus{border-color:#4f63d8}
#planif-ta:empty:before{content:attr(data-ph);opacity:.45;pointer-events:none}
#planif-ta[contenteditable=false]{border-style:dashed}
#planif-ta.lv2:focus,#planif-ta.lv3:focus{box-shadow:0 0 0 4px rgba(122,92,255,.18),0 0 22px rgba(79,176,239,.28)}
#planif-ta.lv3{border-image:linear-gradient(90deg,#7a5cff,#4fb0ef,#3cc68f,#ffd43b,#ff6b9d) 1;border-width:2px;border-radius:0}
#planif-ta.lv3.flashy{animation:taFlash .9s ease-out}
@keyframes taFlash{0%{box-shadow:0 0 0 0 rgba(122,92,255,.55)}100%{box-shadow:0 0 0 14px rgba(122,92,255,0)}}
#planif-ta.corr-mode{border-color:var(--pp-corr,#e03131);border-style:solid;border-width:2px}
#planif-pad .hint i.sw{display:inline-block;width:11px;height:11px;border-radius:50%;vertical-align:-1px;margin:0 3px}
body.planif-pad-on{padding-bottom:calc(var(--planif-pad-h) + 70px)!important}
.planif-pad-on #planif-tools,.planif-pad-on #planif-hud{bottom:calc(var(--planif-pad-h) + 12px)}
@media (max-width:900px){#planif-hud .gl,#planif-hud .nx{display:none}}
#planif-boss{position:fixed;left:12px;bottom:56px;z-index:9998;display:flex;align-items:center;gap:6px;width:262px;
  padding:6px 10px 7px 6px;border-radius:14px;background:var(--pf-card);color:var(--pf-ink);box-shadow:var(--pf-shadow);
  font:600 12px/1.2 system-ui,sans-serif;pointer-events:none}
.planif-pad-on #planif-boss{bottom:calc(var(--planif-pad-h) + 56px)}
#planif-boss .bi{font-size:38px;line-height:1;position:relative}
#planif-boss .bh{font-size:34px;line-height:1;display:inline-block}
#planif-boss .bh.atk{animation:heroAtk .35s ease-out}
@keyframes heroAtk{40%{transform:translateX(9px) rotate(8deg)}}
#planif-boss .bi.hit{animation:bossHit .35s}
#planif-boss .bi.hit::after{content:'';position:absolute;inset:0;border-radius:50%;background:rgba(255,80,80,.45);animation:hitFlash .4s forwards}
@keyframes hitFlash{to{opacity:0}}
@keyframes bossHit{25%{transform:translateX(-4px) rotate(-6deg)}50%{transform:translateX(4px) rotate(5deg)}75%{transform:translateX(-2px)}}
#planif-boss .bt{flex:1;min-width:0}
#planif-boss .bn{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
#planif-boss .bn small{opacity:.6;font-weight:500}
#planif-boss .hb{height:8px;border-radius:8px;background:var(--pf-soft);overflow:hidden;margin:4px 0 2px}
#planif-boss .hf{height:100%;border-radius:9px;background:linear-gradient(90deg,#e03131,#ff6b6b);transition:width .45s cubic-bezier(.3,1.2,.5,1)}
#planif-boss .hv{font-size:10.5px;opacity:.7;font-weight:500}
#planif-boss .hb{position:relative}
#planif-boss .hs{position:absolute;right:0;top:0;bottom:0;background:repeating-linear-gradient(45deg,#868e96,#868e96 3px,#adb5bd 3px,#adb5bd 6px);border-radius:9px}
#planif-boss .hx{display:flex;flex-direction:column;gap:2px;margin-top:3px}
#planif-boss .hx span{font-size:10.5px;font-weight:700;border-radius:6px;padding:1px 5px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
#planif-boss .hx .bad{background:rgba(224,49,49,.12);color:#c92a2a} #planif-boss .hx .good{background:rgba(47,158,68,.14);color:#2b8a3e}
#planif-boss.rage{box-shadow:inset 3px 0 0 var(--pf-red),var(--pf-shadow)}
#planif-boss.atk{animation:bAtk .6s}
@keyframes bAtk{20%{transform:translate(6px,-4px) scale(1.06)}40%{transform:translate(-5px,2px)}60%{transform:translate(4px,0)}}
#planif-atk{position:fixed;z-index:100001;font:600 13px/1.35 system-ui,sans-serif;color:var(--pf-ink)}
#planif-atk.banner{left:50%;top:18px;transform:translateX(-50%);display:flex;gap:10px;align-items:center;max-width:min(560px,92vw);
  background:#fff;border-radius:16px;padding:10px 16px 10px 10px;box-shadow:0 10px 40px rgba(0,0,0,.3);border:3px solid #e03131;
  animation:atkIn .45s cubic-bezier(.2,1.5,.4,1);cursor:pointer}
#planif-atk.banner.res-ok{border-color:#2f9e44} #planif-atk.banner.res-ko{border-color:#f08c00}
#planif-atk.out{opacity:0;transition:opacity .4s}
@keyframes atkIn{from{transform:translate(-50%,-40px) scale(.7);opacity:0}}
#planif-atk .qart{font-size:40px;line-height:1;flex:0 0 auto;animation:bossHit .5s}
#planif-atk .qt{font-weight:800;font-size:15px;color:var(--pf-red)}
#planif-atk .qb{font-weight:500}
#planif-atk.quiz{inset:0;display:flex;align-items:center;justify-content:center;background:rgba(10,8,25,.45);animation:fadeIn .3s}
@keyframes fadeIn{from{opacity:0}}
#planif-atk .qcard{position:relative;overflow:hidden;background:var(--pf-card);border-radius:16px;padding:18px 20px 16px 22px;width:min(560px,92vw);
  box-shadow:0 18px 50px rgba(0,0,0,.3);animation:atkIn2 .45s cubic-bezier(.2,1.3,.35,1)}
#planif-atk .qcard::before{content:'';position:absolute;left:0;top:0;bottom:0;width:4px;background:var(--pf-red)}
@keyframes atkIn2{from{transform:translateY(24px);opacity:0}}
#planif-atk .qtop{display:flex;gap:12px;align-items:center;margin-bottom:10px}
#planif-atk .qq{font-size:17px;font-weight:700;background:var(--pf-soft);border-radius:12px;padding:12px 14px;margin-bottom:12px;max-height:30vh;overflow:auto}
#planif-atk .qc{display:grid;grid-template-columns:1fr 1fr;gap:8px}
#planif-atk .qc button{font:600 14px system-ui,sans-serif;text-align:left;padding:10px 12px;border-radius:12px;border:1.5px solid var(--pf-line);background:transparent;color:var(--pf-ink);cursor:pointer;transition:border-color .15s,background .15s}
#planif-atk .qc button:hover:not(:disabled){border-color:var(--pf-accent);background:rgba(107,77,255,.06)}
#planif-atk .qc button b{display:inline-block;width:20px;height:20px;border-radius:6px;background:var(--pf-soft);text-align:center;font-size:12px;line-height:20px;margin-right:4px}
#planif-atk .qc button.picked{border-color:var(--pf-accent)}
#planif-atk .qc button.good{border-color:var(--pf-green);background:rgba(47,158,68,.1)} #planif-atk .qc button.bad{border-color:var(--pf-red);background:rgba(214,51,108,.08)}
#planif-atk .qn{margin-top:10px;font-size:12px;color:#868e96} #planif-atk .qn.ok{color:#2b8a3e;font-size:14px;font-weight:800} #planif-atk .qn.ko{color:#c92a2a;font-size:14px;font-weight:800}
#planif-timer{position:fixed;right:18px;top:18px;z-index:100000;background:#fff;border:3px solid #f08c00;border-radius:999px;padding:6px 14px;
  font:900 20px system-ui,sans-serif;color:#e8590c;box-shadow:0 6px 20px rgba(0,0,0,.2);animation:atkIn2 .3s}
#planif-timer.over{border-color:#868e96;color:#868e96}
@media (max-width:600px){#planif-atk .qc{grid-template-columns:1fr}}

.planif-dmg{position:fixed;z-index:10002;pointer-events:none;font:900 22px system-ui,sans-serif;color:#e03131;
  text-shadow:0 1px 0 rgba(255,255,255,.9);animation:dmgUp 1.1s ease-out forwards}
.planif-dmg.crit{font-size:28px;color:#f08c00}
@keyframes dmgUp{0%{opacity:0;transform:translate(0,6px) scale(.6)}15%{opacity:1;transform:translate(0,-6px) scale(1.2)}
  100%{opacity:0;transform:translate(0,-46px) scale(1)}}
.planif-pad-on #planif-bubble{bottom:calc(var(--planif-pad-h) + 60px)}
.planif-pad-on .planif-float{bottom:calc(var(--planif-pad-h) + 70px)}
#planif-lvl{position:fixed;inset:0;z-index:100000;display:flex;flex-direction:column;align-items:center;justify-content:center;
  background:radial-gradient(circle at 50% 42%,rgba(40,30,80,.82),rgba(8,10,18,.92));color:#fff;cursor:pointer;
  font-family:system-ui,sans-serif;text-align:center;animation:plIn .35s ease-out}
#planif-lvl.out{animation:plOut .6s ease-in forwards}
@keyframes plIn{from{opacity:0}} @keyframes plOut{to{opacity:0}}
#planif-lvl .stage{position:relative;width:260px;height:260px;display:flex;align-items:center;justify-content:center}
#planif-lvl .rays{position:absolute;left:50%;top:50%;width:560px;height:560px;margin:-280px 0 0 -280px;border-radius:50%;opacity:0;
  background:repeating-conic-gradient(from 0deg,rgba(255,214,90,.2) 0deg 9deg,transparent 9deg 22deg);
  -webkit-mask:radial-gradient(circle,#000 18%,transparent 68%);mask:radial-gradient(circle,#000 18%,transparent 68%);
  animation:plRays 1s ease-out forwards,plSpin 14s linear infinite}
#planif-lvl .glow{position:absolute;width:200px;height:200px;border-radius:50%;background:radial-gradient(circle,rgba(255,230,140,.45),transparent 70%);opacity:0;animation:plRays 1s ease-out forwards}
#planif-lvl .m{position:absolute;font-size:150px;line-height:1;filter:drop-shadow(0 10px 30px rgba(0,0,0,.45))}
#planif-lvl .flash{position:fixed;inset:0;background:#fff;opacity:0;pointer-events:none}
#planif-lvl .txt{opacity:0;transform:translateY(16px);animation:plTxt .6s ease-out forwards}
#planif-lvl .t1{font-size:15px;letter-spacing:.14em;text-transform:uppercase;color:#ffd65a;margin-top:18px}
#planif-lvl .t2{font-size:40px;font-weight:800;margin-top:4px}
#planif-lvl .t3{font-size:19px;margin-top:8px;color:#e8e2ff}
#planif-lvl .t4{font-size:12px;margin-top:26px;color:rgba(255,255,255,.55)}
/* simple montée de niveau */
#planif-lvl.simple .old{display:none}
#planif-lvl.simple .new{animation:plPop .9s cubic-bezier(.2,1.6,.4,1) both}
#planif-lvl.simple .rays,#planif-lvl.simple .glow{animation-delay:.1s,0s}
#planif-lvl.simple .txt{animation-delay:.45s}
/* évolution : l'œuf tremble, flash, éclosion */
#planif-lvl.evo .old{animation:plShake 1.5s ease-in both,plBurst .35s ease-in 1.5s forwards}
#planif-lvl.evo .new{opacity:0;transform:scale(0);animation:plPop .9s cubic-bezier(.2,1.6,.4,1) 1.62s forwards}
#planif-lvl.evo .flash{animation:plFlash .7s ease-out 1.5s}
#planif-lvl.evo .rays,#planif-lvl.evo .glow{animation-delay:1.6s,1.6s;animation-fill-mode:forwards}
#planif-lvl.evo .glow{animation-delay:1.6s}
#planif-lvl.evo .txt{animation-delay:2.1s}
@keyframes plShake{0%{transform:rotate(0)}10%{transform:rotate(-4deg)}20%{transform:rotate(4deg)}30%{transform:rotate(-7deg)}
  40%{transform:rotate(7deg)}50%{transform:rotate(-10deg) scale(1.03)}60%{transform:rotate(10deg) scale(1.05)}
  70%{transform:rotate(-14deg) scale(1.07)}80%{transform:rotate(14deg) scale(1.09)}90%{transform:rotate(-16deg) scale(1.12)}
  100%{transform:rotate(0) scale(1.15)}}
@keyframes plBurst{to{transform:scale(1.9);opacity:0;filter:brightness(3) blur(4px)}}
@keyframes plFlash{0%{opacity:0}15%{opacity:.95}100%{opacity:0}}
@keyframes plPop{0%{opacity:0;transform:scale(0) rotate(-20deg)}60%{opacity:1;transform:scale(1.25) rotate(6deg)}100%{opacity:1;transform:scale(1) rotate(0)}}
@keyframes plRays{from{opacity:0;transform:scale(.4)}to{opacity:1;transform:scale(1)}}
@keyframes plSpin{to{rotate:360deg}}
@keyframes plTxt{to{opacity:1;transform:none}}
@media (prefers-reduced-motion:reduce){#planif-lvl *,#planif-lvl{animation-duration:.01s!important;animation-delay:0s!important}}
@media (prefers-reduced-motion:reduce){.planif-float,.planif-bounce,#planif-combo.pop{animation:none}}
"""

WEATHER_JS = r"""
/* ───── météo animée (pluie, neige, orage, nuages, étoiles) ───── */
function planifWeather(kind,phase){
  function go(){
    if(document.getElementById('planif-wx'))return;
    var cv=document.createElement('canvas');cv.id='planif-wx';
    cv.style.cssText='position:fixed;inset:0;width:100%;height:100%;pointer-events:none;z-index:0;opacity:.55';
    document.body.insertBefore(cv,document.body.firstChild);
    var ctx=cv.getContext('2d'),W,H,P=[],clouds=[],stars=[],flash=0;
    function size(){W=cv.width=innerWidth;H=cv.height=innerHeight;}
    size();addEventListener('resize',size);
    var rain=kind==='rain'||kind==='storm',snow=kind==='snow';
    var n=rain?(kind==='storm'?110:80):snow?60:0;
    for(var i=0;i<n;i++)P.push({x:Math.random()*W,y:Math.random()*H,v:rain?6+Math.random()*5:0.4+Math.random()*.9,
      r:snow?1.2+Math.random()*2:0,l:rain?8+Math.random()*9:0,d:Math.random()*6.28});
    var nc=kind==='clouds'?4:(kind==='clear'?(phase==='night'?0:1):(kind==='fog'?0:3));
    for(var c=0;c<nc;c++)clouds.push({x:Math.random()*W,y:20+Math.random()*H*.35,s:.6+Math.random()*.9,v:.15+Math.random()*.25});
    if(phase==='night'&&kind==='clear')for(var k=0;k<70;k++)stars.push({x:Math.random()*W,y:Math.random()*H*.75,r:Math.random()*1.4+.3,t:Math.random()*6.28});
    var dark=phase==='night'||kind==='storm'||kind==='rain';
    function cloud(x,y,s){ctx.beginPath();
      [[0,0,28],[26,-10,24],[50,0,26],[22,8,24],[-22,6,20]].forEach(function(b){ctx.moveTo(x+b[0]*s+b[2]*s,y+b[1]*s);ctx.arc(x+b[0]*s,y+b[1]*s,b[2]*s,0,6.29);});
      ctx.fill();}
    function frame(){
      ctx.clearRect(0,0,W,H);
      stars.forEach(function(st){st.t+=.015;ctx.globalAlpha=.25+.45*Math.abs(Math.sin(st.t));ctx.fillStyle='#fff';ctx.beginPath();ctx.arc(st.x,st.y,st.r,0,6.29);ctx.fill();});
      ctx.globalAlpha=1;
      ctx.fillStyle=dark?'rgba(120,130,150,.25)':'rgba(255,255,255,.45)';
      clouds.forEach(function(c){c.x+=c.v*.6;if(c.x>W+120)c.x=-160;cloud(c.x,c.y,c.s);});
      if(kind==='fog'){var t=Date.now()/4000;for(var f=0;f<4;f++){ctx.fillStyle='rgba(255,255,255,.12)';
        ctx.fillRect(0,H*(.2+f*.2)+Math.sin(t+f)*20,W,H*.12);}}
      
      if(rain){ctx.strokeStyle=dark?'rgba(190,210,240,.35)':'rgba(120,140,170,.35)';ctx.lineWidth=1;ctx.beginPath();
        P.forEach(function(p){ctx.moveTo(p.x,p.y);ctx.lineTo(p.x-p.l*.25,p.y+p.l);p.y+=p.v;p.x-=p.v*.25;
          if(p.y>H){p.y=-20;p.x=Math.random()*(W+100);}});ctx.stroke();}
      if(snow){ctx.fillStyle=dark?'rgba(255,255,255,.55)':'rgba(170,185,205,.6)';P.forEach(function(p){p.d+=.02;p.y+=p.v;p.x+=Math.sin(p.d)*.6;
        if(p.y>H){p.y=-5;p.x=Math.random()*W;}ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,6.29);ctx.fill();});}
      if(kind==='storm'){if(flash>0){ctx.fillStyle='rgba(255,255,255,'+flash+')';ctx.fillRect(0,0,W,H);flash-=.015;}
        else if(Math.random()<.002){flash=.18;}}
      requestAnimationFrame(frame);
    }
    frame();
  }
  if(document.body)go();else document.addEventListener('DOMContentLoaded',go);
}
"""

REVIEWER_JS = SFX_JS + CONFETTI_JS + "var PLANIF_COIN='" + art.COIN + "';" + r"""
var planifCombo=0,planifCount=0,planifBubbleT=null,planifToastT=null;
var PLANIF_PHRASES=['Tu gères ! 💪','Encore quelques cartes et c\'est bon 🔥','Ton cerveau muscle ses neurones 🧠',
  'Chaque carte te rapproche de l\'examen 📅','Belle régularité 👏','On lâche rien ! ✨'];
function planifTabPlace(el,anchor,side){
  if(!anchor){el.classList.add('free');return;}el.classList.remove('free');
  var r=anchor.getBoundingClientRect();el.style.bottom=(innerHeight-r.top-1)+'px';
  if(side==='left'){el.style.left=(r.left+14)+'px';el.style.right='auto';}
  else{el.style.right=Math.max(8,innerWidth-r.right+16)+'px';el.style.left='auto';}
}
function planifTabShow(el){el.classList.remove('out');if(!el.classList.contains('on')){void el.offsetWidth;el.classList.add('on');}
  else{el.classList.remove('pop');void el.offsetWidth;el.classList.add('pop');}}
function planifTabHide(el){if(el&&el.classList.contains('on')){el.classList.remove('on','pop');el.classList.add('out');}}
function planifEl(id,tag){var e=document.getElementById(id);if(!e){e=document.createElement(tag||'div');e.id=id;document.body.appendChild(e);}return e;}
var planifLocked=false;
function planifToolBtn(id){
  var box=planifEl('planif-tools');
  var b=document.getElementById(id);
  if(!b){b=document.createElement('button');b.id=id;box.appendChild(b);}
  return b;
}
function planifLock(on){
  planifLocked=!!on;
  var b=planifToolBtn('planif-lock');
  b.className=on?'on':'';
  b.textContent=on?'🔒 Clavier bloqué':'⌨️ Clavier actif';
  b.title=on?'Clique pour réactiver les raccourcis clavier d\'Anki':'Clique pour bloquer les raccourcis clavier d\'Anki';
  b.onclick=function(e){e.preventDefault();pycmd('planif:lock');};
}
document.addEventListener('keydown',function(e){
  var tg=e.target,inText=tg&&(tg.tagName==='TEXTAREA'||tg.tagName==='INPUT'||tg.isContentEditable);
  var mod=e.metaKey||e.ctrlKey;
  if(planifTypeOn){
    if(planifSide==='q'){
      if(mod&&e.key==='Enter'){e.preventDefault();e.stopPropagation();pycmd('planif:reveal');return;}
      if(mod&&!e.shiftKey&&(e.key==='z'||e.key==='Z')){var tz=planifTA();
        if(!tz||!tz.innerText.trim()){e.preventDefault();e.stopPropagation();pycmd('planif:undo');return;}}
      if(e.key==='Tab'){e.preventDefault();return;}
      if(!inText&&!mod&&e.key.length===1){var t=planifTA();if(t)planifFocusEnd(t);}
      return;
    }
    if(planifCorr){
      if(e.key==='Escape'||(mod&&e.key==='Enter')){e.preventDefault();e.stopPropagation();planifEndCorr();return;}
      if(e.key==='Tab'){e.preventDefault();return;}
      if(!mod&&!e.isComposing&&(e.key.length===1||e.key==='Enter'||e.key==='Dead'))planifCorrColor();
      return;
    }
    if(/^[1-4]$/.test(e.key)&&!mod&&!e.altKey){e.preventDefault();e.stopPropagation();pycmd('planif:ease:'+e.key);return;}
    if(e.key==='Tab'){e.preventDefault();e.stopPropagation();planifStartCorr(true);return;}
    if(!mod){e.preventDefault();e.stopPropagation();}
    return;
  }
  if(!planifLocked||inText)return;
  e.preventDefault();e.stopPropagation();
  planifToast('🔒 Clavier bloqué : touche le cadenas en bas à gauche pour le réactiver');
},true);
/* ───── zone de réponse tapée ───── */
var PLANIF_PAD_SIZES=[22,32,45],planifTypeOn=false,planifPadSize=1,planifSide='q';
function planifTA(){return document.getElementById('planif-ta');}
function planifTypeBuild(){
  var p=document.createElement('div');p.id='planif-pad';
  p.innerHTML='<div class="bar"><span class="hint" id="pp-hint"></span><span class="sp"></span>'+
    '<button id="pp-size" title="Changer la taille">↕ Taille</button>'+
    '<button id="pp-close" title="Fermer (reste fermée pour les cartes suivantes)">✕</button></div>'+
    '<div id="planif-ta" contenteditable="true" spellcheck="false" data-ph="Tape ta réponse ici…"></div>';
  document.body.appendChild(p);
  var ta=planifTA();
  ta.addEventListener('paste',function(e){e.preventDefault();
    var t=(e.clipboardData||window.clipboardData).getData('text/plain');if(planifCorr)planifCorrColor();
    document.execCommand('insertText',false,t);});
  ta.addEventListener('mousedown',function(){if(planifTypeOn&&planifSide==='a'&&!planifCorr)planifStartCorr(false);});
  planifApplyBox();
  document.getElementById('pp-close').onclick=function(e){e.preventDefault();pycmd('planif:type:off');};
  document.getElementById('pp-size').onclick=function(e){e.preventDefault();
    planifPadSize=(planifPadSize+1)%PLANIF_PAD_SIZES.length;pycmd('planif:padsize:'+planifPadSize);planifPadApplySize();};
  planifHint();
}
function planifPadApplySize(){document.documentElement.style.setProperty('--planif-pad-h',PLANIF_PAD_SIZES[planifPadSize]+'vh');}
var planifCorr=false,planifBox=null;
function planifCorrSwatch(){var c=(planifBox&&planifBox.corr)||{value:'#e03131'};return '<i class="sw" style="background:'+c.value+'"></i>';}
function planifHint(){
  var h=document.getElementById('pp-hint');if(!h)return;
  if(planifSide==='a'&&planifCorr){h.className='hint';h.innerHTML='✍️ Correction'+planifCorrSwatch()+'en cours : <b>Échap</b> ou <b>⌘ + Entrée</b> pour terminer';}
  else if(planifSide==='a'){h.className='hint ans';h.innerHTML='Note : <b>1</b> À revoir <b>2</b> Difficile <b>3</b> Correct <b>4</b> Facile · <b>Tab</b> ou clic pour corriger'+planifCorrSwatch();}
  else{h.className='hint';h.innerHTML='<b>⌘ + Entrée</b> pour retourner la carte · <b>⌘ + Z</b> annule ta note précédente';}
}
function planifFocusEnd(t){t.focus();var r=document.createRange();r.selectNodeContents(t);r.collapse(false);
  var s=window.getSelection();s.removeAllRanges();s.addRange(r);}
function planifTypeFocus(){var t=planifTA();if(t&&planifTypeOn&&planifSide==='q'){planifFocusEnd(t);}}
function planifApplyBox(){
  var t=planifTA(),b=planifBox;if(!t||!b)return;
  var m={'--pp-bg':b.bg,'--pp-ink':b.ink,'--pp-border':b.border,'--pp-lines':b.lines,'--pp-pl':b.pl,
         '--pp-shadow':b.shadow,'--pp-font':b.font,'--pp-corr':b.corr.value};
  for(var k in m)t.style.setProperty(k,m[k]);
  t.classList.toggle('lv2',b.lv>=2);t.classList.toggle('lv3',b.lv>=3);
  planifHint();
}
function planifCorrColor(){
  var c=(planifBox&&planifBox.corr)||{kind:'color',value:'#e03131'};
  try{document.execCommand('styleWithCSS',false,true);
    if(c.kind==='highlight'){document.execCommand('hiliteColor',false,c.value);document.execCommand('foreColor',false,c.ink);}
    else document.execCommand('foreColor',false,c.value);}catch(e){}
}
function planifStartCorr(toEnd){
  var t=planifTA();if(!t)return;
  planifCorr=true;t.contentEditable='true';t.classList.add('corr-mode');
  if(toEnd)planifFocusEnd(t);else t.focus();
  planifHint();
}
function planifEndCorr(){
  planifCorr=false;var t=planifTA();
  if(t){t.contentEditable='false';t.classList.remove('corr-mode');t.blur();}
  planifHint();
}
function planifType(on,size,box){
  planifTypeOn=!!on;if(box){planifBox=box;planifApplyBox();}if(size!=null)planifPadSize=Math.max(0,Math.min(PLANIF_PAD_SIZES.length-1,size));
  var b=planifToolBtn('planif-typebtn');b.className=on?'on':'';
  b.textContent=on?'⌨️ Réponse ✓':'⌨️ Réponse';
  b.title=on?'Fermer la zone de réponse':'Ouvrir une zone pour taper ta réponse';
  b.onclick=function(e){e.preventDefault();pycmd('planif:type:'+(planifTypeOn?'off':'on'));};
  if(on){if(!document.getElementById('planif-pad'))planifTypeBuild();document.body.classList.add('planif-pad-on');planifPadApplySize();}
  else{document.body.classList.remove('planif-pad-on');planifCorr=false;var t=planifTA();if(t)t.blur();}
  var lb=document.getElementById('planif-lock');if(lb)lb.style.display=on?'none':'';
}
function planifTypeQuestion(){
  planifSide='q';planifCorr=false;var t=planifTA();
  if(t){t.innerHTML='';t.contentEditable='true';t.classList.remove('corr-mode');
    if(t.classList.contains('lv3')){t.classList.remove('flashy');void t.offsetWidth;t.classList.add('flashy');}}
  planifHint();setTimeout(planifTypeFocus,40);
}
function planifTypeAnswer(){
  planifSide='a';var t=planifTA();
  planifCorr=false;
  if(t){t.contentEditable='false';t.classList.remove('corr-mode');t.blur();}
  planifHint();
}
function planifLevelUp(L){
  var old=document.getElementById('planif-lvl');if(old)old.remove();
  var esc=function(x){var e=document.createElement('span');e.textContent=x==null?'':String(x);return e.innerHTML;};
  var o=document.createElement('div');o.id='planif-lvl';o.className=L.evolved?'evo':'simple';
  var who=L.name?esc(L.name)+' : ':'';
  o.innerHTML='<div class="flash"></div><div class="stage"><div class="rays"></div><div class="glow"></div>'+
    '<div class="m old">'+L.from+'</div><div class="m new">'+L.to+'</div></div>'+
    '<div class="txt t1">'+(L.evolved?'Évolution !':'Niveau supérieur !')+'</div>'+
    '<div class="txt t2">Niveau '+L.level+'</div>'+
    '<div class="txt t3">'+(L.evolved?who+esc(L.from_name)+' → '+esc(L.stage):'Tu es maintenant '+esc(L.title))+'</div>'+
    '<div class="txt t4">Clique pour continuer</div>';
  document.body.appendChild(o);
  if(L.evolved){sfx('shake');setTimeout(function(){sfx('boom');sfx('level');},1550);}else sfx('level');
  var sparkAt=L.evolved?1600:150;
  setTimeout(function(){
    var st=o.querySelector('.stage');if(!st)return;
    for(var i=0;i<14;i++){(function(i){
      var s=document.createElement('div');s.textContent=i%3?'✨':'⭐';
      s.style.cssText='position:absolute;left:50%;top:50%;font-size:'+(18+Math.random()*16)+'px;pointer-events:none';
      st.appendChild(s);var a=i/14*Math.PI*2,r=140+Math.random()*80;
      s.animate([{transform:'translate(-50%,-50%) scale(.3)',opacity:1},
        {transform:'translate(calc(-50% + '+Math.cos(a)*r+'px),calc(-50% + '+Math.sin(a)*r+'px)) scale(1)',opacity:0}],
        {duration:1100+Math.random()*400,easing:'cubic-bezier(.15,.8,.3,1)',fill:'forwards'});})(i);}
  },sparkAt);
  var close=function(){if(!o.parentNode)return;o.classList.add('out');setTimeout(function(){o.remove();},600);};
  o.onclick=close;setTimeout(close,L.evolved?7000:4800);
}
/* ───── barre d'infos (niveau, XP restante, prochaine récompense, pièces) ───── */
var planifFlying=0,planifLatest=null,planifCoinsShown=null,planifSayT=null,planifTypeT=null;
function planifPadOffset(){var p=document.getElementById('planif-pad');return (document.body.classList.contains('planif-pad-on')&&p)?p.offsetHeight:0;}
function planifHUDBuild(){
  var h=planifEl('planif-hud');
  if(!h.dataset.built){h.dataset.built='1';
    h.innerHTML='<span class="wxb" id="ph-wx"><span class="wxfx" id="ph-wxfx"></span><span class="m" id="planif-mascot"></span>'+
      '<span class="wxacc" id="ph-wxacc"></span><span class="wxt" id="ph-wxt"></span></span>'+
      '<div class="lv"><div class="tp"><b id="ph-lv"></b><span id="ph-need"></span></div><div class="xb"><div id="ph-xp"></div></div></div>'+
      '<span class="nx" id="ph-next"></span><span class="co" id="ph-coins"></span><span class="gl" id="ph-goal"></span>';}
  return h;
}
function planifHUDValues(d,anim){
  var xp=document.getElementById('ph-xp');if(!xp)return;
  xp.style.width=Math.round(Math.max(0,Math.min(1,d.xp_cur/d.xp_need))*100)+'%';
  document.getElementById('ph-need').textContent='encore '+Math.max(0,d.xp_need-d.xp_cur)+' XP';
  var co=document.getElementById('ph-coins');
  if(anim&&planifCoinsShown!=null&&planifCoinsShown!==d.coins){
    var from=planifCoinsShown,to=d.coins,t0=performance.now();
    (function f(t){var k=Math.min(1,(t-t0)/450);co.innerHTML=PLANIF_COIN+' '+Math.round(from+(to-from)*k);if(k<1)requestAnimationFrame(f);})(t0);
    co.classList.remove('bump');void co.offsetWidth;co.classList.add('bump');
    xp.parentNode.classList.remove('bump');void xp.offsetWidth;xp.parentNode.classList.add('bump');
  } else co.innerHTML=PLANIF_COIN+' '+d.coins;
  planifCoinsShown=d.coins;
}
function planifBoss(b){
  var el=planifEl('planif-boss');
  if(!el.dataset.built){el.dataset.built='1';
    el.innerHTML='<span class="bh" id="pb-hero"></span><span class="bi" id="pb-art"></span><div class="bt"><div class="bn" id="pb-name"></div>'+
      '<div class="hb"><div class="hf" id="pb-hp"></div><div class="hs" id="pb-sh"></div></div><div class="hv" id="pb-val"></div><div class="hx" id="pb-fx"></div></div>';}
  var art=document.getElementById('pb-art'),hero=document.getElementById('pb-hero');
  if(b.hero&&hero.dataset.k!==b.hero){hero.innerHTML=b.hero;hero.dataset.k=b.hero;}
  if(art.dataset.lvl!==String(b.level)){art.innerHTML=b.art;art.dataset.lvl=String(b.level);}
  var nm=document.getElementById('pb-name');nm.textContent='⚔️ '+b.name+' ';
  var sm=document.createElement('small');sm.textContent='niv. '+b.level;nm.appendChild(sm);
  document.getElementById('pb-hp').style.width=Math.max(0,Math.min(100,100*b.hp/b.max))+'%';
  document.getElementById('pb-val').textContent=b.hp+' / '+b.max+' PV'+(b.rage?' · 😡 ENRAGÉ':'');
  el.classList.toggle('rage',!!b.rage);
  document.getElementById('pb-sh').style.width=Math.max(0,Math.min(100,100*(b.shield||0)/b.max))+'%';
  var fxe=document.getElementById('pb-fx');fxe.innerHTML='';
  (b.fx||[]).forEach(function(f){var s=document.createElement('span');s.className=f.bad?'bad':'good';s.textContent=f.icon+' '+f.label;fxe.appendChild(s);});
  fxe.innerHTML=fxe.innerHTML.split('🪙').join(PLANIF_COIN);
  if(b.dmg>0){
    sfx(b.crit?'crit':'hit');
    hero.classList.remove('atk');void hero.offsetWidth;hero.classList.add('atk');
    art.classList.remove('hit');void art.offsetWidth;art.classList.add('hit');
    var r=art.getBoundingClientRect(),t=document.createElement('div');
    t.className='planif-dmg'+(b.crit?' crit':'');t.textContent=(b.crit?'CRITIQUE ! ':'')+'−'+b.dmg;
    t.style.left=(r.left+6)+'px';t.style.top=(r.top-30)+'px';
    document.body.appendChild(t);setTimeout(function(){t.remove();},1150);
  }
  if(b.down)planifBossDown(b.down);
}
function planifBossAttack(a){
  var esc=function(x){var e=document.createElement('span');e.textContent=x==null?'':String(x);return e.innerHTML;};
  var coin=function(h){return h.split('🪙').join(PLANIF_COIN);};
  var old=document.getElementById('planif-atk');if(old)old.remove();
  var box=document.getElementById('planif-boss');if(box){box.classList.remove('atk');void box.offsetWidth;box.classList.add('atk');}
  sfx('shake');setTimeout(function(){sfx('hit');},300);
  var o=document.createElement('div');o.id='planif-atk';
  if(a.type==='quiz'){
    o.className='quiz';
    o.innerHTML='<div class="qcard"><div class="qtop"><span class="qart">'+a.art+'</span><div><div class="qt">'+esc(a.icon+' '+a.title+' !')+'</div>'+
      '<div class="qb">'+esc(a.boss)+' te pose une question sur tes cartes</div></div></div>'+
      '<div class="qq">'+esc(a.q)+'</div><div class="qc">'+a.choices.map(function(c,i){return '<button data-i="'+i+'"><b>'+(i+1)+'</b> '+esc(c)+'</button>';}).join('')+'</div>'+
      '<div class="qn">'+esc(a.text)+'</div></div>';
    document.body.appendChild(o);
    var done=false,pick=function(i){if(done)return;done=true;o.querySelectorAll('.qc button').forEach(function(b){b.disabled=true;});
      o.querySelector('.qc button[data-i="'+i+'"]').classList.add('picked');pycmd('planif:quiz:'+i);};
    o.querySelectorAll('.qc button').forEach(function(b){b.onclick=function(){pick(+b.dataset.i);};});
    var kh=function(e){if(!document.getElementById('planif-atk')){window.removeEventListener('keydown',kh,true);return;}
      e.stopImmediatePropagation();e.preventDefault();var n=parseInt(e.key,10);if(n>=1&&n<=4)pick(n-1);};
    window.addEventListener('keydown',kh,true);o._kh=kh;
    return;
  }
  planifBossTab(a.icon,a.title+' !',coin(esc(a.text)),'t-'+a.type,6500);
}
var planifBtkT=null;
function planifBossTab(icon,title,html,cls,ms){
  var t=planifEl('planif-btk');t.className='planif-tab '+(cls||'');
  var e=document.createElement('span');e.textContent=title;
  t.innerHTML='<span class="ba">'+icon+'</span><span><b>'+e.innerHTML+'</b><small>'+html+'</small></span>';
  var tm=document.getElementById('planif-btm');if(tm&&tm.classList.contains('on'))tm.style.visibility='hidden';
  planifTabPlace(t,document.getElementById('planif-boss'),'left');
  if(t.classList.contains('free')){t.style.left='12px';t.style.right='auto';t.style.bottom=(planifPadOffset()+140)+'px';}
  planifTabShow(t);clearTimeout(planifBtkT);
  planifBtkT=setTimeout(function(){planifTabHide(t);if(tm)tm.style.visibility='';},ms||5000);
}
function planifBossResult(r){
  var esc=function(x){var e=document.createElement('span');e.textContent=x==null?'':String(x);return e.innerHTML;};
  sfx(r.ok?'crit':'lose');
  if(window.planifTimerStop)planifTimerStop();
  var o=document.getElementById('planif-atk');
  if(o&&o.classList.contains('quiz')){
    o.querySelectorAll('.qc button').forEach(function(b){if(+b.dataset.i===r.good)b.classList.add('good');else if(b.classList.contains('picked'))b.classList.add('bad');});
    var n=o.querySelector('.qn');n.className='qn '+(r.ok?'ok':'ko');n.textContent=r.text;
    var close=function(){if(o._kh)window.removeEventListener('keydown',o._kh,true);if(o.parentNode){o.classList.add('out');setTimeout(function(){o.remove();},400);}};
    setTimeout(function(){o.onclick=close;},400);setTimeout(close,r.ok?2600:4200);
    if(r.ok)planifConfetti(1);
    return;
  }
  if(o)o.remove();
  planifBossTab(r.ok?'✅':'⚠️',r.ok?'Réussi !':'Raté…',esc(r.text),r.ok?'res-ok':'res-ko',4200);
}
function planifBossTimer(secs){
  var old=document.getElementById('planif-timer');if(old)old.remove();
  var bt=document.getElementById('planif-btk');if(bt){clearTimeout(planifBtkT);planifTabHide(bt);}
  var t=planifEl('planif-btm');t.className='planif-tab';t.style.visibility='';
  t.innerHTML='⏱️ <b>'+secs+'</b><small>s</small><i class="tb"><i></i></i>';
  planifTabPlace(t,document.getElementById('planif-boss'),'right');
  if(t.classList.contains('free')){t.style.right='auto';t.style.left='12px';t.style.bottom=(planifPadOffset()+140)+'px';}
  planifTabShow(t);
  var bar=t.querySelector('.tb i'),b=t.querySelector('b'),end=Date.now()+secs*1000;
  bar.style.transition='none';bar.style.width='100%';void bar.offsetWidth;
  bar.style.transition='width '+secs+'s linear';bar.style.width='0%';
  var iv=setInterval(function(){var left=Math.ceil((end-Date.now())/1000);
    if(left<=0){clearInterval(iv);t.classList.remove('hurry');t.classList.add('over');b.textContent='0';setTimeout(function(){planifTabHide(t);},900);return;}
    if(left<=3){if(!t.classList.contains('hurry'))t.classList.add('hurry');sfx('tick',2200);}
    if(b.textContent!==String(left))b.textContent=left;},250);
  window.planifTimerStop=function(){clearInterval(iv);planifTabHide(t);};
}
function planifBossDown(L){
  var old=document.getElementById('planif-lvl');if(old)old.remove();
  var esc=function(x){var e=document.createElement('span');e.textContent=x==null?'':String(x);return e.innerHTML;};
  var o=document.createElement('div');o.id='planif-lvl';o.className='evo';
  o.innerHTML='<div class="flash"></div><div class="stage"><div class="rays"></div><div class="glow"></div>'+
    '<div class="m old">'+L.art+'</div><div class="m new" style="font-size:130px">🏆</div></div>'+
    '<div class="txt t1">Boss vaincu !</div><div class="txt t2" style="font-size:30px">'+esc(L.name)+'</div>'+
    '<div class="txt t3">Butin : '+L.items.map(esc).join(' · ').split('🪙').join(PLANIF_COIN)+'</div>'+
    '<div class="txt t4">Prochain adversaire : '+esc(L.next)+' (niv. '+L.next_level+') · clique pour continuer</div>';
  document.body.appendChild(o);sfx('shake');
  setTimeout(function(){sfx('boom');},1500);setTimeout(function(){sfx('big');planifConfetti();},1650);
  var close=function(){if(!o.parentNode)return;o.classList.add('out');setTimeout(function(){o.remove();},600);};
  o.onclick=close;setTimeout(close,8000);
}
var PLANIF_WX_KEY='';
function planifWxBubble(w){
  var box=document.getElementById('ph-wx');if(!box)return;
  w=w||{};var key=[w.kind,w.phase,w.temp].join('|');if(key===PLANIF_WX_KEY)return;PLANIF_WX_KEY=key;
  box.className='wxb k-'+(w.kind||'none')+' p-'+(w.phase||'day');
  var fx='',acc='',t=w.temp;
  if(w.kind==='rain'||w.kind==='storm'){fx='<i class="d"></i><i class="d"></i><i class="d"></i><i class="d"></i>';acc='<span class="umb">☂️</span>';
    if(w.kind==='storm')fx+='<i class="bolt">⚡</i>';}
  else if(w.kind==='snow'){fx='<i class="f">❄</i><i class="f">❄</i><i class="f">❄</i>';acc='<span class="scarf">🧣</span>';}
  else if(w.kind==='fog'){fx='<i class="fog"></i>';}
  else if(w.kind==='clouds'){fx='<i class="cl">☁️</i>';}
  if((w.kind==='clear'||w.kind==='clouds')&&w.phase==='night'){fx+='<i class="moon">🌙</i><i class="st"></i><i class="st"></i>';acc+='<span class="zz">z</span>';}
  else if(w.kind==='clear'&&w.phase==='day'){fx+='<i class="sun">☀️</i>';if(t!=null&&t>=24)acc+='<span class="shades">🕶️</span>';}
  if(t!=null&&t<=2&&w.kind!=='snow')acc+='<span class="scarf">🧣</span>';
  document.getElementById('ph-wxfx').innerHTML=fx;
  document.getElementById('ph-wxacc').innerHTML=acc;
  document.getElementById('ph-wxt').textContent=t!=null?Math.round(t)+'°':'';
}
function planifHUD(d){
  if(!d||(d.effects||[]).indexOf('gains')<0){var o=document.getElementById('planif-hud');if(o)o.remove();planifLatest=d;return;}
  planifLatest=d;planifHUDBuild();
  var mEl=document.getElementById('planif-mascot');
  if(mEl.dataset.k!==d.mascot){mEl.innerHTML=d.mascot;mEl.dataset.k=d.mascot;}
  planifWxBubble(d.wx);
  document.getElementById('ph-lv').textContent='Niv. '+d.level;
  var n=d.next||{};
  document.getElementById('ph-next').innerHTML=n.evo?'→ <span class="big">'+n.evo+'</span> niv. '+n.level:'→ niv. '+n.level+' <b>+'+n.coins+' '+PLANIF_COIN+'</b>';
  document.getElementById('ph-goal').textContent='🎯 '+Math.round((d.pct||0)*100)+' %';
  if(planifFlying>0)return;
  planifHUDValues(d,false);
}
function planifFly(x0,y0,target,html,cls,delay,done){
  planifFlying++;
  var f=document.createElement('div');f.className='planif-fly '+cls;f.innerHTML=html;
  f.style.left=x0+'px';f.style.top=y0+'px';document.body.appendChild(f);
  var r=target.getBoundingClientRect(),dx=r.left+r.width/2-x0,dy=r.top+r.height/2-y0;
  var mx=dx*.3+(Math.random()-.5)*90,my=-70-Math.random()*50;
  var a=f.animate([
    {transform:'translate(-50%,-50%) scale(.3)',opacity:0},
    {transform:'translate(-50%,-50%) scale(1.15)',opacity:1,offset:.18},
    {transform:'translate(-50%,-50%) scale(1)',opacity:1,offset:.38},
    {transform:'translate(calc(-50% + '+mx+'px),calc(-50% + '+my+'px)) scale(.9)',opacity:1,offset:.62},
    {transform:'translate(calc(-50% + '+dx+'px),calc(-50% + '+dy+'px)) scale(.35)',opacity:.9}],
    {duration:1500,delay:delay||0,easing:'cubic-bezier(.45,0,.55,1)',fill:'forwards'});
  a.onfinish=function(){f.remove();planifFlying=Math.max(0,planifFlying-1);if(done)done();
    target.classList.remove('bump');void target.offsetWidth;target.classList.add('bump');
    if(planifFlying===0&&planifLatest)planifHUDValues(planifLatest,true);};
}
function planifToast(html){
  var t=planifEl('planif-toast');t.innerHTML=html;t.classList.add('on');
  clearTimeout(planifToastT);planifToastT=setTimeout(function(){t.classList.remove('on');},3800);
}
/* ───── la mascotte parle ───── */
function planifSay(d,txt){
  var b=planifEl('planif-buddy');
  b.innerHTML='<span class="bm">'+d.mascot+'</span><div class="bb"><span class="nm"></span><span class="tx"></span></div>';
  b.querySelector('.nm').textContent=d.mname||'';
  var tx=b.querySelector('.tx'),i=0,plain=txt;
  clearInterval(planifTypeT);clearTimeout(planifSayT);
  requestAnimationFrame(function(){b.classList.add('on');});
  planifTypeT=setInterval(function(){i+=2;tx.textContent=plain.slice(0,i);if(i>=plain.length){clearInterval(planifTypeT);
    tx.innerHTML=tx.innerHTML.split('🪙').join(PLANIF_COIN);}},22);
  planifSayT=setTimeout(function(){b.classList.remove('on');},2600+plain.length*30);
}
function planifSparks(big,lv){
  lv=lv||1;
  var cols=['#ffd43b','#ff922b','#51cf66','#4dabf7','#ff6b9d','#b197fc'],off=planifPadOffset();
  var x=innerWidth/2,y=innerHeight-215-off,n=(big?30:22)+(lv-1)*16;
  if(lv>=2){var r2=document.createElement('div');r2.className='planif-ring rainbow';r2.style.left=x+'px';r2.style.top=y+'px';document.body.appendChild(r2);
    r2.animate([{transform:'translate(-50%,-50%) scale(.1)',opacity:1},{transform:'translate(-50%,-50%) scale(1.5)',opacity:0}],
      {duration:900,easing:'cubic-bezier(.2,.8,.3,1)'}).onfinish=function(){r2.remove();};}
  if(lv>=3){var fl=document.createElement('div');fl.className='planif-glow';document.body.appendChild(fl);
    fl.animate([{opacity:.55},{opacity:0}],{duration:600}).onfinish=function(){fl.remove();};
    for(var q=0;q<5;q++){(function(q){var s=document.createElement('div');s.className='planif-shoot';s.textContent='✦';
      s.style.left=x+'px';s.style.top=y+'px';document.body.appendChild(s);var a=-Math.PI*(.15+q*.175),dist=innerWidth*.45;
      s.animate([{transform:'translate(-50%,-50%) scale(.6)',opacity:1},{transform:'translate(calc(-50% + '+Math.cos(a)*dist+'px),calc(-50% + '+Math.sin(a)*dist+'px)) scale(1.3)',opacity:0}],
        {duration:1100,delay:q*60,easing:'cubic-bezier(.2,.7,.3,1)'}).onfinish=function(){s.remove();};})(q);}}
  var ring=document.createElement('div');ring.className='planif-ring';ring.style.left=x+'px';ring.style.top=y+'px';
  document.body.appendChild(ring);ring.animate([{transform:'translate(-50%,-50%) scale(.2)',opacity:.9},
    {transform:'translate(-50%,-50%) scale(1)',opacity:0}],{duration:700,easing:'cubic-bezier(.2,.8,.3,1)'}).onfinish=function(){ring.remove();};
  for(var i=0;i<n;i++){(function(i){
    var s=document.createElement('div'),star=i%3===0;
    s.className=star?'planif-spark star':'planif-spark';
    if(star)s.textContent=i%2?'✨':'⭐';else{var sz=7+Math.random()*9;s.style.width=s.style.height=sz+'px';
      s.style.background=cols[i%cols.length];s.style.boxShadow='0 0 10px '+cols[i%cols.length];}
    s.style.left=x+'px';s.style.top=y+'px';document.body.appendChild(s);
    var a=Math.random()*Math.PI*2,v=130+Math.random()*(big?260:190),g=60+Math.random()*80;
    s.animate([{transform:'translate(-50%,-50%) scale(1.2)',opacity:1},
      {transform:'translate(calc(-50% + '+Math.cos(a)*v*.7+'px),calc(-50% + '+Math.sin(a)*v*.7+'px)) scale(1)',opacity:1,offset:.55},
      {transform:'translate(calc(-50% + '+Math.cos(a)*v+'px),calc(-50% + '+(Math.sin(a)*v+g)+'px)) scale(.3)',opacity:0}],
      {duration:900+Math.random()*500,easing:'cubic-bezier(.15,.75,.35,1)'}).onfinish=function(){s.remove();};})(i);}
}
/* ───── gains : un petit ticket qui sort de derrière la barre d'XP, puis s'y glisse ───── */
var planifTk={x:0,c:0,T:null};
function planifRoll(el,a,b){var t0=performance.now();
  (function f(t){var k=Math.min(1,(t-t0)/480);el.textContent='+'+Math.round(a+(b-a)*(1-Math.pow(1-k,3)));if(k<1)requestAnimationFrame(f);})(t0);}
function planifTicket(d,lv){
  var hud=document.getElementById('planif-hud');if(!hud)return;
  var tk=planifEl('planif-tk');tk.classList.add('planif-tab');
  if(!tk.dataset.built){tk.dataset.built='1';
    tk.innerHTML='<span class="x"><b id="ptk-x">+0</b> XP</span><span class="bo" id="ptk-bo">×2</span><i class="sep"></i>'+
      '<span class="c">'+PLANIF_COIN+'<b id="ptk-c">+0</b></span><i class="sh"></i>';}
  planifTabPlace(tk,hud,'right');
  var fresh=!tk.classList.contains('on'),fx=planifTk.x,fc=planifTk.c;
  if(fresh){fx=fc=0;planifTk.x=planifTk.c=0;}
  planifTk.x+=d.xp||0;planifTk.c+=d.gain_coins||0;
  tk.querySelector('.x').style.display=planifTk.x>0?'':'none';
  tk.querySelector('.c').style.display=planifTk.c>0?'':'none';
  tk.querySelector('.sep').style.display=planifTk.x>0&&planifTk.c>0?'':'none';
  document.getElementById('ptk-bo').style.display=d.boost?'':'none';
  tk.classList.toggle('miss',d.ease===1);tk.classList.toggle('lv2',lv>=2);tk.classList.toggle('lv3',lv>=3);
  planifRoll(document.getElementById('ptk-x'),fx,planifTk.x);planifRoll(document.getElementById('ptk-c'),fc,planifTk.c);
  planifTabShow(tk);
  clearTimeout(planifTk.T);
  planifTk.T=setTimeout(function(){
    planifTabHide(tk);planifFlying=0;
    setTimeout(function(){
      if(planifLatest)planifHUDValues(planifLatest,true);
      var xb=document.getElementById('ph-xp');if(xb){xb=xb.parentNode;xb.classList.remove('sweep');void xb.offsetWidth;xb.classList.add('sweep');}
      if(lv>=3){var hc=document.getElementById('ph-coins');if(hc){hc.classList.remove('sparkle');void hc.offsetWidth;hc.classList.add('sparkle');}}
    },230);
  },1500);
}
function planifGain(d){
  var fx=d.effects||[];planifCount++;var LV=d.fxlv||{};
  var hudOn=fx.indexOf('gains')>=0,gains=hudOn&&(d.xp>0||d.gain_coins>0);
  if(gains){if(planifCoinsShown==null)planifCoinsShown=d.coins-d.gain_coins;planifFlying=1;}
  planifHUD(d);
  if(gains){
    planifTicket(d,LV.gains||1);
    if(d.ease>=3)setTimeout(function(){sfx('coin');},380);else if(d.ease===2)sfx('soft');else sfx('miss');
    var m=document.getElementById('planif-mascot');
    if(m){m.classList.remove('planif-bounce');void m.offsetWidth;m.classList.add('planif-bounce');}
  }
  if(fx.indexOf('etincelles')>=0 && d.ease>=3){planifSparks(d.ease===4,LV.etincelles);sfx('sparkle');}
  if(fx.indexOf('combo')>=0){
    planifCombo = d.ease>1 ? planifCombo+1 : 0;
    var c=planifEl('planif-combo');c.classList.add('planif-tab');
    if(planifCombo>=3){c.innerHTML='<span>🔥 Combo ×'+planifCombo+'</span>';
      planifTabPlace(c,document.getElementById('planif-hud'),'left');
      if(!document.getElementById('planif-hud')){c.style.left='16px';c.style.bottom=(planifPadOffset()+122)+'px';}
      planifTabShow(c);
      if((LV.combo||1)>=2){c.style.color=planifCombo<10?'#e8590c':planifCombo<25?'#d6336c':planifCombo<50?'#9c36b5':'#1c7ed6';}
      if((LV.combo||1)>=3&&planifCombo%10===0){var bb=document.createElement('div');bb.className='planif-combo-big';
        bb.textContent='COMBO ×'+planifCombo+' !';document.body.appendChild(bb);sfx('big');
        setTimeout(function(){bb.remove();},1600);}}
    else{planifTabHide(c);c.style.color='';}
  }
  if(d.talk){planifSay(d,d.talk);setTimeout(function(){sfx('pop');},150);}
  if(d.celebrate && fx.indexOf('confettis')>=0) planifConfetti(LV.confettis||1);
}
"""


# Barre du bas des révisions : transmet ⌘+Entrée, 1-4 et la frappe vers la zone de réponse
BOTTOMBAR_JS = r"""
document.addEventListener('keydown',function(e){
  var mod=e.metaKey||e.ctrlKey;
  if(mod&&e.key==='Enter'){pycmd('planif:key:reveal');return;}
  if(mod&&!e.shiftKey&&(e.key==='z'||e.key==='Z')){pycmd('planif:key:undo');return;}
  if(/^[1-4]$/.test(e.key)&&!mod&&!e.altKey){pycmd('planif:key:'+e.key);return;}
  if(!mod&&e.key.length===1){pycmd('planif:key:focus');}
},true);
"""


# ───────────────────────────────────────────── vitrine de badges (écran d'accueil)
DISPLAYS = {
    "bois": {"name": "Étagère en bois", "price": 0,
             "desc": "Tes badges posés sur de belles planches."},
    "liege": {"name": "Tableau de liège", "price": 600,
              "desc": "Tes badges épinglés comme des macarons."},
    "jean": {"name": "Veste en jean", "price": 1000,
             "desc": "Des écussons brodés cousus sur du denim."},
    "vitrine": {"name": "Vitrine en verre", "price": 1400,
                "desc": "Étagères de verre éclairées, badges lumineux."},
    "dore": {"name": "Salle des trophées dorée", "price": 2400,
             "desc": "Médailles à rubans, cadre or et velours bordeaux."},
}
WALL_COLORS = ["#e03131", "#f08c00", "#2f9e44", "#1971c2", "#9c36b5", "#e64980", "#0ca678", "#f59f00"]

WALL_CSS = r"""
.pw{border-radius:16px;padding:12px 12px 10px;font-family:system-ui,-apple-system,sans-serif;text-align:center;box-sizing:border-box}
.pw .hd{font-weight:700;font-size:14px;margin-bottom:8px;display:flex;justify-content:space-between;align-items:center;gap:6px}
.pw .hd span{font-size:12px;opacity:.75}
.pw .row{display:grid;grid-template-columns:repeat(4,1fr);gap:4px;align-items:end;padding:4px 2px 0}
.pw .b{position:relative;height:44px;display:flex;align-items:flex-end;justify-content:center}
.pw .b .e{font-size:28px;line-height:1;transition:transform .2s;display:inline-flex;align-items:center;justify-content:center}
.pw .b i{font-style:normal}
.pw .b:hover .e{transform:scale(1.22) translateY(-3px)}
.pw .b.lock i{filter:grayscale(1) brightness(0);opacity:.2}
.pw .b.new::after{content:'✨';position:absolute;top:-4px;right:2px;font-size:12px;animation:pwTw 1.4s ease-in-out infinite}
@keyframes pwTw{50%{opacity:.2;transform:scale(.7)}}
.pw .ft{font-size:11.5px;margin-top:8px;opacity:.75;cursor:pointer;text-decoration:underline}
/* bois */
.pw-bois{background:linear-gradient(180deg,#f6ecdc,#eadbc2);color:#5a3a1c;border:1px solid #d9c3a0}
.pw-bois .plank{height:10px;margin:0 -4px 8px;border-radius:3px;background:linear-gradient(180deg,#b98352,#8a5a2b);box-shadow:0 5px 6px -2px rgba(70,40,10,.45)}
.pw-bois .b .e{filter:drop-shadow(0 3px 2px rgba(60,30,0,.35))}
.nightMode .pw-bois,.night-mode .pw-bois,body.night_mode .pw-bois{background:linear-gradient(180deg,#3b2b1d,#2b1f15);color:#f1dcc0;border-color:#5a4028}
.nightMode .pw-bois .plank,.night-mode .pw-bois .plank{background:linear-gradient(180deg,#8a5a2b,#5e3b1a)}
.nightMode .pw-bois .b.lock i,.night-mode .pw-bois .b.lock i{filter:grayscale(1) brightness(2.2);opacity:.12}
/* liège */
.pw-liege{background-color:#c89f6d;background-image:radial-gradient(rgba(90,55,20,.35) 1px,transparent 1.5px),radial-gradient(rgba(255,240,210,.25) 1px,transparent 1.5px);
  background-size:7px 7px,11px 11px;border:8px solid #7a5230;color:#3d2410}
.pw-liege .hd{background:#fffbe8;padding:4px 8px;border-radius:3px;transform:rotate(-1.5deg);box-shadow:0 2px 4px rgba(0,0,0,.25)}
.pw-liege .plank{display:none}
.pw-liege .row{gap:4px;padding:7px 0}
.pw-liege{padding:10px 6px 8px}
.pw-liege .b{height:auto}
.pw-liege .b .e{width:36px;height:36px;border-radius:50%;background:#fff;border:3px solid var(--c);font-size:18px;transform:rotate(var(--r));box-shadow:0 3px 5px rgba(0,0,0,.3)}
.pw-liege .b:hover .e{transform:rotate(0) scale(1.15)}
.pw-liege .b::before{content:'';position:absolute;top:-3px;left:50%;width:9px;height:9px;margin-left:-4px;border-radius:50%;background:radial-gradient(circle at 35% 35%,#ff8a8a,#b3121a);z-index:2;box-shadow:0 1px 2px rgba(0,0,0,.4)}
.pw-liege .b.lock .e{background:rgba(255,248,230,.35);border:2px dashed rgba(90,55,20,.5);box-shadow:none}
.pw-liege .b.lock::before{display:none}
/* jean */
.pw-jean{background-color:#3d5f93;background-image:repeating-linear-gradient(45deg,rgba(255,255,255,.06) 0 2px,transparent 2px 5px),repeating-linear-gradient(-45deg,rgba(0,0,0,.09) 0 2px,transparent 2px 5px);
  color:#fdf3dd;outline:2px dashed #e8c27a;outline-offset:-7px}
.pw-jean .hd{font-family:'Marker Felt','Segoe Print',cursive;letter-spacing:.5px}
.pw-jean .plank{display:none}
.pw-jean .row{gap:8px;padding:7px 2px}
.pw-jean .b{height:auto}
.pw-jean .b .e{width:42px;height:42px;border-radius:50%;font-size:21px;background:var(--c);box-shadow:0 0 0 3px var(--c),0 4px 7px rgba(0,0,0,.4);outline:2px dashed rgba(255,255,255,.75);outline-offset:-5px;transform:rotate(var(--r))}
.pw-jean .b:hover .e{transform:rotate(0) scale(1.15)}
.pw-jean .b.lock .e{background:rgba(255,255,255,.07);box-shadow:none;outline-color:rgba(255,255,255,.28)}
/* vitrine */
.pw-vitrine{background:radial-gradient(ellipse at 50% -10%,rgba(160,210,255,.38),transparent 60%),linear-gradient(180deg,#1c2536,#111726);color:#dfe9ff;border:2px solid #5a6b8c}
.pw-vitrine .plank{height:6px;margin:0 -4px 10px;background:linear-gradient(180deg,rgba(255,255,255,.6),rgba(255,255,255,.12));border-radius:2px;box-shadow:0 6px 14px rgba(120,180,255,.22)}
.pw-vitrine .b .e{filter:drop-shadow(0 0 8px rgba(140,200,255,.8))}
.pw-vitrine .b.lock i{filter:grayscale(1) brightness(2);opacity:.1}
/* doré */
.pw-dore{background:radial-gradient(ellipse at 50% 0%,rgba(255,215,120,.25),transparent 55%),linear-gradient(180deg,#4a1322,#2a0913);color:#ffe7a8;border:5px double #d4a017}
.pw-dore .hd{font-family:Georgia,serif;letter-spacing:1px}
.pw-dore .plank{height:5px;margin:2px -4px 10px;background:linear-gradient(90deg,#8a6508,#ffd86b,#8a6508);border-radius:3px}
.pw-dore .b{height:auto;padding-top:12px}
.pw-dore .b .e{width:38px;height:38px;border-radius:50%;font-size:19px;background:radial-gradient(circle at 35% 30%,#fff4c2,#e3b12a 55%,#9c7412);box-shadow:0 3px 6px rgba(0,0,0,.45),inset 0 0 0 2px rgba(255,255,255,.35)}
.pw-dore .b::before{content:'';position:absolute;top:0;left:50%;width:16px;height:16px;margin-left:-8px;background:linear-gradient(90deg,#c0392b 0 33%,#fff 33% 66%,#2f5fd0 66%);clip-path:polygon(0 0,100% 0,100% 100%,50% 70%,0 100%)}
.pw-dore .b.lock .e{background:rgba(255,255,255,.07);box-shadow:inset 0 0 0 2px rgba(255,215,120,.25)}
.pw-dore .b.lock::before{opacity:.2}
/* niveaux de la vitrine */
.pw.lv2,.pw.lv3{box-shadow:0 14px 40px rgba(0,0,0,.22),0 0 0 3px rgba(255,214,90,.35)!important}
.pw.lv2 .b:not(.lock) .e,.pw.lv3 .b:not(.lock) .e{filter:drop-shadow(0 0 7px rgba(255,214,90,.75))}
.pw.lv3{outline:3px solid #e0a100;outline-offset:3px}
.pw.lv3 .hd{text-shadow:0 0 10px rgba(255,214,90,.6)}
.pw.lv3 .b:not(.lock)::before{content:'';position:absolute;inset:-2px;border-radius:12px;pointer-events:none;z-index:3;
  background:linear-gradient(115deg,transparent 42%,rgba(255,255,255,.75) 50%,transparent 58%);background-size:260% 100%;animation:pwShine 5s linear infinite}
.pw.lv3 .b:nth-child(2)::before{animation-delay:-1.2s}.pw.lv3 .b:nth-child(3)::before{animation-delay:-2.4s}.pw.lv3 .b:nth-child(4)::before{animation-delay:-3.6s}
@keyframes pwShine{from{background-position:130% 0}to{background-position:-130% 0}}
/* aperçu dans la boutique */
.pw-mini{padding:8px 8px 2px;border-radius:12px}
.pw-mini .row{padding-top:2px}
"""

WALL_PAGE_CSS = r"""
#planif-side{position:fixed;top:50%;transform:translateY(-50%);width:300px;max-height:calc(100vh - 20px);overflow:auto;
  z-index:50;display:flex;flex-direction:column;gap:12px;scrollbar-width:none;padding:18px;box-sizing:border-box}
#planif-side::-webkit-scrollbar{display:none}
#planif-side.side-right,#planif-wall-mini.side-right{right:24px}
#planif-side.side-left,#planif-wall-mini.side-left{left:24px}
#planif-wall{box-shadow:0 14px 40px rgba(0,0,0,.22);padding:16px 16px 12px}
.pexw{border-radius:16px;padding:12px 14px;background:var(--planif-surface,rgba(255,255,255,.85));border:1px solid var(--planif-line,rgba(128,128,128,.25));
  box-shadow:0 10px 30px rgba(0,0,0,.12);font:13px/1.35 system-ui,-apple-system,sans-serif;text-align:left;cursor:pointer}
.pexw h4{margin:0 0 8px;font-size:15px}
.pex{padding:7px 0;border-top:1px solid var(--planif-line,rgba(128,128,128,.2))}
.pex:first-of-type{border-top:none;padding-top:0}
.pex .r{display:flex;justify-content:space-between;align-items:center;gap:8px}
.pex .n{font-weight:700;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.pex .j{font-weight:800;font-size:15px;color:var(--planif-accent,#4f63d8);white-space:nowrap}
.pex .b{height:6px;border-radius:6px;background:rgba(128,128,128,.22);overflow:hidden;margin:5px 0 4px}
.pex .b div{height:100%;border-radius:6px;background:var(--planif-accent,#4f63d8)}
.pex .st{display:inline-block;font-size:11px;font-weight:700;border-radius:999px;padding:1px 8px}
.pex .st.ahead,.pex .st.done{color:#1f9e6e;background:rgba(31,158,110,.14)}
.pex .st.ontime{color:#1c7ed6;background:rgba(28,126,214,.14)}
.pex .st.late{color:#e03131;background:rgba(224,49,49,.14)}
.pex .st.unknown,.pex .st.none{color:#868e96;background:rgba(134,142,150,.15)}
.pex small{opacity:.7}
#planif-wall .hd{font-size:17px;margin-bottom:10px}
#planif-wall .hd span{font-size:13px}
#planif-wall .row{gap:8px}
#planif-wall .b{height:58px}
#planif-wall .b .e{font-size:38px}
#planif-wall.pw-liege .b .e{width:50px;height:50px;font-size:25px}
#planif-wall.pw-jean .b .e{width:52px;height:52px;font-size:26px}
#planif-wall.pw-dore .b .e{width:50px;height:50px;font-size:25px}
#planif-wall.pw-liege .b,#planif-wall.pw-jean .b,#planif-wall.pw-dore .b{height:auto}
#planif-wall .ft{font-size:12.5px}
#planif-wall-mini{display:none;position:fixed;top:14px;z-index:50;padding:6px 12px;border-radius:999px;
  background:rgba(128,128,128,.2);font:700 14px system-ui,sans-serif;cursor:pointer}
#planif-wtip{position:fixed;z-index:60;width:230px;padding:10px 12px;border-radius:12px;background:rgba(22,24,32,.95);color:#fff;
  font:13px/1.4 system-ui,sans-serif;box-shadow:0 8px 24px rgba(0,0,0,.3);pointer-events:none;opacity:0;transform:translateX(6px);
  transition:opacity .15s,transform .15s;text-align:left}
#planif-wtip.on{opacity:1;transform:none}
#planif-wtip b{display:block;font-size:14px;margin-bottom:2px}
#planif-wtip small{display:block;margin-top:5px;color:#ffd65a}
#planif-wtip.lock small{color:#9aa3b5}
"""

WALL_PLACE_JS = r"""
(function(){
  function zone(){
    var W=innerWidth,left=W,right=0,found=false;
    ['#decktree','table','#planif-summary'].forEach(function(sel){
      var e=document.querySelector(sel);if(!e)return;var r=e.getBoundingClientRect();if(!r.width)return;
      found=true;left=Math.min(left,r.left);right=Math.max(right,r.right);});
    if(!found){left=W/2-260;right=W/2+260;}
    return {W:W,left:left,right:right};
  }
  function put(col,mini,sd,maxw,minw){
    if(!col)return;var z=zone(),free=sd==='left'?z.left:z.W-z.right;
    if(free<minw){col.style.display='none';if(mini){mini.style.display='block';mini.style[sd]='14px';}return;}
    if(mini)mini.style.display='none';col.style.display='';
    var ww=Math.min(maxw,free-12);col.style.width=ww+'px';
    var cx=sd==='left'?z.left/2:z.right+free/2;
    col.style.left=Math.round(cx-ww/2)+'px';col.style.right='auto';
  }
  function place(){
    var side=document.getElementById('planif-side'),w=document.getElementById('planif-wall');
    if(side&&w)put(side,document.getElementById('planif-wall-mini'),w.dataset.side,376,290);
    var ex=document.getElementById('planif-exams');
    if(ex)put(ex,document.getElementById('planif-exams-mini'),ex.dataset.side,340,270);
  }
  place();addEventListener('resize',place);setTimeout(place,250);setTimeout(place,1000);
  var w=document.getElementById('planif-wall');if(!w)return;
  var tip=document.createElement('div');tip.id='planif-wtip';document.body.appendChild(tip);
  w.querySelectorAll('.b').forEach(function(b){
    b.addEventListener('mouseenter',function(){
      tip.innerHTML='';var n=document.createElement('b'),d=document.createElement('div'),s=document.createElement('small');
      n.textContent=b.dataset.n;d.textContent=b.dataset.d;s.textContent=b.dataset.w;tip.appendChild(n);tip.appendChild(d);tip.appendChild(s);
      tip.className=b.classList.contains('lock')?'on lock':'on';
      var r=b.getBoundingClientRect(),wr=w.getBoundingClientRect(),tw=230;
      var left=w.dataset.side==='left'?wr.right+12:wr.left-tw-12;
      tip.style.left=Math.max(8,left)+'px';tip.style.top=Math.max(8,Math.min(innerHeight-110,r.top+r.height/2-40))+'px';
    });
    b.addEventListener('mouseleave',function(){tip.className='';});
  });
})();
"""


def exams_widget(exams, side):
    """Calendrier des examens, dans sa propre colonne (à l'opposé de la vitrine)."""
    import html as _h
    if not exams:
        return ""
    months = ["janv.", "févr.", "mars", "avr.", "mai", "juin", "juil.", "août", "sept.", "oct.", "nov.", "déc."]
    rows = []
    for e in exams:
        pl = e.get("plan") or {"state": "todo", "label": ""}
        dd = e["date"]
        when = f"{int(dd[8:10])} {months[int(dd[5:7]) - 1]}"
        pct_today = 100 if not e["target"] else min(100, round(100 * e["intro_today"] / e["target"]))
        fix = (f'<button class="pxfix" onclick="event.stopPropagation();pycmd(\'planif:fix:{e["id"]}\');return false;">Corriger</button>'
               if pl.get("fixable") else "")
        rows.append(
            f'<div class="pxe st-{pl["state"]}">'
            f'<div class="pxring" style="--p:{e["seen_pct"]}"><span><b>J-{e["days_to_exam"]}</b></span></div>'
            f'<div class="pxb"><div class="pxn">{_h.escape(e["name"])}</div>'
            f'<div class="pxd">{when} · {e["seen_pct"]} % du paquet vu</div>'
            f'<div class="pxt"><div style="width:{pct_today}%"></div></div>'
            f'<div class="pxs"><span>{_h.escape(pl["label"])}</span>{fix}</div>'
            f'<div class="pxd">{e["intro_today"]}/{e["target"]} nouvelles · {e["due"]} révisions dues</div></div></div>')
    return (f'<div id="planif-exams" data-side="{side}" onclick="pycmd(\'planif:open:planning\');return false;">'
            f'<div class="pxh"><span class="pxi">📅</span><div><b>Mes examens</b><small>{len(exams)} à venir</small></div></div>'
            + "".join(rows) + '<div class="pxf">Voir le planning →</div></div>'
            f'<div id="planif-exams-mini" data-side="{side}" onclick="pycmd(\'planif:open:planning\');return false;">📅 {len(exams)}</div>')


EXAMS_CSS = r"""
#planif-exams{position:fixed;top:50%;transform:translateY(-50%);width:320px;max-height:calc(100vh - 28px);overflow:auto;z-index:50;
  border-radius:22px;padding:0 0 10px;background:var(--planif-surface,rgba(255,255,255,.9));border:1px solid var(--planif-line,rgba(128,128,128,.25));
  box-shadow:0 18px 44px rgba(0,0,0,.18);font:13px/1.35 system-ui,-apple-system,sans-serif;text-align:left;cursor:pointer;scrollbar-width:none}
#planif-exams::-webkit-scrollbar{display:none}
.nightMode #planif-exams,.night-mode #planif-exams{background:rgba(40,42,52,.92)}
#planif-exams .pxh{display:flex;align-items:center;gap:12px;padding:14px 16px;border-radius:22px 22px 0 0;margin-bottom:6px;
  background:linear-gradient(135deg,var(--planif-accent,#4f63d8),var(--planif-accent2,#7a5cff));color:#fff}
#planif-exams .pxi{font-size:26px;line-height:1;background:rgba(255,255,255,.2);border-radius:12px;padding:6px}
#planif-exams .pxh b{display:block;font-size:16px}
#planif-exams .pxh small{opacity:.85}
.pxe{display:flex;gap:12px;align-items:flex-start;padding:10px 14px;margin:0 6px;border-radius:14px;--c:#4f63d8;transition:background .15s}
.pxe:hover{background:rgba(128,128,128,.1)}
.pxe.st-done,.pxe.st-finished{--c:#1f9e6e} .pxe.st-notset{--c:#e03131} .pxe.st-late{--c:#e8590c}
.nightMode .pxe,.night-mode .pxe{--c:#8193ff} .nightMode .pxe.st-done,.night-mode .pxe.st-done,.nightMode .pxe.st-finished,.night-mode .pxe.st-finished{--c:#4cd69c}
.nightMode .pxe.st-notset,.night-mode .pxe.st-notset{--c:#ff6b6b} .nightMode .pxe.st-late,.night-mode .pxe.st-late{--c:#ff9a5c}
.pxring{flex:none;width:58px;height:58px;border-radius:50%;display:flex;align-items:center;justify-content:center;
  background:conic-gradient(var(--c) calc(var(--p)*1%),rgba(128,128,128,.22) 0)}
.pxring span{width:46px;height:46px;border-radius:50%;display:flex;align-items:center;justify-content:center;
  background:var(--canvas,#fff)}
.nightMode .pxring span,.night-mode .pxring span{background:#2c2c34}
.pxring b{font-size:13.5px;color:var(--c);letter-spacing:-.3px}
.pxb{flex:1;min-width:0}
.pxn{font-weight:750;font-size:14.5px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.pxd{font-size:11.5px;opacity:.65}
.pxt{height:6px;border-radius:6px;background:rgba(128,128,128,.22);overflow:hidden;margin:6px 0 5px}
.pxt div{height:100%;border-radius:6px;background:var(--c)}
.pxs{display:flex;align-items:center;justify-content:space-between;gap:6px;font-weight:700;font-size:12px;color:var(--c);margin-bottom:2px}
.pxfix{border:none!important;background:var(--c)!important;color:#fff!important;border-radius:999px!important;padding:3px 11px!important;
  font:700 11.5px system-ui!important;cursor:pointer;box-shadow:none!important}
#planif-exams .pxf{text-align:center;font-size:12px;opacity:.6;margin-top:6px}
#planif-exams-mini{display:none;position:fixed;top:14px;z-index:50;padding:6px 12px;border-radius:999px;
  background:rgba(128,128,128,.2);font:700 14px system-ui,sans-serif;cursor:pointer}
"""


def wall_html(badges, key, side, today_iso, exams=None, lv=1):
    """badges : liste de dicts {icon, name, desc, date}. La vitrine et le calendrier sont de part et d'autre."""
    import html as _h
    key = key if key in DISPLAYS else "bois"
    ex_side = "right" if side == "left" else "left"
    if side == "off":
        return (f'<style>{EXAMS_CSS}</style>' + exams_widget(exams, "left") + f'<script>{WALL_PLACE_JS}</script>')
    side = "left" if side == "left" else "right"
    got = sum(1 for b in badges if b.get("date"))
    rows = []
    for r0 in range(0, len(badges), 4):
        cells = []
        for i, b in enumerate(badges[r0:r0 + 4]):
            n = r0 + i
            cls = "b" + ("" if b.get("date") else " lock") + (" new" if b.get("date") == today_iso else "")
            when = (f"Obtenu le {b['date'][8:10]}/{b['date'][5:7]}" if b.get("date") else "À débloquer")
            cells.append(f'<div class="{cls}" data-n="{_h.escape(b["name"])}" data-d="{_h.escape(b["desc"])}" '
                         f'data-w="{when}" style="--r:{(n * 37) % 15 - 7}deg;'
                         f'--c:{WALL_COLORS[n % len(WALL_COLORS)]}"><span class="e"><i>{b["icon"]}</i></span></div>')
        rows.append('<div class="row">' + "".join(cells) + '</div><div class="plank"></div>')
    return (f'<style>{WALL_CSS}{WALL_PAGE_CSS}{EXAMS_CSS}</style>' + exams_widget(exams, ex_side) +
            f'<div id="planif-side" class="side-{side}">'
            f'<div id="planif-wall" class="pw pw-{key} lv{lv}" data-side="{side}"><div class="hd">🏆 Mes trophées <span>{got}/{len(badges)}</span></div>'
            + "".join(rows) +
            '<div class="ft" onclick="pycmd(\'planif:open:badges\');return false;">Voir le détail</div></div></div>'
            f'<div id="planif-wall-mini" class="side-{side}" title="Mes trophées" '
            f'onclick="pycmd(\'planif:open:badges\');return false;">🏆 {got}</div>'
            f'<script>{WALL_PLACE_JS}</script>')


# ───────────────────────────────────────────── université (tycoon)
# (clé, nom, coût de base, pièces/heure par niveau, niveau requis, description)
UNIV = [
    ("biblio", "Bibliothèque", 300, 20, 1, "Le cœur du campus : tes premiers revenus."),
    ("hall", "Grand Hall", 800, 0, 2, "Agrandit la caisse (+1 000 par niveau) et booste toute la production (+5 % par niveau)."),
    ("cafe", "Cafétéria", 500, 30, 2, "Les étudiants ont besoin de café pour réviser."),
    ("amphi", "Amphithéâtre", 900, 50, 3, "Des cours magistraux qui rapportent gros."),
    ("residence", "Résidence étudiante", 1400, 70, 4, "Plus d'étudiants logés, plus de revenus."),
    ("labo", "Laboratoire", 2200, 110, 5, "Des contrats de recherche très rentables."),
    ("serre", "Serre botanique", 3200, 160, 7, "Des plantes rares qui attirent les visiteurs."),
    ("observatoire", "Observatoire", 5000, 240, 9, "Le fleuron du campus : prestige et revenus."),
]
UNIV_MAX = 5
UNIV_MIN_PER_CARD = 2      # minutes d'énergie gagnées par carte révisée
UNIV_ENERGY_CAP = 720      # 12 h d'énergie maximum en réserve

# ───────────────────────────────────────────── collection de spécimens
RARITIES = [("commune", 60, 20, "#868e96"), ("rare", 28, 60, "#1c7ed6"),
            ("epique", 10, 200, "#9c36b5"), ("legendaire", 2, 800, "#f08c00")]
RARITY_LABEL = {"commune": "Commune", "rare": "Rare", "epique": "Épique", "legendaire": "Légendaire"}
SPECIMENS = [
    ("amanite", "🍄", "Amanite tue-mouches", "commune"), ("bacterie", "🦠", "Bacille", "commune"),
    ("fougere", "🌿", "Fougère aigle", "commune"), ("escargot", "🐌", "Escargot de Bourgogne", "commune"),
    ("fourmi", "🐜", "Fourmi rousse", "commune"), ("mousse", "🌱", "Mousse des bois", "commune"),
    ("ver", "🪱", "Ver de terre", "commune"), ("coccinelle", "🐞", "Coccinelle à 7 points", "commune"),
    ("morpho", "🦋", "Morpho bleu", "rare"), ("rainette", "🐸", "Rainette verte", "rare"),
    ("herisson", "🦔", "Hérisson d'Europe", "rare"), ("orchidee", "🌺", "Orchidée sauvage", "rare"),
    ("pieuvre", "🐙", "Pieuvre commune", "rare"), ("lezard", "🦎", "Lézard vert", "rare"),
    ("requin", "🦈", "Requin-baleine", "epique"), ("grandduc", "🦉", "Grand-duc d'Europe", "epique"),
    ("baleine", "🐋", "Baleine bleue", "epique"), ("adn", "🧬", "Double hélice d'ADN", "epique"),
    ("paon", "🦚", "Paon bleu", "epique"), ("corail", "🪸", "Corail des récifs", "epique"),
    ("diplodocus", "🦕", "Diplodocus", "legendaire"), ("trex", "🦖", "Tyrannosaure", "legendaire"),
    ("dodo", "🦤", "Dodo", "legendaire"), ("mammouth", "🦣", "Mammouth laineux", "legendaire"),
]


# ───────────────────────────────────────────── forge du héros
# (emplacement, nom, icône, stat, valeurs par palier 0..6, description)
GEAR = [
    ("arme", "Arme", "⚔️", "Dégâts", [0, 1, 2, 3, 4, 6, 8], "+{v} dégâts par bonne réponse"),
    ("casque", "Casque", "🪖", "Critique", [0, 3, 6, 9, 12, 16, 20], "+{v} % de chance de critique"),
    ("bouclier", "Bouclier", "🛡️", "Puissance", [0, .2, .4, .6, .8, 1.0, 1.5], "critiques ×{c}"),
    ("armure", "Armure", "🦺", "Butin", [0, 10, 20, 30, 40, 50, 70], "+{v} % de butin sur les boss"),
    ("amulette", "Amulette", "📿", "Fortune", [0, 2, 4, 6, 8, 10, 14], "+{v} % de pièces en révisant"),
]
TIERS = [None, ("Bois", 1, 300), ("Fer", 3, 700), ("Acier", 5, 1500), ("Or", 8, 3000),
         ("Cristal", 11, 6000), ("Légendaire", 15, 12000)]     # (matériau, niveau requis, prix)
TIER_COLORS = [None, "#a0703f", "#8d99a6", "#5a7bb0", "#e0a100", "#27b3d1", "#9c36b5"]


def gear_desc(slot, tier):
    g = next(x for x in GEAR if x[0] == slot)
    v = g[4][tier]
    return g[5].format(v=v, c=f"{2 + v:g}".replace(".", ","))


# ───────────────────────────────────────────── niveaux des cosmétiques
UPG_CATS = ("theme", "wallpaper", "effect", "display", "box_theme")
UPG_MAX = 3
LV_DESC = {
    "theme": ["Les couleurs du thème", "+ boutons et paquet sélectionné en dégradé lumineux",
              "+ reflet animé sur les grands boutons et halo sur ton paquet"],
    "wallpaper": ["Le fond d'écran", "+ vignette douce qui donne de la profondeur", "+ poussière d'étoiles scintillante"],
    "display": ["La vitrine", "+ éclairage et badges lumineux", "+ cadre doré et reflets qui passent sur tes badges"],
    "box_theme": ["Le style de la case", "+ halo coloré quand tu écris", "+ bordure arc-en-ciel et éclat à chaque nouvelle carte"],
    "effect": {
        "gains": ["Pièces qui s'envolent", "+ plus de pièces et gain qui brille", "+ pluie de pièces et compteur étincelant"],
        "etincelles": ["Gerbe d'étincelles", "+ double anneau arc-en-ciel et plus d'étincelles", "+ étoiles filantes et éclat lumineux"],
        "combo": ["Compteur de combo", "+ flammes qui changent de couleur en montant", "+ explosion géante tous les 10 combos"],
        "confettis": ["Pluie de confettis", "+ deux fois plus de confettis, avec des étoiles", "+ feux d'artifice"],
    },
}


def lv_desc(cat, key):
    d = LV_DESC.get(cat)
    if isinstance(d, dict):
        return d.get(key, ["", "", ""])
    return d or ["", "", ""]


def upgrade_cost(price, to_level):
    base = price if price > 0 else 300
    if to_level == 2:
        return max(250, int(round(base * .8 / 10.0)) * 10)
    return max(600, int(round(base * 1.6 / 10.0)) * 10)


# ───────────────────────────────────────────── boutique en « lignes d'évolution »
# Un seul objet par catégorie : on l'améliore niveau par niveau et il traverse les styles
# dans l'ordre (comme la forge du héros). Avec « polish », chaque style a 3 crans (★ → ★★★).
# (catégorie, titre, icône, styles dans l'ordre, polish, style « éteint » possible)
TRACKS = [
    ("theme", "Thème de couleurs", "🎨", ["moderne", "menthe", "lavande", "ocean", "sakura", "or", "neon"], True, "classique"),
    ("wallpaper", "Fond d'écran des révisions", "🖼️", ["bonbon", "cahier", "ocean", "foret", "coucher", "aurore", "etoiles"], True, "aucun"),
    ("effect", "Effets pendant les révisions", "✨", ["gains", "etincelles", "combo", "confettis"], True, None),
    ("mascot", "Mascotte", "🦉", ["hibou", "plante", "chat", "dragon", "chouette"], False, None),
    ("box_theme", "Case de réponse", "📝", ["classique", "cahier", "postit", "tableau", "terminal", "parchemin", "nuit", "neon"], True, None),
    ("box_font", "Police de la case", "🔤", ["systeme", "georgia", "machine", "code", "manuscrite", "craie", "marqueur", "calligraphie"], False, None),
    ("corr", "Couleur des corrections", "🖍️", ["rouge", "vert", "bleu", "orange", "violet", "rose", "or", "surligneur"], False, None),
    ("display", "Vitrine de badges", "🏆", ["bois", "liege", "jean", "vitrine", "dore"], True, None),
]
TRACK = {t[0]: t for t in TRACKS}
CUMULATIVE = {"effect"}   # chaque niveau ajoute un effet de plus (ils restent tous actifs)
STYLE_LEVEL_STEP = 2      # un nouveau style tous les 2 niveaux de joueur
TRACK_GROWTH = 1.15       # chaque cran coûte 15 % de plus que le précédent


def _cat_items(cat):
    return {"theme": THEMES, "wallpaper": WALLPAPERS, "effect": EFFECTS, "mascot": MASCOTS, "box_theme": BOX_THEMES,
            "box_font": BOX_FONTS, "corr": CORR_STYLES, "display": DISPLAYS}[cat]


def track_polish(cat):
    return UPG_MAX if TRACK[cat][4] else 1


def track_max(cat):
    return len(TRACK[cat][3]) * track_polish(cat)


def track_start(cat):
    first = TRACK[cat][3][0]
    return 1 if _cat_items(cat)[first]["price"] == 0 else 0


def track_step(cat, lv):
    """Ce que débloque le niveau lv : (index du style, cran de polish 1..3)."""
    n, P = len(TRACK[cat][3]), track_polish(cat)
    if cat in CUMULATIVE:
        return (lv - 1) % n, (lv - 1) // n + 1
    return (lv - 1) // P, (lv - 1) % P + 1


def track_unlocked(cat, lv):
    """[(clé du style, cran)] pour tout ce qui est débloqué au niveau lv."""
    styles = TRACK[cat][3]
    n, P = len(styles), track_polish(cat)
    if lv <= 0:
        return []
    if cat in CUMULATIVE:
        return [(styles[i], (lv - i + n - 1) // n) for i in range(n) if lv > i]
    idx, pol = track_step(cat, lv)
    return [(styles[i], P) for i in range(idx)] + [(styles[idx], pol)]


def track_current(cat, lv):
    u = track_unlocked(cat, lv)
    if not u:
        return None, 0
    if cat in CUMULATIVE:
        idx, _p = track_step(cat, lv)
        return u[idx]
    return u[-1]


def track_cost(cat, lv):
    """Prix pour passer au niveau lv."""
    if not TRACK[cat][4]:  # un style par niveau : son prix d'origine
        idx, _p = track_step(cat, lv)
        return max(300, _cat_items(cat)[TRACK[cat][3][idx]]["price"])
    return int(round(250 * TRACK_GROWTH ** (lv - 1) / 10.0)) * 10


def track_need(cat, lv):
    """Niveau de joueur requis pour passer au niveau lv (seulement pour un nouveau style)."""
    idx, pol = track_step(cat, lv)
    return 1 + STYLE_LEVEL_STEP * idx if pol == 1 else 1


def track_label(cat, lv):
    idx, pol = track_step(cat, lv)
    key = TRACK[cat][3][idx]
    name = _cat_items(cat)[key]["name"]
    if pol == 1:
        return key, f"Nouveau style : {name}", _cat_items(cat)[key].get("desc", "")
    d = lv_desc(cat, key)
    return key, f"{name} {'★' * pol}", (d[pol - 1] if pol - 1 < len(d) else "")


def track_from_owned(cat, owned, cos_lv):
    """Niveau de départ calculé à partir de ce que tu possédais dans l'ancienne boutique."""
    styles = TRACK[cat][3]
    n, P = len(styles), track_polish(cat)
    best = track_start(cat)
    for i, k in enumerate(styles):
        if k not in owned:
            continue
        c = max(1, min(P, int(cos_lv.get(f"{cat}:{k}", 1)))) if P > 1 else 1
        best = max(best, (c - 1) * n + i + 1 if cat in CUMULATIVE else i * P + c)
    return min(best, track_max(cat))


SKIN_L2 = r"""
tr.deck.current td{background:linear-gradient(90deg,var(--planif-soft),transparent 85%)!important}
#study,button#study,#ansbut,button#ansbut{background:linear-gradient(120deg,var(--planif-accent),var(--planif-accent2),var(--planif-accent))!important;
  background-size:220% 100%!important;box-shadow:0 8px 22px var(--planif-soft),0 0 0 3px var(--planif-soft)!important}
.new-count,.learn-count,.review-count{box-shadow:inset 0 0 0 1px currentColor}
.zero-count{box-shadow:none}
button:hover{box-shadow:0 0 0 3px var(--planif-soft)!important}
.hitem:hover{box-shadow:0 0 14px var(--planif-soft)}
"""
SKIN_L3 = r"""
#study:hover,#ansbut:hover{animation:pfSheen 1.6s linear infinite}
@keyframes pfSheen{to{background-position:220% 0}}
tr.deck.current td:first-child{box-shadow:inset 4px 0 0 var(--planif-accent),-10px 0 22px -8px var(--planif-accent)!important}
a.deck:hover{text-shadow:0 0 14px var(--planif-accent)}
tr.deck.current a.deck{text-shadow:0 0 12px var(--planif-soft)}
"""
DUST_SVG = ('<svg xmlns="http://www.w3.org/2000/svg" width="300" height="300">'
            + "".join(f'<circle cx="{(i * 97) % 300}" cy="{(i * 61) % 300}" r="{.6 + (i % 3) * .45}" fill="#fff" opacity="{.25 + (i % 4) * .15}"/>'
                      for i in range(38)) + '</svg>')
