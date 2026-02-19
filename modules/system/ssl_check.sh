#!/data/data/com.termux/files/usr/bin/bash
set -e

source "$(dirname "$0")/../../lib/log.sh"

HOST="${1:-}"
PORT="${2:-443}"

[ -z "$HOST" ] && { log_error "Usage: ij system ssl <host> [port]"; exit 1; }

# Fetch cert dates
OUT="$(echo | openssl s_client -servername "$HOST" -connect "$HOST:$PORT" 2>/dev/null | openssl x509 -noout -dates -issuer -subject 2>/dev/null || true)"

if [ -z "$OUT" ]; then
  log_error "Could not fetch certificate for $HOST:$PORT"
  exit 2
fi

NOT_AFTER="$(echo "$OUT" | awk -F= '/notAfter/ {print $2}')"
ISSUER="$(echo "$OUT" | awk -F= '/issuer/ {print $2}')"

# Convert to epoch (Termux: date -d works with coreutils)
EXP_EPOCH="$(date -d "$NOT_AFTER" +%s 2>/dev/null || echo "")"
NOW_EPOCH="$(date +%s)"

if [ -z "$EXP_EPOCH" ]; then
  log_warn "Expiry: $NOT_AFTER"
  log_info "Issuer: $ISSUER"
  exit 0
fi

DAYS_LEFT="$(( (EXP_EPOCH - NOW_EPOCH) / 86400 ))"

if [ "$DAYS_LEFT" -le 7 ]; then
  log_error "$HOST:$PORT expires in $DAYS_LEFT days  |  $NOT_AFTER"
elif [ "$DAYS_LEFT" -le 30 ]; then
  log_warn "$HOST:$PORT expires in $DAYS_LEFT days  |  $NOT_AFTER"
else
  log_info "$HOST:$PORT expires in $DAYS_LEFT days  |  $NOT_AFTER"
fi

log_info "Issuer: $ISSUER"
