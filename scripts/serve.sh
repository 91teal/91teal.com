#!/bin/sh
set -eu

PORT="${1:-8000}"

case "$PORT" in
  *[!0-9]*|'')
    echo "Port must be a number." >&2
    exit 2
    ;;
esac

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
SITE_DIR=$(dirname -- "$SCRIPT_DIR")

echo "Previewing 91teal.com at http://localhost:$PORT"
echo "Press Control-C to stop."
cd "$SITE_DIR"
exec python3 -m http.server "$PORT" --bind 127.0.0.1
