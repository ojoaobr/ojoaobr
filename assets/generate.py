"""Generate the Matrix-themed SVGs (desktop and mobile variants).

Usage: python3 assets/generate.py assets
"""
import random, os, sys
from xml.sax.saxutils import escape

random.seed(7)
OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)

GREEN = "#00FF41"
DARK = "#008F11"
BG = "#0D0208"
FONT = "'Courier New', Courier, monospace"
CHARS = "ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜﾝ0123456789#$%&*+=<>{}"


def write(name, svg):
    open(os.path.join(OUT, name), "w").write(svg)


def rain(width, height, size=14, trail=18, opacity=1.0):
    cols = width // size
    out = [f'<g font-family="{FONT}" font-size="{size}" opacity="{opacity}">']
    for c in range(cols):
        if random.random() < 0.25:
            continue
        x = c * size + size / 2
        dur = random.uniform(4, 10)
        delay = -random.uniform(0, dur)
        out.append(
            f'<g class="drop" style="animation-duration:{dur:.2f}s;animation-delay:{delay:.2f}s">'
        )
        for i in range(trail):
            ch = escape(random.choice(CHARS))
            y = i * size
            if i == trail - 1:
                fill, op = "#D7FFD9", 1
            else:
                fill, op = GREEN, round(0.08 + 0.75 * (i / trail), 2)
            out.append(f'<text x="{x}" y="{y}" fill="{fill}" opacity="{op}" text-anchor="middle">{ch}</text>')
        out.append("</g>")
    out.append("</g>")
    return "\n".join(out), trail * size


