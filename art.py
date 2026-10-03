# -*- coding: utf-8 -*-
"""Illustrations vectorielles (SVG) des compagnons illustrés."""

_S = 'style="width:1.15em;height:1.15em;vertical-align:-.22em;overflow:visible" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg"'

_EYES = ('<circle cx="{lx}" cy="{y}" r="{r}" fill="#fff"/><circle cx="{rx}" cy="{y}" r="{r}" fill="#fff"/>'
         '<circle cx="{lpx}" cy="{py}" r="{p}" fill="#2B2140"/><circle cx="{rpx}" cy="{py}" r="{p}" fill="#2B2140"/>'
         '<circle cx="{lhx}" cy="{hy}" r="{h}" fill="#fff"/><circle cx="{rhx}" cy="{hy}" r="{h}" fill="#fff"/>')


def _eyes(lx, rx, y, r):
    p = r * .5
    return _EYES.format(lx=lx, rx=rx, y=y, r=r, lpx=lx + r * .15, rpx=rx + r * .15, py=y + r * .1, p=p,
                        lhx=lx + r * .35, rhx=rx + r * .35, hy=y - r * .25, h=r * .2)


_SHADOW = '<ellipse cx="50" cy="94" rx="{w}" ry="4.5" fill="#000" opacity=".13"/>'
_SPOTS = ('<circle cx="37" cy="46" r="5.5" fill="#B9A3F0"/><circle cx="63" cy="63" r="7" fill="#B9A3F0"/>'
          '<circle cx="44" cy="77" r="4" fill="#B9A3F0"/><circle cx="64" cy="36" r="3.5" fill="#B9A3F0"/>')
_STAR = '<path d="M{x} {y} l{a} {b} {b} {a} -{b} {a} -{a} {b} -{a} -{b} -{b} -{a} {b} -{a}z" fill="{c}"/>'


def _star(x, y, s, c="#FFD65A"):
    return _STAR.format(x=x, y=y - 2 * s, a=s * .45, b=s * 1.55, c=c)


EGG = (f'<svg {_S}>' + _SHADOW.format(w=24) +
       '<path d="M50 10C31 10 20 40 20 61C20 81 34 93 50 93S80 81 80 61C80 40 69 10 50 10Z" fill="#F7EFDD" stroke="#D8C7A4" stroke-width="2.2"/>'
       + _SPOTS +
       '<path d="M32 33Q35 23 42 19" stroke="#fff" stroke-width="4.5" stroke-linecap="round" fill="none" opacity=".85"/>'
       + _star(82, 22, 3.2) + _star(15, 40, 2.2, "#C9B6FF") + '</svg>')

HATCH = (f'<svg {_S}>' + _SHADOW.format(w=26) +
         '<circle cx="50" cy="50" r="23" fill="#8B6FD8"/>'
         '<path d="M38 32Q42 24 46 31M54 31Q58 24 62 32" stroke="#7458C4" stroke-width="3" fill="none" stroke-linecap="round"/>'
         + _eyes(41, 59, 45, 7.5) +
         '<path d="M46.5 52L53.5 52L50 57.5Z" fill="#F5A524"/>'
         '<g transform="rotate(-14 48 26)"><path d="M28 36L34 29L40 35L46 27L52 34L58 27L64 33L71 28C67 16 59 11 50 11C39 11 31 21 28 36Z" fill="#F7EFDD" stroke="#D8C7A4" stroke-width="2.2"/>'
         '<circle cx="44" cy="20" r="3" fill="#B9A3F0"/><circle cx="58" cy="19" r="2.2" fill="#B9A3F0"/></g>'
         '<path d="M19 62L27 55L33 62L40 55L47 63L54 55L61 62L68 55L75 62L81 58C81 81 67 93 50 93S19 82 19 62Z" fill="#F7EFDD" stroke="#D8C7A4" stroke-width="2.2"/>'
         '<circle cx="36" cy="76" r="4.5" fill="#B9A3F0"/><circle cx="62" cy="80" r="5.5" fill="#B9A3F0"/>'
         + _star(84, 30, 3, "#FFD65A") + _star(14, 30, 2.4, "#FFD65A") + '</svg>')

OWLET = (f'<svg {_S}>' + _SHADOW.format(w=27) +
         '<path d="M44 33Q50 18 56 33" fill="#8B6FD8"/>'
         '<ellipse cx="22" cy="66" rx="8" ry="14" fill="#7458C4" transform="rotate(18 22 66)"/>'
         '<ellipse cx="78" cy="66" rx="8" ry="14" fill="#7458C4" transform="rotate(-18 78 66)"/>'
         '<ellipse cx="50" cy="62" rx="30" ry="30" fill="#8B6FD8"/>'
         '<ellipse cx="50" cy="71" rx="18" ry="18" fill="#F3E6D0"/>'
         '<path d="M42 68q2 3 4 0M50 72q2 3 4 0M44 78q2 3 4 0M54 79q2 3 4 0" stroke="#D9C3A0" stroke-width="1.8" fill="none" stroke-linecap="round"/>'
         '<ellipse cx="39" cy="53" rx="12" ry="12" fill="#A58DE6"/><ellipse cx="61" cy="53" rx="12" ry="12" fill="#A58DE6"/>'
         + _eyes(39, 61, 53, 9) +
         '<path d="M46 61L54 61L50 67Z" fill="#F5A524"/>'
         '<ellipse cx="29" cy="63" rx="4" ry="2.5" fill="#FF9EC0" opacity=".7"/><ellipse cx="71" cy="63" rx="4" ry="2.5" fill="#FF9EC0" opacity=".7"/>'
         '<path d="M40 91l-3 3M40 91v4M40 91l3 3M60 91l-3 3M60 91v4M60 91l3 3" stroke="#F5A524" stroke-width="2.6" stroke-linecap="round"/>'
         '</svg>')


def _owl_body(dark="#7B5CD0", mid="#8B6FD8", wing="#6A4DBF"):
    return ('<path d="M27 32L33 12L42 28Z" fill="' + dark + '"/><path d="M73 32L67 12L58 28Z" fill="' + dark + '"/>'
            '<ellipse cx="22" cy="64" rx="9" ry="19" fill="' + wing + '" transform="rotate(12 22 64)"/>'
            '<ellipse cx="78" cy="64" rx="9" ry="19" fill="' + wing + '" transform="rotate(-12 78 64)"/>'
            '<path d="M50 20C28 20 21 42 21 60C21 80 34 92 50 92S79 80 79 60C79 42 72 20 50 20Z" fill="' + mid + '"/>'
            '<path d="M50 50C36 50 32 62 32 72C32 84 40 90 50 90S68 84 68 72C68 62 64 50 50 50Z" fill="#F3E6D0"/>'
            '<path d="M41 64q2.5 3.5 5 0M52 64q2.5 3.5 5 0M46 72q2.5 3.5 5 0M40 80q2.5 3.5 5 0M55 80q2.5 3.5 5 0" stroke="#D9C3A0" stroke-width="1.8" fill="none" stroke-linecap="round"/>'
            '<path d="M30 40C30 30 40 27 50 33C60 27 70 30 70 40C70 50 60 53 50 49C40 53 30 50 30 40Z" fill="#B7A2EE"/>')


_GLASSES = ('<circle cx="40" cy="40" r="10.5" fill="none" stroke="#2B2140" stroke-width="2.6"/>'
            '<circle cx="60" cy="40" r="10.5" fill="none" stroke="#2B2140" stroke-width="2.6"/>'
            '<path d="M49.5 39Q50 37 50.5 39" stroke="#2B2140" stroke-width="2.6" fill="none"/>')
_BEAK = '<path d="M46 47L54 47L50 53.5Z" fill="#F5A524"/>'
_FEET = '<path d="M42 91l-3 3M42 91v4M42 91l3 3M58 91l-3 3M58 91v4M58 91l3 3" stroke="#F5A524" stroke-width="2.6" stroke-linecap="round"/>'
_BOOK = ('<g transform="rotate(-8 50 80)"><rect x="33" y="72" width="34" height="18" rx="2" fill="#D6455D"/>'
         '<rect x="35" y="74" width="30" height="14" rx="1" fill="#FFF6E8"/><path d="M50 74v14" stroke="#D6455D" stroke-width="1.6"/>'
         '<path d="M38 78h9M38 82h7M53 78h9M53 82h7" stroke="#C9B9A0" stroke-width="1.2"/></g>'
         '<ellipse cx="34" cy="80" rx="5" ry="6" fill="#6A4DBF"/><ellipse cx="66" cy="80" rx="5" ry="6" fill="#6A4DBF"/>')

STUDENT = (f'<svg {_S}>' + _SHADOW.format(w=28) + _owl_body() + _eyes(40, 60, 40, 8) + _GLASSES + _BEAK + _FEET + _BOOK + '</svg>')

SAGE = (f'<svg {_S}>'
        '<defs><radialGradient id="pfAura" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#FFE9A6" stop-opacity=".95"/>'
        '<stop offset=".6" stop-color="#C9B6FF" stop-opacity=".35"/><stop offset="1" stop-color="#C9B6FF" stop-opacity="0"/></radialGradient></defs>'
        '<circle cx="50" cy="54" r="50" fill="url(#pfAura)"/>' + _SHADOW.format(w=28)
        + _owl_body(dark="#5E3FB8", mid="#6D4FC2", wing="#57389F") + _eyes(40, 40 + 20, 40, 8) + _GLASSES + _BEAK + _FEET + _BOOK +
        '<path d="M22 20L50 9L78 20L50 31Z" fill="#2B2140"/><path d="M36 25V33Q50 40 64 33V25L50 31Z" fill="#3A2D57"/>'
        '<path d="M70 19V33" stroke="#FFC83A" stroke-width="2.2"/><circle cx="70" cy="35" r="3" fill="#FFC83A"/>'
        + _star(10, 58, 3.4) + _star(90, 50, 3) + _star(84, 84, 2.4, "#FFE9A6") + _star(14, 86, 2.2, "#FFE9A6") + '</svg>')

