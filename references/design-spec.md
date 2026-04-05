# 信息卡设计规范

## 字体引入

**标题字体**：仓耳今楷02（本地 TTF）
**正文字体**：仓耳今楷02（同一字体，统一视觉风格）

```html
<style>
@font-face {
  font-family: 'TsangerJinKai';
  src: url('file:///Users/joe/.claude/skills/qiaomu-info-card-designer/assets/TsangerJinKai02-W04.ttf') format('truetype');
  font-weight: normal;
  font-style: normal;
  font-display: block;
}
</style>
```

**字体栈定义**（写在 CSS 变量中）：
```css
:root {
  --font-title: 'TsangerJinKai', serif;
  --font-body: 'TsangerJinKai', serif;
  --font-label: 'TsangerJinKai', sans-serif;
  --font-mono: 'SF Mono', 'Menlo', monospace;
}
```

> **为什么用本地字体**：Google Fonts 在 `file://` 协议下可能加载失败或延迟，导致截图时字体 fallback 为系统默认。本地 @font-face 保证 100% 命中，截图零等待。

## 字号规范（手机阅读优先）

**核心原则**：卡片最终以图片形式在手机上全屏阅读。600px CSS × 2x 截图 = 1200px 图片，iPhone 3x 屏近 1:1 显示。换算公式：`CSS px × 2 ÷ 3 ≈ 手机上的 pt`。**正文必须 ≥ 13pt（20px CSS），标签必须 ≥ 10pt（16px CSS）**。

| 层级 | 600px 固定值 | 手机 pt | 说明 |
|------|-------------|---------|------|
| 主标题 | 56px | ~37pt | 视觉冲击，楷体不加粗 |
| 条目标题 h3 | 28px | ~18pt | 视觉锚点，扫读入口 |
| 正文 | 20px | ~13pt | 舒适阅读底线 |
| 副标题/金句 | 22px | ~14pt | 略大于正文 |
| 标签/speaker/dim | 16px | ~10pt | 清晰可辨 |
| 页脚 | 15px | ~10pt | 最小可读 |
| 金句出处 | 15px, color #777 | ~10pt | 不用 #999 |

## 基础卡片 CSS

```css
:root {
  --color-bg: #f5f3ed;
  --color-text: #1a1a1a;
  --color-accent: #2c3e8c; /* 根据主题替换 */
  --color-muted: #555;
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
  margin: 0;
  background: var(--color-bg);
}

.card {
  width: 600px;
  background: var(--color-bg);
  padding: 38px;
  display: flex;
  flex-direction: column;
  gap: 24px;
  position: relative;
  overflow: hidden;
}

/* 噪点纹理 */
.card::before {
  content: '';
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.04'/%3E%3C/svg%3E");
  pointer-events: none;
  z-index: 0;
}

.card > * { position: relative; z-index: 1; }

/* 标题 — 仓耳今楷，楷书质感 */
.main-title {
  font-family: var(--font-title);
  font-size: 56px;
  font-weight: normal;  /* 楷书字体自带笔画粗细变化，不需要 bold */
  line-height: 1.15;
  color: #0a0a0a;
  letter-spacing: 0.02em;  /* 楷书适合微正间距 */
}

/* 正文 — 仓耳今楷，统一风格 */
.content-body {
  font-family: var(--font-body);
  font-size: 20px;
  line-height: 1.65;
  color: #1a1a1a;
}

/* Accent 装饰线 */
.accent-bar {
  height: 6px;
  background: var(--color-accent);
  width: 80px;
}

.accent-bar-full {
  height: 4px;
  background: var(--color-accent);
  width: 100%;
}

/* 标签 — 可选元素，仅在系列卡片需要编号或用户要求时添加 */
.label {
  font-family: var(--font-label);
  font-size: 16px;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--color-accent);
}

/* 背景色块 */
.bg-block {
  background: rgba(0,0,0,0.03);
  padding: 18px 20px;
  border-left: 4px solid var(--color-accent);
}

/* 数字大字 — 系统字体 */
.stat-number {
  font-family: var(--font-label);
  font-size: 120px;
  font-weight: 700;
  line-height: 1.0;
  color: var(--color-accent);
  letter-spacing: -0.05em;
}

/* 多栏布局 */
.grid-2col {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px 40px;
}

.grid-3col {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 20px 30px;
}

.col-divider {
  border-left: 2px solid rgba(0,0,0,0.12);
  padding-left: 30px;
}

/* 页脚/来源 */
.footer {
  font-size: 15px;
  color: #888;
  letter-spacing: 0.05em;
  border-top: 1px solid rgba(0,0,0,0.1);
  padding-top: 15px;
  margin-top: 10px;
}
```

