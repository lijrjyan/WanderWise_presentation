# Intuit Proud Project（~7min）逐条验收材料（Checklist-Style）

目标：把 Intuit 官方 Proud Project 要求拆成可验收项，并给出**可直接复述的英文句子** + **代码证据锚点** + **风险等级**（Low/Medium/High）。

> 说明：本材料只使用 repo 内可验证的信息；对无法从代码/数据直接证明的内容，明确标注为“需要你补充/实测”。

---

## 0) 7 分钟讲述结构（STAR + discussion-friendly）

建议你把 7 分钟拆成 6 段，任何一段被打断都能继续讲：

1. **Role (15s)**：一句话角色定义 + 责任边界
2. **Situation (30s)**：用户痛点（旅行信息分散、路线难规划）
3. **Task (30s)**：目标（NL → route + recommendations + map）
4. **Action (4m)**：按“LLM → Maps → Route → Retrieval → UI”模块讲，每段 30–60s
5. **Result (45s)**：给出可验证结果（数据规模/闭环/可 demo）
6. **Learnings + Hindsight (45s)**：至少 2 条“如果重来我会…”的明确句子

---

## 1) 验收项 1：Your specific role（角色）

**验收目标**：面试官不用推断，你的 ownership/边界清晰。

**推荐开场金句（英文，可背）**

- **版本 A（最稳 / end-to-end owner）**  
  “I was the end-to-end owner of WanderWise, responsible for the system architecture, backend APIs, and the interactive map-based frontend.”

- **版本 B（强调 trade-offs）**  
  “I owned the key engineering decisions end-to-end, especially the trade-offs between quality, latency, and cost across the pipeline.”

**你需要补充的一句话（自填，避免被动）**

- “This was a **[solo / team]** project. My responsibility was **[architecture + backend + frontend + data pipeline]**.”

**代码证据锚点**

- Frontend entry + flow: `frontend/src/App.tsx`, `frontend/src/components/SearchPage.tsx`, `frontend/src/hooks/useLocations.ts`
- Backend entry + flow: `backend/fastApiProject/main.py`, `backend/fastApiProject/app/routers/router.py`

**风险等级**

- 如果你不明确说 “solo / team”：**Medium**
- 如果你提前给出一句标准答案：**Low**

---

## 2) 验收项 2：Project goals and how you achieved them（目标 + 达成方式）

**验收目标**：目标清晰，并且 Action 与目标一一对应。

**可复述目标句（英文）**

“The goal was to turn a natural-language travel request into an executable route and nearby recommendations, and visualize everything on a map with a smooth user experience.”

**达成方式（把目标拆成 4 个可对应的动作）**

- Understand intent from NL query (LLM)
- Resolve real places and route points (Google Places + Directions)
- Retrieve nearby enriched content (Elasticsearch + MySQL mapping)
- Render an interactive experience (React + Google Maps UI)

**代码证据锚点**

- LLM query parsing: `backend/fastApiProject/app/external/DeepSeek.py`
- Places + routing: `backend/fastApiProject/app/external/GoogleMap.py`, `backend/fastApiProject/app/core/RoutePlanner.py`
- Retrieval: `backend/fastApiProject/app/services/PlaceService.py`, `backend/fastApiProject/app/services/PostService.py`, `backend/fastApiProject/app/services/PlacePostService.py`
- Frontend rendering: `frontend/src/components/map/MapContainer.tsx`, `frontend/src/components/map/PathDisplay.tsx`, `frontend/src/components/map/LocationCard.tsx`

**风险等级**：Low（你当前材料这一项已经很强）

---

## 3) 验收项 3：Problem-solving skills demonstrated（问题解决能力）

**验收目标**：不是“罗列问题”，而是“发生了什么 → 我怎么判断 → 我怎么取舍 → 结果如何”。

下面给你 3 个“现成可讲”的 problem-solving story cards（都能从代码找到证据）。

