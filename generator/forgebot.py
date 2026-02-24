#!/usr/bin/env python3
from __future__ import annotations
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "generator" / "catalog.json"
TEMPL_DIR = ROOT / "generator" / "templates"
STATE_PATH = ROOT / ".forgebot" / "state.json"
LAST_RUN_PATH_DEFAULT = ROOT / ".forgebot" / "last.json"
TOOLS_DIR = ROOT / "tools"

def jload(path: Path, default):
  if not path.exists():
    return default
  return json.loads(path.read_text(encoding="utf-8"))

def jsave(path: Path, obj):
  path.parent.mkdir(parents=True, exist_ok=True)
  path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")

def slug_safe(s: str) -> str:
  allowed = "abcdefghijklmnopqrstuvwxyz0123456789-_"
  s = s.lower().replace(" ", "-")
  return "".join(ch for ch in s if ch in allowed).strip("-")

def render(t: str, ctx: dict) -> str:
  for k, v in ctx.items():
    t = t.replace(f"__{k}__", str(v))
  return t

def update_index(line: str):
  idx = TOOLS_DIR / "README.md"
  if not idx.exists():
    TOOLS_DIR.mkdir(parents=True, exist_ok=True)
    idx.write_text("# Forge Atlas Operators (Free Samples)\n\n## Index\n\n", encoding="utf-8")
  txt = idx.read_text(encoding="utf-8")
  if line in txt:
    return
  idx.write_text(txt + line + "\n", encoding="utf-8")

def cmd_generate(out_path: Path):
  catalog = jload(CATALOG_PATH, {"items": []}).get("items", [])
  state = jload(STATE_PATH, {"used_ids": []})
  used = set(state.get("used_ids", []))

  next_item = None
  for it in catalog:
    if it["id"] not in used:
      next_item = it
      break
  if not next_item:
    raise SystemExit("No remaining catalog items. Add more to generator/catalog.json")

  now = datetime.now(timezone.utc)
  date_ymd = now.strftime("%Y%m%d")

  tool_id = next_item["id"]
  slug = slug_safe(next_item["slug"])
  lang = next_item["lang"]
  ext = {"bash": "sh", "python": "py"}[lang]

  template_path = TEMPL_DIR / next_item["template"]
  if not template_path.exists():
    raise SystemExit(f"Missing template: {template_path}")

  ctx = {
    "TITLE": next_item["title"],
    "DESC": next_item["desc"],
    "DATE_UTC": now.isoformat().replace("+00:00", "Z"),
    "WEBSITE": "https://forge-atlas.io",
    "GITHUB": "https://github.com/ironjesus74-hub",
    "TOOL_ID": tool_id,
  }

  tool_dir = TOOLS_DIR / slug
  tool_dir.mkdir(parents=True, exist_ok=True)

  tool_file = tool_dir / f"{slug}.{ext}"
  tool_file.write_text(render(template_path.read_text(encoding="utf-8"), ctx), encoding="utf-8")

  jsave(tool_dir / "meta.json", {
    "id": tool_id, "slug": slug, "title": next_item["title"], "desc": next_item["desc"],
    "lang": lang, "created_utc": ctx["DATE_UTC"], "website": ctx["WEBSITE"]
  })

  readme = (
    f"# {next_item['title']}\n\n"
    f"- **What it does:** {next_item['desc']}\n"
    f"- **Site:** {ctx['WEBSITE']}\n"
    f"- **Marketplace:** {ctx['WEBSITE']}/marketplace\n\n"
    f"## Run\n\n"
  )
  readme += "```sh\n" + ("bash" if lang == "bash" else "python3") + f" {slug}.{ext}\n```\n"
  (tool_dir / "README.md").write_text(readme, encoding="utf-8")

  update_index(f"- **{next_item['title']}** — {next_item['desc']} (`tools/{slug}/`)")

  pr_body_file = ROOT / ".forgebot" / "pr_body.md"
  pr_body_file.parent.mkdir(parents=True, exist_ok=True)
  pr_body_file.write_text(
    f"### {next_item['title']}\n\n"
    f"- {next_item['desc']}\n"
    f"- Added at: {ctx['DATE_UTC']}\n"
    f"- Location: `tools/{slug}/`\n\n"
    f"Links:\n"
    f"- Site: {ctx['WEBSITE']}\n"
    f"- Marketplace: {ctx['WEBSITE']}/marketplace\n",
    encoding="utf-8",
  )

  state["used_ids"] = list(used | {tool_id})
  jsave(STATE_PATH, state)

  jsave(out_path, {
    "tool_id": tool_id,
    "slug": slug,
    "branch": f"forgebot/{date_ymd}-{slug}",
    "title": next_item["title"],
    "body_file": str(pr_body_file),
  })

def main():
  ap = argparse.ArgumentParser()
  ap.add_argument("--out", default=str(LAST_RUN_PATH_DEFAULT))
  args = ap.parse_args()
  cmd_generate(Path(args.out))

if __name__ == "__main__":
  main()
