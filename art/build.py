"""Generates the hero portraits (heroes/<name>.svg) in the same style as heroes/percy.svg.

Run:  python3 public/art/build.py
"""
import math
import os
import random

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'heroes')

SKINS = {
    'fair':   dict(light='#fbe0c8', base='#f1c7a4', shadow='#d5a079', outline='#b07a55', line='#c48d66', blush='#ee8f7c'),
    'tanned': dict(light='#f2c9a4', base='#e2ad82', shadow='#c28a5f', outline='#9a6440', line='#b07a52', blush='#e8806a'),
    'pale':   dict(light='#f8e3d3', base='#eccdb5', shadow='#cfab92', outline='#a07e68', line='#b8957c', blush='#e8a0a0'),
    'tan':    dict(light='#e0a77c', base='#c98b5e', shadow='#a86c43', outline='#7d4b2b', line='#935a35', blush='#c8604a'),
    'golden': dict(light='#f0caa0', base='#e0b07c', shadow='#c08f5c', outline='#966638', line='#a8784a', blush='#e08670'),
    'brown':  dict(light='#a87252', base='#8a5a3c', shadow='#6a4029', outline='#4a2a18', line='#5a3420', blush='#b0503c'),
}


def grad(id_, stops, vertical=False, x2=1, y2=1):
    if vertical:
        x2, y2 = 0, 1
    s = ''.join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
    return f'<linearGradient id="{id_}" x1="0" y1="0" x2="{x2}" y2="{y2}">{s}</linearGradient>'


def defs(c, sk):
    h, s, i = c['hair'], c['shirt'], c['eyes']
    return f'''<defs>
  {grad('sky', [(0, '#e3f6ff'), (.55, '#8fd0f5'), (1, '#2a9df4')], vertical=True)}
  <radialGradient id="sun" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#fff" stop-opacity=".95"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>
  <radialGradient id="skin" cx=".38" cy=".35" r=".75"><stop offset="0" stop-color="{sk['light']}"/><stop offset=".6" stop-color="{sk['base']}"/><stop offset="1" stop-color="{sk['shadow']}"/></radialGradient>
  {grad('hair', [(0, h[0]), (.5, h[1]), (1, h[2])])}
  {grad('shirt', [(0, s[0]), (.6, s[1]), (1, s[2])])}
  {grad('bronze', [(0, '#ffe7a3'), (.5, '#e0ac3e'), (1, '#9a6d18')], x2=1, y2=0)}
  {grad('dark', [(0, '#6a6a7a'), (.5, '#33333f'), (1, '#15151c')], x2=1, y2=0)}
  <radialGradient id="iris" cx=".45" cy=".4" r=".6"><stop offset="0" stop-color="{i[0]}"/><stop offset=".6" stop-color="{i[1]}"/><stop offset="1" stop-color="{i[2]}"/></radialGradient>
</defs>'''


BACKGROUND = '''<rect width="300" height="500" fill="url(#sky)"/>
<circle cx="235" cy="80" r="85" fill="url(#sun)"/>
<path d="M0 345 Q30 330 60 345 T120 345 T180 345 T240 345 T300 345 V500 H0Z" fill="#1c86b8" opacity=".75"/>
<path d="M0 375 Q30 362 60 375 T120 375 T180 375 T240 375 T300 375 V500 H0Z" fill="#0d4f7a" opacity=".8"/>'''


def sword(fill='url(#bronze)', grip='#5a3a1e'):
    return f'''<g transform="translate(0 -16) rotate(28 214 318)" stroke="#3b2a12" stroke-width="2">
  <rect x="207" y="250" width="14" height="62" rx="4" fill="{grip}"/>
  <path d="M207 262 h14 M207 274 h14 M207 286 h14 M207 298 h14" stroke-width="1.5"/>
  <rect x="188" y="310" width="52" height="11" rx="5" fill="{fill}"/>
  <circle cx="214" cy="246" r="9" fill="{fill}"/>
</g>'''


def dagger():
    return '''<g transform="translate(0 -14) rotate(-30 86 318)" stroke="#3b2a12" stroke-width="2">
  <rect x="80" y="272" width="12" height="40" rx="3" fill="#5a3a1e"/>
  <path d="M80 284 h12 M80 296 h12" stroke-width="1.5"/>
  <rect x="66" y="310" width="40" height="9" rx="4" fill="url(#bronze)"/>
  <circle cx="86" cy="268" r="7" fill="url(#bronze)"/>
</g>'''


