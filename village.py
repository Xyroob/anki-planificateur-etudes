# -*- coding: utf-8 -*-
"""Le village universitaire : chaque bâtiment change d'allure à chaque niveau,
et le campus entier (chemins, arbres, fontaine, étudiants…) grandit avec lui."""

# Repère local d'un bâtiment : 200 de large, sol à y = 200, centre en x = 100.

MATS = [None,
        {"name": "Cabane en bois", "wall": "#D6A774", "dark": "#8C5A3C", "roof": "#9C6B3F", "tex": "pvPlank"},
        {"name": "Maison en crépi", "wall": "#F3E6CF", "dark": "#A47148", "roof": None, "tex": None},
        {"name": "Bâtisse en brique", "wall": "#D9805F", "dark": "#7E3426", "roof": None, "tex": "pvBrick"},
        {"name": "Édifice en pierre", "wall": "#E6E2D8", "dark": "#6F7882", "roof": None, "tex": "pvStone"},
        {"name": "Palais de marbre", "wall": "#FCFAF4", "dark": "#B8860B", "roof": None, "tex": "pvMarble"}]
GOLD = "#E8B10C"

DEFS = ('<defs>'
        '<pattern id="pvPlank" width="12" height="7" patternUnits="userSpaceOnUse">'
        '<path d="M0 6.5H12M8 0V6.5" stroke="#9C6B3F" stroke-width="1" opacity=".55"/></pattern>'
        '<pattern id="pvBrick" width="14" height="8" patternUnits="userSpaceOnUse">'
        '<path d="M0 7.5H14M0 3.5H14M4 0V3.5M11 3.5V7.5" stroke="#A9533E" stroke-width="1" opacity=".6"/></pattern>'
        '<pattern id="pvStone" width="22" height="12" patternUnits="userSpaceOnUse">'
        '<path d="M0 11.5H22M0 5.5H22M8 0V5.5M17 5.5V11.5" stroke="#B9B2A3" stroke-width="1" opacity=".75"/></pattern>'
        '<pattern id="pvMarble" width="40" height="30" patternUnits="userSpaceOnUse">'
        '<path d="M2 4q10 6 16 2t20 8M0 20q8-4 14 2t18 4" stroke="#E3DAC6" stroke-width="1" fill="none"/></pattern>'
        '<radialGradient id="pvGlow"><stop offset="0" stop-color="#FFE27A" stop-opacity=".9"/>'
        '<stop offset="1" stop-color="#FFE27A" stop-opacity="0"/></radialGradient>'
        '</defs>')


def _f(v):
    return f"{v:.1f}".rstrip("0").rstrip(".")


# ─────────────────────────────────────────────────────── petites briques de dessin

def _wall(x, y, w, h, lv, fill=None):
    m = MATS[lv]
    s = (f'<rect x="{_f(x)}" y="{_f(y)}" width="{_f(w)}" height="{_f(h)}" fill="{fill or m["wall"]}" '
         f'stroke="{m["dark"]}" stroke-width="2"/>')
    if m["tex"]:
        s += f'<rect x="{_f(x + 1)}" y="{_f(y + 1)}" width="{_f(w - 2)}" height="{_f(h - 2)}" fill="url(#{m["tex"]})"/>'
    if lv == 5:  # corniche dorée
        s += f'<rect x="{_f(x - 2)}" y="{_f(y - 3)}" width="{_f(w + 4)}" height="4" fill="{GOLD}"/>'
    return s


def _win(x, y, w, h, lv):
    m = MATS[lv]
    if lv >= 4:  # fenêtres en arc
        r = w / 2
        d = f"M{_f(x)} {_f(y + h)}V{_f(y + r)}a{_f(r)} {_f(r)} 0 0 1 {_f(w)} 0V{_f(y + h)}Z"
        return (f'<path class="win" d="{d}" fill="#BFE3FF" stroke="{m["dark"]}" stroke-width="1.6"/>'
                f'<path d="M{_f(x + r)} {_f(y)}V{_f(y + h)}M{_f(x)} {_f(y + h * .6)}H{_f(x + w)}" stroke="{m["dark"]}" stroke-width="1"/>')
    s = (f'<rect class="win" x="{_f(x)}" y="{_f(y)}" width="{_f(w)}" height="{_f(h)}" rx="1" fill="#BFE3FF" '
         f'stroke="{m["dark"]}" stroke-width="1.6"/>'
         f'<path d="M{_f(x + w / 2)} {_f(y)}V{_f(y + h)}M{_f(x)} {_f(y + h / 2)}H{_f(x + w)}" stroke="{m["dark"]}" stroke-width="1"/>')
    if lv == 1:  # volets
        s += (f'<rect x="{_f(x - 4)}" y="{_f(y)}" width="4" height="{_f(h)}" fill="#7A9A4A"/>'
              f'<rect x="{_f(x + w)}" y="{_f(y)}" width="4" height="{_f(h)}" fill="#7A9A4A"/>')
    return s


def _windows(x, y, w, rows, cols, lv, ww=10, wh=12, gap_y=20):
    out = ""
    step = w / cols
    for r in range(rows):
        for c in range(cols):
            out += _win(x + step * c + (step - ww) / 2, y + r * gap_y, ww, wh, lv)
    return out


def _door(cx, base, w, h, lv):
    m = MATS[lv]
    r = w / 2
    s = (f'<path d="M{_f(cx - r)} {_f(base)}V{_f(base - h + r)}a{_f(r)} {_f(r)} 0 0 1 {_f(w)} 0V{_f(base)}Z" '
         f'fill="#7A4A2A" stroke="{GOLD if lv == 5 else m["dark"]}" stroke-width="{2.4 if lv == 5 else 1.6}"/>'
         f'<circle cx="{_f(cx + r * .45)}" cy="{_f(base - h * .45)}" r="1.3" fill="{GOLD}"/>')
    return s


def _gable(x1, x2, y, peak, color, lv):
    m = MATS[lv]
    cx = (x1 + x2) / 2
    s = (f'<path d="M{_f(x1 - 6)} {_f(y)}L{_f(cx)} {_f(y - peak)}L{_f(x2 + 6)} {_f(y)}Z" fill="{color}" '
         f'stroke="{GOLD if lv == 5 else m["dark"]}" stroke-width="2" stroke-linejoin="round"/>')
    if lv >= 3:  # tuiles
        for i in range(1, 4):
            k = i / 4.0
            s += (f'<path d="M{_f(x1 - 6 + (cx - x1 + 6) * k)} {_f(y - peak * k)}H{_f(x2 + 6 - (x2 + 6 - cx) * k)}" '
                  f'stroke="#000" stroke-opacity=".15" stroke-width="1.2"/>')
    return s


def _flat_roof(x, y, w, color, lv):
    m = MATS[lv]
    return (f'<rect x="{_f(x - 4)}" y="{_f(y - 7)}" width="{_f(w + 8)}" height="8" rx="2" fill="{color}" '
            f'stroke="{GOLD if lv == 5 else m["dark"]}" stroke-width="1.6"/>')