CHOUETTE_STAGES = [(EGG, "Œuf enchanté"), (HATCH, "Éclosion"), (OWLET, "Chouetton"),
                   (STUDENT, "Chouette étudiante"), (SAGE, "Grande sage")]
CHOUETTE_LEVELS = [1, 3, 6, 10, 15]


# ═════════════════════════════════════════════ outils communs
def eyes(lx, rx, y, r, iris=None, look=.15):
    out = f'<circle cx="{lx}" cy="{y}" r="{r}" fill="#fff"/><circle cx="{rx}" cy="{y}" r="{r}" fill="#fff"/>'
    if iris:
        out += (f'<circle cx="{lx + r * look}" cy="{y + r * .08}" r="{r * .68}" fill="{iris}"/>'
                f'<circle cx="{rx + r * look}" cy="{y + r * .08}" r="{r * .68}" fill="{iris}"/>')
    p = r * (.38 if iris else .5)
    out += (f'<circle cx="{lx + r * look}" cy="{y + r * .1}" r="{p}" fill="#1E1830"/>'
            f'<circle cx="{rx + r * look}" cy="{y + r * .1}" r="{p}" fill="#1E1830"/>'
            f'<circle cx="{lx + r * .38}" cy="{y - r * .28}" r="{r * .21}" fill="#fff"/>'
            f'<circle cx="{rx + r * .38}" cy="{y - r * .28}" r="{r * .21}" fill="#fff"/>')
    return out


def shadow(w=26):
    return f'<ellipse cx="50" cy="94" rx="{w}" ry="4.5" fill="#000" opacity=".13"/>'


def svg(inner, defs=""):
    return f'<svg {_S}>' + (f"<defs>{defs}</defs>" if defs else "") + inner + '</svg>'


def aura(idc, c1, c2):
    return (f'<radialGradient id="{idc}" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="{c1}" stop-opacity=".95"/>'
            f'<stop offset=".6" stop-color="{c2}" stop-opacity=".35"/><stop offset="1" stop-color="{c2}" stop-opacity="0"/></radialGradient>')


def egg(fill, stroke, spots):
    return ('<path d="M50 10C31 10 20 40 20 61C20 81 34 93 50 93S80 81 80 61C80 40 69 10 50 10Z" fill="'
            + fill + '" stroke="' + stroke + '" stroke-width="2.2"/>' + spots +
            '<path d="M32 33Q35 23 42 19" stroke="#fff" stroke-width="4.5" stroke-linecap="round" fill="none" opacity=".8"/>')


def shell_bottom(fill, stroke):
    return ('<path d="M19 62L27 55L33 62L40 55L47 63L54 55L61 62L68 55L75 62L81 58C81 81 67 93 50 93S19 82 19 62Z" fill="'
            + fill + '" stroke="' + stroke + '" stroke-width="2.2"/>')


def shell_top(fill, stroke):
    return ('<g transform="rotate(-14 48 24)"><path d="M28 34L34 27L40 33L46 25L52 32L58 25L64 31L71 26C67 14 59 9 50 9C39 9 31 19 28 34Z" fill="'
            + fill + '" stroke="' + stroke + '" stroke-width="2.2"/></g>')


# ═════════════════════════════════════════════ HIBOU (brun, yeux orange)
HB, HD, HW, HL, HF, HI = "#8C5A3C", "#6B412B", "#734832", "#F2DEC1", "#B98563", "#F59F00"
_hspots = ''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#A8784F"/>' for x, y, r in
                  [(36, 40, 3), (60, 32, 2.4), (65, 55, 3.4), (44, 62, 2.6), (55, 76, 3), (33, 72, 2.2), (68, 72, 2)])


def _hibou_body(scale=""):
    return ('<path d="M27 34L32 14L42 29Z" fill="' + HD + '"/><path d="M73 34L68 14L58 29Z" fill="' + HD + '"/>'
            '<ellipse cx="22" cy="63" rx="9" ry="19" fill="' + HW + '" transform="rotate(12 22 63)"/>'
            '<ellipse cx="78" cy="63" rx="9" ry="19" fill="' + HW + '" transform="rotate(-12 78 63)"/>'
            '<path d="M50 20C28 20 21 42 21 60C21 80 34 91 50 91S79 80 79 60C79 42 72 20 50 20Z" fill="' + HB + '"/>'
            '<path d="M50 50C36 50 32 62 32 72C32 84 40 90 50 90S68 84 68 72C68 62 64 50 50 50Z" fill="' + HL + '"/>'
            '<path d="M40 63l3 3 3-3M48 67l3 3 3-3M56 63l3 3 3-3M43 74l3 3 3-3M53 74l3 3 3-3M48 81l3 3 3-3" stroke="#C49A6C" stroke-width="1.8" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
            '<path d="M29 41C29 30 40 27 50 33C60 27 71 30 71 41C71 51 60 54 50 50C40 54 29 51 29 41Z" fill="' + HF + '"/>'
            + eyes(40, 60, 41, 8.5, HI) + '<path d="M46 48L54 48L50 55Z" fill="#E8890C"/>')


HIBOU_STAGES = [
    (svg(shadow(24) + egg("#EAD5B2", "#C8A77A", _hspots) + _star(82, 22, 3)), "Œuf moucheté"),
    (svg(shadow(26) + f'<circle cx="50" cy="50" r="23" fill="{HB}"/>'
         f'<path d="M34 34L37 22L45 31ZM66 34L63 22L55 31Z" fill="{HD}"/>'
         + eyes(41, 59, 46, 8, HI) + '<path d="M46.5 53L53.5 53L50 58Z" fill="#E8890C"/>'
         + shell_top("#EAD5B2", "#C8A77A") + shell_bottom("#EAD5B2", "#C8A77A")
         + '<circle cx="35" cy="76" r="3" fill="#A8784F"/><circle cx="62" cy="80" r="3.6" fill="#A8784F"/>'
         + _star(85, 32, 2.8)), "Éclosion"),
    (svg(shadow(27) + f'<path d="M40 36Q43 22 48 33Q50 20 52 33Q57 22 60 36Z" fill="{HB}"/>'
         f'<ellipse cx="22" cy="67" rx="8" ry="13" fill="{HW}" transform="rotate(18 22 67)"/>'
         f'<ellipse cx="78" cy="67" rx="8" ry="13" fill="{HW}" transform="rotate(-18 78 67)"/>'
         f'<circle cx="50" cy="62" r="30" fill="{HB}"/><ellipse cx="50" cy="72" rx="18" ry="17" fill="{HL}"/>'
         f'<ellipse cx="39" cy="54" rx="12.5" ry="12" fill="{HF}"/><ellipse cx="61" cy="54" rx="12.5" ry="12" fill="{HF}"/>'
         + eyes(39, 61, 54, 9, HI) + '<path d="M46 62L54 62L50 68Z" fill="#E8890C"/>'
         '<path d="M40 91l-3 3M40 91v4M40 91l3 3M60 91l-3 3M60 91v4M60 91l3 3" stroke="#E8890C" stroke-width="2.6" stroke-linecap="round"/>'),
     "Hiboudon"),
    (svg(shadow(30) + _hibou_body() +
         '<path d="M8 91Q50 84 92 91" stroke="#7A5230" stroke-width="7" stroke-linecap="round" fill="none"/>'
         '<path d="M84 88q8-8 12-2q-6 6-12 2z" fill="#5FA84E"/>'
         '<path d="M42 87l-3 5M45 87v6M58 87l3 5M55 87v6" stroke="#E8890C" stroke-width="2.6" stroke-linecap="round"/>'),
     "Hibou des bois"),
    (svg(f'<circle cx="50" cy="50" r="49" fill="#1D2450"/><circle cx="50" cy="50" r="49" fill="url(#pfNight)"/>'
         '<path d="M78 14a13 13 0 1 0 8 23a10 10 0 1 1-8-23z" fill="#FFE08A"/>'
         + _star(18, 20, 2.4, "#fff") + _star(30, 10, 1.6, "#fff") + _star(90, 60, 1.8, "#fff")
         + _hibou_body() +
         '<path d="M8 91Q50 84 92 91" stroke="#7A5230" stroke-width="7" stroke-linecap="round" fill="none"/>'
         '<path d="M42 87l-3 5M45 87v6M58 87l3 5M55 87v6" stroke="#E8890C" stroke-width="2.6" stroke-linecap="round"/>'
         '<circle cx="40" cy="41" r="11" fill="none" stroke="#FFD65A" stroke-width="1.4" opacity=".7"/>'
         '<circle cx="60" cy="41" r="11" fill="none" stroke="#FFD65A" stroke-width="1.4" opacity=".7"/>',
         aura("pfNight", "#4B5BB5", "#1D2450")), "Grand-duc de minuit"),
]

# ═════════════════════════════════════════════ PLANTE (pot avec visage)
POT, POTD, LEAF, LEAFD = "#E07A4F", "#C4623A", "#6CC56A", "#4DA553"