## 布局速查（密度 → 模板选择）

| 密度 | 内容量 | 推荐模板 | 主标题字号 | 条目标题 | 正文字号 |
|------|--------|---------|-----------|---------|---------|
| 低密度 | 1 个核心观点 | **模板 A** 大字符主义 | 72-96px | — | 22px |
| 中密度 | 2-4 要点 | **模板 B** 标准单栏 | 56-72px | 26-30px | 20-22px |
| 高密度 | 5+ 要点 | **模板 D** 单栏列表（推荐） | 48-56px | 24-28px | 18-20px |
| 高密度+桌面 | 5+ 要点，用户要求多栏 | **模板 C** 多栏网格（可选） | 48px | 24-28px | 18-20px |

> **字体**：全部使用 `TsangerJinKai`（仓耳今楷，本地 TTF），不使用系统字体。
> **默认宽度**：600px，所有模板统一。

## 布局模板

### 模板 A：大字符主义（低密度内容）

适用：单一观点/数据/金句

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=600">
  <style>
  @font-face {
    font-family: 'TsangerJinKai';
    src: url('file:///Users/joe/.claude/skills/qiaomu-info-card-designer/assets/TsangerJinKai02-W04.ttf') format('truetype');
    font-weight: normal;
    font-style: normal;
    font-display: block;
  }
  /* 基础CSS + 本模板样式 */
  </style>
</head>
<body>
<div class="card" style="min-height: 900px; justify-content: space-between;">
  <!-- 顶部标签（可选，仅系列卡片编号或用户要求时添加） -->
  <!-- <div class="label">主题标签</div> -->

  <!-- 核心内容区 -->
  <div>
    <div class="accent-bar" style="margin-bottom: 20px;"></div>
    <h1 class="main-title" style="font-size: 96px;">核心<br>观点</h1>
  </div>

  <!-- 补充说明 -->
  <div class="content-body" style="max-width: 600px;">
    一句补充说明文字，字号 18-20px，清晰可读。
  </div>

  <!-- 页脚 -->
  <div class="footer">来源 / 出处 · 日期</div>
</div>
</body>
</html>
```

### 模板 B：标准单栏（中密度内容）

适用：2-4 个要点、文章摘要

```html
<div class="card">
  <!-- 顶部标签（可选，仅系列卡片编号或用户要求时添加）
  <div style="display: flex; align-items: center; gap: 16px;">
    <div class="label">分类 · 1/N</div>
    <div class="accent-bar"></div>
  </div>
  -->

  <!-- 主标题 -->
  <div>
    <h1 class="main-title" style="font-size: 56px;">文章主标题</h1>
    <p class="content-body" style="margin-top: 12px; color: #555;">副标题或一句话摘要</p>
  </div>

  <!-- 分割线 -->
  <div class="accent-bar-full"></div>

  <!-- 正文要点 -->
  <div class="content-body">
    <p>第一个要点，正文 18-19px，行高 1.6。</p>
    <div class="bg-block" style="margin: 16px 0;">
      <p>重点引用或数据，放在色块中突出。</p>
    </div>
    <p>第二个要点，继续描述。</p>
  </div>

  <!-- 页脚 -->
  <div class="footer">@vista8 · 向阳乔木推荐看</div>
