#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail
LOG_DIR="${LOG_DIR:-$HOME/ironjesus-lab/logs}"
mkdir -p "$LOG_DIR"
ts(){ date +"%Y-%m-%d %H:%M:%S"; }
log(){ echo "[$(ts)] $*" | tee -a "$LOG_DIR/run.log" >/dev/null; }
die(){ echo "ERROR: $*" >&2; exit 1; }
need(){ command -v "$1" >/dev/null 2>&1 || die "Missing dependency: $1"; }
color(){
  local c="$1"; shift
  case "$c" in
    red)    printf "\033[31m%s\033[0m\n" "$*";;
    green)  printf "\033[32m%s\033[0m\n" "$*";;
    yellow) printf "\033[33m%s\033[0m\n" "$*";;
    blue)   printf "\033[34m%s\033[0m\n" "$*";;
    *)      echo "$*";;
  esac
}