### Story A：LLM 输出不稳定 → 解析/兜底（Reliability）

**Situation/Problem**  
LLM 输出是概率性的，早期会出现非 JSON 或结构不完整，导致下游流程断掉。

**Action（英文可复述）**  
“I treated the LLM as an unreliable component and added a parse-and-validate layer: I extracted the JSON payload, attempted strict JSON decoding, and used safe fallbacks when parsing failed so downstream services wouldn’t crash.”

**Evidence**  
`backend/fastApiProject/app/external/DeepSeek.py`：用正则提取 JSON，再 `json.loads`，失败返回空列表/默认分数。

**Risk**  
你能说“我做了稳定性兜底”，但别夸大成“完全解决 hallucination”。  
风险等级：Low–Medium（取决于你是否说得过满）。

### Story B：路线最优 vs 响应速度 → 选择贪心（Trade-off）

**Situation/Problem**  
路线规划可以做最优（TSP/OR-Tools），但会增加实现复杂度与响应时间。

**Action（英文可复述）**  
“For the MVP, I prioritized responsiveness and reliability over optimality. I implemented a greedy nearest-neighbor route planner, which is fast and good enough for an interactive experience, and left room for future optimization like 2-opt.”

**Evidence**  
`backend/fastApiProject/app/core/RoutePlanner.py`：角落起点 + 最近邻贪心；备注提到可扩展 2-opt。

**Risk**：Low（这是典型工程 trade-off，面试官通常喜欢）

### Story C：重复召回/噪声结果 → 去重 + 距离采样（Quality + Cost）

**Situation/Problem**  
路线采样点附近检索会产生重复地点；采样点过密会放大 ES 查询次数与成本。

**Action（英文可复述）**  
“To keep results stable and avoid redundant retrieval work, I deduplicated places across sampled route points and limited the retrieval size per point. I also sampled route points by distance to control query volume.”

**Evidence**  
`backend/fastApiProject/app/external/GoogleMap.py`：`sample_distance=500` 米采样（默认）；`max_retries=3`。  
`backend/fastApiProject/app/routers/router.py`：`places_set` 去重，且每个点 `size=10` 拉取。

**Risk**：Low（讲清楚“为什么这么做”即可）

---

## 3.5) Repo 可证的 Trade-offs（至少 2 条，直接可讲）

> 目标：把 trade-off 讲成“我为什么不选更复杂方案”的工程决策，而不是技术堆砌。

### Trade-off 1：路线质量（最优） vs 延迟/可交付（MVP）

- **What I traded off**：最优路径（TSP/OR-Tools/2-opt） vs 快速响应、稳定可交付的 MVP。
- **Why**：面向交互式地图体验，延迟和稳定性更重要；先打通闭环再优化。
- **Evidence**：`backend/fastApiProject/app/core/RoutePlanner.py`（最近邻贪心；并留有优化占位 `optimize_route`）。
- **20 秒可复述（英文）**  
  “For routing, I intentionally chose a greedy nearest-neighbor planner instead of an optimal solver. It’s fast and reliable for an interactive MVP, and I left room to add a lightweight optimizer like 2-opt later.”

**风险等级**：Low（典型工程 trade-off，面试官通常喜欢）

### Trade-off 2：结果覆盖/精度 vs 成本/延迟（路线采样点）

- **What I traded off**：更密集采样（更高覆盖、更精细的周边召回） vs 更少查询次数（更低成本、更低延迟）。
- **Why**：每个采样点都会触发 ES 周边检索；采样过密会放大查询次数、延迟和噪声。
- **Evidence**：`backend/fastApiProject/app/external/GoogleMap.py`（`sample_distance=500` 米采样点）；`backend/fastApiProject/app/routers/router.py`（对 sampled_points 循环检索）。
- **20 秒可复述（英文）**  
  “To control latency and cost, I sampled route points by distance instead of querying every polyline point. That reduces the number of geo-queries while still covering the route well enough for nearby recommendations.”