def bow():
    return '''<path d="M224 236 L248 480" stroke="#f4efe4" stroke-width="1.6"/>
<path d="M224 236 Q300 340 248 480" fill="none" stroke="#3b2a12" stroke-width="10" stroke-linecap="round"/>
<path d="M224 236 Q300 340 248 480" fill="none" stroke="#a8743c" stroke-width="6" stroke-linecap="round"/>
<path d="M232 252 Q262 290 270 330" fill="none" stroke="#e0b07a" stroke-width="1.6" stroke-linecap="round" opacity=".8"/>'''


def cape():
    return '''<path d="M96 288 Q40 320 30 500 L270 500 Q260 320 204 288 Z" fill="#5e2a92" stroke="#2c1048" stroke-width="2.5" stroke-linejoin="round"/>
<path d="M60 360 Q52 430 50 500 M240 360 Q248 430 250 500" fill="none" stroke="#3f1a66" stroke-width="2" opacity=".7"/>'''


def arms(sk, sleeve_fill=None):
    fill_l = sleeve_fill or sk['base']
    fill_r = sleeve_fill or sk['shadow']
    stroke = '#0a0a10' if sleeve_fill else sk['outline']
    lines = '' if sleeve_fill else f'''<g fill="none" stroke="{sk['line']}" stroke-width="1.6" stroke-linecap="round" opacity=".6">
  <path d="M70 400 Q68 440 74 480"/><path d="M230 400 Q232 440 226 480"/></g>'''
    return f'''<g stroke="{stroke}" stroke-width="2" stroke-linejoin="round">
  <path d="M90 356 L60 354 Q52 420 62 500 L94 500 Q90 430 90 356 Z" fill="{fill_l}"/>
  <path d="M210 356 L240 354 Q248 420 238 500 L206 500 Q210 430 210 356 Z" fill="{fill_r}"/>
</g>{lines}'''


def neck(sk):
    return f'''<path d="M134 236 Q134 262 128 284 Q150 298 172 284 Q166 262 166 236 Z" fill="{sk['base']}" stroke="{sk['outline']}" stroke-width="1.5"/>
<path d="M128 232 Q150 272 172 232 L170 250 Q150 276 130 250 Z" fill="{sk['shadow']}" opacity=".55"/>
<path d="M140 262 Q146 274 148 284 M160 262 Q154 274 152 284" fill="none" stroke="{sk['line']}" stroke-width="1.4" stroke-linecap="round" opacity=".6"/>'''


SHIRT_PATH = ('M134 278 Q150 292 166 278 L204 290 Q222 296 228 314 L242 362 L214 370 L210 346 '
              'Q210 420 206 500 L94 500 Q90 420 90 346 L86 370 L58 362 L72 314 Q78 296 96 290 Z')
JACKET_PATH = ('M134 278 Q150 292 166 278 L204 290 Q222 296 228 314 L246 420 L250 500 L50 500 '
               'L54 420 L72 314 Q78 296 96 290 Z')


def shirt(c):
    s = c['shirt']
    out = f'''<path d="{SHIRT_PATH}" fill="url(#shirt)" stroke="{s[3]}" stroke-width="2.5" stroke-linejoin="round"/>
<path d="M134 278 Q150 293 166 278" fill="none" stroke="{s[3]}" stroke-width="5" stroke-linecap="round"/>
<path d="M134 278 Q150 293 166 278" fill="none" stroke="{s[0]}" stroke-width="2" stroke-linecap="round"/>
<g fill="none" stroke="{s[2]}" stroke-width="2" stroke-linecap="round" opacity=".6">
  <path d="M90 346 Q100 342 104 330"/><path d="M210 346 Q200 342 196 330"/>
  <path d="M190 400 Q196 440 192 480"/><path d="M108 420 Q104 450 108 485"/></g>'''
    return out


def jacket():
    return f'''<path d="{JACKET_PATH}" fill="url(#dark)" stroke="#08080b" stroke-width="2.5" stroke-linejoin="round"/>
<path d="M134 278 Q150 292 166 278 L160 330 Q158 420 162 500 L138 500 Q142 420 140 330 Z" fill="url(#shirt)" stroke="#08080b" stroke-width="1.5"/>
<path d="M134 278 L118 300 L140 340 M166 278 L182 300 L160 340" fill="#3a3a46" stroke="#08080b" stroke-width="2" stroke-linejoin="round"/>
<path d="M90 400 Q92 450 88 500 M210 400 Q208 450 212 500" fill="none" stroke="#000" stroke-width="2" opacity=".5"/>
<circle cx="132" cy="400" r="3" fill="#8a8a96"/><circle cx="132" cy="440" r="3" fill="#8a8a96"/>'''


