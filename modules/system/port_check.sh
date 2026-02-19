#!/data/data/com.termux/files/usr/bin/bash
set -e

source "$(dirname "$0")/../../lib/log.sh"

HOST="${1:-}"
PORT="${2:-}"

[ -z "$HOST" ] || [ -z "$PORT" ] && { log_error "Usage: ij system port <host> <port>"; exit 1; }

if nc -z -w 3 "$HOST" "$PORT" >/dev/null 2>&1; then
  log_success "OPEN  $HOST:$PORT"
  exit 0
else
  log_error "CLOSED/FAIL  $HOST:$PORT"
  exit 2
fi
