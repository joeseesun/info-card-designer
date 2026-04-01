---
name: qiaomu-info-card-designer
description: |
  将任意文本/URL/信息转化为杂志质感 HTML 信息卡片，并自动截图保存为图片。
  支持直接输入 URL（X/Twitter、网页文章等），自动抓取内容、提炼要点、生成卡片。
  适合分享到 X (Twitter)、微信、小红书等平台。
  触发词："生成信息卡"、"做张信息卡"、"把这段内容做成卡片"、"信息卡片"、"make info card"、"generate card"、"把这个链接做成卡片"。
  卡片特点：大字号、强排版张力、瑞士国际主义 + 杂志质感风格，生成后自动截图，超长智能分割输出图片。
---

# Info Card Designer

将任意内容转化为杂志质感信息卡，自动截图 + 超长分割，适配 X/Twitter、微信、小红书分享。

## 工作流

### Step 0：获取内容（如果输入是 URL）

如果用户给的是 URL 而非纯文本，先抓取内容再进入 Step 1。

**路由规则**：

| URL 类型 | 抓取方式 |
|----------|---------|
| `arxiv.org/abs/` | 提取论文 ID，优先抓 HTML 版 `https://arxiv.org/html/{id}v1`，失败则抓 PDF `https://arxiv.org/pdf/{id}.pdf` |
| `x.com` / `twitter.com` | `curl -sL "https://r.jina.ai/{url}"` |
| `mp.weixin.qq.com` | `python3 ~/.claude/skills/markdown-proxy/scripts/fetch_weixin.py "{url}"` （如存在） |
| 其他网页 | `curl -sL "https://r.jina.ai/{url}"`，失败则 `curl -sL "https://defuddle.md/{url}"` |

**arXiv 专用逻辑**（抓全文，不是摘要）：
```bash
# 从 https://arxiv.org/abs/2603.25694 提取 ID
paper_id=$(echo "$url" | grep -oP 'arxiv.org/abs/\K[\d.]+')

# 优先抓 HTML 版（内容最完整）
html_url="https://arxiv.org/html/${paper_id}v1"
curl -sL "$html_url" 2>/dev/null || curl -sL "https://r.jina.ai/https://arxiv.org/pdf/${paper_id}.pdf"
```

**通用代码**（覆盖 90% 场景）：
```bash
curl -sL "https://r.jina.ai/{url}" 2>/dev/null
```

> **原则**：skill 自己能抓就自己抓，不依赖外部 skill。r.jina.ai 免费、无需 API key、支持 X/Twitter/普通网页。arXiv 论文优先抓 HTML 版（比 PDF 更易提取），只有公众号等特殊页面才回退到专用脚本。

### Step 1：提炼核心信息（最重要）

> **目标**：让读者只看图片就能理解文章最核心、最重要的概念和信息，不需要点进原文。

**提炼原则**：
1. **找核心论点**：文章最反直觉、最颠覆认知的 1 个观点，作为主标题或核心金句
2. **找关键数据**：文中的具体数字（百分比、倍数、年份、金额），数字比文字更有冲击力
3. **找因果链**：A 导致 B，B 导致 C → 每个环节就是一个要点
4. **砍到 4-6 个要点**：不是所有内容都值得放，只放"删了会损失信息"的
5. **每个要点 ≤ 2 句话**：第一句给事实/数据，第二句给洞察/结论

**主标题写法（卡片成败关键）**：
- ✅ **必须是结论性的**：直接亮出文章最反直觉的发现/结论，读者看到就被勾住
- ✅ 用数字驱动："把品牌面积放大100倍"、"500年越做越小，现在越做越大"
- ✅ 用动词驱动："买表先排队，卖表被追踪"、"雅痞拯救了机械表"
- ❌ **不能是描述性的**："在中国AI生态待了两周后"、"关于品牌的思考"（像日记标题，没冲击力）
- ❌ 避免名词性标题："表壳即品牌的进化"、"人为制造稀缺"（太抽象）

> **检验标准**：如果读者只看到主标题，就想知道"为什么？"——说明标题是对的。如果反应是"哦"——说明标题是错的。

**条目标题写法**：
- ✅ 有具体数字的反直觉发现："200家机器人公司，几乎全部没有收入"
- ✅ 直接给结论："VC只投好简历，历史证明这是错的"
- ❌ 平铺直叙："软件差距在扩大"、"估值泡沫"

