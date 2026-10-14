"""Build assets/stack.svg: a terminal-style tree of categories with skillicons.dev-style tiles.

Usage: python3 assets/generate_stack.py assets
"""
import re, sys, os, subprocess

OUT = sys.argv[1] if len(sys.argv) > 1 else "assets"
SKILLICONS = ["cs", "dotnet", "rabbitmq", "kafka", "redis", "mongodb", "aws", "azure", "docker"]
DEVICON = "https://cdn.jsdelivr.net/gh/devicons/devicon@v2.16.0/icons/{name}/{name}-plain.svg"
SI = "https://cdn.jsdelivr.net/npm/simple-icons@16.35.0/icons/{}.svg"


def fetch(url):
    return subprocess.run(["curl", "-fsSL", url], check=True, capture_output=True, text=True).stdout


def simple_icon(slug, bg):
    path = re.search(r'<path d="([^"]+)"', fetch(SI.format(slug))).group(1)
    return (f'<svg width="256" height="256" viewBox="0 0 256 256"><rect width="256" height="256" rx="60" fill="{bg}"/>'
            f'<g transform="translate(48 48) scale(6.6667)"><path fill="#fff" d="{path}"/></g></svg>')


def devicon(name, bg):
    src = fetch(DEVICON.format(name=name))
    paths = "".join(f'<path fill="#fff" d="{d}"/>' for d in re.findall(r'<path[^>]*\sd="([^"]+)"', src))
    return (f'<svg width="256" height="256" viewBox="0 0 256 256"><rect width="256" height="256" rx="60" fill="{bg}"/>'
            f'<g transform="translate(48 48) scale(1.25)">{paths}</g></svg>')


def text_tile(bg, big, small):
    return (f'<svg width="256" height="256" viewBox="0 0 256 256"><rect width="256" height="256" rx="60" fill="{bg}"/>'
            f'<text x="128" y="142" text-anchor="middle" fill="#fff" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-weight="800" font-size="78">{big}</text>'
            f'<text x="128" y="190" text-anchor="middle" fill="#fff" fill-opacity=".85" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-weight="600" font-size="34">{small}</text></svg>')


combined = fetch("https://skillicons.dev/icons?theme=dark&perline=20&i=" + ",".join(SKILLICONS))
tiles = re.findall(r'<g transform="translate\([^)]*\)">\s*(<svg.*?</svg>)\s*</g>', combined, re.S)
assert len(tiles) == len(SKILLICONS), len(tiles)
icons = dict(zip(SKILLICONS, tiles))
icons["aspnet"] = text_tile("#512BD4", "ASP", ".NET Core")
icons["sqlserver"] = devicon("microsoftsqlserver", "#CC2927")
icons["datadog"] = simple_icon("datadog", "#632CA6")
icons["xunit"] = text_tile("#1E7B34", "xUnit", ".net")
icons["gatling"] = simple_icon("gatling", "#F78557")

icons["claude"] = simple_icon("claude", "#D97757")
icons["copilot"] = simple_icon("githubcopilot", "#242938")
icons["cursor"] = simple_icon("cursor", "#242938")

CATEGORIES = [
    ("back-end", ["cs", "dotnet", "aspnet"]),
    ("messaging", ["rabbitmq", "kafka", "redis"]),
    ("databases", ["sqlserver", "mongodb"]),
    ("cloud-devops", ["aws", "azure", "docker"]),
    ("observability", ["datadog"]),
    ("testing", ["xunit", "gatling"]),
    ("ai-tools", ["claude", "copilot", "cursor"]),
]

GREEN, DARK, BG = "#00FF41", "#008F11", "#0D0208"
FONT = "'Courier New', Courier, monospace"
ICON, GAP, ROW, PAD = 44, 10, 58, 16
LABEL_W = 196
W = LABEL_W + 3 * ICON + 2 * GAP + PAD
TOP = 44
H = TOP + ROW * len(CATEGORIES) + 6
scale = ICON / 256

rows = []
for r, (label, names) in enumerate(CATEGORIES):
    y = TOP + r * ROW
    branch = "└──" if r == len(CATEGORIES) - 1 else "├──"
    tiles = "".join(
        f'<g transform="translate({LABEL_W + k * (ICON + GAP)}, {y + (ROW - ICON) / 2:.1f}) scale({scale:.5f})">{icons[n]}</g>'
        for k, n in enumerate(names))
    rows.append(
        f'<g class="row" style="animation-delay:{0.3 + r * 0.15:.2f}s">'
        f'<text class="label" x="{PAD}" y="{y + ROW / 2 + 5:.1f}"><tspan fill="{DARK}">{branch} </tspan>{label}/</text>{tiles}</g>')

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none">
<style>
  .label {{ font: 15px {FONT}; fill: {GREEN}; white-space: pre; }}
  .row {{ opacity: 0; animation: in .4s ease-out forwards; }}
  @keyframes in {{ from {{ opacity: 0; transform: translateX(-8px); }} to {{ opacity: 1; transform: none; }} }}
</style>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="10" fill="{BG}" stroke="{DARK}" stroke-width="2"/>
<text class="label" x="{PAD}" y="28" font-weight="bold">~/stack<tspan fill="#D7FFD9" font-weight="normal"> $ tree -d</tspan></text>
{chr(10).join(rows)}
</svg>
'''
open(os.path.join(OUT, "stack.svg"), "w").write(svg)
print("ok", len(svg))