</div>
```

### 模板 C：多栏网格（高密度内容，可选/桌面端）

> ⚠️ 多栏在手机上每栏太窄，**仅在用户明确要求或桌面端展示时使用**。默认高密度内容推荐模板 D。

适用：5+ 要点、对比、列表（桌面端展示）

```html
<div class="card">
  <!-- 顶部（标签可选，仅系列卡片编号或用户要求时添加） -->
  <div>
    <!-- <div class="label">专题 · 1/N</div> -->
    <h1 class="main-title" style="font-size: 48px; margin-top: 8px;">标题</h1>
    <div class="accent-bar-full" style="margin-top: 16px;"></div>
  </div>

  <!-- 2栏内容 -->
  <div class="grid-2col">
    <div>
      <div class="label" style="margin-bottom: 8px;">Part 01</div>
      <h2 style="font-size: 24px; font-weight: 700; margin-bottom: 10px;">子标题</h2>
      <p class="content-body">内容文字，18px，清晰可读。</p>
    </div>
    <div class="col-divider">
      <div class="label" style="margin-bottom: 8px;">Part 02</div>
      <h2 style="font-size: 24px; font-weight: 700; margin-bottom: 10px;">子标题</h2>
      <p class="content-body">内容文字，18px，清晰可读。</p>
    </div>
  </div>

  <!-- 页脚 -->
  <div class="footer">@vista8 · 向阳乔木推荐看</div>
</div>
```

### 模板 D：单栏列表（高密度内容，推荐）

适用：5+ 要点、文章要点列表、手机端高密度展示

> ✅ 高密度内容的**默认选择**，手机上每个要点都能完整展示，不会被挤压。

```html
<div class="card">
  <!-- 顶部标签（可选，仅系列卡片编号或用户要求时添加）
  <div style="display: flex; align-items: center; gap: 16px;">
    <div class="label">专题 · 1/N</div>
    <div class="accent-bar"></div>
  </div>
  -->

  <!-- 主标题 -->
  <div>
    <h1 class="main-title" style="font-size: 52px;">标题</h1>
    <div class="accent-bar-full" style="margin-top: 16px;"></div>
  </div>

  <!-- 要点列表（单栏，每条独立） -->
  <div style="display: flex; flex-direction: column; gap: 24px;">
    <!-- 要点 1 -->
    <div style="border-left: 4px solid var(--color-accent); padding-left: 20px;">
      <h3 style="font-family: var(--font-title); font-size: 22px; font-weight: normal; margin-bottom: 6px; color: #0a0a0a;">条目标题</h3>
      <p class="content-body" style="font-size: 16px;">要点描述，1-2 句话，手机上清晰可读。</p>
    </div>
    <!-- 要点 2 -->
    <div style="border-left: 4px solid var(--color-accent); padding-left: 20px;">
      <h3 style="font-family: var(--font-title); font-size: 22px; font-weight: normal; margin-bottom: 6px; color: #0a0a0a;">条目标题</h3>
      <p class="content-body" style="font-size: 16px;">要点描述。</p>
    </div>
    <!-- 更多要点... -->
  </div>

  <!-- 金句引用（可选） -->
  <div class="bg-block">
    <p style="font-family: var(--font-body); font-size: 18px; font-style: italic; line-height: 1.6;">"原文中最有冲击力的一句话"</p>
  </div>

  <!-- 页脚 -->
  <div class="footer">@vista8 · 向阳乔木推荐看</div>