**要点之间的逻辑**：
- 要点不是随机罗列，要有叙事弧线
- 推荐顺序：**发现问题 → 分析原因 → 关键证据 → 意外/反转**
- 让读者看完有"哦原来如此"的感觉

**金句选取**：
- 从原文中找最有冲击力的 1 句话放引用块
- 如果原文没有现成金句，可以用原文事实重新组织一句（不改事实，改表达）

**数据准确性（强制）**：
- 引用数字时必须忠实于原文的表述方式
- ARR（年化收入）和单月收入是不同概念，不能混用
- 不能为了冲击力而改变数据含义
- 原文说"reportedly"/"approximately"等不确定表述，卡片中要保留"据报道"/"约"等修饰

**内容原则（强制）**：
- 卡片内容必须 100% 来自用户提供的原文/URL/文本，严禁自行编造或使用占位符
- 标题、描述、来源、金句均须与原文一致，Hook 改写只改表达方式，不改事实
- 用户说"保持原文"或"不改描述"时关闭 Hook 模式

### Step 2：分析布局

- **低密度**（1 个核心观点）→ 大字符主义布局（模板 A）
- **中密度**（2-4 要点）→ 标准单栏布局（模板 B）
- **高密度**（5+ 要点）→ 单栏列表布局（模板 D，推荐）；多栏网格（模板 C）仅在用户明确要求或桌面端展示时使用

### Step 3：生成 HTML

读取 `references/design-spec.md` 获取完整设计规范（字号、配色、布局模板、CSS 变量等），**所有视觉参数以 design-spec.md 为准**。

**硬性约束**：
- 卡片宽度：默认 **600px**，仅在用户明确要求时使用 480 / 900
- `<meta name="viewport" content="width=[指定宽度]">` 防缩放
- 背景色 `#f5f3ed`
- 字号用 `clamp()` 写法（见 design-spec.md 字号规范），确保多宽度等比缩放
- **手机可读性底线**：正文 ≥ 15px，辅助文字 ≥ 12px，任何可读内容不低于 10px

保存路径：`/tmp/info-card-[关键词].html`

### Step 4：截图（必须执行）

**使用 Playwright Python 截图**（不用 Chrome DevTools MCP，避免端口冲突）：

```python
from playwright.sync_api import sync_playwright
import os

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 600, "height": 900}, device_scale_factor=2)
    page.goto("file:///tmp/info-card-xxx.html")
    page.wait_for_timeout(2000)  # 等待字体加载
    page.screenshot(path="/tmp/info-card-xxx.png", full_page=True)
    browser.close()

from PIL import Image
img = Image.open("/tmp/info-card-xxx.png")
print(f"Dimensions: {img.size[0]}x{img.size[1]}")
print(f"File size: {os.path.getsize('/tmp/info-card-xxx.png') / 1024:.0f}KB")
```

**宽度与倍率对应**：

| 卡片宽度 | devicePixelRatio | 输出 PNG 宽度 |
|---------|-----------------|-------------|
| 480px | **3x** | 1440px |
| 600px | **2x** | 1200px |
| 900px | **2x** | 1800px |

> **为什么不用 Chrome DevTools MCP**：经常因为浏览器端口占用、extension 冲突导致连接失败。Playwright Python 是独立 headless 浏览器，零依赖冲突，支持 `full_page=True` 全页截图。

### Step 5：超长分割（默认不执行）

> **默认不分割**。截图后直接输出完整长图，不管高度多少。
> 只有当用户明确要求"切分"、"分割"、"拆成多张"时，才执行分割。

**用户要求分割时**：

```bash
python3 ~/.claude/skills/qiaomu-info-card-designer/scripts/split_card.py [图片路径] 1200
```

分割后输出 `card-1.png`, `card-2.png` ... 等文件。

### Step 6：整理并输出

**保存路径规则**：
```
~/乔木新知识库/60-69 素材/65 附件库/info-cards/
  └── [YYYYMMDD]-[来源]-[主题关键词]/
        ├── card.png          # 默认：完整长图
        ├── card-1.png        # 用户要求分割时
        └── card-2.png
```

示例：`info-cards/20260316-paulgraham-brand-age/card.png`

> 文件夹名格式：`日期-来源-主题`，一目了然

告知用户：图片路径 + 共几张

---

> **所有视觉参数（字号、配色、布局模板）的唯一真相源是 `references/design-spec.md`。**
