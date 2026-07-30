# Sarasa Term SC Nerd

> **本项目是 [laishulu/Sarasa-Term-SC-Nerd](https://github.com/laishulu/Sarasa-Term-SC-Nerd) 的更新版本**，使用最新的 Sarasa Gothic 和 Nerd Fonts 重新构建，原项目已停止更新。

[更纱终端书呆黑体-简](https://github.com/be5invis/Sarasa-Gothic)与 [Nerd Fonts](https://github.com/ryanoasis/nerd-fonts) 图标合并的中文等宽字体，适用于终端和代码编辑器。

## 当前版本

| 组件 | 版本 |
|---|---|
| Sarasa Gothic | v1.0.40 |
| Nerd Fonts | v3.4.0 |

## 下载安装

从 [Releases](../../releases) 页面下载字体包：

- `SarasaTermSCNerd.ttf.7z` — 10 个独立 TTF（按字重分开，推荐）
- `SarasaTermSCNerd.ttc.7z` — 单个 TTC 合集文件

解压后，Windows 下全选 TTF 文件，右键 → **为所有用户安装**。

## 字重

| 文件名 | 字重 |
|---|---|
| SarasaTermSCNerd-ExtraLight.ttf | 特细 |
| SarasaTermSCNerd-ExtraLightItalic.ttf | 特细斜体 |
| SarasaTermSCNerd-Light.ttf | 细 |
| SarasaTermSCNerd-LightItalic.ttf | 细斜体 |
| SarasaTermSCNerd-Regular.ttf | 常规 |
| SarasaTermSCNerd-Italic.ttf | 斜体 |
| SarasaTermSCNerd-SemiBold.ttf | 中粗 |
| SarasaTermSCNerd-SemiBoldItalic.ttf | 中粗斜体 |
| SarasaTermSCNerd-Bold.ttf | 粗 |
| SarasaTermSCNerd-BoldItalic.ttf | 粗斜体 |

## 自行构建

### 环境要求（Windows）

- [FontForge](https://fontforge.org/) — 字体处理（提供 ffpython.exe）
- [Anaconda Python](https://www.anaconda.com/) + `pip install fonttools`
- [7-Zip](https://www.7-zip.org/)
- [Git Bash](https://gitforwindows.org/)

### 步骤

1. 克隆本仓库
2. 根据实际安装路径编辑 `config.sh`（工具路径）
3. 在 Git Bash 中运行：
   ```bash
   bash scripts/update.sh
   ```
4. 产物输出到 `output/`

### 更新上游版本

编辑 `config.sh` 中的版本号，再次运行 `bash scripts/update.sh` 即可。

## 与原项目的区别

| 方面 | laishulu/Sarasa-Term-SC-Nerd | 本项目 |
|---|---|---|
| 构建环境 | Ubuntu / macOS | Windows (Git Bash) |
| Patch 方式 | `.patch` 文件 | Python 字符串替换 |
| 版本追踪 | 停留在旧版本 | 持续跟进上游 |
| CI | GitHub Actions | 手动构建 |

## 致谢

- [laishulu](https://github.com/laishulu) — 原始 patch 方案和改动思路
- [be5invis](https://github.com/be5invis) — [Sarasa Gothic](https://github.com/be5invis/Sarasa-Gothic) 字体
- [ryanoasis](https://github.com/ryanoasis) — [Nerd Fonts](https://github.com/ryanoasis/nerd-fonts) 图标集

## 许可证

[SIL Open Font License 1.1](LICENSE)

---

*本项目由 [Claude Code](https://claude.ai/code) 辅助生成。*
