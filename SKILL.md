---
name: info-card-designer
description: |
  将任意文本/信息转化为杂志质感 HTML 信息卡片，并自动截图保存为图片。
  适合分享到 X (Twitter)、微信、小红书等平台。
  触发词："生成信息卡"、"做张信息卡"、"把这段内容做成卡片"、"信息卡片"、"make info card"、"generate card"。
  卡片特点：大字号、强排版张力、瑞士国际主义 + 杂志质感风格，生成后自动截图，超长自动分割输出图片。
---

# Info Card Designer

将任意内容转化为杂志质感信息卡，自动截图 + 超长分割，适配 X/Twitter、小红书分享。

## 工作流

### Step 1：分析内容密度

- **低密度**（1 个核心观点）→ 大字符主义布局
- **中密度**（2-4 要点）→ 标准单栏布局
- **高密度**（5+ 要点）→ 多栏网格布局

### Step 2：生成 HTML

读取 `references/design-spec.md` 获取完整规范。

**硬性约束**：
- 卡片宽度：默认 **600px**，可指定 480 / 600 / 900（用户说"480宽"/"900宽"时生效）
- `<meta name="viewport" content="width=[指定宽度]">` 防缩放
- 背景色 `#f5f3ed`
- 截图时 `resize_page` width 设为指定宽度

**字号用 vw 单位，随宽度自动缩放**：
- 主标题：`font-size: clamp(40px, 13vw, 130px)` — 480px→62px / 600px→78px / 900px→117px
- 条目标题：`font-size: clamp(16px, 4vw, 40px)` — 480px→19px / 600px→24px / 900px→36px
- 正文：`font-size: clamp(14px, 3.2vw, 24px)` — 480px→15px / 600px→19px / 900px→28px
- 辅助/标签：`font-size: clamp(11px, 2.2vw, 16px)`

**内容原则（强制）**：
- 卡片内容必须 100% 来自用户提供的原文/URL/文本，严禁自行编造或使用占位符
- 标题、描述、来源、金句均须与原文一致，Hook 改写只改表达方式，不改事实

**描述风格（Hook 模式，默认开启）**：
- 每条描述改写为 **10-20 字的钩子句**，有信息量 + 有冲击感
- 保留核心事实，用主动语态，让读者想点进去看
- 用户说"保持原文"或"不改描述"时关闭

保存路径：`/tmp/info-card-[关键词].html`

### Step 3：截图（必须执行）

优先用 **Chrome DevTools MCP**：

1. `navigate_page` → `file:///tmp/info-card-xxx.html`
2. `resize_page` → width=600, height=900
3. `take_screenshot` → fullPage=true, filePath=[初始路径]

### Step 4：超长分割

截图后检查图片高度。**若高度 > 1200px**，执行分割：

```bash
python3 ~/.claude/skills/info-card-designer/scripts/split_card.py [图片路径] 1200
```

分割后输出 `card-1.png`, `card-2.png` ... 等文件。

### Step 5：整理并输出

**保存路径规则**：
```
~/乔木新知识库/60-69 素材/65 附件库/info-cards/
  └── [YYYYMMDD]-[来源]-[主题关键词]/
        ├── card.png          # 未分割时
        ├── card-1.png        # 分割时
        └── card-2.png
```

示例：`info-cards/20260316-wisereads-134/card-1.png`

> 文件夹名格式：`日期-来源-主题`，一目了然

告知用户：图片路径 + 共几张

---

## 设计速查

完整规范见 `references/design-spec.md`。

| 场景 | 布局 | 主标题字号 | 正文字号 |
|------|------|-----------|---------|
| 低密度 | 大字符主义 | 72-120px | 20px |
| 中密度 | 标准单栏 | 48-56px | 18px |
| 高密度 | 2-3 栏网格 | 36-44px | 16px |

**字体**：标题 `Noto Serif SC`；正文 `Inter / Noto Sans SC`

**配色**：靛蓝 `#1a3a6b`（知识）/ 深红 `#c0392b`（警示）/ 墨绿 `#1a4a3a`（生活）/ 深金 `#8b6914`（财经）
