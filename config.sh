#!/bin/bash
# config.sh — 版本号和工具路径配置
# 上游更新时只需修改这里，然后运行 bash scripts/update.sh

# ── 版本号 ────────────────────────────────────────────────────────────────────
# Sarasa Gothic 最新版本：https://github.com/be5invis/Sarasa-Gothic/releases
SARASA_VERSION="1.0.39"

# Nerd Fonts 最新版本：https://github.com/ryanoasis/nerd-fonts/releases
NERD_VERSION="3.4.0"

# ── Windows 工具路径 ───────────────────────────────────────────────────────────
# FontForge（含 ffpython.exe）：https://fontforge.org/
FFPYTHON="C:/Program Files/FontForgeBuilds/bin/ffpython.exe"

# Anaconda Python（需安装 fonttools：pip install fonttools）
ANACONDA_PYTHON="D:/softwares/anaconda3/python.exe"

# 7-Zip：https://www.7-zip.org/
SEVENZIP="C:/Program Files/7-Zip/7z.exe"

# fonttools 所在的 site-packages（自动从 ANACONDA_PYTHON 推导）
export PYTHONPATH="$(dirname "$ANACONDA_PYTHON")/Lib/site-packages"
