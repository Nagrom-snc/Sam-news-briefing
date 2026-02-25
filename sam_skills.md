# Sam Skills – Core Intelligence Framework

This file defines the standardized logic for:

1. Content Extraction
2. Analysis Framework
3. Trend Forecasting
4. Market Impact Scoring
5. Action Prioritization

All modifications to Sam's reasoning must be reflected here first.

---

# 1️⃣ Content Extraction Protocol

## Step 1 – Relevance Filter

An article qualifies if:

- Mentions China (policy, economy, geopolitics, tech)
OR
- Mentions AI (technology, regulation, enterprise adoption)

Priority if both appear.

### China Keywords
- Geographic: china, chinese, beijing, shanghai, shenzhen, hong kong, taiwan
- Political: xi jinping, ccp, prc, politburo, state council
- Companies: huawei, bytedance, tiktok, alibaba, tencent, baidu, xiaomi, byd, catl, Deepseek, Zhipu, Minimax
- Economic: belt and road, made in china, dual circulation

### AI Keywords
- Core: artificial intelligence, ai, machine learning, deep learning, neural network
- Products: chatgpt, gpt, claude, llm, large language model, generative ai
- Companies: openai, anthropic, deepseek, nvidia, meta ai, google ai
- Hardware: semiconductor, chip, gpu, tpu, ai accelerator

---

## Article ingestion (batch scraper to raw)

To avoid manual copy-paste from the browser, use the Firefox scraper with your profile (paywall bypass):

- **Single URL:** `python scripts/firefox_scraper.py <url>` — saves to `data/raw/YYYY-MM-DD/{ARTICLE_ID}.md`.
- **Batch from file:** `python scripts/firefox_scraper.py --url-list urls.txt` — one URL per line (lines starting with `#` ignored).
- **Batch from stdin:** `python scripts/firefox_scraper.py --url-list -` — paste or pipe URLs.
- **Paywalled sites:** `python scripts/firefox_scraper.py --no-headless --url-list urls.txt` — opens visible Firefox so profile cookies/session are used; close other Firefox windows using that profile first.

Output is raw-format (title, author/date, URL, body) so the rest of the pipeline (run Sam news on `data/raw/...`) is unchanged. Optional `--processed` writes to `data/processed` with YAML frontmatter instead.

---

## Step 2 – Article Processing Workflow

For each scraped article, execute the following tasks in sequence:

### Task 0: Article Numbering

Assign a unique article ID using the format:

```
{DATE}_{OUTLET}_{SEQ}
```

| Component | Format | Example |
|-----------|--------|---------|
| DATE | YYYYMMDD | 20260222 |
| OUTLET | Uppercase abbreviation | REUTERS, FT, SCMP, BLOOM |
| SEQ | 3-digit sequence | 001, 002, 003 |

**Example IDs:**
- `20260222_REUTERS_001`
- `20260222_FT_002`
- `20260222_SCMP_003`

**Outlet Abbreviations:**

| Outlet | Abbreviation |
|--------|--------------|
| Reuters | REUTERS |
| Bloomberg | BLOOM |
| Financial Times | FT |
| The Economist | ECON |
| Wall Street Journal | WSJ |
| South China Morning Post | SCMP |
| Nikkei Asia | NIKKEI |
| AP News | AP |
| Politico | POLITICO |
| TechCrunch | TC |
| The Verge | VERGE |

**Date Format Standard (ISO 8601):**

All dates must use ISO 8601 format:

| Field | Format | Example |
|-------|--------|---------|
| Publication date | `YYYY-MM-DD` | `2026-02-19` |
| Processing timestamp | `YYYY-MM-DDTHH:MM:SS` | `2026-02-22T14:30:00` |
| Article ID date component | `YYYYMMDD` | `20260222` |

The scraper automatically converts various date formats (e.g., "FEB 19 2026", "February 19, 2026", "19/02/2026") to ISO format.

---

### Task 1: Full Text Transcription

Save the full article as markdown:

**Filename:** `{ARTICLE_ID}.md`

**Example:** `20260222_REUTERS_001.md`

**Content Structure:**
```markdown
# {Article Title}

**Article ID:** {ARTICLE_ID}
**Source:** {Outlet Name}
**URL:** {Original URL}
**Date:** {Publication Date}
**Author:** {Author Name}

---

{Full article text in markdown format}

---

*Scraped: {Processing Timestamp}*
```

---

### Task 2: Metadata Standardization

Each article must contain the following YAML frontmatter:

