# info-card-designer

> Turn any text or URL into a magazine-quality info card image — auto screenshot included.
> 将任意文本或链接一键转化为杂志质感信息卡片，自动截图输出图片，适合分享到 X、小红书、微信。

**[English](#english) | [中文](#中文)**

---

<a name="english"></a>
## English

### What it does

Give Claude a URL, paste text, or describe a topic — this skill designs a magazine-style HTML info card and **automatically screenshots it to PNG** ready to post on X (Twitter), Xiaohongshu, or WeChat.

**Key features:**
- Swiss International Style + editorial magazine aesthetic
- Big titles, punchy hook-style summaries (10–20 chars each)
- Supports 480 / 600 / 900px width — just say "make it 480px wide"
- Auto-splits cards taller than 1200px into multiple images
- vw-based font sizing: fonts scale proportionally with card width

### Prerequisites

- [ ] **Chrome DevTools MCP** installed and connected (used for headless screenshot)
  - Install: add `chrome-devtools` MCP server to your Claude Code config
  - Verify: Claude can call `navigate_page`, `take_screenshot`
- [ ] **Python 3** with Pillow (for image splitting)
  - Install: `pip3 install Pillow`
  - Verify: `python3 -c "from PIL import Image; print('ok')"`

### Installation

```bash
npx skills add joeseesun/info-card-designer
```

### How to trigger

Say any of these to Claude:

- "生成信息卡" / "做张信息卡" / "信息卡片"
- "把这段内容做成卡片"
- "make info card" / "generate card"

### Usage examples

```
用户: 把这个链接做成信息卡 https://wise.readwise.io/issues/wisereads-vol-134/
用户: 把这段内容做成 480 宽的信息卡
用户: generate a card from this text, keep the original descriptions
```

### Width options

| Width | Best for |
|-------|----------|
| 480px | Mobile-first, compact |
| 600px | Default, balanced (recommended) |
| 900px | Desktop / large-screen sharing |

### Troubleshooting

| Problem | Solution |
|---------|----------|
| Screenshot fails / page not found | Make sure Chrome DevTools MCP is connected and Chrome is running |
| `No module named PIL` | Run `pip3 install Pillow` |
| Card content is wrong / made up | The skill is instructed to use only your source content — re-trigger with the URL or paste the text directly |
| Card too tall (1 image) | Splitting is automatic when height > 1200px; check that Pillow is installed |

---

<a name="中文"></a>
## 中文

### 功能说明

给 Claude 一个 URL、粘贴一段文字，或描述一个主题——这个 skill 会自动设计成杂志质感 HTML 信息卡，并**自动截图输出 PNG**，可直接发到 X、小红书、微信。

**核心特点：**
- 瑞士国际主义 + 杂志编辑风格
- 大标题、强视觉张力
- Hook 模式（默认开启）：每条描述改写为 10-20 字钩子句，有冲击感
- 支持 480 / 600 / 900px 宽度，说"生成 480 宽的卡片"即可切换
- 超长卡片（>1200px）自动分割成多张图

### 前置条件

- [ ] **Chrome DevTools MCP** 已安装并连接
  - 用于无头截图（headless screenshot）
  - 验证：Claude 能调用 `navigate_page`、`take_screenshot`
- [ ] **Python 3 + Pillow**（用于超长图片分割）
  - 安装：`pip3 install Pillow`
  - 验证：`python3 -c "from PIL import Image; print('ok')"`

### 安装

```bash
npx skills add joeseesun/info-card-designer
```

### 触发方式

对 Claude 说：

- "生成信息卡"
- "做张信息卡"
- "把这段内容做成卡片"
- "信息卡片"
- "make info card" / "generate card"

### 使用示例

```
把这个链接做成信息卡：https://wise.readwise.io/issues/wisereads-vol-134/
把这段文字做成 480 宽的卡片
生成信息卡，保持原文描述
```

### Hook 模式开关

| 说法 | 效果 |
|------|------|
| 默认 | 自动将描述改写为 10-20 字钩子句 |
| "保持原文" / "不改描述" | 使用原始文字，不改写 |

### 常见问题

| 问题 | 解决方法 |
|------|----------|
| 截图失败 | 检查 Chrome DevTools MCP 是否已连接 |
| `No module named PIL` | 运行 `pip3 install Pillow` |
| 内容不对 / 有编造 | 提供原文链接或直接粘贴文本，重新触发 |
| 超长卡没有分割 | 确认 Pillow 已安装，高度 >1200px 才触发分割 |
