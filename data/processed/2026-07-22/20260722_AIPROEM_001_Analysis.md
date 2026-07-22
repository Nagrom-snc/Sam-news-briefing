---
id: "20260722_AIPROEM_001"
title: "Quick take on Kimi K3 and the end of \"DeepSeek moments\""
url: "https://aiproem.substack.com/p/quick-take-on-kimi-k3-and-the-end"
source: "AI Proem"
date: "2026-07-20"
author: "Grace Shao"
analyzed_at: "2026-07-22T07:35:00Z"
language: "zh-hant"
---

# Quick take on Kimi K3 and the end of "DeepSeek moments" — 分析報告

## Phase 0 — 語意建模（Semantic Layer）

### 核心命題
- Kimi K3 為 Moonshot AI（月之暗面）最新旗艦模型，是當前 AI 圈討論焦點。
- 中國開源／開放權重模型整體尚未在所有任務上追平最強美國閉源前沿，但 Kimi K3 已在部分領域（尤其前端程式碼）展現超越 OpenAI、Anthropic 旗艦的表現。
- 完整開放權重釋出預計至 7 月 27 日，部分性能宣稱仍待獨立驗證。
- 作者主張：中國重大模型發布已頻繁到不應再稱每次為「DeepSeek moment」。
- 中國模型雖未必長期居絕對第一，但在能力、成本與迭代速度上已足以改變整體 AI 市場經濟學。
- Moonshot 定價仍明顯低於 Anthropic 旗艦 Fable 5（輸入 $10／百萬 token、輸出 $50／百萬 token）。
- 前沿實驗室的核心風險不是模型突然無用，而是前沿級能力難以以溢價定價變現。
- Kimi 推出分級定價並急於擴展算力；GLM、DeepSeek 也曾因算力限制而選擇性服務客戶；企業客戶通常優先於消費者。
- 算力壓力亦推升對中國國內晶片供應商的需求。
- OpenAI 據報正探索降價，並面臨模型定價壓力。
- 企業與新創 increasingly 將工作負載導向更便宜的開源與中國模型（DeepSeek、Kimi、智譜 GLM、阿里 Qwen、Nvidia Nemotron）。
- 客戶不再默認以 Anthropic、OpenAI 作為所有任務的預設基礎設施，而改採編排層（orchestration）選擇「夠用且最便宜」的模型，形成混合模型策略。
- 最貴的前沿模型 increasingly 保留給困難推理、程式碼等高價值工作流。
- DeepSeek 自 2025 年 5 月中旬起為 OpenRouter 使用量最高的 AI 公司。
- OpenRouter 高支出客戶中，2025 秋至 2026 春開源 token 使用量增速為閉源的約四倍；逾 500 家機構從專有模型轉向開源。
- 作者不認為這代表前沿實驗室終結：閉源旗艦仍可能在最高價值 token 份額占優，開源／中國模型可能在最高 volume 份額占優——類比 Apple 對 Android，而非贏者全拿。
- 對 AI 基礎設施供應商，推理成本下降可能擴大總 consumption（Jevons 悖論）。
- 企業長期價值可能不在租用「最聰明的通用模型」，而在 proprietary data、產業知識、工作流，以及選擇／微調最適模型。
- 文末回應「楊植麟為何不留在美國」的輿論：問題本身被作者視為荒謬；原因可能涉及個人、家庭、本土市場與文化認同；中國創業環境並非更容易（VC 較小、競爭激烈、變現難），但美國反中情緒上升可能增加華裔研究者的不適。
- 模型訓練仍屬資本密集、能源密集且日益政治化的基礎設施週期。
- Kimi K3 不會終結「AI trade」，但使價值分配更複雜：前沿 lab 每 token 收入可能下降；hyperscaler 可能在編排層獲益；企業靠數據與工作流留值；開源模型可能主導 token 量；晶片、電力與實體基建供應商或因便宜 intelligence 刺激需求而受益。
- 前沿競賽未消失，只是玩家增多。