def _pot(big=False):
    w = 30 if big else 24
    return (f'<path d="M{50 - w} 62H{50 + w}L{50 + w - 6} 91H{50 - w + 6}Z" fill="{POT}"/>'
            f'<rect x="{50 - w - 3}" y="57" width="{2 * w + 6}" height="9" rx="3" fill="{POTD}"/>'
            '<ellipse cx="42" cy="76" rx="2.6" ry="3.4" fill="#3A2320"/><ellipse cx="58" cy="76" rx="2.6" ry="3.4" fill="#3A2320"/>'
            '<circle cx="42.8" cy="74.8" r=".9" fill="#fff"/><circle cx="58.8" cy="74.8" r=".9" fill="#fff"/>'
            '<path d="M46 82q4 3.5 8 0" stroke="#3A2320" stroke-width="1.8" fill="none" stroke-linecap="round"/>'
            '<ellipse cx="36" cy="81" rx="3.4" ry="2" fill="#FF9EC0" opacity=".75"/><ellipse cx="64" cy="81" rx="3.4" ry="2" fill="#FF9EC0" opacity=".75"/>')


def _leaf(x, y, rot, s=1.0, c=LEAF):
    return (f'<g transform="translate({x} {y}) rotate({rot}) scale({s})"><path d="M0 0C6-10 18-12 24-8C18 2 8 5 0 0Z" fill="{c}"/>'
            f'<path d="M2 -1C9-5 15-7 21-7" stroke="{LEAFD}" stroke-width="1.2" fill="none"/></g>')


def _flower(x, y, c="#FF8FB8"):
    petals = "".join(f'<ellipse cx="{x}" cy="{y - 5}" rx="3.4" ry="5" fill="{c}" transform="rotate({a} {x} {y})"/>' for a in range(0, 360, 72))
    return petals + f'<circle cx="{x}" cy="{y}" r="3" fill="#FFD43B"/>'


PLANTE_STAGES = [
    (svg(shadow(28) + '<ellipse cx="50" cy="84" rx="32" ry="10" fill="#8A5A3B"/><ellipse cx="50" cy="81" rx="28" ry="7" fill="#A06B45"/>'
         '<path d="M50 42V30" stroke="#4DA553" stroke-width="2.6" stroke-linecap="round"/>'
         '<path d="M50 33C44 26 37 27 35 30C40 35 46 35 50 33Z" fill="#6CC56A"/><path d="M50 31C56 23 64 24 66 27C61 33 55 33 50 31Z" fill="#7ED67A"/>'
         '<ellipse cx="50" cy="60" rx="22" ry="19" fill="#E3B373" stroke="#B07A3C" stroke-width="2.4"/>'
         '<path d="M36 52Q40 45 47 43" stroke="#F4D3A0" stroke-width="3.2" stroke-linecap="round" fill="none"/>'
         '<path d="M40 60q3 3 6 0M54 60q3 3 6 0" stroke="#3A2320" stroke-width="2" fill="none" stroke-linecap="round"/>'
         '<path d="M47 67q3 2 6 0" stroke="#3A2320" stroke-width="1.6" fill="none" stroke-linecap="round"/>'
         '<ellipse cx="37" cy="66" rx="3.4" ry="2" fill="#FF9EC0" opacity=".75"/><ellipse cx="63" cy="66" rx="3.4" ry="2" fill="#FF9EC0" opacity=".75"/>'
         '<text x="70" y="30" font-size="10" font-family="system-ui" fill="#8A7BB8" font-weight="700">z</text>'
         '<text x="78" y="21" font-size="7" font-family="system-ui" fill="#8A7BB8" font-weight="700">z</text>'
         + _star(22, 30, 2.4)), "Graine endormie"),
    (svg(shadow(24) + '<path d="M50 58V44" stroke="' + LEAFD + '" stroke-width="3" stroke-linecap="round"/>'
         + _leaf(50, 46, -150, .8) + _leaf(50, 44, -30, .85) + _pot()), "Pousse"),
    (svg(shadow(26) + '<path d="M50 58C50 44 48 34 50 22" stroke="' + LEAFD + '" stroke-width="3.2" fill="none" stroke-linecap="round"/>'
         + _leaf(50, 50, -160, 1) + _leaf(50, 46, -20, 1.05) + _leaf(49, 34, -145, .9) + _leaf(50, 30, -35, .9)
         + _leaf(50, 23, -95, .6) + _pot()), "Jeune plante"),
    (svg(shadow(28) + '<path d="M50 58C50 44 47 32 42 20M50 58C50 44 53 32 60 18M50 58V28" stroke="' + LEAFD + '" stroke-width="3" fill="none" stroke-linecap="round"/>'
         + _leaf(50, 50, -160, 1.1) + _leaf(50, 47, -20, 1.1) + _leaf(46, 36, -150, .85) + _leaf(54, 34, -30, .85)
         + _flower(42, 20) + _flower(60, 18, "#FFB86B") + _flower(50, 27, "#C9A7FF") + _pot()), "Plante en fleurs"),
    (svg('<circle cx="50" cy="40" r="46" fill="url(#pfTree)"/>' + shadow(32) +
         '<path d="M46 60C47 48 44 42 40 36M54 60C53 48 57 42 62 36M48 60V34M52 60V34" stroke="#8A5A30" stroke-width="5" fill="none" stroke-linecap="round"/>'
         '<circle cx="50" cy="28" r="20" fill="' + LEAFD + '"/><circle cx="32" cy="34" r="14" fill="' + LEAF + '"/>'
         '<circle cx="68" cy="34" r="14" fill="' + LEAF + '"/><circle cx="50" cy="20" r="15" fill="#7ED67A"/>'
         '<circle cx="38" cy="22" r="10" fill="#7ED67A"/><circle cx="62" cy="22" r="10" fill="#7ED67A"/>'
         + _flower(36, 26) + _flower(60, 16, "#FFB86B") + _flower(66, 36) + _flower(46, 12, "#C9A7FF") + _flower(28, 38, "#FFB86B")
         + '<circle cx="54" cy="34" r="3.2" fill="#E8412F"/><circle cx="40" cy="38" r="3" fill="#E8412F"/>'
         + _pot(big=True) + _star(10, 60, 2.8) + _star(90, 56, 2.6), aura("pfTree", "#FFF3B0", "#B8F0A8")), "Arbre ancien"),
]

# ═════════════════════════════════════════════ CHAT (tigré orange, yeux verts)
CO, CD, CL, CI = "#F4A259", "#D9822B", "#FFF1DC", "#58B368"


def _cat_head(cx, cy, r, iris=CI):
    return (f'<path d="M{cx - r * .95} {cy - r * .2}L{cx - r * .8} {cy - r * 1.15}L{cx - r * .25} {cy - r * .8}Z" fill="{CO}"/>'
            f'<path d="M{cx + r * .95} {cy - r * .2}L{cx + r * .8} {cy - r * 1.15}L{cx + r * .25} {cy - r * .8}Z" fill="{CO}"/>'
            f'<path d="M{cx - r * .78} {cy - r * .45}L{cx - r * .72} {cy - r * .95}L{cx - r * .4} {cy - r * .75}Z" fill="#FFB3C6"/>'
            f'<path d="M{cx + r * .78} {cy - r * .45}L{cx + r * .72} {cy - r * .95}L{cx + r * .4} {cy - r * .75}Z" fill="#FFB3C6"/>'
            f'<ellipse cx="{cx}" cy="{cy}" rx="{r}" ry="{r * .88}" fill="{CO}"/>'
            f'<path d="M{cx - 5} {cy - r * .86}l2 {r * .3}M{cx} {cy - r * .88}v{r * .32}M{cx + 5} {cy - r * .86}l-2 {r * .3}" stroke="{CD}" stroke-width="2.2" stroke-linecap="round"/>'
            f'<ellipse cx="{cx}" cy="{cy + r * .35}" rx="{r * .55}" ry="{r * .4}" fill="{CL}"/>'
            + eyes(cx - r * .38, cx + r * .38, cy - r * .05, r * .27, iris, look=.05) +
            f'<path d="M{cx - 2.5} {cy + r * .25}h5l-2.5 3z" fill="#FF7FA0"/>'
            f'<path d="M{cx} {cy + r * .25 + 3}q-3 4-6 1M{cx} {cy + r * .25 + 3}q3 4 6 1" stroke="#7A4A2A" stroke-width="1.4" fill="none" stroke-linecap="round"/>'
            f'<path d="M{cx - r * .55} {cy + r * .3}h-{r * .45}M{cx - r * .55} {cy + r * .42}l-{r * .42} {r * .12}M{cx + r * .55} {cy + r * .3}h{r * .45}M{cx + r * .55} {cy + r * .42}l{r * .42} {r * .12}" stroke="#fff" stroke-width="1.2" stroke-linecap="round" opacity=".9"/>')


