#!/data/data/com.termux/files/usr/bin/bash
set -e

BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$BASE_DIR/../../lib/log.sh"

cmd="${1:-help}"
shift || true

case "$cmd" in
  ssl)
    "$BASE_DIR/ssl_check.sh" "$@"
    ;;
  port)
    "$BASE_DIR/port_check.sh" "$@"
    ;;
  snapshot)
    "$BASE_DIR/snapshot.sh" "$@"
    ;;
  help|"")
    echo "ij system commands:"
    echo "  ij system ssl <host> [port]        # SSL expiry + issuer"
    echo "  ij system port <host> <port>       # TCP reachability"
    echo "  ij system snapshot                 # system + network snapshot"
    ;;
  *)
    log_error "Unknown system command: $cmd"
    exit 1
    ;;
esac