### 關鍵實體與關係
| 實體 | 角色／關係 |
|------|------------|
| Moonshot AI / Kimi K3 | 中國前沿模型發布者；K3 為本文核心案例 |
| OpenAI、Anthropic | 美國閉源前沿對照組；定價與能力基準 |
| DeepSeek、智譜 GLM、阿里 Qwen、Nvidia Nemotron | 便宜替代與路由選項 |
| OpenRouter | 使用量與開源／閉源遷移的量化證據來源 |
| 楊植麟（Yang Zhilin） | Moonshot 創辦人；「為何不留美」輿論對象 |
| Grace Shao / AI Proem | 作者與出版平台 |
| 中國國內晶片製造商 | 算力缺口下的受益／承壓方 |
| 企業用戶 vs 消費者 | 算力稀缺時的優先序 |

### 時間與不確定標記
- Kimi K3 完整 open-weight 預期：**2026-07-27**（待驗證）
- DeepSeek OpenRouter 領先：**2025 年 5 月中旬起**
- OpenRouter 開源 vs 閉源增速對照：**2025 秋—2026 春**
- WAIC 2026：Globe and Mail 報導 Moonshot 展位（背景脈絡，非本文主論證）

### 論述類型
- 產業快評（quick take）＋定價經濟學分析＋人才／地緣文化評論＋價值鏈再分配推演

---

## Phase 1 — 邏輯還原（不評論）

### 主線論證結構
1. **現象設定**：Kimi K3 成為話題；但「中國趕超美國前沿」需限縮表述——整體仍落後最強 OpenAI／Anthropic，部分任務領先，且 open-weight 尚未完全釋出。
2. **概念修正**：「DeepSeek moment」標籤因重複而失去意義；真正訊號是 AI 前沿更全球化、更競爭、更少專有化。
3. **經濟機制**：中國模型「夠近、夠便宜、夠快」→ 改變 token 經濟 → 威脅前沿 lab 的**溢價變現能力**（非模型報廢）。
4. **定價證據**：Moonshot 定價低於 Anthropic Fable 5 一個量級以上（具體數字引用）。
5. **供給側摩擦**：Kimi 分級定價、搶算力；同業（GLM、DeepSeek）曾有類似算力配給；企業優先；倒逼國產晶片。
6. **需求側轉向**：OpenAI 探索降價；客戶用 orchestration 做任務級路由；高難度任務留給貴模型。
7. **量化佐證**：OpenRouter 上 DeepSeek 使用量第一；高支出客戶開源 token 四倍速；500+ 機構遷移。
8. **反終局論**：前沿 lab 不會死——Apple／Android 式分工：高價值 token vs 高 volume token。
9. **基礎設施樂觀面**：更低 inference 成本 → Jevons 悖論 → 總 token 需求上升 → 對 infra 供應商可能淨正面。
10. **企業 moat 重定義**：價值在 proprietary data／workflow，不在租用單一最強 GP 模型。
11. **人才敘事插段**：駁斥「楊植麟應留美」的簡化問法；列舉中美創業環境與 Sinophobia 因素。
12. **總結**：Kimi K3 不 kill AI trade，但打散價值分配；競賽持續、玩家增加。

### 隱含前提（作者未明言但論證依賴）
- Token 定價與路由行為可代表產業結構變遷。
- OpenRouter 樣本能外推至 broader enterprise／startup 行為。
- 「夠便宜且夠好」的模型對多數任務具有可替代性。
- 算力稀缺是短期結構性約束，而非永久瓶頸。

---

## Phase 2 — 8個 Key Takeaways

1. **「DeepSeek moment」已過時**：中國重大模型發布從驚喜事件變成常態，真正議題是持續性的全球前沿競爭，而非單次震撼。
2. **追平是「整體仍差一點、局部已領先」**：Kimi K3 整體仍不及最強 OpenAI／Anthropic，但前端 coding 等領域已有超越案例；7 月 27 日前 claims 需獨立 benchmark 驗證。
3. **核心威脅是 monetization，不是 obsolescence**：前沿 lab 的風險在於難以對「可被 open-weight 以極低成本覆蓋的任務」收取溢價。
4. **定價差距具體且巨大**：Moonshot 定價 materially below Anthropic Fable 5（$10/$50 per M tokens），這是 enterprise 路由決策的硬錨點。
5. **混合模型＋orchestration 成主流**：客戶按任務選最便宜夠用模型；貴模型 reserved for hard reasoning／coding。
6. **OpenRouter 數據支持開源 volume 遷移**：DeepSeek 使用量第一；高支出客戶開源 token 增速 4×；500+ org 從 proprietary 轉向 open-source。
7. **產業結構像 Apple vs Android，非 winner-take-all**：閉源占 high-value token share；開源／中國模型占 high-volume share；兩者可長期共存。
8. **價值鏈再分配**：前沿 lab 每 token 收入↓；hyperscaler orchestration↑；企業 data/workflow moat↑；晶片／電力／基建或因 Jevons 效應↑。