def armor():
    return '''<path d="M100 300 Q150 284 200 300 L206 420 Q150 440 94 420 Z" fill="url(#bronze)" stroke="#6b4a10" stroke-width="2.5" stroke-linejoin="round"/>
<path d="M150 296 V430 M112 340 Q150 356 188 340 M110 380 Q150 396 190 380" fill="none" stroke="#9a6d18" stroke-width="2"/>
<path d="M94 420 L90 500 M206 420 L210 500" stroke="#2c1048" stroke-width="2"/>
<path d="M94 420 Q150 440 206 420 L210 500 L90 500 Z" fill="#7d4ab0" stroke="#2c1048" stroke-width="2"/>
<circle cx="96" cy="296" r="9" fill="url(#bronze)" stroke="#6b4a10" stroke-width="2"/>
<circle cx="204" cy="296" r="9" fill="url(#bronze)" stroke="#6b4a10" stroke-width="2"/>'''


def emblem(kind, col):
    if kind == 'owl':
        return f'''<g fill="none" stroke="{col}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" opacity=".9">
  <path d="M126 368 L130 350 L140 362 Q150 358 160 362 L170 350 L174 368 Q178 400 150 418 Q122 400 126 368 Z"/>
  <circle cx="140" cy="378" r="7"/><circle cx="160" cy="378" r="7"/></g>
<path d="M150 386 l-4 6 h8z" fill="{col}"/>'''
    if kind == 'gear':
        teeth = ''.join(
            f'<rect x="146" y="352" width="8" height="12" rx="1.5" transform="rotate({a} 150 385)"/>' for a in range(0, 360, 45))
        return f'''<g fill="{col}" opacity=".9">{teeth}<circle cx="150" cy="385" r="22"/></g>
<circle cx="150" cy="385" r="8" fill="url(#shirt)"/>'''
    if kind == 'gem':
        return f'''<g fill="none" stroke="{col}" stroke-width="3.5" stroke-linejoin="round" opacity=".9">
  <path d="M132 368 L142 356 H158 L168 368 L150 410 Z"/><path d="M132 368 H168 M142 356 L150 368 L158 356 M144 368 L150 410 L156 368"/></g>'''
    if kind == 'arrows':
        return f'''<g fill="none" stroke="{col}" stroke-width="4" stroke-linecap="round" opacity=".9">
  <path d="M128 412 L172 358 M172 412 L128 358"/>
  <path d="M172 358 l-12 2 M172 358 l-2 12 M128 358 l12 2 M128 358 l2 12"/>
  <path d="M128 412 l-6 -2 M128 412 l2 6 M172 412 l6 -2 M172 412 l-2 6"/></g>'''
    if kind == 'sun':
        rays = ''.join(
            f'<path d="M150 {353} v-0" transform="rotate({a} 150 385)"/>' for a in [])
        rays = ''.join(
            f'<line x1="150" y1="355" x2="150" y2="364" transform="rotate({a} 150 385)"/>' for a in range(0, 360, 30))
        return f'''<g stroke="{col}" stroke-width="4" stroke-linecap="round" opacity=".9">{rays}</g>
<circle cx="150" cy="385" r="14" fill="{col}" opacity=".9"/>'''
    if kind == 'skull':
        return f'''<g opacity=".9">
  <path d="M136 384 Q132 358 150 356 Q168 358 164 384 Q164 392 158 394 V402 H142 V394 Q136 392 136 384 Z" fill="{col}"/>
  <circle cx="144" cy="378" r="4.5" fill="#2a2a33"/><circle cx="156" cy="378" r="4.5" fill="#2a2a33"/>
  <path d="M150 384 l-2.5 5 h5z" fill="#2a2a33"/>
  <path d="M146 396 V402 M150 396 V402 M154 396 V402" stroke="#2a2a33" stroke-width="1.5"/></g>'''
    return ''


def ears(sk):
    return f'''<path d="M100 172 Q86 168 88 188 Q90 208 104 210 Z" fill="{sk['base']}" stroke="{sk['outline']}" stroke-width="2"/>
<path d="M200 172 Q214 168 212 188 Q210 208 196 210 Z" fill="{sk['shadow']}" stroke="{sk['outline']}" stroke-width="2"/>'''


