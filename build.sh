#!/usr/bin/env bash
# Gera dist/claude-links-<versão>.zip só com os arquivos da extensão.
set -euo pipefail
cd "$(dirname "$0")"
version=$(python3 -c 'import json;print(json.load(open("manifest.json"))["version"])')
mkdir -p dist
out="dist/claude-links-$version.zip"
rm -f "$out"
zip -q -r "$out" manifest.json background.js content.js defaults.js options.html options.js \
  icons/icon-16.png icons/icon-32.png icons/icon-48.png icons/icon-128.png
echo "$out"
unzip -l "$out" | tail -n +4 | head -n -2