---

## Phase 3 — 立場與預設分析

### 作者立場
- **Grace Shao（AI Proem）**：深耕中國 AI 與全球 token 經濟的 industry observer；語氣務實、略帶對 hype 標籤的疲態（「stop calling every release a DeepSeek moment」）。
- 對中國模型：**肯定進步但反對「已全面趕超」的簡化敘事**；強調 cost／iteration 對 market structure 的結構性影響。
- 對美國前沿 lab：**非 bearish 終局**，認為仍握有高價值工作流；但對 premium pricing sustainability 持審慎態度。
- 對楊植麟／人才話題：**明確反對「為何不留美」的框架**，視其為忽视个人與本土創業動機的 ridiculous question；同時承認 Sinophobia 為 real but secondary factor。

### 預設（Assumptions）
| 預設 | 強度 | 說明 |
|------|------|------|
| 價格是 enterprise 採購的一階決策因子 | 高 | 全文反覆以 token  economics 為軸 |
| 多數任務不需要最貴 frontier 模型 | 高 | hybrid routing 敘事核心 |
| OpenRouter 具代表性 | 中 | 樣本偏 developer／API 路由人群 |
| Jevons 悖論適用於 AI inference | 中 | 類比歷史能源效率，未量化驗證 |
| 中國模型共享 R&D base 加速迭代 | 中 | 一筆帶過，缺具體機制證據 |
| Kimi K3 前端 coding 優勢屬實 | 中低 | 待 open-weight 與第三方 replicate |

### 利益相關可能
- AI Proem 為 Substack 付費／訂閱媒體；podcast 系列（Pony.ai CEO 等）暗示作者 ecosystem 嵌入中国 tech narrative。
- 文中多次 internal link（hybrid model、enterprise moat、Yang Zhilin 專訪），有 content funnel 目的，但不必然扭曲主論證。

---

## Phase 4 — 問題層級評估

| 層級 | 問題 | 緊迫度 | 可驗證性 |
|------|------|--------|----------|
| L1 事實 | Kimi K3 整體 benchmark 排名、7/27 open-weight 是否如期 | 高（近 term） | 高——公開 benchmark／release |
| L1 事實 | Moonshot vs Anthropic 官方定價 | 中 | 高——pricing page |
| L2 因果 | 低價 open-weight 是否已 compress  frontier lab gross margin | 高 | 中——需財報／API pricing 變動 |
| L2 因果 | OpenRouter 500 org 遷移是否代表 permanent switch vs experiment | 中 | 中——縱向追蹤 |
| L3 結構 | AI 市場是否穩定走向 Apple/Android 雙軌 | 高 | 低——長期結構假設 |
| L3 結構 | Enterprise moat 是否從 model access 轉向 data/workflow | 高 | 中——需 case study |
| L4 規範 | 「DeepSeek moment」標籤是否應棄用 | 低 | N/A——命名之爭 |
| L4 規範 | 楊植麟留中國的「正當性」 | 低（輿論層） | N/A |

**本文解決深度**：對 L2–L3 產業結構問題有清晰框架與 partial evidence；對 L1 細節 performance 刻意 defer 至 external link 與 7/27 release；對人才話題偏 opinion，非 empirics。

---

## Phase 5 — 論證重構

### 標準形式重構
**主張 P**：Kimi K3 標誌著 AI 前沿競爭全球化與 token 經濟重構，但不終結 frontier lab 或 AI infra 長期需求。

**支撐論據**
- D1：K3 整體仍次於最強 US closed models，但 cost／improvement trajectory 已改變 market economics（部分任務已領先）。
- D2：Moonshot pricing << Anthropic Fable 5 → enterprise 有 strong incentive to route routine tasks away from premium closed models。
- D3：OpenRouter usage data（DeepSeek #1；4× OSS growth；500 org switch）→ demand-side shift is measurable, not anecdotal。
- D4：OpenAI exploring price cuts → even frontier incumbents feel pricing pressure。
- D5：Apple/Android analogy → high-value vs high-volume segmentation is stable equilibrium。
- D6：Jevons paradox → lower unit cost expands total tokens → infra suppliers may benefit net-net。