CHAT_STAGES = [
    (svg(shadow(30) + f'<path d="M31 42L34 24L44 35ZM69 42L66 24L56 35Z" fill="{CO}"/>'
         '<path d="M34 40L35 29L41 35ZM66 40L65 29L59 35Z" fill="#FFB3C6"/>'
         f'<ellipse cx="50" cy="48" rx="21" ry="17" fill="{CO}"/>'
         f'<path d="M45 33l1 5M50 32v5M55 33l-1 5" stroke="{CD}" stroke-width="2.2" stroke-linecap="round"/>'
         f'<ellipse cx="50" cy="55" rx="11" ry="7" fill="{CL}"/>'
         '<path d="M38 47q3.5 3 7 0M55 47q3.5 3 7 0" stroke="#7A4A2A" stroke-width="2" fill="none" stroke-linecap="round"/>'
         '<path d="M48 52h4l-2 2.4z" fill="#FF7FA0"/>'
         '<ellipse cx="36" cy="53" rx="3.4" ry="2" fill="#FF9EC0" opacity=".7"/><ellipse cx="64" cy="53" rx="3.4" ry="2" fill="#FF9EC0" opacity=".7"/>'
         '<path d="M18 58H82L76 90H24Z" fill="#C88A4A"/><path d="M18 58H82" stroke="#A8702F" stroke-width="6" stroke-linecap="round"/>'
         '<path d="M26 66H74M28 74H72M30 82H70" stroke="#A8702F" stroke-width="2" opacity=".6"/>'
         '<path d="M34 60v28M44 60v30M56 60v30M66 60v28" stroke="#A8702F" stroke-width="2" opacity=".45"/>'
         '<text x="76" y="30" font-size="11" font-family="system-ui" fill="#8A7BB8" font-weight="700">z</text>'
         '<text x="84" y="20" font-size="8" font-family="system-ui" fill="#8A7BB8" font-weight="700">z</text>'), "Chaton au panier"),
    (svg(shadow(22) + f'<ellipse cx="50" cy="80" rx="16" ry="13" fill="{CO}"/><ellipse cx="50" cy="83" rx="9" ry="8" fill="{CL}"/>'
         f'<path d="M64 84q14 2 12-14" stroke="{CO}" stroke-width="6" fill="none" stroke-linecap="round"/>'
         '<ellipse cx="42" cy="92" rx="5" ry="3" fill="#FFF1DC"/><ellipse cx="58" cy="92" rx="5" ry="3" fill="#FFF1DC"/>'
         + _cat_head(50, 50, 24)), "Chaton"),
    (svg(shadow(26) + f'<path d="M66 86q22-2 16-28q-2-8 4-10" stroke="{CO}" stroke-width="7" fill="none" stroke-linecap="round"/>'
         f'<path d="M78 66l5 2M80 58l5 1" stroke="{CD}" stroke-width="2.4" stroke-linecap="round"/>'
         f'<path d="M50 50C34 50 30 66 30 78C30 88 38 92 50 92S70 88 70 78C70 66 66 50 50 50Z" fill="{CO}"/>'
         f'<ellipse cx="50" cy="78" rx="11" ry="13" fill="{CL}"/>'
         f'<path d="M33 66l6 2M32 74l6 1M67 66l-6 2M68 74l-6 1" stroke="{CD}" stroke-width="2.4" stroke-linecap="round"/>'
         '<ellipse cx="41" cy="92" rx="6" ry="3.2" fill="#FFF1DC"/><ellipse cx="59" cy="92" rx="6" ry="3.2" fill="#FFF1DC"/>'
         + _cat_head(50, 38, 21)), "Chat agile"),
    (svg(shadow(28) + f'<path d="M66 86q22-2 16-28q-2-8 4-10" stroke="{CO}" stroke-width="7" fill="none" stroke-linecap="round"/>'
         f'<path d="M50 50C34 50 30 66 30 78C30 88 38 92 50 92S70 88 70 78C70 66 66 50 50 50Z" fill="{CO}"/>'
         f'<ellipse cx="50" cy="78" rx="11" ry="13" fill="{CL}"/>'
         '<ellipse cx="41" cy="92" rx="6" ry="3.2" fill="#FFF1DC"/><ellipse cx="59" cy="92" rx="6" ry="3.2" fill="#FFF1DC"/>'
         '<path d="M31 54Q50 64 69 54L70 60Q50 70 30 60Z" fill="#D6455D"/><path d="M60 60l4 16 6-3-4-14Z" fill="#C23A51"/>'
         '<path d="M36 57l3 4M44 60l2 4M54 60l-1 4M62 58l-2 4" stroke="#fff" stroke-width="1.4" opacity=".6"/>'
         + _cat_head(50, 38, 21)
         + '<path d="M22 20L50 9L78 20L50 31Z" fill="#2B2140" transform="translate(0 -2) scale(1)" opacity="0"/>'), "Chat aventurier"),
    (svg('<circle cx="50" cy="50" r="47" fill="url(#pfLion)"/>' + shadow(30)
         + "".join(f'<ellipse cx="50" cy="20" rx="9" ry="15" fill="{c}" transform="rotate({a} 50 47)"/>'
                   for a, c in [(i * 30, "#C8661E" if i % 2 else "#E07F2A") for i in range(12)])
         + f'<circle cx="50" cy="47" r="24" fill="#F0A24A"/>'
         + f'<ellipse cx="50" cy="56" rx="13" ry="9" fill="{CL}"/>'
         + eyes(41, 59, 44, 6.2, "#E8A400", look=.05) +
         '<path d="M46 52h8l-4 4.5z" fill="#6B3A1E"/><path d="M50 56.5q-4 5-8 2M50 56.5q4 5 8 2" stroke="#6B3A1E" stroke-width="1.6" fill="none" stroke-linecap="round"/>'
         '<path d="M30 30l-2-8 8 5ZM70 30l2-8-8 5Z" fill="#F0A24A"/>'
         '<path d="M36 18L40 8L46 15L50 5L54 15L60 8L64 18Z" fill="#FFD43B" stroke="#E0A100" stroke-width="1.4"/>'
         '<circle cx="50" cy="12" r="2" fill="#E8412F"/>'
         '<ellipse cx="38" cy="86" rx="9" ry="7" fill="#F0A24A"/><ellipse cx="62" cy="86" rx="9" ry="7" fill="#F0A24A"/>'
         '<path d="M35 88v3M38 88v4M41 88v3M59 88v3M62 88v4M65 88v3" stroke="#C8661E" stroke-width="1.6" stroke-linecap="round"/>'
         + _star(12, 20, 2.6) + _star(88, 26, 2.4), aura("pfLion", "#FFE9A6", "#FFC56B")), "Roi lion"),
]

# ═════════════════════════════════════════════ DRAGON (vert, ventre doré)
DG, DGD, DB, DH, DWG = "#4CB782", "#37956A", "#F6E3A1", "#F2C86B", "#2F8A5F"
_dscales = ('<path d="M30 40q5 5 10 0q5 5 10 0q5 5 10 0q5 5 10 0M25 58q5 5 10 0q5 5 10 0q5 5 10 0q5 5 10 0q5 5 10 0M30 76q5 5 10 0q5 5 10 0q5 5 10 0q5 5 10 0" '
            'stroke="#3E9E6E" stroke-width="2" fill="none" opacity=".7"/>')


def _dhead(cx, cy, r):
    return (f'<path d="M{cx - r * .6} {cy - r * .7}L{cx - r * .75} {cy - r * 1.35}L{cx - r * .2} {cy - r * .85}Z" fill="{DH}"/>'
            f'<path d="M{cx + r * .6} {cy - r * .7}L{cx + r * .75} {cy - r * 1.35}L{cx + r * .2} {cy - r * .85}Z" fill="{DH}"/>'
            f'<ellipse cx="{cx}" cy="{cy}" rx="{r}" ry="{r * .9}" fill="{DG}"/>'
            f'<ellipse cx="{cx}" cy="{cy + r * .45}" rx="{r * .62}" ry="{r * .38}" fill="#6CCB98"/>'
            f'<circle cx="{cx - r * .22}" cy="{cy + r * .4}" r="1.6" fill="#2A6B4A"/><circle cx="{cx + r * .22}" cy="{cy + r * .4}" r="1.6" fill="#2A6B4A"/>'
            + eyes(cx - r * .4, cx + r * .4, cy - r * .12, r * .27, "#F5A524", look=.05))


def _dbody(wings=1.0, big=False):
    s = 1.12 if big else 1.0
    return (f'<g transform="translate(50 60) scale({s}) translate(-50 -60)">'
            f'<path d="M50 52C32 40 14 30 8 18C22 22 30 30 34 36C30 26 32 16 38 10C40 24 44 34 50 42Z" fill="{DWG}" transform="translate(50 50) scale({wings}) translate(-50 -50)"/>'
            f'<path d="M50 52C68 40 86 30 92 18C78 22 70 30 66 36C70 26 68 16 62 10C60 24 56 34 50 42Z" fill="{DWG}" transform="translate(50 50) scale({wings}) translate(-50 -50)"/>'
            f'<path d="M66 82q22 6 24-12q-8 6-12 2" stroke="{DG}" stroke-width="7" fill="none" stroke-linecap="round"/><path d="M88 66l6-4-1 8Z" fill="{DH}"/>'
            f'<path d="M50 44C33 44 29 62 29 74C29 86 38 92 50 92S71 86 71 74C71 62 67 44 50 44Z" fill="{DG}"/>'
            f'<path d="M50 54C41 54 39 64 39 74C39 84 44 90 50 90S61 84 61 74C61 64 59 54 50 54Z" fill="{DB}"/>'
            '<path d="M41 62h18M40 70h20M40 78h20M42 86h16" stroke="#E0C77A" stroke-width="1.6"/>'
            '<ellipse cx="40" cy="92" rx="7" ry="3.4" fill="#37956A"/><ellipse cx="60" cy="92" rx="7" ry="3.4" fill="#37956A"/></g>')