FACES = {
    'boy':   'M100 168 Q98 118 150 106 Q202 118 200 168 Q201 214 183 238 Q166 258 150 260 Q134 258 117 238 Q99 214 100 168 Z',
    'girl':  'M102 168 Q100 118 150 108 Q200 118 198 168 Q198 210 182 234 Q166 252 150 254 Q134 252 118 234 Q102 210 102 168 Z',
    'broad': 'M98 168 Q96 116 150 104 Q204 116 202 168 Q204 218 188 242 Q170 262 150 263 Q130 262 112 242 Q96 218 98 168 Z',
}


def face(c, sk):
    return f'''<path d="{FACES[c['face']]}" fill="url(#skin)" stroke="{sk['outline']}" stroke-width="2"/>
<path d="M186 150 Q202 190 184 236 Q168 255 150 259 Q175 240 183 205 Q188 180 186 150 Z" fill="{sk['shadow']}" opacity=".35"/>'''


def brows(c):
    col = c['brows']
    if c['face'] == 'girl':
        return f'''<path d="M114 163 Q127 155 141 160" fill="none" stroke="{col}" stroke-width="3.2" stroke-linecap="round"/>
<path d="M159 160 Q173 155 186 163" fill="none" stroke="{col}" stroke-width="3.2" stroke-linecap="round"/>'''
    return f'''<path d="M112 164 Q126 154 142 161 L141 166 Q127 161 113 168 Z" fill="{col}"/>
<path d="M158 160 Q174 152 189 160 L187 165 Q174 159 159 165 Z" fill="{col}"/>'''


def eyes(c, sk):
    lash = c['brows']
    out = f'''<path d="M114 182 Q128 171 143 181 Q128 189 114 182 Z" fill="#fff" stroke="#3a2a22" stroke-width="1"/>
<path d="M157 181 Q172 171 186 182 Q172 189 157 181 Z" fill="#fff" stroke="#3a2a22" stroke-width="1"/>
<circle cx="129" cy="180" r="6.5" fill="url(#iris)"/><circle cx="172" cy="180" r="6.5" fill="url(#iris)"/>
<circle cx="129" cy="180" r="3" fill="#0b1a1a"/><circle cx="172" cy="180" r="3" fill="#0b1a1a"/>
<circle cx="131" cy="177.5" r="1.6" fill="#fff"/><circle cx="174" cy="177.5" r="1.6" fill="#fff"/>
<path d="M113 182 Q128 169 144 181" fill="none" stroke="#1c1f2b" stroke-width="{3.4 if c['face'] == 'girl' else 2.6}" stroke-linecap="round"/>
<path d="M156 181 Q172 169 187 182" fill="none" stroke="#1c1f2b" stroke-width="{3.4 if c['face'] == 'girl' else 2.6}" stroke-linecap="round"/>
<path d="M118 187 Q128 191 139 186 M161 186 Q172 191 182 187" fill="none" stroke="{sk['line']}" stroke-width="1.2" opacity=".7"/>'''
    if c['face'] == 'girl':
        out += '''<path d="M114 182 l-5 -4 M117 178 l-4 -5 M186 182 l5 -4 M183 178 l4 -5" stroke="#1c1f2b" stroke-width="2" stroke-linecap="round"/>'''
    return out


def nose(sk):
    return f'''<path d="M151 186 Q154 202 157 210" fill="none" stroke="{sk['line']}" stroke-width="1.8" stroke-linecap="round"/>
<path d="M141 213 Q147 218 150 216 Q153 218 159 213" fill="none" stroke="{sk['outline']}" stroke-width="2" stroke-linecap="round"/>
<ellipse cx="146" cy="207" rx="3" ry="6" fill="#fff" opacity=".22"/>
<ellipse cx="118" cy="207" rx="10" ry="5" fill="{sk['blush']}" opacity=".28"/>
<ellipse cx="183" cy="207" rx="10" ry="5" fill="{sk['blush']}" opacity=".28"/>'''