**結論 C**：Value capture disperses across orchestration, enterprise data moats, volume OSS, and physical infra; frontier race continues with more players.

### 論證強度評估
- **最強環節**：pricing incentive + OpenRouter 量化 + hybrid routing 行為描述——三者互相 reinforce。
- **最弱環節**：Jevons 外推（缺自家 elasticity 數據）；「共享 R&D base 加速迭代」（assertion）；K3 coding 優勢（pre-release）。

---

## Phase 6 — 謬誤與概念檢查

| 項目 | 判定 | 說明 |
|------|------|------|
| 「moment」語義論 | 合理修辭修正 | 頻繁事件確實 dilute「moment」之意；非邏輯謬誤 |
| OpenRouter → 全市場 | 可能 hasty generalization | 平台用戶 skew toward dev／cost-sensitive routing |
| Apple/Android 類比 | 启发式，非 proof | 忽略 mobile OS 的 lock-in／distribution 與 API model 差异 |
| Jevons 悖論 | 概念借用恰当但未證 | 需觀察 total spend vs unit price 是否反向 |
| False dichotomy 檢查 | 作者主动避免 | 明确说 not end of frontier labs |
| 「ridiculous question」 |  rhetorical dismiss | 對「為何不留美」之 refutation 合情理但可能 overlook structural visa／export control 作為 primary driver 的 cases |
| Survivorship／selection | 未讨论 | 未提及 failed Chinese labs or models that didn't move needle |
| 定價對照 | 需核对 | Fable 5 為作者所称 Anthropic flagship；读者应 verify 型号命名与现行价目是否一致 |

**概念澄清**
- **DeepSeek moment**：指中国模型 release 对全球 AI 秩序造成 shock 的叙事模板；作者认为已 routine化。
- **Frontier-level capability**：接近最强 closed model 的任务表现，未必等于 every benchmark SOTA。
- **Token economics**：不仅单价，还包括 volume mix、routing、fine-tuning TCO。

---

## Phase 7 — 概念白話化

**這篇文章在說什麼？**

想像 AI 模型像計程車方案：以前大家默認坐最貴的「頭等車」（OpenAI、Anthropic 旗艦）去所有地方。現在中国开源模型像平价网约车——多数路程（写邮件、简单代码、客服）够用了，而且便宜很多。Kimi K3 就是最新一款「够快够便宜」的车；它未必在每一条赛道都是第一，但已经让整个市场的计价方式松动。

作者还说：别再每次中国出新车就喊「又一次 DeepSeek 地震」——地震太多次就不叫地震，叫地质常态了。

**那美国大公司会倒吗？** 作者说不会。就像苹果卖高端、安卓卖量——最贵的模型还是会用在最难、最值钱的工作（复杂推理、关键代码）。但靠「我是最贵的所以每单都赚很多」会越来越难。

**跟芯片、电力有什么关系？** 模型越便宜，大家越舍得用，总用量可能反而暴增（像电费便宜了，人反而开更多空调）——所以做芯片、数据中心的人未必吃亏。

**楊植麟那段呢？** 作者觉得问「为什么不留在美国」本身就很蠢——可能是想在家乡创业、陪家人、用母语做产品；中国创业并不轻松，美国反中氛围也可能让人不舒服，但不必简化成单一原因。

---

## Phase 8 — 學習路徑

### 若想理解 Kimi K3 本身
1. 等待 **2026-07-27** open-weight 发布 → 跑独立 benchmark（MMLU、HumanEval、SWE-bench 等）。
2. 对照 Moonshot 官方 pricing 与 API tier 文档。
3. 阅读作者外链：「Have Chinese AI Models Caught Up to the US Frontier?」（AI Proem 长文）。

### 若想理解 token 经济与市场结构
1. OpenRouter rankings / usage reports（DeepSeek、Kimi、closed model share）。
2. Anthropic、OpenAI、Moonshot、DeepSeek pricing pages 横向对比。
3. 企业案例：orchestration 框架（LiteLLM、LangChain router、自建 gateway）如何选 model。

### 若想理解价值分配论点
1. Jevons paradox 原文脉络（William Stanley Jevons, coal consumption）。
2. AI Proem 前文：hybrid model approach、enterprise proprietary data moat。
3. Hyperscaler earnings calls 中 AI inference revenue vs margin commentary。

