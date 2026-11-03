#!/usr/bin/env bash
# Publica uma versão: ajusta o manifest, gera o zip, faz commit, cria a tag
# vX.Y.Z e o release no GitHub com o zip anexado.
#
#   ./release.sh 1.2.0
#
# Antes: escreva a seção da versão no CHANGELOG.md (vira a nota do release).
set -euo pipefail
cd "$(dirname "$0")"

version="${1:?uso: ./release.sh X.Y.Z}"
[[ "$version" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]] || { echo "versão fora do SemVer: $version" >&2; exit 1; }
tag="v$version"
git rev-parse -q --verify "refs/tags/$tag" >/dev/null && { echo "tag $tag já existe" >&2; exit 1; }
grep -q "^## \[$version\]" CHANGELOG.md || { echo "falta a seção [$version] no CHANGELOG.md" >&2; exit 1; }

python3 - "$version" <<'EOF'
import json, sys
d = json.load(open('manifest.json'))
d['version'] = sys.argv[1]
open('manifest.json', 'w').write(json.dumps(d, indent=2, ensure_ascii=False) + '\n')
EOF

# Sem pipe para head: com pipefail, o SIGPIPE do build.sh derrubaria o script.
build_out=$(./build.sh)
zip=${build_out%%$'\n'*}

# Nota do release = seção da versão no CHANGELOG.
notes=$(awk -v v="$version" '
  $0 ~ "^## \\[" v "\\]" { on = 1; next }
  on && /^## \[/ { exit }
  on && /^\[/ { exit }
  on { print }
' CHANGELOG.md)

git add manifest.json CHANGELOG.md
git commit -q -m "chore(release): $tag" || true
git tag -a "$tag" -m "$tag"
git push -q origin HEAD "$tag"
gh release create "$tag" "$zip" --title "$tag" --notes "$notes"
echo "release $tag publicado com $zip"
