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
W, H = 900, 260
drops, trail_h = rain(W, H)
title = "JOÃO FREITAS"
sub = "Wake up, dev... follow the white rabbit(MQ)"
sub_chars = len(sub)
header = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<style>
  .drop {{ animation-name: fall; animation-timing-function: linear; animation-iteration-count: infinite; }}
  @keyframes fall {{ from {{ transform: translateY(-{trail_h}px); }} to {{ transform: translateY({H + 20}px); }} }}
  .title {{ font: bold 54px {FONT}; fill: {GREEN}; letter-spacing: 6px; filter: url(#glow); animation: flicker 4s infinite; }}
  .ghost {{ font: bold 54px {FONT}; letter-spacing: 6px; opacity: 0; animation: glitch 4s infinite; }}
  @keyframes flicker {{ 0%,18%,22%,62%,64%,100% {{ opacity: 1; }} 20%,63% {{ opacity: .35; }} }}
  @keyframes glitch {{ 0%,60%,66%,100% {{ opacity: 0; transform: translate(0,0); }} 61% {{ opacity: .7; transform: translate(-4px,1px); }} 63% {{ opacity: .7; transform: translate(4px,-1px); }} 65% {{ opacity: .5; transform: translate(-2px,0); }} }}
  .sub {{ font: 18px {FONT}; fill: {GREEN}; }}
  .typing {{ animation: type 3.2s steps({sub_chars}) 1s forwards; }}
  @keyframes type {{ from {{ transform: translateX(0); }} to {{ transform: translateX({sub_chars * 10.8:.1f}px); }} }}
  .cursor {{ animation: type 3.2s steps({sub_chars}) 1s forwards, blink 1s step-end infinite; }}
  @keyframes blink {{ 50% {{ opacity: 0; }} }}
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
  <rect x="150" y="70" width="600" height="130" rx="6" fill="{BG}" opacity=".78"/>
  <text class="ghost" x="{W/2}" y="135" text-anchor="middle" fill="#00FFAA">{title}</text>
  <text class="title" x="{W/2}" y="135" text-anchor="middle">{title}</text>
  <text class="ghost" x="{W/2}" y="135" text-anchor="middle" fill="#3BFF00" style="animation-delay:.08s">{title}</text>
  <clipPath id="subclip"><rect x="-4" y="-20" width="{sub_chars * 10.8 + 16:.1f}" height="30"/></clipPath>
  <g transform="translate({W/2 - sub_chars * 10.8 / 2:.1f},175)" clip-path="url(#subclip)">
    <text class="sub" x="0" y="0" textLength="{sub_chars * 10.8:.1f}">{escape(sub)}</text>
    <rect class="typing" x="0" y="-18" width="{sub_chars * 10.8 + 20:.1f}" height="26" fill="{BG}"/>
    <rect class="cursor" x="2" y="-15" width="10" height="20" fill="{GREEN}"/>
  </g>
  <rect class="scan" width="{W}" height="40" fill="url(#scanline)"/>
  <rect width="{W}" height="{H}" fill="url(#crt)"/>
</g>
<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="12" fill="none" stroke="{DARK}" stroke-width="2"/>
</svg>
'''
open(os.path.join(OUT, "header.svg"), "w").write(header)

# ---------- terminal ----------
P = "joao@matrix:~$ "
lines = [
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
CW = 8.4  # Courier New 14px advance
LH = 22
TW = 900
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

terminal = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{TW}" height="{TH}" viewBox="0 0 {TW} {TH}">
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
open(os.path.join(OUT, "terminal.svg"), "w").write(terminal)

# ---------- divider ----------
DW, DH = 900, 24
seq = "".join(random.choice("01") for _ in range(110))
divider = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{DW}" height="{DH}" viewBox="0 0 {DW} {DH}">
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
open(os.path.join(OUT, "divider.svg"), "w").write(divider)
print("ok")