### 若想理解人才与地缘政治
1. Yang Zhilin 专访（作者指一年前 AI Proem  piece）。
2. 中国 AI VC 融资数据 vs 美国（验证「VC pool smaller」）。
3. 出口管制、芯片自给政策对 Moonshot compute scramble 的约束。

---

## Phase 9 — 現勢推演

### 短期（0–3 个月）
- **7/27 Kimi K3 open-weight**：若 benchmark  confirm 前端 coding 优势 → media cycle 再起，但「moment」 framing 可能被 ignore；若不及预期 → 「中国追赶」叙事降温。
- **Frontier lab 定价**：OpenAI 若官宣降价 → 印证 author thesis；Anthropic 若守价 → high-value segment 分化更明显。
- **算力配给**：Kimi tiered pricing、排队、enterprise priority 持续；国产 GPU 订单与交付新闻可作 monitor。

### 中期（3–12 个月）
- **Enterprise routing 常态化**：500+ org 迁移若持续 → OSS／中国 model 在 routine task 成为 default；closed flagship 成「premium tier」。
- **Margin compression vs volume expansion**：观察 frontier lab API revenue growth 是否 decouple from token volume growth（Jevons 是否成立）。
- **Orchestration layer 价值**：云厂商、MaaS、router startups 捕获更多 value chain 环节。

### 长期（1–3 年）
- **双轨结构固化或反弹**：若 closed models 在 agentic／multimodal 拉开 gap → Apple/Android 类比失效，重回 capability-led premium；若 gap 持续 narrow → commoditization accelerates。
- **Enterprise moat 验证**：self-hosted fine-tuned OSS + proprietary workflow 是否成为 Fortune 500 标准架构。
- **地缘政治**：训练算力、芯片、电力、人才流动持续 politicized；「在哪训练、哪推理」成 procurement 合规维度。

### 情景矩阵
| 情景 | 触发 | 含义 |
|------|------|------|
| A. 温和 commoditization | OSS 够好 + 价格战 | 作者 baseline；infra 总量↑、frontier ARPU↓ |
| B. Capability re-widen | 下一代 closed leap | 「moment」叙事回流；routing 回摆向 premium |
| C. 监管／地缘切割 | 跨境 API 限制 | OpenRouter 路径失真；区域化 model markets |
| D. 算力长期稀缺 | 国产芯片不及预期 | 低价 promise 难兑现；tiered access 常态化 |

---

## Phase 10 — 自我驗證（Second Pass）

### 完整性检查
- [x] Phase 0 仅描述、无评价
- [x] 10 个 Phase 齐全
- [x] 分析基于 scraped 全文（非 paywall preview）；文末 subscription CTA 不影响 body 完整性
- [x] Traditional Chinese
- [x] YAML structured data  appended

### 关键缺口（文章未提供、分析已标注）
- Kimi K3 系统 benchmark 数字、参数量、训练 compute——defer 至外链与 7/27 release
- OpenRouter 「四倍速」「500 org」原始 methodology
- 「Fable 5」是否为 Anthropic 当前对外旗舰正式名称——读者需 cross-check
- Nvidia Nemotron 在 enterprise 路由中的实际 penetration

### 评分自检（market_impact）
- 主题：中国 AI + 全球 token 经济 → **+1**（spec adjustment）
- 非纯 speculative preview → **不扣分**
- 属 trend commentary，非单一 corporate/event shock → base **6**，调整后 **7**

### 与原文一致性
- 未引入文章外 factual claims 作为已证实事实
- Apple/Android、Jevons、Sinophobia 等均为 author 原文框架的忠实重构

---

## Analysis Framework (Structured Data)