```yaml
---
# Article Identification
id: string              # Article ID (DATE_OUTLET_SEQ)
source: string          # News outlet name
title: string           # Article headline
url: string             # Original URL
date: string            # Publication date (ISO 8601: YYYY-MM-DD)
author: string          # Author name (if available)

# Classification
themes: [string]        # ["China", "AI", or both]
keywords: [string]      # Key terms extracted from article
entities: [string]      # Named entities (companies, persons, orgs)

# Processing
content_hash: string    # MD5 hash of article body (first 16 chars)
word_count: integer     # Article word count
language: string        # Primary language (en, zh-hant, zh-hans)
processed_at: datetime  # Processing timestamp (ISO 8601 with time)

# Analysis Links
analysis_file: string   # Path to analysis file
analysis_status: string # pending | completed | error
---
```

---

### Task 3: Initial Analysis Generation

Create a separate analysis file:

**Filename:** `{ARTICLE_ID}_Analysis.md`

**Example:** `20260222_REUTERS_001_Analysis.md`

When a material is pulled in or a URL link is provided and the prompt **"Run analysis"** is executed, generate analysis using the following **10-phase framework** (in Traditional Chinese):

---

## 10-Phase Analysis Framework

> **Core Principle:** Phase 0 (Semantic Layer) must be completed BEFORE any evaluative analysis.
> This ensures the author's logic is fully reconstructed before criticism begins.

---

### Phase 0 — 語意建模 (Semantic Layer)

請在不評論、不評價的前提下，完整重建作者的思考框架。

**Output Structure:**
```markdown
# Phase 0 — 語意建模（Semantic Layer）

## 1. Core Question（核心問題）
作者真正試圖回答的中心問題是：
> {以引用格式呈現核心問題}

## 2. Thesis（中心主張）
> {以一句話表達作者的主要結論或主張}

## 3. Argument Chain（推理鏈條）

### 前提（Premises）
- **P1：** {前提1}
- **P2：** {前提2}
- **P3：** {前提3}
...

### 推論步驟（Inferences）
- **I1：** {前提} → {推論}
- **I2：** {前提} → {推論}
...

### 子結論（Intermediates）
- **C1：** {子結論1}
- **C2：** {子結論2}
...

### 最終結論（Final Conclusion）
> {最終結論}

## 4. Key Concepts（關鍵概念）

| 概念 | 定義（作者使用的意義） | 在本文的功能/角色 |
|------|------------------------|-------------------|
| **{概念1}** | {定義} | {功能} |
| **{概念2}** | {定義} | {功能} |
...

## 5. Implicit Assumptions（隱含前提）

### 世界觀假設
- **A1：** {假設}
- **A2：** {假設}

### 因果假設
- **A3：** {假設}
- **A4：** {假設}

### 文化/政治預設
- **A5：** {假設}
- **A6：** {假設}

### 價值/規範性假設
- **A7：** {假設}
- **A8：** {假設}
```

**規則：**
1. 本階段僅限「邏輯還原」，禁止任何形式的評論、立場、評價或改寫
2. 輸出必須清楚、結構化、無重複
3. 語意建模必須在任何後續分析前優先完成

---

### Phase 1 — 邏輯還原（不評論）

請完整還原作者的論證結構，展開敘事層面的分析。

**Output Structure:**
```markdown
# Phase 1 — 邏輯還原（不評論）

## 作者的完整論證結構

### 問題設定
{作者如何設定問題框架}

### 論證展開

**第一層：{主題}**
- {要點}
- {要點}

**第二層：{主題}**
- {要點}
- {要點}

**第三層：{主題}**
- {要點}
- {要點}

（依論證層數展開）

### 論證邏輯
```
{前提1} + {前提2} → {推論1}
    ↓
{推論1} + {前提3} → {推論2}
    ↓
{推論2} → {結論}
```
```

⚠️ 此階段禁止評論對錯，只能重建結構。

---

### Phase 2 — 重點萃取 (Key Takeaways)

整理 8 個主要的 Key Takeaways，供政策研究員參考。

**要求：**
- 可引用性
- 可行動性
- 可轉化為政策或戰略理解

**Output Structure:**
```markdown
# Phase 2 — 8個 Key Takeaways

## 1. {標題}
> {引用或摘要}

**可行動性：** {對政策/投資/策略的意涵}

## 2. {標題}
> {引用或摘要}

**政策含義：** {對政策的意涵}

（依此類推至第8點）
```

---

### Phase 3 — 立場與預設分析 (Stance Check)

請分析文章的隱性立場與預設。