def _flag(x, y, color="#E03131", h=26):
    return (f'<path d="M{_f(x)} {_f(y)}V{_f(y - h)}" stroke="#555" stroke-width="1.8"/>'
            f'<path class="pv-flag" d="M{_f(x)} {_f(y - h)}h16l-4 5 4 5H{_f(x)}z" fill="{color}"/>')


def _column(x, y, h, lv):
    c = "#FFFFFF" if lv >= 4 else "#F6EFE2"
    cap = GOLD if lv == 5 else MATS[lv]["dark"]
    return (f'<rect x="{_f(x)}" y="{_f(y)}" width="7" height="{_f(h)}" fill="{c}" stroke="#CFC6B3" stroke-width="1"/>'
            f'<rect x="{_f(x - 2)}" y="{_f(y - 3)}" width="11" height="4" fill="{cap}"/>'
            f'<rect x="{_f(x - 2)}" y="{_f(y + h - 1)}" width="11" height="4" fill="{cap}"/>')


def _steps(cx, w, lv):
    c = "#D9D3C7" if lv < 5 else "#F1ECE0"
    return (f'<rect x="{_f(cx - w / 2 - 8)}" y="196" width="{_f(w + 16)}" height="4" fill="{c}" stroke="#B8B0A0" stroke-width=".8"/>'
            f'<rect x="{_f(cx - w / 2 - 4)}" y="192" width="{_f(w + 8)}" height="4" fill="{c}" stroke="#B8B0A0" stroke-width=".8"/>')


def _bush(x, y=200, s=1.0, c="#4CAF50"):
    return (f'<g transform="translate({_f(x)} {_f(y)}) scale({_f(s)})">'
            f'<circle cx="-6" cy="-6" r="7" fill="{c}"/><circle cx="5" cy="-7" r="8" fill="{c}"/>'
            f'<circle cx="0" cy="-12" r="7" fill="#66BB6A"/></g>')


def _lamp(x, y=200):
    return (f'<path d="M{_f(x)} {_f(y)}V{_f(y - 30)}" stroke="#3A3A4A" stroke-width="2.2"/>'
            f'<circle class="lamp" cx="{_f(x)}" cy="{_f(y - 33)}" r="4.2" fill="#FFF3BF" stroke="#3A3A4A" stroke-width="1.4"/>')


def _sparkles(pts):
    out = ""
    for i, (x, y, r) in enumerate(pts):
        out += (f'<path class="pv-spark" style="animation-delay:{i * .5:.1f}s" '
                f'd="M{_f(x)} {_f(y - r)}L{_f(x + r * .3)} {_f(y - r * .3)}L{_f(x + r)} {_f(y)}L{_f(x + r * .3)} {_f(y + r * .3)}'
                f'L{_f(x)} {_f(y + r)}L{_f(x - r * .3)} {_f(y + r * .3)}L{_f(x - r)} {_f(y)}L{_f(x - r * .3)} {_f(y - r * .3)}Z" fill="{GOLD}"/>')
    return out


def _sign(x, y, txt_svg, lv):
    m = MATS[lv]
    return (f'<rect x="{_f(x - 12)}" y="{_f(y - 10)}" width="24" height="16" rx="3" fill="#FFF8E7" stroke="{m["dark"]}" stroke-width="1.4"/>'
            + txt_svg)


def _extras(lv, half_w):
    """Jardinets, lampadaires et éclat doré autour des bâtiments les plus avancés."""
    s = ""
    if lv >= 2:
        s += _bush(100 - half_w - 12, 200, .8) + _bush(100 + half_w + 12, 200, .8)
    if lv >= 4:
        s += _lamp(100 - half_w - 26) + _lamp(100 + half_w + 26)
    return s


# ─────────────────────────────────────────────────────── les 8 bâtiments

def _biblio(lv):
    m = MATS[lv]
    W, H = 70 + 16 * lv, 40 + 8 * lv
    x0, base = 100 - W / 2, 200 - (8 if lv >= 3 else 0)
    y0 = base - H
    roof = m["roof"] or ("#2B3A8C" if lv == 5 else "#C0504D")
    s = ""
    if lv >= 4:  # ailes
        ww, wh = 26, H * .7
        for wx in (x0 - ww + 2, x0 + W - 2):
            s += _wall(wx, base - wh, ww, wh, lv) + _windows(wx, base - wh + 8, ww, 2 if lv == 5 else 1, 1, lv)
            s += _flat_roof(wx, base - wh, ww, roof, lv)
    s += _wall(x0, y0, W, H, lv)
    if lv >= 2:
        n = lv + 2
        for i in range(n):
            s += _column(x0 + 6 + i * (W - 19) / (n - 1), y0 + 6, H - 10, lv)
        s += _windows(x0 + 10, y0 + 12, W - 20, 1, n - 1, lv, 8, 12)
    else:
        s += _win(x0 + 8, y0 + 12, 12, 12, lv) + _win(x0 + W - 20, y0 + 12, 12, 12, lv)
    s += _door(100, base, 14 + lv, 20 + 2 * lv, lv)
    peak = 16 + 5 * lv
    s += _gable(x0, x0 + W, y0, peak, roof, lv)
    if lv >= 2:  # livre ouvert dans le fronton
        by = y0 - peak * .42
        s += (f'<path d="M{_f(100 - 9)} {_f(by)}q4.5-3 9 0q4.5-3 9 0v7q-4.5-3-9 0q-4.5-3-9 0z" fill="#fff" stroke="{m["dark"]}" stroke-width="1"/>'
              f'<path d="M100 {_f(by)}v7" stroke="{m["dark"]}" stroke-width="1"/>')
    else:
        s += _sign(100, y0 - 6, f'<text x="100" y="{_f(y0 + 1.5)}" font-size="10" text-anchor="middle">📖</text>', lv)
    if lv >= 3:
        s += _steps(100, W * .5, lv)
    if lv == 5:
        s += (f'<path d="M86 {_f(y0 - peak + 2)}a14 14 0 0 1 28 0z" fill="{GOLD}" stroke="#B8860B" stroke-width="1.4"/>'
              + _flag(100, y0 - peak - 10, "#4F63D8"))
    elif lv >= 3:
        s += _flag(100, y0 - peak + 2, "#4F63D8")
    return s, W / 2 + (26 if lv >= 4 else 0)