DRAGON_STAGES = [
    (svg(shadow(24) + egg("#7FD3A5", "#3E9E6E", _dscales) + '<path d="M50 10l4 7h-8z" fill="#F2C86B"/>' + _star(84, 24, 3)),
     "Œuf de dragon"),
    (svg(shadow(26) + _dhead(50, 50, 23) + shell_top("#7FD3A5", "#3E9E6E") + shell_bottom("#7FD3A5", "#3E9E6E")
         + '<path d="M28 74q5 5 10 0q5 5 10 0q5 5 10 0q5 5 10 0" stroke="#3E9E6E" stroke-width="2" fill="none" opacity=".7"/>'
         + _star(86, 34, 2.8)), "Éclosion"),
    (svg(shadow(26) + _dbody(wings=.55) + _dhead(50, 40, 20)), "Dragonnet"),
    (svg(shadow(30) + _dbody(wings=1.0) + _dhead(50, 38, 20)
         + '<path d="M44 20l3-6 3 6 3-6 3 6" stroke="#2F8A5F" stroke-width="2.4" fill="none" stroke-linejoin="round"/>'), "Dragon"),
    (svg('<circle cx="50" cy="50" r="48" fill="url(#pfDrag)"/>' + shadow(32) + _dbody(wings=1.12, big=True) + _dhead(50, 36, 20)
         + '<path d="M36 17L40 7L45 14L50 4L55 14L60 7L64 17Z" fill="#FFD43B" stroke="#E0A100" stroke-width="1.4"/>'
         '<circle cx="50" cy="11" r="2" fill="#4DABF7"/>'
         '<path d="M68 44q10-2 16 4q-4 2-2 6q-6-2-8 2q-2-6-6-6z" fill="#FF922B"/><path d="M72 46q6 0 9 3q-3 1-2 4q-4-2-5 1q-1-4-4-5z" fill="#FFD43B"/>'
         + _star(10, 30, 2.8) + _star(90, 84, 2.4), aura("pfDrag", "#FFE9A6", "#8CE0B5")), "Dragon ancestral"),
]

MASCOT_LEVELS = [1, 3, 6, 10, 15]

# ═════════════════════════════════════════════ pièce de monnaie
COIN = ('<svg style="width:1em;height:1em;vertical-align:-.15em;overflow:visible" viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg">'
        '<defs><linearGradient id="pfCoinA" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFF1A8"/>'
        '<stop offset=".45" stop-color="#FFC93C"/><stop offset="1" stop-color="#D48A00"/></linearGradient>'
        '<linearGradient id="pfCoinB" x1="1" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#FFE27A"/>'
        '<stop offset="1" stop-color="#C77D00"/></linearGradient></defs>'
        '<circle cx="20" cy="21.5" r="17" fill="#A86500"/>'
        '<circle cx="20" cy="20" r="17" fill="url(#pfCoinA)"/>'
        '<circle cx="20" cy="20" r="12.5" fill="url(#pfCoinB)" stroke="#B87400" stroke-width="1.2"/>'
        '<path d="M20 11.5l2.6 5.4 5.9.8-4.3 4.1 1 5.8L20 24.8l-5.2 2.8 1-5.8-4.3-4.1 5.9-.8z" fill="#FFF3C4" stroke="#C98500" stroke-width="1"/>'
        '<path d="M9 13a13 13 0 0 1 8-6" stroke="#fff" stroke-width="2.2" stroke-linecap="round" fill="none" opacity=".8"/>'
        '</svg>')


# ═════════════════════════════════════════════ coffre de série
_CHEST_BASE = ('<path d="M14 50H86V86Q86 90 82 90H18Q14 90 14 86Z" fill="#9C5B2E"/>'
               '<path d="M14 58H86M14 74H86" stroke="#7A4220" stroke-width="2.4"/>'
               '<rect x="12" y="48" width="8" height="44" rx="2" fill="#F2B93B"/><rect x="80" y="48" width="8" height="44" rx="2" fill="#F2B93B"/>'
               '<rect x="44" y="46" width="12" height="44" fill="#F2B93B"/>'
               '<rect x="41" y="54" width="18" height="16" rx="3" fill="#E0A100" stroke="#B87400" stroke-width="1.6"/>'
               '<circle cx="50" cy="60" r="2.6" fill="#5A3A00"/><path d="M50 61v5" stroke="#5A3A00" stroke-width="2.2" stroke-linecap="round"/>')
CHEST = ('<svg style="width:1.15em;height:1.15em;overflow:visible" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">'
         '<ellipse cx="50" cy="94" rx="40" ry="5" fill="#000" opacity=".15"/>' + _CHEST_BASE +
         '<path d="M14 50V36Q14 18 50 18Q86 18 86 36V50Z" fill="#B36A35"/>'
         '<path d="M14 36Q14 18 50 18Q86 18 86 36" stroke="#7A4220" stroke-width="2.4" fill="none"/>'
         '<path d="M12 50V34Q12 16 20 14V50Z" fill="#F2B93B"/><path d="M88 50V34Q88 16 80 14V50Z" fill="#F2B93B"/>'
         '<path d="M44 19H56V50H44Z" fill="#F2B93B"/><path d="M10 48H90V54H10Z" fill="#E0A100"/></svg>')
CHEST_OPEN = ('<svg style="width:1.15em;height:1.15em;overflow:visible" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">'
              '<ellipse cx="50" cy="94" rx="40" ry="5" fill="#000" opacity=".15"/>'
              '<path d="M14 40Q14 8 50 6Q86 8 86 40L86 46H14Z" fill="#8A4F25"/>'
              '<path d="M12 46V36Q12 10 20 8V46ZM88 46V36Q88 10 80 8V46ZM44 7H56V46H44Z" fill="#F2B93B"/>'
              '<ellipse cx="50" cy="50" rx="36" ry="8" fill="#FFE27A"/><ellipse cx="50" cy="50" rx="30" ry="5" fill="#FFF3C4"/>'
              + _CHEST_BASE + '</svg>')

# ═════════════════════════════════════════════ Halloween
WITCH_HAT = ('<svg style="width:1.15em;height:1.15em;overflow:visible" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">'
             '<ellipse cx="50" cy="80" rx="46" ry="12" fill="#3B2458"/>'
             '<path d="M22 78C30 60 38 30 46 12Q52 4 60 10L70 22Q62 20 58 26C60 44 70 62 78 78Z" fill="#4E2D75"/>'
             '<path d="M26 70Q50 80 74 70L78 78Q50 90 22 78Z" fill="#FF8C1A"/>'
             '<rect x="43" y="70" width="14" height="11" rx="2" fill="none" stroke="#FFD43B" stroke-width="3"/>'
             '<path d="M36 44Q40 40 44 44" stroke="#7A52AD" stroke-width="2" fill="none"/>'
             '<path d="M64 8l2 4 4 1-4 2-2 4-2-4-4-2 4-1z" fill="#FFD43B"/></svg>')

_bats = "".join(
    f'<path transform="translate({x} {y}) scale({s})" d="M0 0q6-8 12-2q4-6 6 0q2-6 6 0q6-6 12 2q-8-2-12 4q-2-3-6-1q-4-2-6 1q-4-6-12-4z" fill="#140a22"/>'
    for x, y, s in [(40, 60, 1.1), (250, 40, .8), (320, 150, 1.3), (120, 200, .9), (360, 250, .7), (60, 260, .6)])
HAUNTED_SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" width="420" height="320" viewBox="0 0 420 320">' + _bats +
    '<circle cx="190" cy="120" r="1.6" fill="#fff" opacity=".7"/><circle cx="30" cy="150" r="1.2" fill="#fff" opacity=".6"/>'
    '<circle cx="400" cy="90" r="1.4" fill="#fff" opacity=".7"/><circle cx="280" cy="290" r="1.2" fill="#fff" opacity=".5"/></svg>')


# ═════════════════════════════════════════════ boss de révision
SLIME = svg(shadow(34) +
    '<path d="M50 22C70 22 84 44 86 66C88 84 76 90 50 90S12 84 14 66C16 44 30 22 50 22Z" fill="#7BD56B"/>'
    '<path d="M50 22C70 22 84 44 86 66C88 84 76 90 50 90" fill="none" stroke="#56B04A" stroke-width="3"/>'
    '<ellipse cx="36" cy="40" rx="7" ry="4" fill="#fff" opacity=".55" transform="rotate(-30 36 40)"/>'
    '<path d="M31 56q7-4 14 0M55 56q7-4 14 0" stroke="#1E1830" stroke-width="3" fill="none" stroke-linecap="round"/>'
    '<path d="M31 56q7 5 14 0M55 56q7 5 14 0" fill="#1E1830" opacity=".8"/>'
    '<path d="M40 70q10 6 20 0" stroke="#1E1830" stroke-width="2.6" fill="none" stroke-linecap="round"/>'
    '<path d="M57 72q2 8 0 10q-3-2-2-9" fill="#bdf2ff"/>'
    '<path d="M18 80q-6 6 0 10q8 0 8-6M84 80q6 6 0 10q-8 0-8-6" fill="#7BD56B"/>'
    '<text x="72" y="26" font-size="12" font-weight="800" font-family="system-ui" fill="#8A7BB8">z</text>'
    '<text x="81" y="15" font-size="9" font-weight="800" font-family="system-ui" fill="#8A7BB8">z</text>')

SPECTRE = svg(shadow(26) +
    '<path d="M50 10C30 10 20 28 20 48V84L28 78L36 86L44 78L52 86L60 78L68 86L76 78L80 84V48C80 28 70 10 50 10Z" fill="#EEF0FF"/>'
    '<path d="M50 10C30 10 20 28 20 48V84" fill="none" stroke="#C9CDF2" stroke-width="3"/>'
    '<ellipse cx="39" cy="40" rx="6.5" ry="9" fill="#1E1830"/><ellipse cx="61" cy="40" rx="6.5" ry="9" fill="#1E1830"/>'
    '<circle cx="41" cy="36" r="2" fill="#fff"/><circle cx="63" cy="36" r="2" fill="#fff"/>'
    '<ellipse cx="50" cy="58" rx="7" ry="5" fill="#1E1830"/>'
    '<g transform="rotate(14 74 60)"><rect x="64" y="46" width="20" height="32" rx="4" fill="#2B2140"/>'
    '<rect x="66.5" y="49" width="15" height="24" rx="2" fill="#74C0FC"/>'
    '<path d="M69 54h10M69 58h7M69 62h9" stroke="#fff" stroke-width="1.6" opacity=".9"/>'
    '<circle cx="81" cy="50" r="3.2" fill="#FF6B6B"/><text x="79.6" y="52.2" font-size="5" font-weight="800" fill="#fff" font-family="system-ui">9</text></g>'
    '<path d="M30 60q-10 4-12 14" stroke="#EEF0FF" stroke-width="7" stroke-linecap="round" fill="none"/>'
    '<path d="M86 30l3 2M88 40l4 0M85 22l2-3" stroke="#74C0FC" stroke-width="2.2" stroke-linecap="round"/>')