**Output Structure:**
```markdown
# Phase 3 — 立場與預設分析

## 隱性價值觀

### 1. {價值觀類型}
{具體描述}

### 2. {價值觀類型}
{具體描述}

## 文化/政治預設

### 1. {預設類型}
{具體描述}

### 2. {預設類型}
{具體描述}

## 這些預設是否限制了問題框架？

**{是/部分/否}：**

1. {限制1}
2. {限制2}
3. {限制3}
```

若無偏頗，也需明確說明理由。

---

### Phase 4 — 問題層級評估 (Problem Assessment)

評估作者是否問對問題。

**Output Structure:**
```markdown
# Phase 4 — 問題層級評估

## 作者是否問對問題？

**{判斷：基本正確/部分正確/問錯方向}**

### 作者的問題
> {作者試圖回答的問題}

### 這是有效的問題，因為：
- {理由1}
- {理由2}

### 但更深層的問題被忽略：

**1. {問題層級}：** {更深層的問題}

**2. {問題層級}：** {更深層的問題}

**3. {問題層級}：** {更深層的問題}

## 真正的核心問題可能是：

> **{重新框架的核心問題}**
```

請說明你的判準。

---

### Phase 5 — 論證重構 (Better Approach)

假設問題設定正確，提出更強的論證路徑。

**Output Structure:**
```markdown
# Phase 5 — 論證重構

## 更強的論證路徑

### 原論證的框架
{概括作者的論證方式}

### 更有效的分析架構：{架構名稱}

**重構版論證：**

1. **{前提/概念重構}：**
   - {要點}
   - {要點}

2. **{推理步驟重構}：**
   - {要點}
   - {要點}

3. **{結論重構}：**
   - {要點}

4. **因此：**
   - {更有力的結論}

### 這個重構為何更強？
- **{優勢1}：** {說明}
- **{優勢2}：** {說明}
- **{優勢3}：** {說明}
```

---

### Phase 6 — 謬誤與概念檢查 (Fallacy Check)

檢查邏輯謬誤與概念誤用。

**Output Structure:**
```markdown
# Phase 6 — 謬誤與概念檢查

## 潛在邏輯問題

### 1. {謬誤類型}
> {引用段落}

**問題：** {為何是謬誤/問題}

### 2. {謬誤類型}
> {引用段落}

**問題：** {為何是謬誤/問題}

## 概念使用問題

### 1. 「{概念}」的{問題類型}
{具體描述}

### 2. 「{概念}」的{問題類型}
{具體描述}
```

請引用具體段落與問題。

---

### Phase 7 — 概念白話化 (Key Concepts Explained)

用高中生能懂的方式解析所有重要術語。

**Output Structure:**
```markdown
# Phase 7 — 概念白話化

## 關鍵術語解釋（高中生版）

### 1. {概念}
**比喻：** {生活化比喻}
**本文用法：** {在文章中的具體意義}

### 2. {概念}
**比喻：** {生活化比喻}
**本文用法：** {在文章中的具體意義}

（依此類推）
```

不使用未定義的專業詞。

---

### Phase 8 — 學習路徑 (Learning Recommendations)

提供深入理解的學習建議。

**Output Structure:**
```markdown
# Phase 8 — 學習路徑

## 必備基礎知識

### 1. {知識領域}
- **重要性：** {為什麼需要}
- **推薦資源：**
  - {書名/資源} — {作者}
  - {書名/資源} — {作者}

### 2. {知識領域}
- **重要性：** {為什麼需要}
- **推薦資源：**
  - {書名/資源} — {作者}

## 進階理論

### 1. {理論名稱}
- **重要性：** {為什麼需要}
- **推薦資源：**
  - {書名/資源} — {作者}

## 實務應用

### 1. {應用領域}
- **重要性：** {為什麼需要}
- **推薦資源：**
  - {書名/資源} — {作者}
```

---

### Phase 9 — 現勢推演 (Scenario Projection)

基於今日最新新聞進行推演。

**Output Structure:**
```markdown
# Phase 9 — 現勢推演

## 各方可能回應

### 1. {行為者}
- **最可能：** {預期行動}
- **{具體面向}：** {詳細說明}
- **（推測）**

### 2. {行為者}
- **最可能：** {預期行動}
- **{具體面向}：** {詳細說明}
- **（推測）**

## 政策/市場可能變化

### 1. {領域}
- **短期：** {影響}
- **中期：** {影響}

### 2. {領域}
- **短期：** {影響}
- **中期：** {影響}

## 二階影響

### 1. {影響領域}
{描述}

### 2. {影響領域}
{描述}
```

請註明哪些是推測。

---

### Phase 10 — 自我驗證 (Second Pass)

執行分析的自我檢驗。

