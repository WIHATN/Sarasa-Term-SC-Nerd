#!/bin/bash -eu
# scripts/update.sh — 一键更新脚本
#
# 用法：bash scripts/update.sh
#   版本号从 config.sh 读取，在那里修改后再运行本脚本
#
# 本脚本完成：
#   1. 下载最新 Sarasa Gothic TTF 和 Nerd Fonts FontPatcher
#   2. 解压到对应目录
#   3. 应用 patch 生成修改后的 font-patcher
#   4. 构建字体（调用 scripts/build.sh）

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
source "$ROOT/config.sh"

SARASA_ARCHIVE="SarasaTermSC-TTF-${SARASA_VERSION}.7z"
PATCHER_ARCHIVE="FontPatcher.zip"
SARASA_URL="https://github.com/be5invis/Sarasa-Gothic/releases/download/v${SARASA_VERSION}/${SARASA_ARCHIVE}"
PATCHER_URL="https://github.com/ryanoasis/nerd-fonts/releases/download/v${NERD_VERSION}/${PATCHER_ARCHIVE}"

echo "=========================================="
echo " Sarasa Term SC Nerd — 更新脚本"
echo " Sarasa Gothic : v${SARASA_VERSION}"
echo " Nerd Fonts    : v${NERD_VERSION}"
echo "=========================================="

# ── Step 1: 下载 ──────────────────────────────────────────────────────────────
echo ""
echo "=== Step 1/4: 下载素材 ==="

if [ -f "$ROOT/$SARASA_ARCHIVE" ]; then
    echo "  已存在 $SARASA_ARCHIVE，跳过下载"
else
    echo "  下载 Sarasa Gothic v${SARASA_VERSION}..."
    curl -L --max-redirs 5 -o "$ROOT/$SARASA_ARCHIVE" "$SARASA_URL"
fi

if [ -f "$ROOT/$PATCHER_ARCHIVE" ]; then
    echo "  已存在 $PATCHER_ARCHIVE，跳过下载"
else
    echo "  下载 Nerd Fonts FontPatcher v${NERD_VERSION}..."
    curl -L --max-redirs 5 -o "$ROOT/$PATCHER_ARCHIVE" "$PATCHER_URL"
fi

# ── Step 2: 解压 ──────────────────────────────────────────────────────────────
echo ""
echo "=== Step 2/4: 解压素材 ==="

echo "  清理旧的 sarasa/ 和 nerd-patcher/ ..."
rm -rf "$ROOT/sarasa" "$ROOT/nerd-patcher" "$ROOT/font-patcher" "$ROOT/bin" "$ROOT/glyphnames.json"

echo "  解压 Sarasa Gothic TTF..."
mkdir -p "$ROOT/sarasa"
"$SEVENZIP" x "$ROOT/$SARASA_ARCHIVE" -o"$ROOT/sarasa/" -y > /dev/null

echo "  解压 Nerd Fonts FontPatcher..."
mkdir -p "$ROOT/nerd-patcher"
"$SEVENZIP" x "$ROOT/$PATCHER_ARCHIVE" -o"$ROOT/nerd-patcher/" -y > /dev/null

echo "  复制运行时文件（bin/、glyphnames.json）..."
cp -r "$ROOT/nerd-patcher/bin" "$ROOT/bin"
cp "$ROOT/nerd-patcher/glyphnames.json" "$ROOT/glyphnames.json"

# ── Step 3: 应用 patch ────────────────────────────────────────────────────────
echo ""
echo "=== Step 3/4: 应用 patch ==="

cp "$ROOT/nerd-patcher/font-patcher" "$ROOT/font-patcher"
"$ANACONDA_PYTHON" "$ROOT/scripts/patch_patcher.py" "$ROOT/font-patcher"

# ── Step 4: 构建 ──────────────────────────────────────────────────────────────
echo ""
echo "=== Step 4/4: 构建字体 ==="
bash "$ROOT/scripts/build.sh"

echo ""
echo "=========================================="
echo " 完成！产物在 output/ 目录："
ls "$ROOT/output/"*.ttf 2>/dev/null | xargs -I{} basename {}
echo " 压缩包："
ls "$ROOT/output/"*.7z 2>/dev/null | xargs -I{} basename {}
echo "=========================================="