def _hall(lv):
    m = MATS[lv]
    W, H = 80 + 14 * lv, 34 + 6 * lv
    x0, base = 100 - W / 2, 200 - (8 if lv >= 3 else 0)
    roof = m["roof"] or ("#2B3A8C" if lv == 5 else "#4F63D8")
    tw, th = 24 + 2 * lv, H + 24 + 14 * lv
    s = ""
    s += _wall(x0, base - H, W, H, lv) + _windows(x0 + 4, base - H + 10, (W - tw) / 2 - 6, 1 + (lv >= 4), 1 + (lv >= 3), lv, 9, 11, 16)
    s += _windows(100 + tw / 2 + 2, base - H + 10, (W - tw) / 2 - 6, 1 + (lv >= 4), 1 + (lv >= 3), lv, 9, 11, 16)
    s += _gable(x0, 100 - tw / 2, base - H, 10 + 2 * lv, roof, lv) + _gable(100 + tw / 2, x0 + W, base - H, 10 + 2 * lv, roof, lv)
    # tour de l'horloge
    ty = base - th
    s += _wall(100 - tw / 2, ty, tw, th, lv)
    cr = 6 + lv
    s += (f'<circle cx="100" cy="{_f(ty + 6 + cr)}" r="{_f(cr)}" fill="#fff" stroke="{GOLD if lv >= 4 else m["dark"]}" stroke-width="2"/>'
          f'<path d="M100 {_f(ty + 6 + cr)}V{_f(ty + 6 + cr * .35)}M100 {_f(ty + 6 + cr)}l{_f(cr * .5)} {_f(cr * .3)}" '
          f'stroke="{m["dark"]}" stroke-width="1.6" stroke-linecap="round"/>')
    if lv >= 2:
        s += _win(100 - 4.5, ty + 12 + 2 * cr, 9, 12, lv)
    s += _door(100, base, 14 + lv, 18 + 3 * lv, lv)
    spire = 14 + 6 * lv
    s += (f'<path d="M{_f(100 - tw / 2 - 4)} {_f(ty)}L100 {_f(ty - spire)}L{_f(100 + tw / 2 + 4)} {_f(ty)}Z" fill="{roof}" '
          f'stroke="{GOLD if lv == 5 else m["dark"]}" stroke-width="2" stroke-linejoin="round"/>')
    if lv >= 3:
        s += _steps(100, tw + 10, lv)
    if lv >= 2:
        s += _flag(100, ty - spire, "#E03131", 18 + 2 * lv)
    if lv == 5:
        s += f'<circle cx="100" cy="{_f(ty - spire)}" r="3.5" fill="{GOLD}"/>'
    return s, W / 2


def _cafe(lv):
    m = MATS[lv]
    W = 70 + 12 * lv
    H = 38 + (20 if lv >= 4 else 0) + 3 * lv
    x0, base = 100 - W / 2, 200
    y0 = base - H
    s = _wall(x0, y0, W, H, lv)
    if lv >= 4:  # étage
        s += _windows(x0 + 6, y0 + 8, W - 12, 1, 3 + (lv == 5), lv, 10, 12)
    aw_y = base - 34
    stripe = m["roof"] or "#E03131"
    n = 4 + lv
    sw = (W + 8) / n
    for i in range(n):
        c = stripe if i % 2 == 0 else "#FFFFFF"
        s += f'<path d="M{_f(x0 - 4 + i * sw)} {_f(aw_y - 10)}h{_f(sw)}l2 12h{_f(-sw)}z" fill="{c}" stroke="#00000020" stroke-width=".6"/>'
    s += _win(x0 + 8, base - 20, 16, 14, lv) + _win(x0 + W - 24, base - 20, 16, 14, lv)
    s += _door(100, base, 13, 22, lv)
    if lv >= 4:
        s += _flat_roof(x0, y0, W, "#8C5A3C" if lv == 4 else "#2B3A8C", lv)
    else:
        s += _gable(x0, x0 + W, y0, 12 + 3 * lv, m["roof"] or "#8C5A3C", lv)
    # enseigne tasse
    sy = y0 - (8 if lv >= 4 else 20 + 3 * lv)
    s += (f'<circle cx="100" cy="{_f(sy)}" r="9" fill="#fff" stroke="{GOLD if lv == 5 else "#8C5A3C"}" stroke-width="2"/>'
          f'<path d="M95.5 {_f(sy - 3)}h7v5a3.5 3.5 0 0 1-7 0zM102.5 {_f(sy - 2)}h1.6a1.8 1.8 0 0 1 0 3.6h-1.6" fill="none" stroke="#8C5A3C" stroke-width="1.6"/>')
    s += f'<path class="pv-steam" d="M98 {_f(sy - 6)}q-2-3 0-6M102 {_f(sy - 6)}q2-3 0-6" stroke="#fff" stroke-width="1.4" fill="none"/>'
    # terrasse
    for i in range(max(0, lv - 1)):
        tx = (x0 - 20 - i * 18) if i % 2 == 0 else (x0 + W + 20 + (i - 1) * 9)
        uc = ["#E03131", "#FFD43B", "#4F63D8", "#20C997"][i % 4]
        s += (f'<path d="M{_f(tx)} 200V178" stroke="#666" stroke-width="1.4"/>'
              f'<path d="M{_f(tx - 11)} 180q11-12 22 0z" fill="{uc}"/>'
              f'<rect x="{_f(tx - 6)}" y="191" width="12" height="2.5" fill="#8C5A3C"/>'
              f'<path d="M{_f(tx - 4)} 193.5V200M{_f(tx + 4)} 193.5V200" stroke="#8C5A3C" stroke-width="1.2"/>')
    if lv == 5:
        s += _sparkles([(x0 + 4, y0 - 12, 4), (x0 + W - 4, y0 - 16, 3.5)])
    return s, W / 2 + (lv - 1) * 9


def _amphi(lv):
    m = MATS[lv]
    W, H = 90 + 14 * lv, 34 + 5 * lv
    x0, base = 100 - W / 2, 200 - (8 if lv >= 3 else 0)
    y0 = base - H
    dome = m["roof"] or {2: "#4F63D8", 3: "#3B5BDB", 4: "#5C7CFA", 5: GOLD}[lv]
    R = 22 + 6 * lv
    s = (f'<path d="M{_f(100 - R)} {_f(y0)}a{_f(R)} {_f(R)} 0 0 1 {_f(2 * R)} 0z" fill="{dome}" '
         f'stroke="{MATS[lv]["dark"]}" stroke-width="2"/>')
    if lv >= 2:
        for k in (.35, .7):
            s += f'<path d="M{_f(100 - R * k)} {_f(y0)}a{_f(R * k)} {_f(R * 1.0)} 0 0 1 {_f(2 * R * k)} 0" fill="none" stroke="#FFFFFF55" stroke-width="1.4"/>'
    s += (f'<rect x="96" y="{_f(y0 - R - 10)}" width="8" height="10" fill="{dome}" stroke="{m["dark"]}" stroke-width="1.2"/>'
          f'<circle cx="100" cy="{_f(y0 - R - 12)}" r="3" fill="{GOLD}"/>')
    s += _wall(x0, y0, W, H, lv)
    if lv >= 3:
        n = lv + 3
        for i in range(n):
            s += _column(x0 + 6 + i * (W - 19) / (n - 1), y0 + 5, H - 9, lv)
    else:
        s += _windows(x0 + 6, y0 + 10, W - 12, 1, 4, lv, 10, 12)
    s += _door(100, base, 16 + lv, 18 + 3 * lv, lv)
    if lv >= 3:
        s += _steps(100, W * .45, lv)
    if lv == 5:
        s += _sparkles([(100 - R - 6, y0 - R * .6, 4), (100 + R + 6, y0 - R * .7, 3.5)])
    return s, W / 2


