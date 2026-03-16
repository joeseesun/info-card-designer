# 信息卡设计规范

## 字体引入

```html
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@700;900&family=Noto+Sans+SC:wght@400;500;700&family=Oswald:wght@500;700&family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
```

## 字号规范（vw 单位，随宽度自动缩放）

**核心原则**：所有字号用 `clamp(min, Xvw, max)` 写，不写固定 px，确保 480/600/900 三种宽度比例一致。

| 层级 | CSS | 480px效果 | 600px效果 | 900px效果 |
|------|-----|-----------|-----------|-----------|
| 主标题 | `clamp(40px, 13vw, 130px)` | ~62px | ~78px | ~117px |
| 条目标题 | `clamp(16px, 4.5vw, 44px)` | ~22px | ~27px | ~40px |
| 正文 | `clamp(14px, 3.2vw, 24px)` | ~15px | ~19px | ~28px |
| 辅助信息 | `clamp(12px, 2.5vw, 20px)` | ~12px | ~15px | ~22px |
| 元数据/标签 | `clamp(10px, 2vw, 15px)` | ~10px | ~12px | ~15px |

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
  padding: 50px;
  display: flex;
  flex-direction: column;
  gap: 30px;
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

/* 标题 */
.main-title {
  font-family: 'Noto Serif SC', serif;
  font-size: 80px;
  font-weight: 900;
  line-height: 1.0;
  color: #0a0a0a;
  letter-spacing: -0.03em;
}

/* 正文 */
.content-body {
  font-family: 'Inter', 'Noto Sans SC', sans-serif;
  font-size: 19px;
  line-height: 1.6;
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

/* 标签 */
.label {
  font-family: 'Oswald', 'Inter', sans-serif;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: var(--color-accent);
}

/* 背景色块 */
.bg-block {
  background: rgba(0,0,0,0.03);
  padding: 20px 24px;
  border-left: 4px solid var(--color-accent);
}

/* 数字大字 */
.stat-number {
  font-family: 'Oswald', 'Inter', sans-serif;
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
  font-size: 13px;
  color: #888;
  letter-spacing: 0.05em;
  border-top: 1px solid rgba(0,0,0,0.1);
  padding-top: 15px;
  margin-top: 10px;
}
```

## 布局模板

### 模板 A：大字符主义（低密度内容）

适用：单一观点/数据/金句

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=900">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@700;900&family=Noto+Sans+SC:wght@400;500;700&family=Oswald:wght@500;700&family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
  <style>/* 基础CSS + 本模板样式 */</style>
</head>
<body>
<div class="card" style="min-height: 900px; justify-content: space-between;">
  <!-- 顶部标签 -->
  <div class="label">主题标签</div>

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
  <!-- 顶部 -->
  <div style="display: flex; align-items: center; gap: 16px;">
    <div class="label">分类</div>
    <div class="accent-bar"></div>
  </div>

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

### 模板 C：多栏网格（高密度内容）

适用：5+ 要点、对比、列表

```html
<div class="card">
  <!-- 顶部标题 -->
  <div>
    <div class="label">专题</div>
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

## X (Twitter) 优化要点

1. **固定宽度 900px**：X 展示图片时按比例缩放，900px 保证文字不会过小
2. **viewport meta**：`<meta name="viewport" content="width=900">` 防止浏览器缩放
3. **推荐比例**：1:1 (900×900) 或 16:9 (900×506) 效果最佳
4. **截图用 fullPage=true**：捕获完整卡片，不裁剪
5. **字号底线**：任何可读文字 **不低于 16px**，正文 **不低于 18px**

## 配色方案

| 主题 | accent 颜色 | 适用场景 |
|------|------------|---------|
| 靛蓝 | `#2c3e8c` | 知识/科技/AI |
| 深红 | `#c0392b` | 警示/激情/重要 |
| 墨绿 | `#1a4a3a` | 生活/健康/自然 |
| 深金 | `#8b6914` | 财经/商业/价值 |
| 深灰 | `#2c2c2c` | 中性/通用/严肃 |
| 紫罗兰 | `#5b2d8e` | 创意/哲学/艺术 |