def mouth(c, sk):
    kind = c['mouth']
    if kind == 'grin':
        return f'''<path d="M131 226 Q150 248 172 223 Q152 234 131 226 Z" fill="#fff" stroke="#5a2a20" stroke-width="2.6" stroke-linejoin="round"/>
<path d="M172 223 Q176 224 176 229" fill="none" stroke="#5a2a20" stroke-width="1.8" stroke-linecap="round"/>'''
    if kind == 'lips':
        lip = c.get('lip', '#c8645a')
        return f'''<path d="M136 230 Q143 225 150 228 Q157 225 164 230 Q150 233 136 230 Z" fill="{lip}"/>
<path d="M137 231 Q150 243 163 231 Q150 236 137 231 Z" fill="{lip}" opacity=".85"/>
<path d="M136 230 Q150 236 164 230" fill="none" stroke="#5a2a20" stroke-width="1.6" stroke-linecap="round"/>
<path d="M146 236 Q150 238 154 236" stroke="#fff" stroke-width="1.2" opacity=".5" fill="none"/>'''
    if kind == 'calm':
        return '''<path d="M138 231 Q150 235 163 229" fill="none" stroke="#6a3a30" stroke-width="2.4" stroke-linecap="round"/>'''
    if kind == 'smile':
        return f'''<path d="M133 227 Q150 242 168 227" fill="none" stroke="#6a3a30" stroke-width="2.6" stroke-linecap="round"/>
<path d="M140 239 Q150 244 160 239" fill="none" stroke="{sk['line']}" stroke-width="2" stroke-linecap="round" opacity=".6"/>'''
    return ''


# ---------- hair ----------

def curls(points, r_range, seed, shine):
    rnd = random.Random(seed)
    out = []
    for x, y in points:
        r = rnd.uniform(*r_range)
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}"/>')
        out.append(f'<path d="M{x - r * .55:.1f} {y - r * .1:.1f} Q{x - r * .2:.1f} {y - r * .7:.1f} {x + r * .4:.1f} {y - r * .45:.1f}" '
                   f'fill="none" stroke="{shine}" stroke-width="1.6" stroke-linecap="round" opacity=".55"/>')
    return out


def arc(cx, cy, rx, ry, a0, a1, n, jitter=0, seed=1):
    rnd = random.Random(seed)
    pts = []
    for k in range(n):
        a = math.radians(a0 + (a1 - a0) * k / (n - 1))
        pts.append((cx + rx * math.cos(a) + rnd.uniform(-jitter, jitter),
                    cy + ry * math.sin(a) + rnd.uniform(-jitter, jitter)))
    return pts


def hair_messy(c, long_sides=False):
    shine = c['hair_shine']
    back = '''<path d="M92 194 Q80 150 90 118 Q104 80 150 74 Q198 72 214 112 Q222 150 208 196 Q204 164 196 144 L106 144 Q99 170 92 194 Z" fill="url(#hair)"/>'''
    front = f'''<g fill="url(#hair)" stroke="{c['hair'][2]}" stroke-width="1" stroke-linejoin="round">
  <path d="M96 116 Q96 84 128 76 Q114 90 118 104 Q104 104 96 116 Z"/>
  <path d="M118 90 Q132 64 162 66 Q186 68 196 86 Q176 78 160 84 Q140 78 118 90 Z"/>
  <path d="M176 82 Q206 80 216 108 Q218 122 212 132 Q206 108 186 98 Z"/>
  <path d="M100 160 Q98 116 136 104 Q118 124 116 150 Q118 162 124 170 Q110 168 100 160 Z"/>
  <path d="M116 146 Q122 108 162 100 Q140 118 138 140 Q138 154 144 164 Q128 160 116 146 Z"/>
  <path d="M136 138 Q148 102 190 104 Q166 116 162 136 Q160 150 166 158 Q148 152 136 138 Z"/>
  <path d="M160 132 Q178 104 208 116 Q190 124 186 140 Q186 150 190 158 Q172 150 160 132 Z"/>
  <path d="M184 128 Q206 118 212 150 Q212 168 206 182 Q204 160 196 150 Q192 138 184 128 Z"/>
  <path d="M94 182 Q88 150 102 128 Q102 154 108 172 Z"/>
</g>'''
    if long_sides:
        front += f'''<g fill="url(#hair)" stroke="{c['hair'][2]}" stroke-width="1" stroke-linejoin="round">
  <path d="M92 150 Q80 210 96 246 Q100 232 104 236 Q100 200 108 160 Z"/>
  <path d="M208 150 Q220 210 204 246 Q200 232 196 236 Q200 200 192 160 Z"/>
  <path d="M98 196 Q94 226 106 240 Q106 220 112 206 Z"/>
  <path d="M202 196 Q206 226 194 240 Q194 220 188 206 Z"/>
</g>'''
    front += f'''<g fill="none" stroke="{shine}" stroke-linecap="round" opacity=".5">
  <path d="M112 96 Q140 74 176 78" stroke-width="3"/><path d="M122 102 Q146 88 170 90" stroke-width="1.6"/>
  <path d="M186 96 Q204 104 210 122" stroke-width="2"/><path d="M110 128 Q118 114 132 110" stroke-width="1.6"/></g>'''
    return '', back, front