**风险等级**：Low–Medium（别说成“最优采样”，说成“可控成本/延迟的工程选择”）

### Trade-off 3（可选）：地图状态实时性 vs 前端流畅度（debounce）

- **What I traded off**：每次拖拽/缩放都即时同步状态 vs 限频更新减少抖动与重渲染。
- **Evidence**：`frontend/src/components/map/MapContainer.tsx`（`onCenterChanged`/`onZoomChanged` 300ms debounce）。
- **一句话可说（英文）**  
  “On the frontend, I debounced map state updates to avoid excessive re-renders—slightly less real-time, but a smoother experience.”

**风险等级**：Low（你能指出具体实现细节，会加分）

## 4) 验收项 4：Project outcomes and accomplishments（成果）

**验收目标**：给出“可验证”的结果信号（哪怕是轻量指标）。

### 4.1 Repo 内可验证的成果（可直接说）

以下数据来自 repo 自带样本数据（可本地复核）：

- Places 数据：`backend/fastApiProject/app/data/place_es_data.json` = **1137** 条
- Posts/Notes 数据：`backend/fastApiProject/app/data/post_es_data.json` = **603** 条
- Place↔Post 映射：`backend/fastApiProject/app/data/place_post_mysql_data.json` = **4729** 条
- 映射覆盖：**1135** 个 unique place_id；平均 **4.17** notes / place；平均 **7.84** places / note（由映射文件统计）

**英文可复述（Result）**

“I shipped an end-to-end MVP and prepared a sample dataset that includes 1,137 places, 603 posts, and 4,729 place-to-post mappings, which supports a full demo flow from query to map visualization.”

### 4.2 你需要补充/实测的 1–2 个指标（面试强信号）

这些指标 repo 里没有直接产出，但你可以用 10–20 分钟跑一次 demo 测出来：

- End-to-end latency（一次查询到地图渲染完成，P50/P95）
- Failure rate（LLM parse fail 的比例；或 fallback 次数）

**风险等级**：Medium（如果完全没有“体验/性能信号”，面试官会追问）

---

## 4.5) “失败 → 修复”小故事（至少 1 条，直接可讲）

> 目标：给面试官一个“真实遇到问题 → 你如何修复”的工程成熟度信号。

### Failure Story 1：LLM 返回不是纯 JSON → 解析失败 → 加强解析与兜底

- **Failure（发生了什么）**：LLM 的回复可能夹杂解释文本/格式不稳定，直接 `json.loads()` 会失败，导致下游流程中断或返回空结果。
- **Fix（怎么修）**：从回复里用正则提取 JSON 子串，再严格解析；解析失败返回安全默认值（空列表/默认分数），避免整个请求崩掉。
- **Evidence**：`backend/fastApiProject/app/external/DeepSeek.py`（正则提取 `[...]` / `{...}` + try/except fallback）。
- **30 秒可复述（英文）**  
  “Early on, the LLM sometimes returned extra text instead of clean JSON, which broke parsing and caused downstream failures. I fixed it by extracting the JSON payload with regex, validating it strictly, and adding safe fallbacks so the pipeline stays stable even when the LLM output isn’t perfect.”

**风险等级**：Low（只要你不夸大成“彻底解决 hallucination”，就是高质量故事）

### Failure Story 2（可选）：前端调用后端被 CORS 拦截 → 用 Vite Proxy 解决

- **Failure**：本地开发时前端(5173)请求后端(8082)会触发浏览器 CORS 限制。
- **Fix**：开发环境下把 baseURL 改为 `/api`，并在 Vite dev server 里配置 proxy 转发并 rewrite path。
- **Evidence**：`frontend/src/services/api.ts`（dev 下返回 `/api`）；`frontend/vite.config.ts`（`server.proxy['/api']` → `http://localhost:8082`）。
- **20 秒可复述（英文）**  
  “During local development, I hit CORS issues between the Vite dev server and the API. I fixed it by using a `/api` proxy in Vite so the browser sees same-origin requests while the dev server forwards them to the backend.”