CHRONO = svg(shadow(28) +
    '<path d="M28 84l-6 8M72 84l6 8" stroke="#6B3A1E" stroke-width="5" stroke-linecap="round"/>'
    '<circle cx="28" cy="20" r="11" fill="#FFC53D" stroke="#C98500" stroke-width="2.4"/>'
    '<circle cx="72" cy="20" r="11" fill="#FFC53D" stroke="#C98500" stroke-width="2.4"/>'
    '<path d="M44 16h12" stroke="#C98500" stroke-width="5" stroke-linecap="round"/>'
    '<circle cx="50" cy="56" r="36" fill="#E8412F"/><circle cx="50" cy="56" r="28" fill="#FFF6E8"/>'
    '<path d="M50 32v4M50 76v4M26 56h4M70 56h4" stroke="#6B3A1E" stroke-width="2.6" stroke-linecap="round"/>'
    '<path d="M36 46l8 4M64 46l-8 4" stroke="#1E1830" stroke-width="3.4" stroke-linecap="round"/>'
    '<circle cx="40" cy="52" r="3.6" fill="#1E1830"/><circle cx="60" cy="52" r="3.6" fill="#1E1830"/>'
    '<path d="M36 64Q50 74 64 64L61 72Q50 78 39 72Z" fill="#1E1830"/>'
    '<path d="M40 65l2 4 2-3 2 4 2-4 2 4 2-4 2 3 2-4 2 3" stroke="#fff" stroke-width="1.6" fill="none" stroke-linejoin="round"/>'
    '<path d="M50 56L50 40M50 56L60 50" stroke="#E8412F" stroke-width="2.4" stroke-linecap="round" opacity=".5"/>')

GOLEM = svg(shadow(34) +
    '<rect x="12" y="46" width="18" height="30" rx="6" fill="#868E96"/><rect x="70" y="46" width="18" height="30" rx="6" fill="#868E96"/>'
    '<rect x="30" y="40" width="40" height="46" rx="8" fill="#9AA2AA"/>'
    '<path d="M36 52l6 6M58 62l6-4M40 74l8-2" stroke="#6E767E" stroke-width="2.4" stroke-linecap="round"/>'
    '<rect x="32" y="12" width="36" height="30" rx="8" fill="#ADB5BD"/>'
    '<path d="M36 22l10 3M64 22l-10 3" stroke="#495057" stroke-width="3.4" stroke-linecap="round"/>'
    '<circle cx="42" cy="29" r="4" fill="#4DABF7"/><circle cx="58" cy="29" r="4" fill="#4DABF7"/>'
    '<circle cx="42" cy="29" r="7" fill="#4DABF7" opacity=".25"/><circle cx="58" cy="29" r="7" fill="#4DABF7" opacity=".25"/>'
    '<path d="M42 37h16" stroke="#495057" stroke-width="3" stroke-linecap="round"/>'
    '<rect x="34" y="84" width="12" height="8" rx="3" fill="#868E96"/><rect x="54" y="84" width="12" height="8" rx="3" fill="#868E96"/>'
    '<g transform="rotate(-10 20 66)"><rect x="4" y="54" width="26" height="32" rx="2" fill="#fff" stroke="#CED4DA" stroke-width="1.4"/>'
    '<path d="M8 62h14M8 67h18M8 72h12" stroke="#ADB5BD" stroke-width="1.6"/>'
    '<text x="19" y="84" font-size="11" font-weight="900" fill="#E03131" font-family="system-ui">?</text></g>')

BOSSES = [
    {"name": "Slime de la Procrastination", "art": SLIME,
     "taunt": "« Pourquoi réviser aujourd'hui quand on peut le faire demain… ? »"},
    {"name": "Spectre de la Distraction", "art": SPECTRE,
     "taunt": "« Juste une petite notif… et puis une autre… »"},
    {"name": "Chronophage", "art": CHRONO,
     "taunt": "« Tic-tac… ton examen approche, et je dévore ton temps ! »"},
    {"name": "Golem des Examens", "art": GOLEM,
     "taunt": "« Aucune question ne passera sans que tu la connaisses par cœur. »"},
]


# ═════════════════════════════════════════════ université (bâtiments)
def _ground(w=40):
    return f'<ellipse cx="50" cy="93" rx="{w}" ry="5" fill="#000" opacity=".13"/>'


def _win(x, y, w=8, h=10, lit=True):
    c = "#FFE27A" if lit else "#A5D8FF"
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="1.5" fill="{c}" stroke="#6B4E3A" stroke-width="1.2"/>'
            f'<path d="M{x + w / 2} {y}v{h}M{x} {y + h / 2}h{w}" stroke="#6B4E3A" stroke-width=".9"/>')


BUILDINGS_ART = {
    "biblio": svg(_ground(42) +
        '<path d="M10 88h80v5H10zM14 83h72v5H14z" fill="#CFC2A8"/>'
        '<rect x="18" y="44" width="64" height="39" fill="#F3E6D0"/>'
        + "".join(f'<rect x="{x}" y="46" width="7" height="37" fill="#fff" stroke="#D9C9A8" stroke-width="1.2"/>' for x in (22, 36, 57, 71)) +
        '<path d="M44 83V62a6 6 0 0 1 12 0v21z" fill="#8C5A3C"/>'
        '<path d="M12 44L50 20L88 44Z" fill="#C0504D"/><path d="M18 42L50 24L82 42Z" fill="#E9D8B4"/>'
        '<rect x="12" y="41" width="76" height="5" fill="#B04441"/>'
        '<path d="M43 34h14v-5c-3 1-5 1-7 3c-2-2-4-2-7-3z" fill="#4F63D8"/>'),
    "cafe": svg(_ground(38) +
        '<rect x="18" y="46" width="64" height="44" rx="3" fill="#FFF3E0"/>'
        '<path d="M14 38h72l-4 14H18z" fill="#E03131"/>'
        + "".join(f'<path d="M{18 + i * 16} 38h8l-1 14h-8z" fill="#fff"/>' for i in range(4)) +
        '<path d="M18 52q4 6 8 0q4 6 8 0q4 6 8 0q4 6 8 0q4 6 8 0q4 6 8 0q4 6 8 0q4 6 8 0" fill="#E03131"/>'
        + _win(24, 62, 16, 14) + _win(60, 62, 16, 14) +
        '<rect x="44" y="64" width="12" height="26" rx="2" fill="#8C5A3C"/>'
        '<circle cx="50" cy="28" r="9" fill="#fff" stroke="#8C5A3C" stroke-width="2"/>'
        '<path d="M45 25h8v6a4 4 0 0 1-8 0zM53 26h2a2 2 0 0 1 0 4h-2" fill="none" stroke="#8C5A3C" stroke-width="1.8"/>'),
    "amphi": svg(_ground(44) +
        '<rect x="8" y="52" width="84" height="38" rx="3" fill="#E7ECF5"/>'
        '<path d="M22 52a28 28 0 0 1 56 0z" fill="#4F63D8"/><path d="M30 52a20 20 0 0 1 40 0" fill="none" stroke="#7B8CEB" stroke-width="2"/>'
        '<rect x="47" y="18" width="6" height="8" fill="#4F63D8"/><circle cx="50" cy="16" r="3" fill="#FFD43B"/>'
        '<path d="M40 90V72a10 10 0 0 1 20 0v18z" fill="#6B4E3A"/>'
        + _win(14, 62, 10, 12) + _win(76, 62, 10, 12) + _win(26, 64, 8, 10) + _win(66, 64, 8, 10)),
    "residence": svg(_ground(32) +
        '<rect x="22" y="22" width="56" height="68" rx="2" fill="#F4A259"/>'
        '<path d="M18 24L50 8L82 24Z" fill="#8C5A3C"/>'
        + "".join(_win(x, y, 9, 10, lit=((x + y) % 3 != 0)) for y in (30, 46, 62) for x in (28, 45.5, 63)) +
        '<rect x="43" y="76" width="14" height="14" rx="2" fill="#6B4E3A"/>'
        '<path d="M22 44h56M22 60h56" stroke="#D9822B" stroke-width="1.4"/>'),
    "labo": svg(_ground(40) +
        '<rect x="14" y="40" width="72" height="50" rx="4" fill="#E6FCF5"/>'
        '<rect x="14" y="40" width="72" height="9" rx="3" fill="#20C997"/>'
        '<rect x="66" y="18" width="10" height="24" fill="#ADB5BD"/>'
        '<circle cx="72" cy="12" r="4" fill="#fff" opacity=".9"/><circle cx="78" cy="6" r="3" fill="#fff" opacity=".7"/>'
        + _win(20, 56, 14, 12, False) + _win(66, 56, 14, 12, False) +
        '<rect x="42" y="66" width="16" height="24" rx="2" fill="#495057"/>'
        '<path d="M46 20h8v8l8 16H38l8-16z" fill="#fff" stroke="#20C997" stroke-width="2"/>'
        '<path d="M41 38h18l3 6H38z" fill="#63E6BE"/><circle cx="48" cy="40" r="1.4" fill="#fff"/>'),
    "serre": svg(_ground(42) +
        '<path d="M10 90V58a40 30 0 0 1 80 0v32z" fill="#D3F9D8" stroke="#8CE99A" stroke-width="2"/>'
        '<path d="M50 28V90M30 36V90M70 36V90M10 60h80M12 75h76" stroke="#fff" stroke-width="2.4" opacity=".9"/>'
        '<path d="M22 90q2-16 8-20q-2 10 0 20M60 90q0-18 10-22q-4 12-2 22M40 90q-4-12 2-18q2 8 2 18" fill="#40C057"/>'
        '<circle cx="30" cy="68" r="3.4" fill="#FF8FB8"/><circle cx="70" cy="66" r="3.4" fill="#FFD43B"/>'
        '<path d="M26 40q10-8 20-6" stroke="#fff" stroke-width="3" fill="none" opacity=".8" stroke-linecap="round"/>'),
    "observatoire": svg(_ground(30) +
        '<rect x="30" y="46" width="40" height="44" rx="2" fill="#DEE2E6"/>'
        '<path d="M24 48a26 26 0 0 1 52 0z" fill="#F8F9FA" stroke="#ADB5BD" stroke-width="2"/>'
        '<path d="M50 22v26" stroke="#495057" stroke-width="5"/>'
        '<path d="M52 36L72 16l6 4L58 40z" fill="#4F63D8"/>'
        '<rect x="44" y="72" width="12" height="18" rx="2" fill="#495057"/>' + _win(34, 56, 8, 10) + _win(58, 56, 8, 10)
        + _star(84, 10, 3.2) + _star(16, 22, 2.4) + _star(90, 36, 2)),
    "hall": svg(_ground(44) +
        '<rect x="10" y="50" width="80" height="40" rx="2" fill="#E9D8B4"/>'
        '<rect x="38" y="16" width="24" height="74" fill="#F3E6D0" stroke="#CFC2A8" stroke-width="1.4"/>'
        '<path d="M34 18L50 4L66 18Z" fill="#4F63D8"/>'
        '<circle cx="50" cy="30" r="8" fill="#fff" stroke="#8C5A3C" stroke-width="2"/>'
        '<path d="M50 30V25M50 30l4 2" stroke="#8C5A3C" stroke-width="1.8" stroke-linecap="round"/>'
        '<path d="M50 4V-6" stroke="#6B4E3A" stroke-width="1.6"/><path d="M50 -6h10l-3 3 3 3H50z" fill="#E03131"/>'
        '<path d="M43 90V70a7 7 0 0 1 14 0v20z" fill="#8C5A3C"/>'
        + _win(16, 60, 10, 12) + _win(28, 60, 6, 12) + _win(66, 60, 6, 12) + _win(74, 60, 10, 12) + _win(46, 44, 8, 10)),
}
PLOT = svg(_ground(36) +
    '<ellipse cx="50" cy="84" rx="36" ry="9" fill="#C8A37A"/><ellipse cx="50" cy="82" rx="30" ry="6" fill="#D9B98F"/>'
    '<rect x="47" y="46" width="5" height="36" fill="#8C5A3C"/>'
    '<rect x="30" y="38" width="40" height="18" rx="3" fill="#FFD43B" stroke="#E0A100" stroke-width="2"/>'
    '<path d="M36 42l6 10M46 42l6 10M56 42l6 10" stroke="#1E1830" stroke-width="3"/>'
    '<path d="M22 82l4-10 4 10zM70 82l4-10 4 10z" fill="#FF922B"/>')


