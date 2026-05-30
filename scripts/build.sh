#!/bin/bash -xeu
# Main build script.
# 通常通过 scripts/update.sh 调用；也可单独运行：bash scripts/build.sh

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
source "$ROOT/config.sh"

SARASA_DIR="$ROOT/sarasa"
PATCHER="$ROOT/font-patcher"
GLYPH_DIR="$ROOT/nerd-patcher/src"
OUTPUT_DIR="$ROOT/output"

# Validate prerequisites
if [ ! -f "$PATCHER" ]; then
  echo "ERROR: font-patcher not found. Run: bash scripts/update.sh"
  exit 1
fi
if [ ! -d "$GLYPH_DIR" ]; then
  echo "ERROR: nerd-patcher/src/ not found. Run: bash scripts/update.sh"
  exit 1
fi
if [ -z "$(ls "$SARASA_DIR"/*.ttf 2>/dev/null)" ]; then
  echo "ERROR: No TTF files in sarasa/. Run: bash scripts/update.sh"
  exit 1
fi

mkdir -p "$OUTPUT_DIR"

# Step 1: patch each TTF
for item in "$SARASA_DIR"/*.ttf; do
  echo "Patching: $item"
  "$FFPYTHON" "$PATCHER" --quiet --adjust-line-height --complete --careful \
    --glyphdir "$GLYPH_DIR/glyphs" \
    --outputdir "$OUTPUT_DIR" \
    "$item"
done

echo "=== Generated TTF files ==="
ls "$OUTPUT_DIR"/*.ttf

# Step 2: merge into TTC
echo "=== Merging into TTC ==="
"$ANACONDA_PYTHON" "$ROOT/scripts/otf2otc.py" \
  -o "$OUTPUT_DIR/SarasaTermSCNerd.ttc" \
  "$OUTPUT_DIR"/SarasaTermSCNerd-*.ttf

# Step 3: package
cd "$OUTPUT_DIR"
echo "=== Creating archives ==="
COPYFILE_DISABLE=1 tar -czvf SarasaTermSCNerd.ttf.tar.gz SarasaTermSCNerd-*.ttf
COPYFILE_DISABLE=1 tar -czvf SarasaTermSCNerd.ttc.tar.gz SarasaTermSCNerd.ttc
"$SEVENZIP" a -mx9 SarasaTermSCNerd.ttf.7z SarasaTermSCNerd-*.ttf
"$SEVENZIP" a -mx9 SarasaTermSCNerd.ttc.7z SarasaTermSCNerd.ttc

echo "=== Done. Output in $OUTPUT_DIR ==="