</div>
```

## 卡片宽度方案

### 手机优先（默认）— 600px

> **80%+ 用户在手机上看图**。600px × 2x = 1200px，iPhone 3x 屏近 1:1 显示，正文 ~13pt 舒适可读。

| 属性 | 值 |
|------|------|
| CSS 宽度 | `600px` |
| viewport | `<meta name="viewport" content="width=600">` |
| 截图 | `device_scale_factor=2`，`fullPage=true` |
| 输出图片 | 1200px 宽 |
| 适用平台 | 微信、X、小红书、即刻、朋友圈 |

### 桌面/平板 — 800px

> 用户提到「桌面」「博客配图」「PPT」「iPad」「宽一点」时自动切换，**无需 AskUserQuestion**。

| 属性 | 值 |
|------|------|
| CSS 宽度 | `800px` |
| viewport | `<meta name="viewport" content="width=800">` |
| 截图 | `device_scale_factor=2`，`fullPage=true` |
| 输出图片 | 1600px 宽 |
| 适用平台 | 博客、知识库、PPT、iPad 阅读 |

**800px 字号适配**（相对 600px 等比放大）：

| 元素 | 600px 值 | 800px 值 |
|------|---------|---------|
| 主标题 | 56px | 64px |
| 副标题 | 22px | 26px |
| 条目标题 h3 | 28px | 32px |
| 正文 | 20px | 22px |
| 标签/speaker | 16px | 18px |
| 页脚 | 15px | 16px |
| 卡片 padding | 38px | 48px |
| 卡片 gap | 24px | 28px |

**切换触发词**：「桌面」「电脑看」「博客」「PPT」「iPad」「宽一点」「800」→ 自动用 800px，不需要问用户。

### 通用规则

1. **截图用 fullPage=true**：捕获完整卡片，不裁剪
2. **字号底线**：标签/页脚 **不低于 15px**（手机 ~10pt），正文 **不低于 20px**（手机 ~13pt）
3. **高密度内容用单栏列表**，不用多栏网格（多栏在手机上每栏太窄）
4. **不再使用 900px**：800px 是桌面端的最佳平衡（单栏行字数适中，iPad 1600px 完美）

## 视觉层级原则（色块优先，线条克制）

> **核心**：区分内容块时，优先用**背景色块**（`bg-block`、浅灰底 `rgba(0,0,0,0.03)`），不要堆叠装饰线。

| 需求 | 正确做法 | 错误做法 |
|------|---------|---------|
| 区分内容块 | 浅灰色块 `.bg-block`、留白间距 | 给每个块加 `border-top` / `border-left` |
| 突出重点 | 色块背景 + accent 左边线（仅 1 条） | 同时用顶部线 + 左边线 + 底部线 |
| 分隔大段落 | `accent-bar-full`（全宽，**全卡最多 1 条**） | 每个段落之间都加分隔线 |
| 多栏/网格分隔 | 留白 `gap` + 色块背景差异 | 每个格子加 `border-top` 彩色线 |

**装饰线预算**：
- 一张卡片中，`accent-bar`（短装饰线）最多 **1 条**，`accent-bar-full`（全宽分隔线）最多 **1 条**
- 条目之间用**留白** `gap` 分隔，不用线
- 需要强调某个条目时，用 `.bg-block`（浅灰底 + 左边线），不要给每个条目都加左边线
- 多栏网格中，用色块底色区分，不用 `border-top` 彩色线

## 移动端紧凑原则

> **核心**：卡片最终在手机上以图片形式阅读。字号是第一优先级，间距服务于字号。

**手机 pt 换算**：600px CSS × 2x 截图 = 1200px 图片，iPhone 3x 屏上 `CSS px × 2 ÷ 3 ≈ pt`。正文 20px ≈ 13pt，标签 16px ≈ 10pt。

**字号底线**（绝对不能低于）：
- 正文：**20px**（手机 ~13pt）
- 条目标题：**28px**（手机 ~18pt）
- 标签/speaker/dim：**16px**（手机 ~10pt）
- 页脚/出处：**15px**（手机 ~10pt）

**卡片 padding**：`38px`，让内容区更宽。

**条目间距**：
- `.points` 容器 gap：`14px`，色块背景色差已足够区分
- 条目内部 padding：`16px 18px`

**条目标签（speaker / dim）**：
- 颜色用 `var(--color-accent)`，不用 `#999`
- 字号 `16px`，`letter-spacing: 0.08em`

**段落间 gap**：
- `.card` 顶层 gap：`24px`
- 金句 `.bg-block` 内部 padding：`18px 20px`