def hair_curly_short(c):
    back = '''<path d="M90 196 Q78 120 120 88 Q150 72 182 88 Q224 120 210 196 Q204 162 196 146 L106 146 Q98 168 90 196 Z" fill="url(#hair)"/>'''
    pts = arc(150, 132, 64, 60, 175, 365, 15, 3, seed=3)
    pts += arc(150, 132, 42, 42, 190, 350, 9, 3, seed=4)
    pts += [(x, 146 + (4 if i % 2 else 0)) for i, x in enumerate(range(110, 194, 14))]
    pts += [(97, 170), (203, 170), (95, 186), (205, 186)]
    front = f'<g fill="url(#hair)" stroke="{c["hair"][2]}" stroke-width="1.2">' + ''.join(curls(pts, (10, 14), 5, c['hair_shine'])) + '</g>'
    return '', back, front


def hair_curly_long(c):
    pts_back = arc(150, 205, 92, 108, 120, 420, 26, 4, seed=7)
    pts_back += arc(150, 205, 70, 86, 140, 400, 16, 4, seed=8)
    behind = (f'<g fill="url(#hair)" stroke="{c["hair"][2]}" stroke-width="1.2">'
              '<ellipse cx="150" cy="205" rx="88" ry="104"/>'
              + ''.join(curls(pts_back, (14, 19), 9, c['hair_shine'])) + '</g>')
    back = '''<path d="M92 196 Q80 120 120 90 Q150 74 182 90 Q222 120 210 196 L106 150 Z" fill="url(#hair)"/>'''
    pts = arc(150, 134, 62, 58, 178, 362, 14, 3, seed=11)
    pts += [(108, 130), (192, 130), (100, 150), (200, 150)]
    sides = [(94, 176), (206, 176), (92, 196), (208, 196), (95, 216), (205, 216)]
    front = (f'<g fill="url(#hair)" stroke="{c["hair"][2]}" stroke-width="1.2">'
             + ''.join(curls(pts, (9, 13), 12, c['hair_shine']))
             + ''.join(curls(sides, (7, 9), 13, c['hair_shine'])) + '</g>'
             f'<path d="M150 104 Q146 120 150 134" fill="none" stroke="{c["hair"][2]}" stroke-width="2"/>')
    return behind, back, front


def hair_ponytail_curls(c):
    pts = arc(150, 262, 52, 18, 10, 170, 9, 2, seed=21)
    behind = (f'<g fill="url(#hair)" stroke="{c["hair"][2]}" stroke-width="1.2">'
              '<path d="M96 168 Q84 232 104 266 L196 266 Q216 232 204 168 Z"/>'
              + ''.join(curls(pts, (9, 12), 21, c['hair_shine'])) + '</g>')
    back = '''<path d="M94 200 Q82 130 112 98 Q150 76 188 98 Q218 130 206 200 Q200 160 194 146 L106 146 Q100 170 94 200 Z" fill="url(#hair)"/>'''
    front = f'''<path d="M100 170 Q94 104 150 92 Q206 104 200 170 Q196 140 186 126 Q168 114 150 118 Q130 114 114 126 Q104 140 100 170 Z"
      fill="url(#hair)" stroke="{c['hair'][2]}" stroke-width="1.2" stroke-linejoin="round"/>
<g fill="none" stroke="{c['hair'][2]}" stroke-width="1.6" stroke-linecap="round" opacity=".6">
  <path d="M112 116 Q130 102 150 102 M150 100 Q174 100 190 116 M106 136 Q120 116 142 110 M196 136 Q182 116 160 110"/></g>
<g fill="none" stroke="url(#hair)" stroke-width="7" stroke-linecap="round">
  <path d="M104 146 q-9 14 0 26 q9 12 -1 26 q-8 12 1 24"/>
  <path d="M196 146 q9 14 0 26 q-9 12 1 26 q8 12 -1 24"/></g>
<g fill="none" stroke="{c['hair'][2]}" stroke-width="1" stroke-linecap="round" opacity=".7">
  <path d="M100 148 q-9 14 0 26 q9 12 -1 26 q-8 12 1 24"/><path d="M200 148 q9 14 0 26 q-9 12 1 26 q8 12 -1 24"/></g>
<g fill="none" stroke="{c['hair_shine']}" stroke-linecap="round" opacity=".6">
  <path d="M118 108 Q140 94 166 96" stroke-width="3"/><path d="M174 104 Q188 112 194 126" stroke-width="2"/></g>'''
    return behind, back, front