**Output Structure:**
```markdown
# Phase 10 — 自我驗證（Second Pass）

## 1. 站在作者立場反駁我的批評

**對「{批評1}」批評的反駁：**
> {作者可能的辯護}

**對「{批評2}」批評的反駁：**
> {作者可能的辯護}

## 2. 檢查自己的分析是否過度延伸

### 可能的過度延伸：
1. {Phase X的分析可能過度，因為...}
2. {Phase Y的分析可能過度，因為...}
3. {Phase Z的分析可能過度，因為...}

## 3. 最可能出錯的部分

1. **{判斷1}：** {為何可能錯}
2. **{判斷2}：** {為何可能錯}
3. **{判斷3}：** {為何可能錯}

## 4. 最終修正版結論

> **{經過自我驗證後的最終結論，應更精確、更平衡}**
```

---

## 分析完成標準

分析必須同時具備：
- ✅ 結構完整（10個Phase全部完成）
- ✅ 概念清晰
- ✅ 邏輯穩定
- ✅ 批判與公平兼具
- ✅ 具備政策或策略價值

若未達成，請自動修正後再輸出。

---

### Task 4: Proceed to Step 2 Analysis Framework

After completing Tasks 0-3, proceed to the **Analysis Framework** (Section 2) for structured data extraction:

- Generate `key_entities` list
- Identify `trend_signals`
- Calculate `market_impact` score
- Set `monitoring_triggers`
- Determine `action_required` and `urgency`

---

## Step 3 – Content Cleaning

1. Remove HTML tags, scripts, styles
2. Strip advertisements and navigation
3. Extract main article body
4. Preserve paragraph structure
5. Normalize whitespace

---

# 2️⃣ Analysis Framework (Step 2 Structured Analysis)

> **Note:** This section is executed as **Task 4** after completing the Initial Analysis (Tasks 0-3).
> The 9-point qualitative analysis (`{ARTICLE_ID}_Analysis.md`) provides deep reading;
> this section generates structured data for aggregation and prioritization.

## Analysis Output Schema

For each article, generate (append to `{ARTICLE_ID}_Analysis.md`):

```yaml
summary: "2-3 sentence summary of key points"

key_entities:
  - name: "Entity name"
    type: "company|government|person|organization"
    relevance: "high|medium|low"
    context: "Role in the story"

trend_signals:
  - signal: "Description of trend"
    direction: "emerging|accelerating|stable|declining"
    confidence: 0.0-1.0
    implications: "Future outlook"

market_impact:
  score: 1-10
  rationale: "Scoring justification"
  sectors: ["affected sectors"]
  timeframe: "immediate|short|medium|long"
  direction: "positive|negative|neutral|mixed"

monitoring_triggers:
  - trigger: "Condition to watch"
    threshold: "When to act"
    action: "Recommended response"

action_required: true|false
urgency: "immediate|today|this_week|monitor"
tags: ["topic", "tags"]
```

---

## Entity Classification

| Type | Examples |
|------|----------|
| Government | CCP, State Council, NDRC, SAMR, White House, EU Commission |
| Company | Huawei, NVIDIA, OpenAI, Alibaba, Meta |
| Person | Xi Jinping, Sam Altman, Jensen Huang |
| Organization | IMF, WTO, IEEE, ASEAN |
| Technology | GPT-4, DeepSeek-V3, Kirin chip |

---

## Trend Signal Directions

| Direction | Definition | Example |
|-----------|------------|---------|
| Emerging | First signs of new development | New AI regulation proposed |
| Accelerating | Existing trend gaining momentum | Export controls tightening |
| Stable | Consistent pattern, no change | Ongoing chip shortage |
| Declining | Trend losing relevance | Trade war de-escalation |

---

# 3️⃣ Trend Forecasting

## Multi-Article Pattern Detection

When analyzing multiple articles:

1. **Dominant Themes** – Most frequently appearing topics
2. **Emerging Patterns** – New developments across sources
3. **Contrarian Signals** – Evidence against mainstream narrative
4. **Cross-Cutting Issues** – Connections between unrelated stories

## Trend Output Schema

```yaml
dominant_themes:
  - theme: "Theme name"
    article_count: N
    key_developments: ["Development 1", "Development 2"]
    significance: "high|medium|low"

emerging_patterns:
  - pattern: "Pattern description"
    evidence: ["Supporting articles"]
    potential_impact: "Impact description"

contrarian_signals:
  - mainstream_view: "Common narrative"
    contrarian_indicator: "Counter-evidence"
    watch_for: "Validation criteria"

cross_cutting_issues:
  - issue: "Issue description"
    connections: ["How articles relate"]
    synthesis: "Combined insight"

overall_assessment: "2-3 sentence day summary"
```