```css
/* 移动端参考值 */
.card { padding: 38px; gap: 24px; }
.main-title { font-size: 56px; }
.subtitle { font-size: 22px; }
.point h3 { font-size: 28px; }
.point p { font-size: 20px; line-height: 1.65; }
.point .dim,
.point .speaker { font-size: 16px; color: var(--color-accent); }
.label { font-size: 16px; }
.bg-block p { font-size: 22px; }
.footer { font-size: 15px; }
.points { gap: 14px; }
.point { padding: 16px 18px; }
.bg-block { padding: 18px 20px; }
```

## 图标使用规范

> **原则**：禁止使用 emoji。所有图标统一使用 Lucide Icons（开源，MIT协议），通过 CDN 引入。

### 引入方式

```html
<!-- 在 <head> 中引入 -->
<script src="https://unpkg.com/lucide@latest/dist/umd/lucide.min.js"></script>

<!-- 在 HTML 中使用 -->
<i data-lucide="book-open" class="icon"></i>

<!-- 在 </body> 前初始化 -->
<script>lucide.createIcons();</script>
```

### 图标样式 CSS

```css
.icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 22px;
  height: 22px;
  vertical-align: middle;
  color: var(--color-accent);  /* 继承 accent 颜色 */
}

/* section 标题旁图标（稍大） */
.section-icon {
  width: 26px;
  height: 26px;
  color: var(--color-accent);
  flex-shrink: 0;
}
```

### 常用图标速查

| 场景 | 图标名 | 用法 |
|------|--------|------|
| 教育/阅读 | `book-open` | 教育理念区块 |
| 家庭/关系 | `users` | 家庭关系区块 |
| 财富/增长 | `trending-up` | 财富话题 |
| 升级/转变 | `arrow-right` | 对比/升级列表 |
| 决策/平衡 | `scale` | 决策框架 |
| 确认/原则 | `check-circle` | 核心规则列表 |
| 合作 | `handshake` | 合作规则 |
| 运动/健康 | `activity` | 运动习惯 |
| 饮食/自然 | `leaf` | 饮食建议 |
| 人生方向 | `compass` | 哲学/方向 |
| 思考/洞见 | `lightbulb` | 学习方法 |
| 反复改进 | `repeat-2` | 迭代/成长 |
| 警示 | `alert-triangle` | 注意事项 |
| 流程步骤 | `arrow-right` | 四步流程 |
| 金句引用 | `quote` | 引用块装饰 |
| 健康跑步 | `footprints` | 跑步习惯 |
| 时钟/时间 | `clock` | 时间相关 |
| 简洁/极简 | `minimize-2` | 简单原则 |

### 注意事项

- **Playwright 截图前必须等待 CDN 加载**：`page.wait_for_timeout(3000)`（比普通卡片多 1s）
- 图标颜色默认继承 `currentColor`，通过父容器 `color` 属性控制
- 图标大小用 CSS 控制，不用 HTML 属性
- 不要在正文段落内行内混入图标（影响阅读节奏），只在标题/标签区块使用

**⚠️ 关键 Bug：CSS 选择器必须同时覆盖 `i` 和 `svg`**

Lucide 的 `createIcons()` 会把 `<i data-lucide="...">` 替换成 `<svg>` 元素。替换后，原来针对 `i` 的 CSS 选择器就失效了。

正确写法（必须同时写 `i` 和 `svg`）：

```css
/* ✅ 正确 */
.rule-item i, .rule-item svg { width: 20px; height: 20px; color: var(--accent); }

/* ❌ 错误：替换后 i 选择器失效，图标颜色变成继承色 */
.rule-item i { color: var(--accent); }
```

最可靠的替代方案：在图标的**父容器**上设置 `color: var(--accent)`，SVG 通过 `currentColor` 自动继承，无需依赖选择器：

```css
/* 最稳定的方式：父容器设色 */
.section-label { color: var(--accent); }  /* 子图标自动继承 */
```

---

## 配色方案

### 经典/杂志风格配色（A/B 风格）