# ═════════════════════════════════════════════ héros (équipement par palier)
TIERS = [None,
         {"name": "bronze", "c": "#C8864B", "d": "#8F5A2C", "l": "#E8B07A"},
         {"name": "fer", "c": "#9AA3AD", "d": "#6B737C", "l": "#C9D0D6"},
         {"name": "acier", "c": "#6F8196", "d": "#46566A", "l": "#A9BACB"},
         {"name": "mithril", "c": "#5FB4F0", "d": "#2F7DBF", "l": "#B6E0FF"},
         {"name": "légendaire", "c": "#F5C23A", "d": "#C48A0A", "l": "#FFF0A8"}]


def hero_svg(gear, size_em=1.15):
    g = {k: int(gear.get(k, 0)) for k in ("weapon", "helmet", "armor", "shield", "amulet")}
    T = lambda k: TIERS[g[k]]
    parts = []
    legend = any(v == 5 for v in g.values())
    if legend:
        parts.append('<circle cx="60" cy="62" r="54" fill="url(#hAura)"/>')
    parts.append('<ellipse cx="60" cy="114" rx="30" ry="5" fill="#000" opacity=".15"/>')
    # jambes et bottes
    parts.append('<rect x="47" y="88" width="10" height="20" rx="3" fill="#4A3B6B"/><rect x="63" y="88" width="10" height="20" rx="3" fill="#4A3B6B"/>'
                 '<rect x="44" y="104" width="15" height="8" rx="3" fill="#5A3A22"/><rect x="61" y="104" width="15" height="8" rx="3" fill="#5A3A22"/>')
    # bouclier (bras gauche, derrière)
    if g["shield"]:
        t = T("shield")
        parts.append(f'<path d="M14 60h26v18c0 12-8 20-13 23c-5-3-13-11-13-23z" fill="{t["c"]}" stroke="{t["d"]}" stroke-width="2.4"/>'
                     f'<path d="M27 64v32M17 76h20" stroke="{t["d"]}" stroke-width="2" opacity=".7"/>'
                     f'<circle cx="27" cy="76" r="4.5" fill="{t["l"]}" stroke="{t["d"]}" stroke-width="1.5"/>')
    # corps : tunique ou armure
    if g["armor"]:
        t = T("armor")
        parts.append(f'<path d="M40 56q20-8 40 0l3 34H37z" fill="{t["c"]}" stroke="{t["d"]}" stroke-width="2"/>'
                     f'<path d="M44 62q16 6 32 0M42 74q18 6 36 0" stroke="{t["d"]}" stroke-width="1.8" fill="none"/>'
                     f'<path d="M48 58q12 8 24 0" stroke="{t["l"]}" stroke-width="2" fill="none" opacity=".8"/>'
                     f'<circle cx="38" cy="58" r="7" fill="{t["c"]}" stroke="{t["d"]}" stroke-width="2"/><circle cx="82" cy="58" r="7" fill="{t["c"]}" stroke="{t["d"]}" stroke-width="2"/>')
    else:
        parts.append('<path d="M40 56q20-8 40 0l3 34H37z" fill="#6C8EBF"/><path d="M40 84h43" stroke="#8C5A3C" stroke-width="4"/>'
                     '<circle cx="38" cy="58" r="6" fill="#6C8EBF"/><circle cx="82" cy="58" r="6" fill="#6C8EBF"/>')
    # bras
    parts.append('<rect x="30" y="58" width="9" height="22" rx="4" fill="#F2C9A0"/><rect x="81" y="58" width="9" height="22" rx="4" fill="#F2C9A0"/>')
    # amulette
    if g["amulet"]:
        t = T("amulet")
        parts.append(f'<path d="M52 52q8 10 16 0" stroke="#D9B45A" stroke-width="1.6" fill="none"/>'
                     f'<path d="M60 60l5 5-5 6-5-6z" fill="{t["l"]}" stroke="{t["d"]}" stroke-width="1.6"/>')
    # tête
    parts.append('<circle cx="60" cy="36" r="17" fill="#F2C9A0"/>'
                 '<circle cx="54" cy="37" r="2.4" fill="#2B2140"/><circle cx="66" cy="37" r="2.4" fill="#2B2140"/>'
                 '<path d="M55 44q5 4 10 0" stroke="#8A4A3A" stroke-width="1.8" fill="none" stroke-linecap="round"/>'
                 '<ellipse cx="49" cy="42" rx="3" ry="1.8" fill="#FF9EC0" opacity=".6"/><ellipse cx="71" cy="42" rx="3" ry="1.8" fill="#FF9EC0" opacity=".6"/>')
    if g["helmet"]:
        t = T("helmet")
        parts.append(f'<path d="M42 34a18 18 0 0 1 36 0v4H42z" fill="{t["c"]}" stroke="{t["d"]}" stroke-width="2"/>'
                     f'<path d="M60 17v17" stroke="{t["d"]}" stroke-width="2"/><path d="M47 26q13-8 26 0" stroke="{t["l"]}" stroke-width="2" fill="none" opacity=".8"/>')
        if g["helmet"] >= 3:
            plume = "#E03131" if g["helmet"] < 5 else "#7A5CFF"
            parts.append(f'<path d="M60 17q8-14 20-10q-10 2-14 12z" fill="{plume}"/>')
    else:
        parts.append('<path d="M43 32q4-16 17-16q15 0 17 16q-6-6-17-6q-11 0-17 6z" fill="#6B3F22"/>')
    # arme (main droite)
    if g["weapon"]:
        t = T("weapon")
        parts.append(f'<g transform="rotate(-28 88 78)"><rect x="85" y="30" width="7" height="44" rx="2" fill="{t["l"]}" stroke="{t["d"]}" stroke-width="1.6"/>'
                     f'<path d="M85 30l3.5-8 3.5 8z" fill="{t["l"]}" stroke="{t["d"]}" stroke-width="1.6"/>'
                     f'<rect x="79" y="72" width="19" height="5" rx="2" fill="#D9B45A" stroke="#9C7A2A" stroke-width="1.2"/>'
                     f'<rect x="86" y="77" width="5" height="10" rx="2" fill="#6B3F22"/></g>')
        if g["weapon"] >= 4:
            parts.append(f'<g transform="rotate(-28 88 78)"><rect x="87" y="34" width="3" height="36" fill="#fff" opacity=".6"/></g>')
    else:
        parts.append('<g transform="rotate(-28 88 78)"><rect x="86" y="50" width="5" height="34" rx="2" fill="#A0703F"/></g>')
    defs = ('<defs><radialGradient id="hAura"><stop offset="0" stop-color="#FFE9A6" stop-opacity=".9"/>'
            '<stop offset=".7" stop-color="#FFD43B" stop-opacity=".25"/><stop offset="1" stop-color="#FFD43B" stop-opacity="0"/></radialGradient></defs>')
    return (f'<svg style="width:{size_em}em;height:{size_em}em;vertical-align:-.22em;overflow:visible" viewBox="0 0 120 120" '
            f'xmlns="http://www.w3.org/2000/svg">{defs}' + "".join(parts) + '</svg>')


