#!/usr/bin/env bash
# Run on a Linux host or inside a rooted adb/waydroid shell.
set -euo pipefail

echo "== identity =="
id || true
uname -a || true

echo "== kernel =="
cat /proc/version 2>/dev/null || true

echo "== mounts (first 20) =="
mount 2>/dev/null | head -n 20 || true

echo "== processes (first 30) =="
(ps -A || ps) 2>/dev/null | head -n 30 || true

echo "== cgroups =="
cat /proc/1/cgroup 2>/dev/null || true

echo "Aether next step: install the Python daemon as a user service, do not touch the kernel yet."