| 主题 | accent 颜色 | 适用场景 |
|------|------------|---------|
| 靛蓝 | `#2c3e8c` | 知识/科技/AI |
| 深红 | `#c0392b` | 警示/激情/重要 |
| 墨绿 | `#1a4a3a` | 生活/健康/自然 |
| 深金 | `#8b6914` | 财经/商业/价值 |
| 深灰 | `#2c2c2c` | 中性/通用/严肃 |
| 紫罗兰 | `#5b2d8e` | 创意/哲学/艺术 |

### 艺术风格配色（C 风格）

> **原则**：避开上方的常见"安全色"，选有气质的非常规色，背景加微渐变或色温偏移。

| 主题 | 背景 | accent | 适用场景 |
|------|------|--------|---------|
| 赭石棕 | `#F7F3EE` → `#F2ECE4`（微暖渐变） | `#7A3B1E` | 人文/教育/历史 |
| 苔藓绿 | `#EDF2ED` → `#E4EDE5`（微冷渐变） | `#2D5016` | 自然/健康/生活 |
| 茄紫 | `#F2EEF8` → `#EBE5F5` | `#3D1F6E` | 哲学/创意/精神 |
| 古铜暗 | `#0F0C07`（深暗底） | `#7A5C1E` | 财富/权威/深度 |
| 烟灰蓝 | `#EEF0F4` → `#E8EBF2` | `#2A3A5C` | 科技/理性/冷静 |
| 胭脂红 | `#F8EEEE` → `#F2E5E5` | `#8B1A2A` | 激情/警示/重要 |

**艺术风格背景渐变写法**：
```css
background: linear-gradient(160deg, #F7F3EE 0%, #F2ECE4 100%);
```

### 多卡片同色系渐变

> **原则**：多张卡片组成系列时，在主色系内做色相/明度微调，保持系列感又避免单调。

**做法**：以主题色为基准，每张卡片在色相环上偏移 10-20°，或在明度上做 ±10% 调整。

**示例（深金系列 4 张）**：

| 卡片 | 色名 | 色值 | 偏移 |
|------|------|------|------|
| 1/N | 深金（基准） | `#8b6914` | — |
| 2/N | 赤铜 | `#8a4a1a` | 偏暖红 |
| 3/N | 橄榄金 | `#6b5b1e` | 偏绿沉稳 |
| 4/N | 琥珀 | `#9c5a0a` | 偏亮收尾 |

**规则**：
- 第 1 张用主题基准色
- 中间卡片交替偏暖/偏冷
- 最后一张可略提亮度，收尾提气
- 所有色值与 `--color-bg: #f5f3ed` 对比度需 ≥ 4.5:1（WCAG AA）

## 深色卡片设计规范（艺术风格 C 专用）

> 深色背景卡片有独特的对比度挑战，以下规则**强制执行**，违反任意一条都会导致截图不可读。

### 三字体混排（Style C 必须）

```css
/* 必须声明两个本地字体 */
@font-face { font-family:'TsangerJinKai'; src:url('file:///Users/joe/.claude/skills/qiaomu-info-card-designer/assets/TsangerJinKai02-W04.ttf') format('truetype'); font-weight:normal; font-style:normal; font-display:block; }
@font-face { font-family:'NotoSerifSC'; src:url('file:///Users/joe/.claude/skills/qiaomu-info-card-designer/assets/NotoSerifSC-Regular.ttf') format('truetype'); font-weight:normal; font-style:normal; font-display:block; }

:root {
  --kai: 'TsangerJinKai', serif;    /* 标题、条目标题 */
  --song: 'NotoSerifSC', serif;     /* 正文描述、金句 */
  --sans: -apple-system, 'Helvetica Neue', sans-serif; /* 编号、标签、eyebrow、footer */
}
```

**字体分工**：
| 层级 | 字体 | 示例元素 |
|------|------|---------|
| 主标题 / 条目标题 | `--kai` 仓耳今楷 | `.main-title`, `.item-title` |
| 正文描述 / 引用 | `--song` NotoSerifSC | `.item-sub`, `.quote-text` |
| 编号 / 标签 / eyebrow / footer | `--sans` 系统无衬线 | `.num`, `.eyebrow`, `.section-label` |

### 深色背景对比度规则