def hair_braid(c):
    behind = '''<path d="M96 170 Q88 240 112 276 L188 276 Q212 240 204 170 Z" fill="url(#hair)"/>'''
    back = ''
    front = f'''<path d="M98 178 Q92 102 150 94 Q208 102 202 178 Q200 142 188 126 Q170 112 152 118 L150 106 L148 118 Q130 112 112 126 Q100 142 98 178 Z"
      fill="url(#hair)" stroke="{c['hair'][2]}" stroke-width="1.2" stroke-linejoin="round"/>
<g fill="none" stroke="{c['hair_shine']}" stroke-linecap="round" opacity=".55">
  <path d="M112 116 Q128 102 146 102" stroke-width="3"/><path d="M156 102 Q176 104 188 118" stroke-width="3"/>
  <path d="M104 146 Q108 128 118 120" stroke-width="1.6"/><path d="M196 146 Q192 128 182 120" stroke-width="1.6"/></g>'''
    links = []
    for k in range(9):
        y = 252 + k * 22
        x = 116 - k * 2.2
        rot = 25 if k % 2 else -25
        links.append(f'<ellipse cx="{x:.1f}" cy="{y}" rx="{13 - k * .5:.1f}" ry="15" transform="rotate({rot} {x:.1f} {y})"/>')
    braid = (f'<g fill="url(#hair)" stroke="{c["hair"][2]}" stroke-width="1.4">' + ''.join(links) + '</g>'
             '<rect x="88" y="440" width="22" height="8" rx="3" fill="url(#bronze)" stroke="#6b4a10" stroke-width="1.5"/>'
             f'<path d="M92 448 Q90 464 96 474 M99 448 Q99 466 100 476 M106 448 Q108 464 104 474" stroke="{c["hair"][1]}" stroke-width="4" stroke-linecap="round" fill="none"/>')
    return behind, back, front, braid


def hair_buzz(c):
    front = f'''<path d="M100 172 Q96 106 150 98 Q204 106 200 172 Q198 150 194 140 Q188 128 172 124 Q160 120 150 126 Q140 120 128 124 Q112 128 106 140 Q102 150 100 172 Z"
      fill="url(#hair)" stroke="{c['hair'][2]}" stroke-width="1.2" stroke-linejoin="round"/>
<path d="M112 120 Q140 100 170 104" fill="none" stroke="{c['hair_shine']}" stroke-width="3" stroke-linecap="round" opacity=".45"/>'''
    return '', '', front


HAIR = {
    'messy': hair_messy,
    'shaggy': lambda c: hair_messy(c, long_sides=True),
    'curly_short': hair_curly_short,
    'curly_long': hair_curly_long,
    'ponytail_curls': hair_ponytail_curls,
    'braid': hair_braid,
    'buzz': hair_buzz,
}


def goggles():
    return '''<path d="M98 122 Q150 104 202 122" fill="none" stroke="#3a2a1a" stroke-width="8" stroke-linecap="round"/>
<g stroke="#5a3a12" stroke-width="2.5">
  <circle cx="129" cy="114" r="14" fill="url(#bronze)"/><circle cx="171" cy="114" r="14" fill="url(#bronze)"/>
  <circle cx="129" cy="114" r="9" fill="#5fb3d9"/><circle cx="171" cy="114" r="9" fill="#5fb3d9"/></g>
<path d="M124 110 l5 -3 M166 110 l5 -3" stroke="#fff" stroke-width="2.5" stroke-linecap="round"/>
<path d="M143 114 h14" stroke="#5a3a12" stroke-width="4"/>'''


def necklace():
    return '''<path d="M134 282 Q150 314 166 282" fill="none" stroke="#3b2a12" stroke-width="1.8"/>
<circle cx="150" cy="298" r="3.5" fill="#e0ac3e" stroke="#6b4a10" stroke-width="1"/>'''