# ═════════════════════════════════════════════ héros (avatar équipable)
# (base, clair, sombre) pour chaque matériau : 1 bois, 2 fer, 3 acier, 4 or, 5 cristal, 6 légendaire
MAT = [None, ("#a0703f", "#cf9f6a", "#6e4a28"), ("#8d99a6", "#d3dae1", "#58636e"), ("#5a7bb0", "#b3c8e8", "#34507d"),
       ("#e0a100", "#ffe08a", "#a36f00"), ("#27b3d1", "#bff4fc", "#12788f"), ("#9c36b5", "#f0b8ff", "#62207a")]
GEM = [None, "#51cf66", "#74c0fc", "#5c7cfa", "#ff6b6b", "#3bc9db", "#f783ac"]


def avatar_svg(g, size="1.15em"):
    t = lambda s: max(0, min(6, int((g or {}).get(s, 0))))
    A, H, B, S, M = t("arme"), t("casque"), t("armure"), t("bouclier"), t("amulette")
    out = [f'<svg style="width:{size};height:{size};overflow:visible" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">']
    legend = max(A, H, B, S, M) >= 6
    if legend:
        out.append('<defs><radialGradient id="pfHeroAura" cx="50%" cy="55%" r="50%"><stop offset="0" stop-color="#f0b8ff" stop-opacity=".8"/>'
                   '<stop offset="1" stop-color="#9c36b5" stop-opacity="0"/></radialGradient></defs>'
                   '<circle cx="50" cy="56" r="48" fill="url(#pfHeroAura)"/>')
    out.append('<ellipse cx="50" cy="94" rx="26" ry="4.5" fill="#000" opacity=".15"/>')
    # cape
    if B >= 4:
        cc = "#7b2cbf" if B >= 6 else "#c92a2a"
        out.append(f'<path d="M36 50 Q30 72 26 90 L74 90 Q70 72 64 50 Z" fill="{cc}"/>')
        if B >= 6:
            out.append(_star(34, 78, 2.2, "#ffe08a") + _star(64, 70, 1.8, "#ffe08a") + _star(56, 86, 1.6, "#ffe08a"))
    # jambes et bottes
    out.append('<rect x="40" y="74" width="8" height="15" rx="3" fill="#3f3558"/><rect x="52" y="74" width="8" height="15" rx="3" fill="#3f3558"/>'
               '<path d="M38 87h11v5H37zM51 87h11l1 5H51z" fill="#5c3b1e"/>')
    # tunique
    out.append('<path d="M34 50Q50 44 66 50L68 77Q50 81 32 77Z" fill="#4f63d8"/>')
    # armure
    if B >= 1:
        b, l, d = MAT[B]
        out.append(f'<path d="M36 50Q50 45 64 50L65 70Q50 75 35 70Z" fill="{b}" stroke="{d}" stroke-width="1.6"/>'
                   f'<path d="M40 52Q50 49 60 52L60 58Q50 55 40 58Z" fill="{l}" opacity=".85"/>'
                   f'<path d="M50 50V72" stroke="{d}" stroke-width="1.2" opacity=".6"/>'
                   f'<rect x="34" y="70" width="32" height="5" rx="2" fill="{d}"/><rect x="47" y="69.5" width="6" height="6" rx="1" fill="#ffd43b"/>')
        if B >= 5:
            out.append(f'<circle cx="50" cy="60" r="3" fill="{GEM[B]}" stroke="#fff" stroke-width=".8"/>')
        out.append(f'<ellipse cx="33" cy="52" rx="6" ry="5" fill="{b}" stroke="{d}" stroke-width="1.4"/>'
                   f'<ellipse cx="67" cy="52" rx="6" ry="5" fill="{b}" stroke="{d}" stroke-width="1.4"/>')
    # bras
    out.append('<path d="M31 54Q26 62 29 70" stroke="#4f63d8" stroke-width="7" stroke-linecap="round" fill="none"/>'
               '<path d="M69 54Q75 60 74 67" stroke="#4f63d8" stroke-width="7" stroke-linecap="round" fill="none"/>'
               '<circle cx="29" cy="71" r="4" fill="#f5c9a0"/><circle cx="74" cy="68" r="4" fill="#f5c9a0"/>')
    # tête
    out.append('<circle cx="50" cy="33" r="14" fill="#f5c9a0"/>'
               '<circle cx="45" cy="34" r="2" fill="#2b2140"/><circle cx="55" cy="34" r="2" fill="#2b2140"/>'
               '<circle cx="45.7" cy="33.3" r=".7" fill="#fff"/><circle cx="55.7" cy="33.3" r=".7" fill="#fff"/>'
               '<path d="M46 40q4 3 8 0" stroke="#8a4b2a" stroke-width="1.6" fill="none" stroke-linecap="round"/>'
               '<ellipse cx="41" cy="38" rx="2.4" ry="1.4" fill="#ff9eb0" opacity=".7"/><ellipse cx="59" cy="38" rx="2.4" ry="1.4" fill="#ff9eb0" opacity=".7"/>')
    if H == 0:
        out.append('<path d="M36 30Q38 17 50 18Q63 17 64 30Q58 23 50 25Q42 23 36 30Z" fill="#7a4a2a"/>')
    else:
        b, l, d = MAT[H]
        out.append(f'<path d="M35 29Q35 14 50 14Q65 14 65 29L65 30L35 30Z" fill="{b}" stroke="{d}" stroke-width="1.6"/>'
                   f'<path d="M39 22Q44 18 50 18" stroke="{l}" stroke-width="2.4" fill="none" stroke-linecap="round"/>'
                   f'<rect x="34" y="27.5" width="32" height="3.6" rx="1.8" fill="{d}"/>')
        if H >= 4:
            pc = "#ffd43b" if H >= 6 else "#e03131"
            out.append(f'<path d="M50 15Q54 4 64 6Q58 10 56 16Z" fill="{pc}"/>')
        if H >= 6:
            out.append('<path d="M39 16L42 9L46 14L50 7L54 14L58 9L61 16Z" fill="#ffd43b" stroke="#e0a100" stroke-width="1"/>'
                       '<circle cx="50" cy="12" r="1.6" fill="#f783ac"/>')
    # bouclier
    if S >= 1:
        b, l, d = MAT[S]
        out.append(f'<path d="M14 52H34V64Q34 76 24 81Q14 76 14 64Z" fill="{b}" stroke="{d}" stroke-width="2"/>'
                   f'<path d="M18 55H30V64Q30 72 24 76Q18 72 18 64Z" fill="{l}" opacity=".5"/>')
        emb = _star(24, 65, 3.4, "#ffd43b") if S >= 4 else f'<path d="M24 57V73M18 64H30" stroke="{d}" stroke-width="2.4"/>'
        out.append(emb)
        if S >= 6:
            out.append('<path d="M14 52H34V64Q34 76 24 81Q14 76 14 64Z" fill="none" stroke="#f0b8ff" stroke-width="1.4" opacity=".9"/>')
    # arme
    if A == 0:
        pass
    else:
        b, l, d = MAT[A]
        if A == 1:
            out.append('<path d="M74 66L86 26" stroke="#a0703f" stroke-width="5" stroke-linecap="round"/>'
                       '<path d="M68 64L80 68" stroke="#6e4a28" stroke-width="3.4" stroke-linecap="round"/>')
        else:
            out.append(f'<path d="M72.5 62L85 20L89 22L77 64Z" fill="{l}" stroke="{d}" stroke-width="1.2"/>'
                       f'<path d="M84 21L87 12L89 22Z" fill="{l}" stroke="{d}" stroke-width="1"/>'
                       f'<path d="M67 62L82 67" stroke="{"#ffd43b" if A >= 4 else d}" stroke-width="3.6" stroke-linecap="round"/>'
                       '<path d="M74.5 66L72 74" stroke="#5c3b1e" stroke-width="3.4" stroke-linecap="round"/>'
                       f'<circle cx="71.5" cy="75" r="2.2" fill="{GEM[A] if A >= 3 else "#ffd43b"}"/>')
            if A >= 5:
                out.append(f'<path d="M79 40L85 20" stroke="#fff" stroke-width="1.4" opacity=".8"/>')
            if A >= 6:
                out.append(_star(92, 16, 2.4, "#f0b8ff") + _star(80, 30, 1.8, "#fff") + _star(94, 34, 1.6, "#f0b8ff"))
    # amulette
    if M >= 1:
        out.append(f'<path d="M44 46Q50 52 56 46" stroke="#ffd43b" stroke-width="1" fill="none"/>'
                   f'<path d="M50 49l3 3.4-3 3.4-3-3.4z" fill="{GEM[M]}" stroke="#fff" stroke-width=".7"/>')
    out.append('</svg>')
    return "".join(out)
