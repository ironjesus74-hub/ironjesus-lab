#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parents[1]
INP = ROOT / ".status" / "forgebot.json"
OUT = ROOT / ".status" / "forgebot.svg"

W = 980
H = 220

def load_status() -> dict:
    if INP.exists():
        try:
            return json.loads(INP.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {
        "workflow": "ForgeBot - Daily Operator Drop",
        "status": "unknown",
        "conclusion": "unknown",
        "run_id": "",
        "run_url": "",
        "updated_at": "",
        "head_branch": "",
        "head_sha": "",
    }

def color_for(conclusion: str) -> str:
    c = (conclusion or "").lower()
    if c == "success":
        return "#2ee59d"
    if c in ("failure", "cancelled", "timed_out", "action_required"):
        return "#ff4d4d"
    if c in ("neutral", "skipped", "stale"):
        return "#ffd24d"
    return "#7d89ff"

def main() -> int:
    d = load_status()
    workflow = escape(str(d.get("workflow", "")))
    status = escape(str(d.get("status", "")))
    conclusion = escape(str(d.get("conclusion", "")))
    updated_at = escape(str(d.get("updated_at", "")))
    head_branch = escape(str(d.get("head_branch", "")))
    head_sha = escape(str(d.get("head_sha", ""))[:12])
    run_url = str(d.get("run_url", "") or "")
    dot = color_for(str(d.get("conclusion", "")))

    badge = f"{status.upper()} / {conclusion.upper()}"
    if status == "unknown" and conclusion == "unknown":
        badge = "NO RUN DATA YET"

    # If no run_url, link to workflow list
    if not run_url:
        run_url = "https://github.com/ironjesus74-hub/ironjesus-lab/actions/workflows/forgebot.yml"

    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#070b14"/>
      <stop offset="100%" stop-color="#111a33"/>
    </linearGradient>
    <linearGradient id="stroke" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#7d89ff"/>
      <stop offset="50%" stop-color="#2ee59d"/>
      <stop offset="100%" stop-color="#ff4d4d"/>
    </linearGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur in="SourceAlpha" stdDeviation="6" result="blur"/>
      <feOffset in="blur" dx="0" dy="6" result="off"/>
      <feColorMatrix in="off" type="matrix"
        values="0 0 0 0 0
                0 0 0 0 0
                0 0 0 0 0
                0 0 0 0.45 0" result="shadow"/>
      <feMerge>
        <feMergeNode in="shadow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="10" y="10" width="{W-20}" height="{H-20}" rx="18" fill="url(#bg)" filter="url(#softShadow)"/>
  <rect x="10" y="10" width="{W-20}" height="{H-20}" rx="18" fill="none" stroke="url(#stroke)" stroke-width="2"/>

  <text x="38" y="58" font-family="ui-sans-serif,system-ui,Segoe UI,Roboto,Arial" font-size="22" fill="#e8eeff" font-weight="700">
    FORGEBOT LIVE STATUS
  </text>
  <text x="38" y="84" font-family="ui-sans-serif,system-ui,Segoe UI,Roboto,Arial" font-size="13" fill="#9fb0ff">
    Built Different · forge-atlas.io
  </text>

  <circle cx="900" cy="54" r="8" fill="{dot}"/>
  <text x="920" y="58" font-family="ui-sans-serif,system-ui,Segoe UI,Roboto,Arial" font-size="12" fill="#cfd8ff">
    {escape(badge)}
  </text>

  <text x="38" y="122" font-family="ui-monospace,Menlo,Consolas,monospace" font-size="13" fill="#cfd8ff">
    workflow: {workflow}
  </text>
  <text x="38" y="146" font-family="ui-monospace,Menlo,Consolas,monospace" font-size="13" fill="#cfd8ff">
    branch: {head_branch}   sha: {head_sha}
  </text>
  <text x="38" y="170" font-family="ui-monospace,Menlo,Consolas,monospace" font-size="13" fill="#cfd8ff">
    updated: {updated_at}
  </text>

  <text x="38" y="198" font-family="ui-sans-serif,system-ui,Segoe UI,Roboto,Arial" font-size="12" fill="#9fb0ff">
    source: {escape(run_url)}
  </text>
</svg>
"""
    OUT.write_text(svg, encoding="utf-8")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
