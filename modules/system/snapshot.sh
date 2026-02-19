#!/data/data/com.termux/files/usr/bin/bash
set -e

source "$(dirname "$0")/../../lib/log.sh"

TS="$(date +%Y%m%d_%H%M%S)"
OUT="snapshot_$TS.txt"

{
  echo "=== IronJesus Snapshot ==="
  echo "Date: $(date)"
  echo

  echo "--- System ---"
  uname -a || true
  echo
  echo "Android: $(getprop ro.build.version.release 2>/dev/null || echo n/a)"
  echo "Model:   $(getprop ro.product.model 2>/dev/null || echo n/a)"
  echo

  echo "--- Storage ---"
  df -h 2>/dev/null || true
  echo

  echo "--- Network ---"
  ip a 2>/dev/null || true
  echo
  echo "DNS:"
  getprop | grep -i dns 2>/dev/null || true
  echo

  echo "--- Connectivity ---"
  ping -c 1 -W 2 1.1.1.1 2>/dev/null && echo "Ping 1.1.1.1: OK" || echo "Ping 1.1.1.1: FAIL"
  ping -c 1 -W 2 google.com 2>/dev/null && echo "Ping google.com: OK" || echo "Ping google.com: FAIL"
  echo
} > "$OUT"

log_success "Saved: $OUT"