```yaml
summary: "Grace Shao 認為 Kimi K3 顯示中國開源模型在成本與迭代速度上已結構性改變 AI token 經濟，但整體仍略遜最強美國閉源前沿；「DeepSeek moment」標籤因頻繁發布而失效。她主張市場將走向 Apple 對 Android 式分工——閉源占高價值 token、開源占高 volume——前沿 lab 面臨的是溢價變現壓力而非終局，而編排層、企業數據護城河與晶片／電力基建可能重新分配價值。"
key_entities:
  - name: "Moonshot AI"
    type: "company"
    relevance: "high"
    context: "Kimi K3 發布方；定價低於美系旗艦，正擴展算力與分級定價"
  - name: "Kimi K3"
    type: "technology"
    relevance: "high"
    context: "本文核心案例；open-weight 預計 7/27 釋出，部分性能待驗證"
  - name: "OpenAI"
    type: "company"
    relevance: "high"
    context: "美國閉源前沿對照；據報探索降價"
  - name: "Anthropic"
    type: "company"
    relevance: "high"
    context: "Fable 5 定價標竿（$10/$50 per M tokens）；高價值工作流保留地"
  - name: "DeepSeek"
    type: "company"
    relevance: "high"
    context: "OpenRouter 使用量第一；開源遷移標誌性案例"
  - name: "OpenRouter"
    type: "organization"
    relevance: "medium"
    context: "提供開源 vs 閉源 token 增速與 500+ org 遷移數據"
  - name: "楊植麟"
    type: "person"
    relevance: "medium"
    context: "Moonshot 創辦人；人才留美輿論之回應對象"
  - name: "Grace Shao"
    type: "person"
    relevance: "medium"
    context: "AI Proem 作者；產業快評與 token 經濟論述"
  - name: "智譜 GLM"
    type: "company"
    relevance: "low"
    context: "曾算力配給；便宜路由選項之一"
  - name: "阿里 Qwen"
    type: "company"
    relevance: "low"
    context: "企業路由中的中國開源選項"
  - name: "Nvidia Nemotron"
    type: "technology"
    relevance: "low"
    context: " increasingly 被路由的開源／開放權重選項"
trend_signals:
  - signal: "中國 open-weight 模型以低價覆蓋 routine tasks"
    direction: "accelerating"
    confidence: 0.82
    implications: "美系 frontier API 溢價承壓；enterprise 混合路由成標配"
  - signal: "OpenRouter 開源 token 增速遠超閉源"
    direction: "accelerating"
    confidence: 0.75
    implications: "volume share 向 OSS 傾斜；需追蹤是否為永久遷移"
  - signal: "Frontier lab 探索降價"
    direction: "emerging"
    confidence: 0.7
    implications: "價格戰可能從中國模型外溢至美系 incumbent"
  - signal: "算力稀缺導致 tiered access 與 enterprise 優先"
    direction: "stable"
    confidence: 0.78
    implications: "國產晶片需求上升；消費者端體驗可能不均"
  - signal: "企業價值從 model rental 轉向 data/workflow moat"
    direction: "emerging"
    confidence: 0.65
    implications: "自托管微調 OSS 架構可能加速"
  - signal: "AI 推理 Jevons 效應（量增快於價跌）"
    direction: "emerging"
    confidence: 0.55
    implications: "晶片／電力／數據中心長期需求可能仍扩张"
market_impact:
  score: 7
  rationale: "文章勾勒中國 AI 與全球 token 定價結構性重組，對 enterprise AI 採購、雲端／API 供應商定價策略及 AI 基建投資框架具參考價值；惟屬快評而非單一財報事件，且 Kimi K3 完整 open-weight 與 benchmark 仍待 7/27 驗證。主題同時涵蓋 China 與 AI（+1）。"
  sectors: ["人工智慧", "雲端運算", "半導體", "企業軟體", "venture capital"]
  timeframe: "short"
  direction: "mixed"
monitoring_triggers:
  - trigger: "Kimi K3 open-weight 發布"
    threshold: "2026-07-27 前後；第三方 benchmark 與官方 claim 偏差 >5% 排名位次"
    action: "更新「中國趕超」敘事強度與 enterprise 路由預設"
  - trigger: "OpenAI / Anthropic 官方 API 降價"
    threshold: "旗艦模型 input 或 output 單價下調 ≥15%"
    action: "確認 premium pricing 壓力由結構性轉為 incumbent 主动应战"
  - trigger: "OpenRouter 開源 token 占比"
    threshold: "連續兩季 OSS share 占新增 token >70%"
    action: "评估 volume commoditization 是否进入不可逆阶段"
  - trigger: "Moonshot 算力／國產芯片交付新聞"
    threshold: "大规模 GPU 集群上线或排队时间显著下降"
    action: "检验 cheap inference promise 能否规模化兑现"
action_required: false
urgency: "monitor"
tags: ["Kimi K3", "Moonshot AI", "DeepSeek moment", "token economics", "open weights", "China AI", "hybrid models", "OpenRouter", "frontier labs", "Jevons paradox"]
```
