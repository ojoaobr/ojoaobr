"""Build assets/stack.svg: skillicons.dev tiles plus custom tiles in the same style.

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

ORDER = ["cs", "dotnet", "aspnet", "rabbitmq", "kafka", "redis", "sqlserver",
         "mongodb", "aws", "azure", "docker", "datadog", "xunit", "gatling"]
PER_LINE = 7
rows = (len(ORDER) + PER_LINE - 1) // PER_LINE
vw, vh = PER_LINE * 300 - 44, rows * 300 - 44
scale = 48 / 256
parts = []
for i, name in enumerate(ORDER):
    x, y = (i % PER_LINE) * 300, (i // PER_LINE) * 300
    parts.append(f'<g transform="translate({x}, {y})">{icons[name]}</g>')
svg = (f'<svg width="{vw*scale:.2f}" height="{vh*scale:.2f}" viewBox="0 0 {vw} {vh}" fill="none" '
       f'xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">'
       + "".join(parts) + "</svg>\n")
open(os.path.join(OUT, "stack.svg"), "w").write(svg)
print("ok", len(svg))