def build(c):
    sk = SKINS[c['skin']]
    parts = HAIR[c['hair_style']](c)
    behind, back, front = parts[0], parts[1], parts[2]
    over_body = parts[3] if len(parts) > 3 else ''
    scale = c.get('build', 1)
    body_tf = f'translate(150 0) scale({scale} 1) translate(-150 0)'

    body = []
    if c.get('cape'):
        body.append(cape())
    body.append({'sword': sword(), 'dark_sword': sword('url(#dark)', '#22222a'), 'dagger': dagger(), 'bow': bow(),
                 None: ''}[c.get('back')])
    body.append(arms(sk, '#2a2a33' if c.get('jacket') else None))
    body.append(neck(sk))
    if c.get('jacket'):
        body.append(jacket())
    elif c.get('armor'):
        body.append(shirt(c))
        body.append(armor())
    else:
        body.append(shirt(c))
    body.append(emblem(c.get('emblem'), c.get('emblem_col', '#e8f6ff')))
    body.append(necklace())

    head = [ears(sk), back, face(c, sk), brows(c), eyes(c, sk), nose(sk), mouth(c, sk), front]
    if c.get('goggles'):
        head.append(goggles())

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 500" width="300" height="500">
{defs(c, sk)}
{BACKGROUND}
{behind}
<g transform="{body_tf}">
{chr(10).join(body)}
</g>
{over_body}
{chr(10).join(head)}
</svg>
'''
    with open(os.path.join(OUT, f"{c['name']}.svg"), 'w') as f:
        f.write(svg)


HEROES = [
    dict(name='reyna', skin='tan', face='girl', mouth='lips', lip='#a8463c',
         hair_style='braid', hair=('#4a3632', '#1c1414', '#0c0808'), hair_shine='#7a6460', brows='#1c1414',
         eyes=('#a8744e', '#4a2a18', '#22120a'), shirt=('#b58ad6', '#7d4ab0', '#55307e', '#2c1048'),
         cape=True, armor=True, build=.94),
    dict(name='leo', skin='tan', face='boy', mouth='grin',
         hair_style='curly_short', hair=('#6a4a36', '#2e1f16', '#170f0a'), hair_shine='#a07a5e', brows='#241810',
         eyes=('#c08a50', '#7a4a22', '#3d2410'), shirt=('#ef7b70', '#c0392b', '#8e2a20', '#5e1a14'),
         emblem='gear', emblem_col='#ffe0a0', goggles=True, build=.94),
    dict(name='annabeth', skin='fair', face='girl', mouth='lips', lip='#d0706a',
         hair_style='ponytail_curls', hair=('#fbe7a6', '#e0b552', '#a8792a'), hair_shine='#fff6d6', brows='#a8792a',
         eyes=('#dfe6ec', '#7d8b99', '#46525e'), shirt=('#9fc0e3', '#4f7fb5', '#2f5a8a', '#1f3f63'),
         emblem='owl', emblem_col='#f5f0e1', back='dagger', build=.92),
    dict(name='hazel', skin='brown', face='girl', mouth='lips', lip='#7a3a30',
         hair_style='curly_long', hair=('#b8744a', '#6b3a1f', '#3d1f0f'), hair_shine='#e0a07a', brows='#2a140a',
         eyes=('#ffe9a0', '#d4a017', '#8a6508'), shirt=('#c4a0e2', '#7d4ab0', '#55307e', '#3a1f57'),
         emblem='gem', emblem_col='#fff1b8', back='sword', build=.92),
    dict(name='frank', skin='golden', face='broad', mouth='smile',
         hair_style='buzz', hair=('#4a4e5c', '#1a1b22', '#0b0b10'), hair_shine='#7a8094', brows='#14151b',
         eyes=('#8a6a50', '#4a3020', '#22160c'), shirt=('#a8c470', '#5f7f33', '#3f5a1f', '#2b3f14'),
         emblem='arrows', emblem_col='#f2ead0', back='bow', build=1.1),
    dict(name='will', skin='tanned', face='boy', mouth='smile',
         hair_style='messy', hair=('#fff0b8', '#e9c25a', '#b0842a'), hair_shine='#fffbe6', brows='#a8792a',
         eyes=('#bfe6ff', '#3a8fd6', '#1c5a96'), shirt=('#ffe98f', '#f2c230', '#c99712', '#8a6508'),
         emblem='sun', emblem_col='#c0602a', back='bow'),
    dict(name='nico', skin='pale', face='boy', mouth='calm',
         hair_style='shaggy', hair=('#3c404e', '#14151b', '#07070a'), hair_shine='#6a7088', brows='#14151b',
         eyes=('#7a6a5e', '#3a2a20', '#1a120c'), shirt=('#7a7d88', '#4a4d58', '#2e3038', '#14151b'),
         emblem='skull', emblem_col='#e0e4ec', back='dark_sword', jacket=True, build=.94),
]

if __name__ == '__main__':
    for hero in HEROES:
        build(hero)
    print('built', ', '.join(h['name'] for h in HEROES))
