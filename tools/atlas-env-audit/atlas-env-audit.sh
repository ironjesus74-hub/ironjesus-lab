#!/usr/bin/env bash
set -euo pipefail
# Atlas Env Audit | Local environment inventory (OS/CPU/disk + tool versions) with safe output.
# Built Different — https://forge-atlas.io | 2026-02-25T06:44:23.050247Z

have(){ command -v "$1" >/dev/null 2>&1; }

echo "atlas_title=Atlas Env Audit"
echo "atlas_tool_id=op-env-audit-001"
echo "atlas_created_utc=2026-02-25T06:44:23.050247Z"
echo "atlas_site=https://forge-atlas.io"
echo "atlas_github=https://github.com/ironjesus74-hub"
echo
echo "uname=$(uname -a 2>/dev/null || true)"
if have df; then echo "disk_root=$(df -h / 2>/dev/null | tail -n 1 | awk '{print $2" total, "$4" free"}')"; fi
for t in git python3 node npm docker kubectl terraform; do
  if have "$t"; then echo "tool_${t}=$("$t" --version 2>/dev/null | head -n 1 || true)"; else echo "tool_${t}=missing"; fi
done