**section-label 最小字号**：

```css
/* ✅ 正确：13px 手机可读 */
.section-label { font-size: 13px; letter-spacing: 0.14em; }

/* ❌ 错误：10px 手机上几乎不可见 */
.section-label { font-size: 10px; }
```

**编号 `.num` 对比度要求**：

- 编号字号 ≥ 42px（属于大字体，WCAG 大字标准：≥ 3:1）
- 冷色系 accent（蓝/绿/紫）在深色背景上天然亮度低，直接用往往不达标
- 暖色系（金/铜/橙）对比度更稳定

```css
/* ✅ 正确：使用提亮版本的固定色值 */
.num { color: #4E6E96; }  /* 蓝系，~4.8:1 on #06090F */
.num { color: #3C7850; }  /* 绿系，~5:1 on #050D07 */
.num { color: #6848A0; }  /* 紫系，~3.7:1 on #08050E */
.num { color: #8C6830; }  /* 金系，~4.6:1 on #0D0A05 */

/* ❌ 错误：直接使用 accent 颜色（可能过暗） */
.num { color: var(--accent); }  /* #6A8FBC 在深蓝背景上只有 2.8:1，不合规 */
```

### 禁止 opacity 叠加

**opacity 叠加在深色背景上会把颜色压成几乎不可见的黑色**：

```css
/* ❌ 错误：opacity 叠加 */
.eyebrow { color: var(--accent); opacity: 0.45; }  /* 实际渲染极暗 */
.num { color: var(--accent); opacity: 0.22; }       /* 几乎看不见 */

/* ✅ 正确：直接用固定色值 */
.eyebrow { color: #5A789C; }  /* 不用 opacity，直接给合规的颜色 */
.num { color: #4E6E96; }
```

### hex 颜色必须恰好 6 位

```css
/* ❌ 错误：7 位 hex，浏览器静默回退为黑色！ */
color: #6040888;  /* 7 位，无效 */

/* ✅ 正确：恰好 6 位 */
color: #604088;   /* 6 位，有效 */
```

### 各色系 num 颜色参考值

| 色系 | 背景 | num 颜色 | 对比度 |
|------|------|---------|--------|
| 古铜暗（金系） | `#0D0A05` | `#8C6830` | ~4.6:1 |
| 钢青（蓝系） | `#06090F` | `#4E6E96` | ~4.8:1 |
| 苔绿（绿系） | `#050D07` | `#3C7850` | ~5.0:1 |
| 深紫（紫系） | `#08050E` | `#6848A0` | ~3.7:1 |
| 暖铜（铜系） | `#0E0907` | `#7A5430` | ~4.5:1 |

---

## 顶部标签使用规则

> **默认不加标签**。顶部标签（`.label` + `.accent-bar`）是可选元素，不是必须的。

| 场景 | 是否添加 | 示例 |
|------|---------|------|
| 单张独立卡片 | ❌ 不加 | — |
| 多张系列卡片 | ✅ 加编号 | `圆桌复盘 · 2/5` |
| 用户明确要求分类标签 | ✅ 加 | `AI 趋势` |
| 内容本身有明确主题分类 | 可选 | 根据内容判断 |

## 风格方案（生成卡片时用 AskUserQuestion 让用户选择）

### 方案一：经典风格（默认）

沿用上方基础 CSS，全部使用 TsangerJinKai。适合快速出图、风格统一。

### 方案二：杂志风格

在经典风格基础上做精致化升级，适合正式发布、社交媒体传播。

**与经典风格的差异**：

| 元素 | 经典风格 | 杂志风格 |
|------|---------|---------|
| 卡片 padding | `38px` | `44px 42px` |
| 卡片 gap | `24px` | `28px` |
| 正文颜色 `--color-muted` | `#555` | `#333` |
| 条目列表 | 统一灰底，`gap: 14px` | 奇偶交替底色，`gap: 0` |
| speaker/dim 标签 | `16px` | `13px`, `letter-spacing: 0.15em`, `opacity: 0.85` |
| 条目标题 h3 | `28px` | `26px` |
| 正文 p | `20px`, `line-height: 1.65` | `18px`, `line-height: 1.75` |
| accent-bar | `6px × 80px` | `4px × 60px` |
| label | `16px`, `letter-spacing: 0.12em` | `15px`, `letter-spacing: 0.18em` |
| 页脚 | 直线分隔 | `· · ·` 装饰符分隔 |
| 金句引用 | `.bg-block`（浅灰底 + 左边线） | `.pull-quote`（见下方） |