# ---------- header ----------
def header(W, H, title_lines, title_size, title_spacing, subs, sub_size, title_y, line_gap, sub_gap):
    drops, trail_h = rain(W, H)
    cw = sub_size * 0.6  # Courier advance
    title_h = title_size * len(title_lines) + line_gap * (len(title_lines) - 1)
    box_w = max(max(len(t) for t in title_lines) * (title_size * 0.6 + title_spacing), max(len(s) for s in subs) * cw) + 60
    box_y = title_y - title_size - 20
    box_h = title_h + sub_gap + (len(subs) - 1) * (sub_size + 8) + 40

    titles = []
    for i, t in enumerate(title_lines):
        y = title_y + i * (title_size + line_gap)
        titles.append(f'''  <text class="ghost" x="{W/2}" y="{y}" text-anchor="middle" fill="#00FFAA">{t}</text>
  <text class="title" x="{W/2}" y="{y}" text-anchor="middle">{t}</text>
  <text class="ghost" x="{W/2}" y="{y}" text-anchor="middle" fill="#3BFF00" style="animation-delay:.08s">{t}</text>''')

    typed, start = [], 1.0
    sub_y = title_y + title_h - title_size + sub_gap
    for i, sub in enumerate(subs):
        n = len(sub)
        width = n * cw
        dur = n * 0.075
        last = i == len(subs) - 1
        cursor_anim = f"type{i} {dur:.2f}s steps({n}) {start:.2f}s forwards" + (", blink 1s step-end infinite" if last else f", hide 0s {start + dur:.2f}s forwards")
        typed.append(f'''  <clipPath id="subclip{i}"><rect x="-4" y="-{sub_size + 2}" width="{width + 16:.1f}" height="{sub_size + 12}"/></clipPath>
  <style>@keyframes type{i} {{ to {{ transform: translateX({width:.1f}px); }} }}</style>
  <g transform="translate({W/2 - width/2:.1f},{sub_y + i * (sub_size + 8)})" clip-path="url(#subclip{i})">
    <text class="sub" x="0" y="0" textLength="{width:.1f}">{escape(sub)}</text>
    <rect x="0" y="-{sub_size}" width="{width + 20:.1f}" height="{sub_size + 8}" fill="{BG}" style="animation: type{i} {dur:.2f}s steps({n}) {start:.2f}s forwards"/>
    <rect class="cursor" x="2" y="-{sub_size - 3}" width="{cw:.1f}" height="{sub_size + 2}" fill="{GREEN}" style="opacity:{1 if i == 0 else 0};animation: show 0s {start:.2f}s forwards, {cursor_anim}"/>
  </g>''')
        start += dur + 0.2

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<style>
  .drop {{ animation-name: fall; animation-timing-function: linear; animation-iteration-count: infinite; }}
  @keyframes fall {{ from {{ transform: translateY(-{trail_h}px); }} to {{ transform: translateY({H + 20}px); }} }}
  .title {{ font: bold {title_size}px {FONT}; fill: {GREEN}; letter-spacing: {title_spacing}px; filter: url(#glow); animation: flicker 4s infinite; }}
  .ghost {{ font: bold {title_size}px {FONT}; letter-spacing: {title_spacing}px; opacity: 0; animation: glitch 4s infinite; }}
  @keyframes flicker {{ 0%,18%,22%,62%,64%,100% {{ opacity: 1; }} 20%,63% {{ opacity: .35; }} }}
  @keyframes glitch {{ 0%,60%,66%,100% {{ opacity: 0; transform: translate(0,0); }} 61% {{ opacity: .7; transform: translate(-4px,1px); }} 63% {{ opacity: .7; transform: translate(4px,-1px); }} 65% {{ opacity: .5; transform: translate(-2px,0); }} }}
  .sub {{ font: {sub_size}px {FONT}; fill: {GREEN}; }}
  @keyframes blink {{ 50% {{ opacity: 0; }} }}
  @keyframes show {{ to {{ opacity: 1; }} }}
  @keyframes hide {{ to {{ opacity: 0; }} }}
  .scan {{ animation: scan 6s linear infinite; }}
  @keyframes scan {{ from {{ transform: translateY(-40px); }} to {{ transform: translateY({H}px); }} }}
</style>
<defs>
  <filter id="glow" x="-20%" y="-50%" width="140%" height="200%">
    <feGaussianBlur stdDeviation="3" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <radialGradient id="vignette" cx="50%" cy="50%" r="65%">
    <stop offset="40%" stop-color="{BG}" stop-opacity="0"/>
    <stop offset="100%" stop-color="{BG}" stop-opacity=".95"/>
  </radialGradient>
  <linearGradient id="scanline" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{GREEN}" stop-opacity="0"/>
    <stop offset=".5" stop-color="{GREEN}" stop-opacity=".08"/>
    <stop offset="1" stop-color="{GREEN}" stop-opacity="0"/>
  </linearGradient>
  <pattern id="crt" width="4" height="4" patternUnits="userSpaceOnUse">
    <rect width="4" height="1" fill="#000" opacity=".35"/>
  </pattern>
  <clipPath id="frame"><rect width="{W}" height="{H}" rx="12"/></clipPath>
</defs>
<g clip-path="url(#frame)">
  <rect width="{W}" height="{H}" fill="{BG}"/>
  {drops}
  <rect width="{W}" height="{H}" fill="url(#vignette)"/>
  <rect x="{(W - box_w)/2:.1f}" y="{box_y}" width="{box_w:.1f}" height="{box_h}" rx="6" fill="{BG}" opacity=".78"/>
{chr(10).join(titles)}
{chr(10).join(typed)}
  <rect class="scan" width="{W}" height="40" fill="url(#scanline)"/>
  <rect width="{W}" height="{H}" fill="url(#crt)"/>
</g>
<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="12" fill="none" stroke="{DARK}" stroke-width="2"/>
</svg>
'''


# ---------- terminal ----------
P = "joao@matrix:~$ "
CW = 8.4  # Courier New 14px advance
LH = 22


def terminal(lines, TW):
    top = 52
    TH = top + LH * (len(lines) - 1) + 14
    body = []
    t = 0.6
    for i, (kind, txt) in enumerate(lines):
        y = top + i * LH
        if kind == "gap":
            continue
        if kind == "cmd":
            n = len(txt)
            dur = max(0.4, n * 0.07)
            body.append(f'<text x="20" y="{y}" class="p" style="animation-delay:{t:.2f}s">{escape(P)}<tspan class="c">{escape(txt)}</tspan></text>')
            x0 = 20 + len(P) * CW
            body.append(
                f'<rect x="{x0:.1f}" y="{y-15}" width="{n*CW+12:.1f}" height="20" fill="{BG}" class="cover" '
                f'style="animation:fadein .01s {t:.2f}s forwards, type {dur:.2f}s steps({n}) {t+0.3:.2f}s forwards;--d:{n*CW:.1f}px"/>'
            )
            t += 0.3 + dur + 0.25
        elif kind == "out":
            body.append(f'<text x="20" y="{y}" class="o" style="animation-delay:{t:.2f}s">{escape(txt)}</text>')
            t += 0.18
        else:
            body.append(f'<text x="20" y="{y}" class="p" style="animation-delay:{t:.2f}s">{escape(P)}</text>')
            body.append(f'<rect x="{20 + len(P)*CW + 2:.1f}" y="{y-14}" width="9" height="18" fill="{GREEN}" class="blink" style="animation-delay:{t:.2f}s,{t:.2f}s"/>')

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{TW}" height="{TH}" viewBox="0 0 {TW} {TH}">
<style>
  text {{ font: 14px {FONT}; white-space: pre; }}
  .p, .o {{ opacity: 0; animation: fadein .01s forwards; }}
  .p {{ fill: {GREEN}; font-weight: bold; }}
  .c {{ fill: #D7FFD9; font-weight: normal; }}
  .o {{ fill: {GREEN}; opacity: 0; }}
  .cover {{ opacity: 0; }}
  .blink {{ opacity: 0; animation: fadein .01s forwards, blink 1s step-end infinite; }}
  @keyframes fadein {{ to {{ opacity: 1; }} }}
  @keyframes blink {{ 50% {{ fill-opacity: 0; }} }}
  @keyframes type {{ to {{ transform: translateX(var(--d)); }} }}
  .title {{ font: 13px {FONT}; fill: {DARK}; }}
</style>
<defs>
  <pattern id="crt" width="4" height="3" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#000" opacity=".3"/></pattern>
  <filter id="glow"><feGaussianBlur stdDeviation="1.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>
<rect x="1" y="1" width="{TW-2}" height="{TH-2}" rx="10" fill="{BG}" stroke="{DARK}" stroke-width="2"/>
<rect x="1" y="1" width="{TW-2}" height="30" rx="10" fill="#03160A"/>
<rect x="1" y="20" width="{TW-2}" height="11" fill="#03160A"/>
<line x1="1" y1="31" x2="{TW-1}" y2="31" stroke="{DARK}" stroke-width="1"/>
<circle cx="22" cy="16" r="6" fill="#FF5F56"/><circle cx="42" cy="16" r="6" fill="#FFBD2E"/><circle cx="62" cy="16" r="6" fill="#27C93F"/>
<text x="{TW/2}" y="20" text-anchor="middle" class="title">joao@matrix: ~ — zsh</text>
<g filter="url(#glow)">
{chr(10).join(body)}
</g>
<rect x="2" y="32" width="{TW-4}" height="{TH-34}" fill="url(#crt)"/>
</svg>
'''


TERMINAL_DESKTOP = [
    ("cmd", "whoami"),
    ("out", "João Freitas — Software Engineer · .NET Core · 5 years"),
    ("gap", ""),
    ("cmd", "cat about.txt"),
    ("out", "> Building back-end systems at LATAM's largest car rental company"),
    ("out", "> Event-driven messaging with RabbitMQ & Kafka at high volume"),
    ("out", "> Database performance tuning on SQL Server & MongoDB"),
    ("out", "> Observability & reliability with Datadog"),
    ("out", "> Modernizing legacy apps with clean architecture patterns"),
    ("gap", ""),
    ("cmd", "./stack --list"),
    ("out", "[back-end]   C# · .NET Core · ASP.NET Core"),
    ("out", "[messaging]  RabbitMQ · Kafka · Redis"),
    ("out", "[data]       SQL Server · MongoDB"),
    ("out", "[cloud/ops]  AWS · Azure · Docker · Datadog"),
    ("out", "[testing]    xUnit · Gatling"),
    ("gap", ""),
    ("end", ""),
]

# Max ~45 chars per line at 420px
TERMINAL_MOBILE = [
    ("cmd", "whoami"),
    ("out", "João Freitas"),
    ("out", "Software Engineer · .NET Core · 5 years"),
    ("gap", ""),
    ("cmd", "cat about.txt"),
    ("out", "> Back-end at LATAM's largest car rental"),
    ("out", "> Event-driven: RabbitMQ & Kafka"),
    ("out", "> DB tuning: SQL Server & MongoDB"),
    ("out", "> Observability with Datadog"),
    ("out", "> Legacy modernization, clean arch"),
    ("gap", ""),
    ("cmd", "./stack --list"),
    ("out", "[back-end]  C# · .NET · ASP.NET Core"),
    ("out", "[messaging] RabbitMQ · Kafka · Redis"),
    ("out", "[data]      SQL Server · MongoDB"),
    ("out", "[cloud/ops] AWS · Azure · Docker · Datadog"),
    ("out", "[testing]   xUnit · Gatling"),
    ("gap", ""),
    ("end", ""),
]

# ---------- divider ----------
def divider():
    DW, DH = 900, 24
    seq = "".join(random.choice("01") for _ in range(110))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{DW}" height="{DH}" viewBox="0 0 {DW} {DH}">
<style>
  text {{ font: 13px {FONT}; fill: {DARK}; }}
  .m {{ animation: slide 12s linear infinite; }}
  @keyframes slide {{ to {{ transform: translateX(-{len(seq)*7.8:.1f}px); }} }}
</style>
<defs><linearGradient id="f" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".15" stop-color="#fff"/><stop offset=".85" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<mask id="mk"><rect width="{DW}" height="{DH}" fill="url(#f)"/></mask></defs>
<g mask="url(#mk)"><g class="m">
<text x="0" y="16" textLength="{len(seq)*7.8:.1f}">{seq}</text>
<text x="{len(seq)*7.8:.1f}" y="16" textLength="{len(seq)*7.8:.1f}">{seq}</text>
</g></g>
</svg>
'''


# Desktop assets first so their random output stays stable
write("header.svg", header(900, 260, ["JOÃO FREITAS"], 54, 6,
                           ["Wake up, dev... follow the white rabbit(MQ)"], 18,
                           title_y=135, line_gap=0, sub_gap=40))
write("terminal.svg", terminal(TERMINAL_DESKTOP, 900))
write("divider.svg", divider())

write("header-mobile.svg", header(420, 300, ["JOÃO", "FREITAS"], 52, 6,
                                  ["Wake up, dev...", "follow the white rabbit(MQ)"], 18,
                                  title_y=100, line_gap=8, sub_gap=46))
write("terminal-mobile.svg", terminal(TERMINAL_MOBILE, 420))
print("ok")