**风险等级**：Low（很常见，但你能讲清楚原因和修复方式）

## 5) 验收项 5：Learnings and consideration in hindsight（反思）

**验收目标**：必须有 “If I did it again…” 的明确句子，而不是总结。

下面给你 3 条可直接复述的英文（都与当前 repo 现状一致）：

1) **Config / Secrets**
“If I rebuilt this, I would standardize configuration management end-to-end and enforce that all keys and environment-specific settings only live in environment variables, not in code.”

2) **Scalability / Cost**
“I would add caching and rate limiting around external API calls, and move expensive steps into async jobs so the UI stays responsive under load.”

3) **Quality**
“For routing quality, I would introduce a lightweight optimization step like 2-opt and add an evaluation harness to compare route quality and retrieval relevance across queries.”

**Evidence anchors（用于“我为什么这么说”）**

- Greedy routing placeholder: `backend/fastApiProject/app/core/RoutePlanner.py`
- External API heavy modules: `backend/fastApiProject/app/external/GoogleMap.py`, `backend/fastApiProject/app/external/DeepSeek.py`
- Env example provided: `backend/fastApiProject/.env.example`

**风险等级**：Low（只要你能讲“为什么”，这一项会加分）

---

## 6) Discussion-based “打断包”（高频追问与短答案）

你可以把这些当成“预制回答”，每题 15–25 秒。

1) **Was this a solo or team project?**  
“It was a [solo/team] project. I owned [architecture/backend/frontend/data pipeline], and collaborated on [X] if applicable.”

2) **Why Elasticsearch instead of only using Google Places search?**  
“Google Places gives raw place details, but Elasticsearch lets me index enriched content, support Chinese tokenization, and do geo-distance retrieval with my own ranking logic.”

3) **Why combine ES with FAISS?**  
“ES is great for geo + keyword retrieval. FAISS gives fast semantic similarity for personalization by embeddings, so the system can support both precision retrieval and preference-based recommendations.”

4) **How did you handle LLM hallucinations or malformed outputs?**  
“I don’t assume LLM output is reliable. I parse and validate JSON strictly and use fallbacks, so the rest of the pipeline remains stable.”

5) **Hardest trade-off you made?**  
“For routing, I chose a greedy approach for fast response instead of an optimal solver, because I wanted a smooth interactive experience for the MVP.”

6) **What failed initially?**  
“Early on, malformed LLM responses caused downstream failures. I fixed it with stricter parsing, fallbacks, and a more defensive pipeline.”

7) **How do you control cost/latency of external APIs?**  
“I sample route points by distance and cap the retrieval size per point; next I would add caching and async jobs to further reduce repeated calls.”

8) **How would you scale this to production?**  
“Separate online serving from offline indexing, add caching, async queues, observability, and define SLIs/SLOs for latency and failure rate.”

9) **How do you test this?**  
“For production readiness, I’d add contract tests for API responses and deterministic unit tests for route planner and retrieval logic; external API calls should be mocked.”

10) **What would you do differently?**  
“Standardize config/secrets, add caching + async, and add evaluation to quantify routing/retrieval quality.”

---

## 7) 你现在最少要补齐的 4 个“强信号”（给你一个终版 checklist）

- [ ] 用一句话明确 role + ownership（并准备 solo/team 标准回答）
- [ ] 至少 2 个 trade-off（质量 vs 延迟 / 成本 vs 体验 / 最优 vs MVP）
- [ ] 至少 1–2 个量化信号（哪怕是一次 demo 的 latency 近似值）
- [ ] 至少 1 个“失败→修复”的小故事（LLM parse / 重复召回 / CORS proxy 都可）