**杂志风格条目 CSS**：

```css
/* 条目奇偶交替 */
.points { display: flex; flex-direction: column; gap: 0; }
.point { padding: 20px 22px; }
.point:nth-child(odd) { background: rgba(0,0,0,0.035); }
.point:nth-child(even) { background: transparent; }

/* speaker 标签更精致 */
.point .speaker {
  font-size: 13px; letter-spacing: 0.15em;
  text-transform: uppercase; opacity: 0.85;
}

/* 页脚装饰 */
.footer-divider {
  text-align: center; color: #ccc; font-size: 14px;
  letter-spacing: 0.5em; margin-bottom: -8px;
}
```

**金句引用 `.pull-quote`（克制版）**：

> **原则**：金句是点睛之笔，不是视觉重心。用浅底色 + 左边线 + 装饰引号，融入整体节奏，不喧宾夺主。
> **禁止**：深色反转背景（accent色满底 + 白字）。这会抢走正文内容的注意力。

```css
.pull-quote {
  background: rgba(0,0,0,0.03);
  padding: 24px 24px 20px;
  border-left: 4px solid var(--color-accent);
  position: relative;
}
.pull-quote::before {
  content: '\201C';
  font-family: Georgia, serif;
  font-size: 56px;
  color: var(--color-accent);
  opacity: 0.15;
  position: absolute;
  top: -4px;
  left: 12px;
  line-height: 1;
}
.pull-quote p {
  font-family: var(--font-body);
  font-size: 20px;
  line-height: 1.7;
  color: #1a1a1a;
  font-style: italic;
  position: relative;
  z-index: 1;
}
.pull-quote .attribution {
  font-family: var(--font-label);
  font-size: 14px;
  color: #999;
  margin-top: 10px;
  letter-spacing: 0.08em;
}
```

### 字体方案（可叠加在任一风格上）

| 方案 | 标题 | 正文 | 标签 | 适用场景 |
|------|------|------|------|---------|
| 全楷体（默认） | TsangerJinKai | TsangerJinKai | TsangerJinKai | 国风、文化、通用 |
| 楷宋混排 | TsangerJinKai | NotoSerifSC | TsangerJinKai | 商业、正式、长文 |

**NotoSerifSC 引入**（楷宋混排时额外添加）：
```css
@font-face {
  font-family: 'NotoSerifSC';
  src: url('file:///Users/joe/.claude/skills/qiaomu-info-card-designer/assets/NotoSerifSC-Regular.ttf') format('truetype');
  font-weight: normal; font-style: normal; font-display: block;
}
:root {
  --font-body: 'NotoSerifSC', serif; /* 仅替换正文 */
}
```

## 输出与部署规则

> **截图完成后立即自动 deploy，不询问用户，不等待确认。**

### 工作流

1. **生成 HTML** → `/tmp/` 临时目录
2. **Playwright 截图** → 同目录下 `.png`（2x，fullPage）
3. **自动部署** → 直接复制 HTML + PNG 到目标目录，无需询问

### 目标目录规则

| 条件 | 目标路径 |
|------|---------|
| 用户指定了路径 | 用户指定的路径 |
| 默认 | `~/Downloads/info-cards/{slug}/` |

> **slug 命名规则**：`YYYYMMDD-{来源简称}-{主题关键词}`，全小写英文+连字符。
> 示例：`20260327-justinlin-agentic-thinking`、`20260405-life-wisdom`

### 部署内容

每个目录包含：
- `card*.html` — 源文件（可二次编辑）
- `card*.png` — 截图（直接可用于发布）