def _residence(lv):
    m = MATS[lv]
    floors = lv + 1
    W, fh = 60 + 6 * lv, 22
    H = floors * fh + 8
    x0, base = 100 - W / 2, 200
    y0 = base - H
    s = _wall(x0, y0, W, H, lv)
    cols = 3 if lv < 4 else 4
    lit = 0
    step = W / cols
    for r in range(floors):
        for c in range(cols):
            if r == floors - 1 and c in (cols // 2 - (cols % 2 == 0), cols // 2):
                continue  # porte
            lit += 1
            wx, wy = x0 + step * c + (step - 10) / 2, y0 + 7 + r * fh
            s += _win(wx, wy, 10, 12, lv).replace('class="win"', f'class="win{" off" if lit % 3 == 0 else ""}"')
            if lv >= 4 and r < floors - 1:  # balcons
                s += f'<rect x="{_f(wx - 2)}" y="{_f(wy + 12)}" width="14" height="3" fill="{m["dark"]}"/>'
    s += _door(100, base, 14, 18, lv)
    roof = m["roof"] or {2: "#8C5A3C", 3: "#6B3A2A", 4: "#495057", 5: "#2B3A8C"}[lv]
    s += _gable(x0, x0 + W, y0, 14 + 3 * lv, roof, lv)
    if lv >= 3:  # cheminée
        s += f'<rect x="{_f(x0 + W * .72)}" y="{_f(y0 - 18 - 2 * lv)}" width="8" height="14" fill="{m["dark"]}"/>'
    if lv >= 3:
        s += _flag(x0 + 10, y0 - 4, "#20C997", 18)
    return s, W / 2


def _labo(lv):
    m = MATS[lv]
    W, H = 74 + 14 * lv, 36 + 6 * lv
    x0, base = 100 - W / 2, 200
    y0 = base - H
    band = m["roof"] or {2: "#20C997", 3: "#12B886", 4: "#0CA678", 5: GOLD}[lv]
    s = ""
    # cheminée + fumée
    cx = x0 + W * .78
    ch = 22 + 4 * lv
    s += f'<rect x="{_f(cx)}" y="{_f(y0 - ch)}" width="10" height="{_f(ch)}" fill="#ADB5BD" stroke="#868E96" stroke-width="1.2"/>'
    for i in range(3):
        s += f'<circle class="pv-smoke" style="animation-delay:{i * .9:.1f}s" cx="{_f(cx + 5)}" cy="{_f(y0 - ch - 4)}" r="{4 + i}" fill="#fff"/>'
    if lv >= 3:  # second bloc
        bw, bh = 34, H + 18
        s += _wall(x0 - 4, base - bh, bw, bh, lv) + _windows(x0 - 4, base - bh + 8, bw, 3, 1, lv, 11, 9, 14)
        s += _flat_roof(x0 - 4, base - bh, bw, band, lv)
    s += _wall(x0 + (28 if lv >= 3 else 0), y0, W - (28 if lv >= 3 else 0), H, lv)
    s += _flat_roof(x0 + (28 if lv >= 3 else 0), y0, W - (28 if lv >= 3 else 0), band, lv)
    s += f'<rect x="{_f(x0 + (28 if lv >= 3 else 0))}" y="{_f(y0 + 4)}" width="{_f(W - (28 if lv >= 3 else 0))}" height="4" fill="{band}" opacity=".7"/>'
    s += _windows(x0 + (30 if lv >= 3 else 4), y0 + 14, W - (34 if lv >= 3 else 8), 1, 3 + (lv >= 4), lv, 12, 10)
    s += _door(x0 + W * .55, base, 14, 20, lv)
    # fiole
    fx, fy = x0 + W * .3 + (12 if lv >= 3 else 0), y0 - 8
    s += (f'<path d="M{_f(fx - 3)} {_f(fy - 14)}h6v5l6 10h-18l6-10z" fill="#fff" stroke="{band}" stroke-width="1.6"/>'
          f'<path d="M{_f(fx - 7)} {_f(fy - 1)}h14l1.8 2.5h-17.6z" fill="#63E6BE"/>')
    if lv >= 4:  # parabole
        dx = x0 + 6
        s += (f'<path d="M{_f(dx)} {_f(base - H - 34)}a10 10 0 0 0 16 8z" fill="#E9ECEF" stroke="#868E96" stroke-width="1.2"/>'
              f'<path d="M{_f(dx + 8)} {_f(base - H - 28)}v8" stroke="#868E96" stroke-width="1.6"/>')
    if lv == 5:
        s += _sparkles([(x0 - 6, y0 - 10, 3.5), (x0 + W + 4, y0 - 4, 4)])
    return s, W / 2


def _serre(lv):
    m = MATS[lv]
    bays = lv + 1
    bw = 26
    W = bays * bw
    H = 40 + 6 * lv
    x0 = 100 - W / 2
    frame = GOLD if lv == 5 else ("#8C5A3C" if lv == 1 else "#FFFFFF" if lv >= 3 else "#A47148")
    s = (f'<path d="M{_f(x0)} 200V{_f(200 - H + 18)}Q{_f(x0)} {_f(200 - H)} {_f(x0 + 18)} {_f(200 - H)}H{_f(x0 + W - 18)}'
         f'Q{_f(x0 + W)} {_f(200 - H)} {_f(x0 + W)} {_f(200 - H + 18)}V200Z" fill="#D3F9D8" fill-opacity=".85" '
         f'stroke="{frame}" stroke-width="2.4"/>')
    for i in range(1, bays):
        s += f'<path d="M{_f(x0 + i * bw)} {_f(200 - H)}V200" stroke="{frame}" stroke-width="1.8"/>'
    s += f'<path d="M{_f(x0)} {_f(200 - H * .5)}H{_f(x0 + W)}" stroke="{frame}" stroke-width="1.4"/>'
    # plantes
    for i in range(bays):
        px = x0 + i * bw + bw / 2
        s += (f'<path d="M{_f(px)} 200q-2-14 -8-18q8 4 8 18q0-16 8-22q-6 10-8 22" fill="#40C057"/>'
              f'<circle cx="{_f(px - 4)}" cy="{_f(186 - (i % 2) * 6)}" r="3" fill="{["#FF8FB8", "#FFD43B", "#B197FC"][i % 3]}"/>')
    if lv >= 3:  # coupole centrale
        R = 14 + 3 * lv
        s += (f'<path d="M{_f(100 - R)} {_f(200 - H + 1)}a{_f(R)} {_f(R)} 0 0 1 {_f(2 * R)} 0z" fill="#B2F2BB" fill-opacity=".9" '
              f'stroke="{frame}" stroke-width="2"/>'
              f'<path d="M100 {_f(200 - H - R)}V{_f(200 - H)}M{_f(100 - R * .7)} {_f(200 - H - R * .7)}L100 {_f(200 - H)}L{_f(100 + R * .7)} {_f(200 - H - R * .7)}" fill="none" stroke="{frame}" stroke-width="1.2"/>')
        if lv >= 4:
            s += f'<path d="M95 {_f(200 - H - R)}q-6-12 4-18q-2 8 2 18" fill="#2F9E44"/>'
    s += f'<path d="M{_f(x0 + 10)} {_f(200 - H + 8)}q10-6 20-4" stroke="#fff" stroke-width="2.4" fill="none" opacity=".8" stroke-linecap="round"/>'
    if lv == 5:
        s += _sparkles([(x0 - 4, 200 - H, 4), (x0 + W + 4, 200 - H + 6, 3.5)])
    return s, W / 2


def _observatoire(lv):
    m = MATS[lv]
    tw = 40 + 6 * lv
    th = 30 + 12 * lv
    x0 = 100 - tw / 2
    ty = 200 - th
    s = _wall(x0, ty, tw, th, lv)
    s += _windows(x0, ty + 10, tw, max(1, lv - 1), 2, lv, 8, 10, 16)
    s += _door(100, 200, 12, 18, lv)
    R = tw / 2 + 4
    dome = "#F8F9FA" if lv < 5 else "#FFF4CC"
    s += (f'<path d="M{_f(100 - R)} {_f(ty)}a{_f(R)} {_f(R)} 0 0 1 {_f(2 * R)} 0z" fill="{dome}" '
          f'stroke="{GOLD if lv == 5 else "#ADB5BD"}" stroke-width="2"/>'
          f'<path d="M96 {_f(ty)}V{_f(ty - R + 3)}h8V{_f(ty)}" fill="#495057"/>')
    tl = 14 + 4 * lv
    s += (f'<g transform="rotate(-38 100 {_f(ty - R * .55)})"><rect x="97" y="{_f(ty - R * .55 - tl)}" width="{_f(6 + lv * .6)}" height="{_f(tl)}" rx="2" '
          f'fill="{"#4F63D8" if lv < 5 else GOLD}"/></g>')
    if lv >= 4:  # petite coupole annexe
        ax = x0 + tw + 4
        s += _wall(ax, 200 - 30, 26, 30, lv)
        s += f'<path d="M{_f(ax - 2)} 170a15 15 0 0 1 30 0z" fill="{dome}" stroke="#ADB5BD" stroke-width="1.6"/>'
    s += _sparkles([(x0 - 10, ty - R, 3), (100 + R + 8, ty - R * .4, 2.6)] + ([(100, ty - R - 22, 4)] if lv >= 3 else []))
    return s, tw / 2 + (30 if lv >= 4 else 0)


DRAW = {"biblio": _biblio, "hall": _hall, "cafe": _cafe, "amphi": _amphi, "residence": _residence,
        "labo": _labo, "serre": _serre, "observatoire": _observatoire}


def building_inner(key, lv):
    lv = max(1, min(5, int(lv)))
    body, half = DRAW[key](lv)
    halo = ""
    if lv == 5:
        halo = '<ellipse cx="100" cy="130" rx="110" ry="90" fill="url(#pvGlow)" opacity=".35"/>'
    return (halo + f'<ellipse cx="100" cy="201" rx="{_f(half + 16)}" ry="6" fill="#000" opacity=".14"/>'
            + _extras(lv, half) + body)


def plot_inner(locked=False, need=0):
    if locked:
        return ('<ellipse cx="100" cy="200" rx="58" ry="9" fill="#000" opacity=".08"/>'
                + "".join(f'<rect x="{x}" y="180" width="4" height="20" fill="#A47148"/>' for x in range(50, 151, 20)) +
                '<path d="M48 186H154M48 194H154" stroke="#A47148" stroke-width="2.2"/>'
                f'<rect x="80" y="150" width="40" height="22" rx="4" fill="#FFF8E7" stroke="#A47148" stroke-width="1.6"/>'
                f'<text x="100" y="166" font-size="12" text-anchor="middle" font-weight="700" fill="#6B4E3A">🔒 N{need}</text>')
    return ('<ellipse cx="100" cy="196" rx="62" ry="11" fill="#C8A37A"/><ellipse cx="100" cy="194" rx="54" ry="8" fill="#D9B98F"/>'
            '<path d="M98 194V150" stroke="#8C5A3C" stroke-width="4"/>'
            '<rect x="72" y="138" width="54" height="22" rx="4" fill="#FFD43B" stroke="#E0A100" stroke-width="2"/>'
            '<text x="99" y="153" font-size="10.5" font-weight="800" text-anchor="middle" fill="#3B2F00">À BÂTIR</text>'
            '<path d="M48 196l5-14 5 14zM142 196l5-14 5 14z" fill="#FF922B"/><path d="M50 190h6M144 190h6" stroke="#fff" stroke-width="2"/>')


def building_svg(key, lv, size="100%"):
    """Vignette autonome (fiche du bâtiment, aperçu du niveau suivant)."""
    inner = building_inner(key, lv) if lv > 0 else plot_inner()
    return (f'<svg viewBox="-10 -20 220 230" width="{size}" xmlns="http://www.w3.org/2000/svg" style="overflow:visible">'
            + DEFS + inner + '</svg>')


# ─────────────────────────────────────────────────────── le village entier

# clé → (x du pied, y du pied, échelle)
LOTS = {
    "serre": (120, 272, .8),
    "hall": (500, 252, .95),
    "observatoire": (885, 218, .78),
    "biblio": (285, 305, .92),
    "amphi": (718, 305, .92),
    "labo": (125, 465, 1.05),
    "cafe": (320, 490, 1.1),
    "residence": (690, 492, 1.1),
}
PLAZA = (500, 345)
POND = (885, 430, 82, 30)  # étang (cx, cy, rx, ry)

TREES = [(40, 330, .9, "r"), (960, 330, .85, "p"), (225, 222, .6, "r"), (775, 228, .6, "p"), (400, 214, .55, "r"),
         (600, 212, .55, "r"), (28, 236, .6, "p"), (975, 520, 1.0, "r"), (230, 402, .8, "r"), (35, 525, 1.05, "p"),
         (262, 538, 1.0, "r"), (800, 545, 1.0, "p"), (925, 285, .65, "p"), (338, 206, .5, "p"), (665, 206, .5, "p"),
         (92, 208, .5, "r"), (440, 412, .7, "r"), (562, 412, .7, "r"), (195, 525, .9, "p"), (860, 535, .95, "r"),
         (150, 335, .75, "p"), (790, 395, .75, "r"), (985, 410, .8, "p"), (205, 300, .6, "p"), (805, 305, .6, "r"),
         (60, 410, .8, "r"), (420, 545, .8, "p"), (585, 548, .8, "p")]


def _rng(seed):
    x = seed
    while True:
        x = (x * 1103515245 + 12345) & 0x7FFFFFFF
        yield x / 0x7FFFFFFF


def _tree(x, y, s, kind="r", autumn=False, snow=False):
    if kind == "p":  # sapin
        c1, c2 = "#2B8A3E", "#37B24D"
        cap = '<path d="M-7 -44l7-12 7 12z" fill="#fff"/>' if snow else ""
        body = (f'<path d="M-16 -12L0 -40L16 -12Z" fill="{c1}"/><path d="M-13 -26L0 -52L13 -26Z" fill="{c2}"/>'
                f'<path d="M-9 -40L0 -60L9 -40Z" fill="{c1}"/>{cap}')
        return (f'<g class="deco" transform="translate({_f(x)} {_f(y)}) scale({_f(s)})">'
                f'<ellipse cx="0" cy="0" rx="13" ry="4" fill="#000" opacity=".12"/>'
                f'<rect x="-2.5" y="-14" width="5" height="14" fill="#7A4A2A"/>{body}</g>')
    c1, c2 = ("#E8590C", "#F59F00") if autumn else ("#2F9E44", "#51CF66")
    cap = '<ellipse cx="0" cy="-46" rx="12" ry="5" fill="#fff"/>' if snow else ""
    return (f'<g class="deco" transform="translate({_f(x)} {_f(y)}) scale({_f(s)})">'
            f'<ellipse cx="0" cy="0" rx="14" ry="4" fill="#000" opacity=".12"/>'
            f'<rect x="-3" y="-20" width="6" height="20" fill="#8C5A3C"/>'
            f'<circle cx="0" cy="-30" r="16" fill="{c1}"/><circle cx="-8" cy="-36" r="10" fill="{c2}"/>'
            f'<circle cx="7" cy="-40" r="9" fill="{c2}"/><circle cx="-4" cy="-28" r="2" fill="#fff" opacity=".25"/>{cap}</g>')


def _person(i, path, dur):
    colors = ["#E03131", "#4F63D8", "#F08C00", "#2F9E44", "#9C36B5", "#1098AD", "#E64980"]
    skins = ["#F1C27D", "#C68642", "#8D5524", "#FFDBAC", "#E0AC69"]
    c = colors[i % len(colors)]
    return (f'<g class="deco"><circle cx="0" cy="-15" r="3.6" fill="{skins[i % len(skins)]}"/>'
            f'<path d="M-4 -11h8l1 9h-10z" fill="{c}"/><path d="M-2 -2v4M2 -2v4" stroke="#333" stroke-width="1.6"/>'
            f'<rect x="2" y="-10" width="4" height="5" rx="1" fill="#6B4E3A"/>'
            f'<animateMotion dur="{dur}s" repeatCount="indefinite" begin="-{(i * 3.7) % dur:.1f}s" path="{path}"/></g>')


def _bench(x, y, s=1.0):
    return (f'<g class="deco" transform="translate({_f(x)} {_f(y)}) scale({_f(s)})">'
            '<rect x="-13" y="-9" width="26" height="3" rx="1" fill="#A0522D"/><rect x="-13" y="-14" width="26" height="3" rx="1" fill="#A0522D"/>'
            '<path d="M-10 -6v6M10 -6v6" stroke="#3A3A4A" stroke-width="2"/></g>')


def _flowerbed(x, y, w, seed):
    r = _rng(seed)
    out = f'<g class="deco"><ellipse cx="{_f(x)}" cy="{_f(y)}" rx="{_f(w / 2)}" ry="6" fill="#7A5230" opacity=".55"/>'
    for i in range(int(w / 6)):
        fx = x - w / 2 + 4 + i * 6 + next(r) * 2
        c = ["#FF6B9D", "#FFD43B", "#B197FC", "#FF922B", "#fff"][i % 5]
        out += f'<path d="M{_f(fx)} {_f(y)}v-6" stroke="#2F9E44" stroke-width="1.2"/><circle cx="{_f(fx)}" cy="{_f(y - 7)}" r="2.4" fill="{c}"/>'
    return out + "</g>"


def _pond(snow):
    cx, cy, rx, ry = POND
    water = "#D0E7F5" if snow else "#5FB6E6"
    out = (f'<g class="deco"><ellipse cx="{cx}" cy="{cy + 3}" rx="{rx + 8}" ry="{ry + 6}" fill="#A68A64" opacity=".5"/>'
           f'<ellipse class="water" cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{water}"/>'
           f'<ellipse cx="{cx - 18}" cy="{cy - 8}" rx="{rx * .5}" ry="{ry * .25}" fill="#fff" opacity=".25"/>'
           f'<path class="ripple" d="M{cx - 40} {cy + 6}q10-4 20 0M{cx + 12} {cy + 12}q10-4 20 0" stroke="#fff" stroke-width="1.4" fill="none" opacity=".6"/>')
    # nénuphars et roseaux
    for dx, dy in ((-50, 4), (34, -6), (52, 10)):
        out += f'<ellipse cx="{cx + dx}" cy="{cy + dy}" rx="7" ry="3" fill="#40C057"/><circle cx="{cx + dx + 2}" cy="{cy + dy - 1}" r="1.8" fill="#FF8FB8"/>'
    for dx in (-rx + 4, -rx + 10, rx - 8):
        out += f'<path d="M{cx + dx} {cy + 4}q-2-16 2-24M{cx + dx + 4} {cy + 6}q1-12 4-18" stroke="#2F9E44" stroke-width="2" fill="none"/>'
    if not snow:  # canards
        for i, dx in enumerate((-20, 8)):
            out += (f'<g class="duck" style="animation-delay:-{i * 2}s"><g transform="translate({cx + dx} {cy})">'
                    '<ellipse cx="0" cy="0" rx="7" ry="4" fill="#fff"/><circle cx="5" cy="-4" r="3" fill="#2B8A3E"/>'
                    '<path d="M7.5 -4l3 1-3 1z" fill="#F59F00"/></g></g>')
    # petit pont de bois
    out += (f'<path d="M{cx - 30} {cy + ry - 2}q30-16 60 0" stroke="#8C5A3C" stroke-width="7" fill="none"/>'
            f'<path d="M{cx - 30} {cy + ry - 8}q30-16 60 0" stroke="#A0522D" stroke-width="1.6" fill="none"/>'
            + "".join(f'<path d="M{cx - 24 + i * 12} {cy + ry - 9 - (6 if 0 < i < 4 else 2)}v6" stroke="#A0522D" stroke-width="1.6"/>' for i in range(5))
            + '</g>')
    return out


def _windmill(x, y):
    return (f'<g class="deco" transform="translate({x} {y})">'
            '<path d="M-7 0L-4 -30H4L7 0Z" fill="#F1E3C8" stroke="#A47148" stroke-width="1"/>'
            '<path d="M-6 -30L0 -38L6 -30Z" fill="#C0504D"/>'
            '<g class="blades" style="transform-origin:0px -32px"><path d="M0 -32L-2 -54H2ZM0 -32L-22 -30V-34ZM0 -32L2 -10H-2ZM0 -32L22 -34V-30Z" fill="#fff" stroke="#A47148" stroke-width=".6"/></g>'
            '<circle cx="0" cy="-32" r="1.8" fill="#6B4E3A"/></g>')


def _gate(total):
    stone = total >= 15
    c = "#D9D3C7" if stone else "#A47148"
    d = "#9C9284" if stone else "#7A4A2A"
    out = '<g class="deco">'
    for x in (452, 548):
        out += (f'<rect x="{x - 9}" y="508" width="18" height="52" fill="{c}" stroke="{d}" stroke-width="1.6"/>'
                f'<rect x="{x - 12}" y="502" width="24" height="7" fill="{d}"/>')
        if total >= 25:
            out += f'<circle cx="{x}" cy="497" r="5" fill="{GOLD}"/>'
    out += (f'<path d="M452 512Q500 478 548 512" stroke="{d}" stroke-width="6" fill="none"/>'
            f'<rect x="466" y="490" width="68" height="16" rx="3" fill="#FFF8E7" stroke="{d}" stroke-width="1.4"/>'
            '<text x="500" y="502" font-size="9.5" font-weight="800" text-anchor="middle" fill="#4F3A2A" font-family="system-ui">UNIVERSITÉ</text></g>')
    return out


def campus_svg(levels, need, total, autumn=False, snow=False):
    """levels : {clé: niveau}, need : {clé: niveau de joueur requis si verrouillé}, total : somme des niveaux."""
    road = "#D9C29B" if total < 15 else "#CFCAC0"
    out = [f'<svg class="village-svg" viewBox="0 0 1000 560" xmlns="http://www.w3.org/2000/svg">', DEFS]
    # ── ciel : étoiles (nuit), soleil, lune, nuages, oiseaux
    r = _rng(7)
    out.append('<g class="stars">' + "".join(
        f'<circle cx="{_f(next(r) * 1000)}" cy="{_f(next(r) * 150)}" r="{_f(.6 + next(r) * 1.2)}" fill="#fff" style="animation-delay:{next(r) * 3:.1f}s"/>'
        for _ in range(60)) + '</g>')
    out.append('<g class="sun"><circle cx="140" cy="70" r="46" fill="#FFF3BF" opacity=".5"/><circle cx="140" cy="70" r="30" fill="#FFE066"/></g>'
               '<g class="moonG"><circle cx="860" cy="70" r="26" fill="#FFF8DC"/><circle class="moonCut" cx="872" cy="62" r="22" fill="#1c2352"/></g>')
    for i, (cx, cy, sc) in enumerate([(260, 60, 1), (620, 40, .8), (820, 110, .7), (430, 95, .55)]):
        out.append(f'<g class="cloud" style="animation-delay:-{i * 25}s"><g transform="translate({cx} {cy}) scale({sc})">'
                   '<ellipse cx="0" cy="0" rx="40" ry="14" fill="#fff"/><ellipse cx="-14" cy="-8" rx="18" ry="14" fill="#fff"/>'
                   '<ellipse cx="14" cy="-10" rx="22" ry="16" fill="#fff"/></g></g>')
    out.append('<g class="birds">' + "".join(
        f'<path class="bird" style="animation-delay:-{i * 4}s" d="M{x} {y}q5-5 10 0q5-5 10 0" stroke="#3A3A4A" stroke-width="1.6" fill="none"/>'
        for i, (x, y) in enumerate([(300, 120), (322, 110), (340, 126), (700, 80)])) + '</g>')
    # ── montagnes au loin, collines, champs
    out.append('<path class="mount" d="M0 190L70 120L130 165L210 95L300 170L380 130L450 175L560 105L650 160L740 115L820 165L900 100L1000 160V230H0Z" fill="#A9C1DC"/>'
               '<path class="snowcap" d="M196 108L210 95L224 108L216 106L210 112L203 106ZM546 118L560 105L574 118L566 116L560 122L553 116ZM886 113L900 100L914 113L906 111L900 117L893 111Z" fill="#fff"/>'
               '<path class="hill2" d="M0 200Q160 120 330 185T650 170T1000 150V260H0Z" fill="#9ED39A"/>')
    for i, (x, y, w, c) in enumerate([(360, 196, 64, "#C9E59A"), (432, 200, 52, "#E8D88A"), (585, 197, 62, "#B7DD8F"), (652, 192, 50, "#E3CF7E")]):
        out.append(f'<g class="field"><path d="M{x} {y}l{w} -6l8 14l-{w} 6z" fill="{c}"/>'
                   + "".join(f'<path d="M{x + 4 + k * w / 5} {y + 5 - k * 1.2}l6 -1" stroke="#00000018" stroke-width="2"/>' for k in range(5)) + '</g>')
    out.append(_windmill(48, 205))
    out.append('<path class="hill1" d="M0 225Q250 170 520 215T1000 205V300H0Z" fill="#86C77F"/>'
               '<path class="hill0" d="M720 260Q880 150 1000 175V300H720Z" fill="#7DBE73"/>'
               '<rect class="grass" x="0" y="232" width="1000" height="330" fill="#8FD07F"/>'
               '<path class="grass2" d="M0 360Q300 330 520 370T1000 350V560H0Z" fill="#84C873"/>')
    # ── herbe : touffes, fleurs sauvages, cailloux (sous les chemins)
    r = _rng(42)
    deco = []
    for _ in range(70):
        x, y = next(r) * 1000, 245 + next(r) * 310
        k = next(r)
        if k < .5:
            deco.append(f'<path class="tuft" d="M{_f(x)} {_f(y)}l-3-7M{_f(x)} {_f(y)}l0-9M{_f(x)} {_f(y)}l3-7" stroke="#5DAE52" stroke-width="1.5" stroke-linecap="round"/>')
        elif k < .85:
            c = ["#FFFFFF", "#FFD43B", "#FF8FB8", "#B197FC"][int(next(r) * 4)]
            deco.append(f'<circle class="wf" cx="{_f(x)}" cy="{_f(y)}" r="2.2" fill="{c}"/>')
        else:
            deco.append(f'<ellipse cx="{_f(x)}" cy="{_f(y)}" rx="{_f(4 + next(r) * 5)}" ry="3" fill="#A5A9AD"/>')
    out.append('<g class="deco">' + "".join(deco) + '</g>')
    # ── ruisseau vers l'étang
    cx, cy, rx, ry = POND
    out.append(f'<path class="stream" d="M1000 262Q950 300 970 340T{cx + rx - 10} {cy - 8}" stroke="{"#D0E7F5" if snow else "#5FB6E6"}" stroke-width="10" fill="none" stroke-linecap="round"/>')
    # ── chemins
    px, py = PLAZA
    roads = [f"M{px} 560V{py}"]
    for k, (x, y, _s) in LOTS.items():
        roads.append(f"M{px} {py}Q{(px + x) / 2} {py if y > py else (py + y) / 2 + 10} {x} {y + 4}")
    roads.append(f"M{px + 40} {py + 10}Q{cx - 120} {cy - 10} {cx - rx + 6} {cy}")  # vers l'étang
    rw = 16 + min(10, total // 4)
    for d in roads:
        out.append(f'<path d="{d}" stroke="#00000014" stroke-width="{rw + 4}" fill="none" stroke-linecap="round"/>')
    for d in roads:
        out.append(f'<path d="{d}" stroke="{road}" stroke-width="{rw}" fill="none" stroke-linecap="round"/>')
        if total >= 15:  # pavés
            out.append(f'<path d="{d}" stroke="#B8B0A0" stroke-width="{rw - 4}" stroke-dasharray="3 7" fill="none" opacity=".55"/>')
    out.append(f'<ellipse cx="{px}" cy="{py}" rx="{70 + min(40, total * 2)}" ry="{24 + min(14, total)}" fill="{road}"/>')
    if total >= 15:
        out.append(f'<ellipse cx="{px}" cy="{py}" rx="{56 + min(40, total * 2)}" ry="{18 + min(14, total)}" fill="none" stroke="#B8B0A0" stroke-width="2" stroke-dasharray="4 6"/>')
    out.append(_pond(snow))
    # ── centre de la place
    if total >= 10:
        out.append(f'<g class="deco" transform="translate({px} {py + 6})">'
                   '<ellipse cx="0" cy="0" rx="34" ry="11" fill="#ADB5BD"/><ellipse cx="0" cy="-2" rx="29" ry="8" fill="#74C0FC"/>'
                   '<rect x="-4" y="-24" width="8" height="22" fill="#CED4DA"/><ellipse cx="0" cy="-24" rx="12" ry="4" fill="#ADB5BD"/>'
                   '<path class="pv-water" d="M0 -26q-10 -14 -18 10M0 -26q10 -14 18 10" stroke="#A5D8FF" stroke-width="2.4" fill="none"/>'
                   + (f'<path d="M-6 -38l6-12 6 12z" fill="{GOLD}"/><circle cx="0" cy="-52" r="4" fill="{GOLD}"/>' if total >= 30 else "")
                   + '</g>')
    else:
        out.append(f'<g class="deco" transform="translate({px} {py})"><circle cx="0" cy="0" r="12" fill="#8FD07F"/>'
                   '<circle cx="-4" cy="-2" r="3" fill="#FF8FB8"/><circle cx="4" cy="1" r="3" fill="#FFD43B"/><circle cx="0" cy="4" r="2.6" fill="#fff"/></g>')
    items = []
    # massifs de fleurs le long de l'allée, bancs autour de la place
    if total >= 3:
        for y in (395, 455, 515)[: 1 + (total >= 8) + (total >= 14)]:
            items.append((y, _flowerbed(px - rw / 2 - 22, y, 26, y) + _flowerbed(px + rw / 2 + 22, y, 26, y + 1)))
    if total >= 4:
        for bx, by in ((px - 110, py + 30), (px + 110, py + 30), (px - 120, py - 16), (px + 120, py - 16))[: 2 + 2 * (total >= 12)]:
            items.append((by, _bench(bx, by)))
    # arbres
    n_trees = min(len(TREES), 12 + total // 2)
    for i, (x, y, sc, kind) in enumerate(TREES[:n_trees]):
        items.append((y, _tree(x, y, sc, kind, autumn and i % 3 != 0, snow)))
    # haies basses
    for hx, hy, w in ((60, 300, 60), (940, 470, 40), (380, 395, 40), (620, 395, 40)):
        items.append((hy, f'<g class="deco"><rect x="{hx - w / 2}" y="{hy - 9}" width="{w}" height="10" rx="5" fill="#3E9C47"/>'
                          f'<rect x="{hx - w / 2 + 3}" y="{hy - 11}" width="{w - 6}" height="5" rx="3" fill="#51CF66"/></g>'))
    # lampadaires
    if total >= 6:
        for y in (400, 470, 540)[: 1 + (total >= 12) + (total >= 18)]:
            for x in (px - 34 - rw / 2, px + 34 + rw / 2):
                items.append((y, f'<g transform="translate({_f(x)} {y}) scale(.9)" class="deco streetlamp">'
                                 '<path d="M0 0V-38" stroke="#3A3A4A" stroke-width="3"/>'
                                 '<circle class="lamp" cx="0" cy="-41" r="5" fill="#FFF3BF" stroke="#3A3A4A" stroke-width="1.6"/></g>'))
    if total >= 25:
        for x in (px - 120, px + 120):
            items.append((py + 20, f'<g class="deco" transform="translate({x} {py + 20})"><path d="M0 0V-60" stroke="#555" stroke-width="2.4"/>'
                                   f'<path class="pv-flag" d="M0 -60h18v26l-9-6-9 6z" fill="#4F63D8"/><circle cx="9" cy="-48" r="4" fill="{GOLD}"/></g>'))
    items.append((560, _gate(total)))
    # bâtiments : seule la forme dessinée est cliquable (pas de grand rectangle invisible)
    for k, (x, y, sc) in LOTS.items():
        lv = int(levels.get(k, 0))
        if lv > 0:
            inner = building_inner(k, lv)
            half = DRAW[k](lv)[1]
        else:
            inner = plot_inner(locked=k in need, need=need.get(k, 0))
            half = 60
        tx, ty = x - 100 * sc, y - 200 * sc
        items.append((y, f'<g class="lot lv{lv}{" locked" if k in need else ""}" data-k="{k}" onclick="selBld(\'{k}\')">'
                         f'<g transform="translate({_f(tx)} {_f(ty)}) scale({sc})">'
                         f'<ellipse class="selring" cx="100" cy="200" rx="{_f(half + 22)}" ry="16" fill="none" stroke="#FFD43B" stroke-width="5"/>'
                         f'<ellipse class="hit" cx="100" cy="196" rx="{_f(half + 12)}" ry="14" fill="transparent"/>'
                         f'<g class="bodyg">{inner}</g></g></g>'))
    # étudiants
    n_people = min(16, 2 + total // 2)
    routes = []
    for k, (x, y, _s) in LOTS.items():
        if int(levels.get(k, 0)) > 0:
            routes.append(f"M{x} {y + 6}Q{(px + x) / 2} {py + 4 if y > py else (py + y) / 2 + 14} {px} {py + 8}"
                          f"Q{(px + x) / 2} {py + 4 if y > py else (py + y) / 2 + 14} {x} {y + 6}")
    routes.append(f"M{px} 560V{py + 10}V560")
    routes.append(f"M{px + 40} {py + 14}Q{cx - 120} {cy - 6} {cx - rx + 4} {cy + 4}Q{cx - 120} {cy - 6} {px + 40} {py + 14}")
    for i in range(n_people):
        items.append((py + 1, _person(i, routes[i % len(routes)], 26 + (i * 7) % 18)))
    items.sort(key=lambda t: t[0])
    out.extend(x for _y, x in items)
    out.append('</svg>')
    return "".join(out)