---

# 4️⃣ Market Impact Scoring

## Scoring Scale (1-10)

| Score | Category | Description | Action |
|-------|----------|-------------|--------|
| 1 | Routine | No market relevance | Ignore |
| 2 | Minor | Limited scope, niche interest | Archive |
| 3 | Background | Indirect relevance, context only | Note |
| 4 | Notable | Worth tracking, potential future impact | Monitor |
| 5 | Moderate | Sector-specific implications | Track closely |
| 6 | Significant | Multiple sector implications | Review today |
| 7 | Major | Broad market implications | Action recommended |
| 8 | High Impact | Portfolio-relevant, multi-sector | Prioritize |
| 9 | Critical | Market-moving potential | Immediate review |
| 10 | Crisis | Breaking news, urgent action needed | Act now |

## Scoring Factors

1. **Scope** – How many sectors/companies affected?
2. **Magnitude** – Scale of impact (revenue, policy change)
3. **Timing** – How soon will effects materialize?
4. **Certainty** – Speculation vs confirmed action
5. **Reversibility** – Can decisions be undone?

## Score Adjustments

- **+1** if both China AND AI themes present
- **+1** if from Tier 1 source (Reuters, FT, Bloomberg)
- **-1** if speculative/unconfirmed
- **-1** if rehashing old news

---

# 5️⃣ Action Prioritization

## Priority Score Formula

```
Priority = (Impact × 0.4) + (Urgency × 0.3) + (Theme × 0.2) + (Source × 0.1)
```

Where:
- **Impact**: Market impact score (1-10)
- **Urgency**: immediate=10, today=8, this_week=5, monitor=2
- **Theme**: Both themes=10, Single theme=5
- **Source**: Tier 1=10, Tier 2=7, Tier 3=4

## Priority Categories

| Category | Criteria | Action |
|----------|----------|--------|
| Urgent | Score ≥8.0 OR urgency="immediate" | Immediate attention |
| High | Score ≥6.0 OR urgency="today" | Review within 4 hours |
| Monitor | Score ≥4.0 OR urgency="this_week" | Daily check-in |
| Background | Score <4.0 | Archive for reference |

## Source Tiers

| Tier | Sources | Reliability |
|------|---------|-------------|
| 1 | Reuters, Bloomberg, FT, Economist | Highest |
| 2 | AP News, WSJ, SCMP, Nikkei | High |
| 3 | Politico, The Verge, TechCrunch | Medium |
| 4 | Social media, blogs | Verify first |

---

# 6️⃣ Daily Briefing Structure

## Executive Summary
- Headline: One-line day summary
- Key count: Urgent / High / Monitor items
- Top development per theme (China / AI)

## Urgent Section
- Articles requiring immediate attention
- Recommended actions per item
- Monitoring triggers

## High Priority Section
- Detailed analysis summaries
- Impact rationale
- Watch points

## Monitor Section
- Brief summaries
- Why it matters
- Follow-up timing

## Trend Analysis
- Dominant themes of the day
- Emerging patterns
- Cross-cutting insights

## Full Article Table
- Rank, Title, Source, Impact, Urgency
- Links to original and processed versions

---

# 7️⃣ Quality Assurance

## Analysis Validation

- [ ] Summary accurately reflects article content
- [ ] Entities correctly classified
- [ ] Impact score justified with rationale
- [ ] Urgency level appropriate
- [ ] No hallucinated information

## Briefing Validation

- [ ] All urgent items flagged
- [ ] Priority ranking makes sense
- [ ] Trends supported by evidence
- [ ] Action items are actionable
- [ ] No duplicate articles

---

# 8️⃣ Error Handling

## Scraping Failures
- Log error with source and timestamp
- Continue with other sources
- Report in daily summary

## Analysis Failures
- Use fallback scoring (score=5, urgency=monitor)
- Flag for manual review
- Don't block pipeline

## LLM Failures
- Retry with exponential backoff (3 attempts)
- Fall back to mock analysis
- Alert via notification

---

# Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-02-22 | Initial framework |
| 1.1 | 2026-02-22 | Added Article Processing Workflow (Step 2): numbering, transcription, metadata, 9-point analysis framework |
| 1.2 | 2026-02-22 | Added ISO 8601 date format standard; Firefox scraper implementation (`scripts/firefox_scraper.py`) |
| 1.3 | 2026-02-24 | **Major update:** Upgraded from 9-point to **10-phase analysis framework** — Added Phase 0 (Semantic Layer) for logic reconstruction before evaluation; Added Phase 10 (Second Pass) for self-verification; Restructured all phases with improved output templates |
