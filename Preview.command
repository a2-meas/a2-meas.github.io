#!/bin/zsh
cd -- "${0:A:h}" || exit 1
if ! command -v python3 >/dev/null 2>&1; then
  echo 'Python 3 is required. Install it from https://www.python.org/downloads/ and run this again.'
  read -r '?Press Enter to close.'
  exit 1
fi
echo 'Open http://127.0.0.1:4173 in your browser. Press Ctrl+C to stop.'
python3 scripts/serve.py --port 4173
