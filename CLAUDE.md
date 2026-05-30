# sarasa-nerd-builder

用最新版 Sarasa Gothic + Nerd Fonts 素材，重新生成 Sarasa Term SC Nerd 字体。
复刻 [laishulu/Sarasa-Term-SC-Nerd](https://github.com/laishulu/Sarasa-Term-SC-Nerd) 的思路，但追踪上游最新版本。

## 目标

- 输入：Sarasa Gothic TTF + Nerd Fonts FontPatcher
- 输出：`SarasaTermSCNerd-*.ttf`（各字重）+ `SarasaTermSCNerd.ttc`（合集）
- 构建环境：Git Bash on Windows

## 目录结构

```
sarasa-nerd-builder/
├── CLAUDE.md               # 本文件
├── config.sh               # 版本号与工具路径配置（修改这里来更新）
├── .gitignore
├── font-patcher            # 修改后的 patcher（由 patch_patcher.py 生成，不进 git）
├── glyphnames.json         # Nerd Fonts 提供（构建时自动复制，不进 git）
├── bin/                    # Nerd Fonts 辅助脚本（构建时自动复制，不进 git）
├── sarasa/                 # 源字体 TTF（从 Sarasa Gothic 解压，不进 git）
├── nerd-patcher/           # FontPatcher 原始文件（解压自 FontPatcher.zip，不进 git）
├── output/                 # 构建产物（不进 git）
│   ├── SarasaTermSCNerd-*.ttf
│   ├── SarasaTermSCNerd.ttc
│   └── *.7z / *.tar.gz
└── scripts/
    ├── update.sh           # 一键更新脚本（下载+解压+patch+构建）
    ├── build.sh            # 主构建脚本（被 update.sh 调用）
    ├── patch_patcher.py    # 以 Python 方式将 11 处改动写入 font-patcher
    └── otf2otc.py          # TTF → TTC 合并工具（来自 Adobe）
```

## 当前版本锁定

| 组件 | 版本 |
|---|---|
| Sarasa Gothic | v1.0.39 |
| Nerd Fonts | v3.4.0 (script_version 4.20.3) |
| FontForge | 20251009 |

## 更新流程

上游发布新版本时：

1. 编辑 `config.sh`，修改 `SARASA_VERSION` 和/或 `NERD_VERSION`
2. 在 Git Bash 中执行：
   ```bash
   bash scripts/update.sh
   ```
3. 脚本自动完成：下载 → 解压 → 应用 patch → 构建 → 打包
4. 产物在 `output/`，发布到 GitHub Release

**注意**：如果 Nerd Fonts 版本跨度较大，`patch_patcher.py` 中的 11 处改动可能需要调整（见下方"改动清单"）。构建时若报错，通常是某个字符串匹配失败，在脚本里找对应的 `text.replace(...)` 行修正即可。

## 对 font-patcher 的改动清单

原始思路来自 laishulu，针对 Nerd Fonts 4.16.1 的 `.patch` 文件。本项目改为 Python 字符串替换实现，适配 4.20.3，共 11 处，全部以 `# FOR SARASA` 注释标记。

### 改动逐条说明

1. **文件头变量**：覆盖 `projectName` 为 `"Nerds"`，定义 `looseName = "Sarasa Term SC Nerd"`、`compactName = "SarasaTermSCNerd"`

2. **`check_panose_monospaced()`**：强制 `return 1`（跳过等宽检测）

3. **`is_monospaced()`**：强制 `return (True, None)`

4. **输出文件名**：改为 `f'{compactName}-{self.get_subfamily()}.ttf'`

5. **Material Design Icons 分段**：将 `0xF0001-0xF1AF0` 拆为 11 段，排除空段以控制字形数量（见下方"MDI 范围裁剪说明"）

6. **后缀清理（两处）**：清除 Mono/Propo 等变体后缀

7. **变体缩写清零**：`variant_abbrev = ""`、`variant_full = ""`

8. **双语 SFNT 命名注入**：向 Name Table 写入英文和中文（PRC）字体名称

9. **`font_dim` 加 `'em'` 字段**：`self.font_dim['em'] = self.sourceFont.em`

10. **`get_target_width()` 强制返回 1**：禁用双宽字形判断

11. **末尾新增函数**：`get_subfamily()`、`post_fix()`、`build_hdmx()`、`fix_isFixedPitch()`、`zh_family()`、`zh_subfamily()`、`en_subfamily()`

## MDI 范围裁剪说明

Nerd Fonts 原始的 Material Design Icons 范围 `0xF0001-0xF1AF0` 包含约 6933 个字形。
Sarasa Term SC Regular 基础字形数为 56862，加上所有非 MDI 图标约 2498 个，
再加 MDI 全量会超过 OpenType 65534 字形上限。

本项目采用 laishulu 的分段方案，并针对 Sarasa v1.0.39 的字形数额外裁剪：
将第 4 段的 SymEnd 从 `0xF118E` 收窄至 `0xF0FFF`（削减约 399 个码点）。
该区段在 Nerd Fonts 3.4.0 的 `MaterialDesignIconsDesktop.ttf` 中字形分布均匀，
无自然空隙，因此按页对齐截断。最终字形总数约 65481，在上限以内。

## 验证

构建后检查：
- `output/` 中有 10 个 TTF（Regular/Bold/Light/SemiBold/ExtraLight × 各 Italic）
- `SarasaTermSCNerd.ttc` 存在
- 字形数 ≤ 65534（用 FontForge 打开验证）
- Powerline 符号（U+E0B0）、Nerd 图标（U+E001）、MDI 图标（U+F0001）均存在

## 依赖（Windows）

- **FontForge**（含 ffpython.exe）：https://fontforge.org/
- **Anaconda Python**（含 fonttools）：`pip install fonttools`
- **7-Zip**：https://www.7-zip.org/
- **Git Bash**：https://gitforwindows.org/

工具路径在 `config.sh` 中配置，安装位置不同时修改对应变量即可。

## 不做的事

- 不修改 Sarasa Gothic 本体字形
- 不改变 Nerd Fonts 图标的 Unicode 码位
- 不包含非 SC（简体中文）变体
- 构建产物不进 git（output/ 已在 .gitignore）
