#!/data/data/com.termux/files/usr/bin/bash
set -e
cd "$HOME/ironjesus-lab"
git add .
git commit -m "${1:-update $(date +%F_%T)}" || true
git push
