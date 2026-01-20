# Intuit SDE Intern Interview Notes — WanderWise (Detailed)

目标：10 分钟展示（Intro ~3min + Proud Project ~7min）。重点覆盖：角色、目标、问题解决、成果、反思。风格上与 Intuit 的使命/价值观对齐，回答行为题时可用 Amazon LP 作为结构（结果/冲突/印象题）。

面试官逐条验收（checklist-style）用的材料见：`intuit_proud_project_checklist.md`

---

## 0) 项目事实速览（直接可讲）

- 项目一句话：WanderWise 是 AI 驱动的旅行规划平台，用户用自然语言描述需求，系统自动生成路线与周边推荐，并在地图上可视化。
- 技术栈：
  - 前端：React + TypeScript + Google Maps
  - 后端：FastAPI + Elasticsearch + MySQL + FAISS
  - 外部服务：LLM（DeepSeek API）、Google Maps API、Wikipedia API
- 核心流程（端到端闭环）：  
  用户输入 → LLM 提取地点/关键词 → Google Maps 获取地点详情 → 路线规划 → 周边检索推荐 → 地图 UI 展示
- 数据规模（repo 内样本）：约 1,137 个地点 + 603 条帖子 + 4,729 条地点-帖子映射  
  数据文件：`backend/fastApiProject/app/data/place_es_data.json`，`backend/fastApiProject/app/data/post_es_data.json`，`backend/fastApiProject/app/data/place_post_mysql_data.json`
- 路线算法：最近邻贪心（简化 TSP），从角落点开始排序  
  实现：`backend/fastApiProject/app/core/RoutePlanner.py`
- 向量推荐：FAISS 内积检索（文本向量 + 图像向量拼接）  
  实现：`backend/fastApiProject/app/ai/clustering/Recommend.py`，`backend/fastApiProject/app/ai/vector_database.py`
- LLM 任务：地点抽取、关键词扩展、帖子评分  
  实现：`backend/fastApiProject/app/external/DeepSeek.py`
- 地图与路径：调用 Google Directions + 线路采样点  
  实现：`backend/fastApiProject/app/external/GoogleMap.py`

注意：`backend/fastApiProject/app/config.py` 包含 API Key，面试演示时不要展示真实 key（Intuit “Integrity without compromise”）。

---

## 1) 10 分钟 Slide 结构 + 讲稿（含代码指引）

建议 7 张：2 张 Intro + 5 张 Proud Project（可合并为 6 张）。

### Slide 1 — About Me（~1.5min）
- 讲法：  
  “我叫 [姓名]，目前在 [学校/专业/年级]。我喜欢把复杂信息变成可执行的产品体验，尤其对地图/旅行/内容理解感兴趣。”
- 个性化补充（请填）：  
  学业/经历亮点、一次关键转折

### Slide 2 — Beyond Resume + Why Intuit（~1.5min）
- 讲法（结合 Intuit 使命）：  
  “我做项目的核心驱动力是减少用户决策成本，这与 Intuit ‘Power Prosperity’ 的使命很契合。我喜欢做能直接帮助普通人的产品。”
- 非简历亮点（填 1-2 个）：旅行、地图、摄影、内容创作、开源、社团
- 与 Intuit 价值观对齐关键词：Customer Obsession、Courage to be Bold、Integrity

### Slide 3 — Problem & Vision（~1min）
- 痛点：旅行规划信息分散，路线规划耗时，个性化不足
- 目标：用“一句话输入”把搜索 → 推荐 → 路线 → 展示打通
- Intuit 价值观：Customer Obsession（以用户的真实痛点出发）
- 代码证据：`frontend/src/components/SearchPage.tsx`

### Slide 4 — Architecture & End-to-End Flow（~1.5min）
- 流程：  
  1) LLM 提取地点/关键词  
  2) Google Maps 获取地点详情  
  3) 路线规划 + 采样点  
  4) ES 地理检索 + 相关笔记  
  5) 前端地图可视化  
- 代码证据：  
  `backend/fastApiProject/app/routers/router.py`  
  `backend/fastApiProject/app/external/DeepSeek.py`  
  `backend/fastApiProject/app/external/GoogleMap.py`  
  `backend/fastApiProject/app/core/RoutePlanner.py`  
  `frontend/src/hooks/useLocations.ts`  
  `frontend/src/components/map/MapContainer.tsx`

### Slide 5 — AI/搜索/推荐细节（~1.5min）
- LLM：抽取地点 + 评分 + 关键词扩展  
  `backend/fastApiProject/app/external/DeepSeek.py`
- 数据清洗 & 知识增强：  
  `backend/fastApiProject/app/core/process_data.py`  
  `backend/fastApiProject/app/external/WikipediaFinder.py`
- 搜索与索引：  
  `backend/fastApiProject/app/services/PlaceService.py`  
  `backend/fastApiProject/app/services/PostService.py`  
  `backend/fastApiProject/app/core/ElasticsearchCore.py`
- 向量推荐：  
  `backend/fastApiProject/app/ai/clustering/Recommend.py`  
  `backend/fastApiProject/app/ai/vector_database.py`  
  `backend/fastApiProject/app/models/text_2_vec.py`  
  `backend/fastApiProject/app/models/clip_image_encoder.py`

### Slide 6 — 路线规划 & 地图体验（~1min）
- 路线：最近邻贪心快速给出可执行路径  
  `backend/fastApiProject/app/core/RoutePlanner.py`
- UI 体验：  
  - 线路折线与地图标记  
  - 地点卡片 + 相关笔记  
  - 交互优化（debounce）
- 代码证据：  
  `frontend/src/components/map/PathDisplay.tsx`  
  `frontend/src/components/map/LocationMarker.tsx`  
  `frontend/src/components/map/LocationCard.tsx`  
  `frontend/src/components/map/NoteCard.tsx`  
  `frontend/src/components/map/MapContainer.tsx`

### Slide 7 — Results & Learnings（~1min）
- 成果（可量化）：  
  - 数据规模：1,137 地点 / 603 笔记 / 4,729 映射  
  - MVP 流程完整，支持自然语言查询到路线展示  
  - 你自己的指标（请补充：响应时间、体验反馈、可用性）
- 反思：  
  - LLM 输出不稳定 → JSON 校验 + fallback  
  - 路线规划精度 vs 速度的权衡  
  - API 成本与延迟 → 缓存/异步任务  
- Intuit 价值观：Go the extra mile（把端到端闭环跑通）

---

## 2) Proud Project STAR 讲稿（更细）

### S — Situation
- 旅行规划常见问题：信息分散、路线难、搜索与地图脱节  
- 我想让用户“一句话就能拿到可执行行程”

### T — Task
- 目标：搭建从查询 → 推荐 → 路线 → UI 展示的 MVP  
- 同时解决：内容解析、检索召回、路线生成、可视化交互

### A — Action（分 4 块）
1) LLM 与数据处理  
   - 抽取地点 + 关键词  
   - 评分过滤低质量内容  
   - 引入 Wikipedia 增强描述  
   代码：`backend/fastApiProject/app/external/DeepSeek.py`，`backend/fastApiProject/app/core/process_data.py`，`backend/fastApiProject/app/external/WikipediaFinder.py`
2) 搜索与索引  
   - ES 建立 places/posts 索引，支持地理检索与中文分词  
   代码：`backend/fastApiProject/app/services/PlaceService.py`，`backend/fastApiProject/app/services/PostService.py`
3) 推荐与个性化  
   - FAISS 向量检索，融合文本+图片特征  
   代码：`backend/fastApiProject/app/ai/clustering/Recommend.py`，`backend/fastApiProject/app/ai/vector_database.py`
4) 路线与前端体验  
   - 贪心路线 + 路径点绘制  
   - 地图标记 + 地点卡片  
   代码：`backend/fastApiProject/app/core/RoutePlanner.py`，`frontend/src/components/map/MapContainer.tsx`

### R — Result
- 端到端闭环已跑通，可 demo：输入需求 → 输出路线 + 推荐地点  
- 数据规模：1,137 地点 + 603 笔记 + 4,729 映射  
- 你自己的量化结果（请补充）：请求耗时、路线长度、用户反馈

### Learnings / Hindsight
- LLM 输出结构不稳定 → JSON 解析 + fallback  
  代码：`backend/fastApiProject/app/external/DeepSeek.py`
- 路线优化尚未使用 2-opt / OR-Tools  
  代码：`backend/fastApiProject/app/core/RoutePlanner.py`
- 推荐还可加入关键词或用户画像特征（目前只使用向量）  
  代码：`backend/fastApiProject/app/ai/clustering/Recommend.py`

---

## 3) Intuit 价值观对齐（精修版）

Customer Obsession  
- 用自然语言输入降低门槛，聚焦“用户一句话就能得到可执行路线”  
- 证据：`frontend/src/components/SearchPage.tsx`，`backend/fastApiProject/app/external/DeepSeek.py`

Courage to be Bold  
- 使用 LLM + 向量推荐融合，探索传统搜索之外的智能推荐  
- 证据：`backend/fastApiProject/app/ai/clustering/Recommend.py`

Integrity without Compromise  
- 不展示真实 API Key，演示使用脱敏或占位符  
- 风险点：`backend/fastApiProject/app/config.py`

Stronger Together (D&I)  
- 如果是团队项目：强调分工协作/ code review / 接口约定  
- 如果是个人项目：强调复用开源与外部 API，主动吸收社区最佳实践

Care and Give Back  
- 旅行规划降低信息不对称，让更多普通用户更轻松规划旅行  
- 可在 Q&A 中提“想做成公开 demo / 开源组件”

Go the Extra Mile  
- 从数据清洗 → LLM → 检索 → 路线 → UI 全流程打通  
- 证据：`backend/fastApiProject/app/core/process_data.py`，`frontend/src/hooks/useLocations.ts`

Design for Delight (D4D)  
- Deep customer empathy：从“旅行规划太耗时”出发  
- Go broad to narrow：LLM 产生候选 → ES/FAISS 精选  
- Rapid experiments：先完成 MVP，再做算法优化  

---

## 4) 行为题素材（Amazon LP 视角，结合真实经历补充）

Deliver Results  
- 端到端闭环完成（MVP），强调结果与可 demo

Ownership  
- 独立搭建从数据处理 → 推荐 → 前端地图展示

Dive Deep  
- 研究 ES 分词与排序，提升中文检索效果  
  证据：`backend/fastApiProject/app/services/PostService.py`

Invent and Simplify  
- 用贪心路线算法快速交付，再计划后续优化  
  证据：`backend/fastApiProject/app/core/RoutePlanner.py`

Have Backbone / Disagree & Commit（冲突题模板，需你补充真实情景）
- 背景：同伴希望只做“固定路线模板”，而我坚持先做 LLM 解析  
- 行动：解释用户价值与可扩展性，争取到 MVP 路线  
- 结果：先实现 LLM 版本，后续再做模板兜底

---

## 5) 常见追问 + 作答要点（含代码指引）

Q: 你在项目中具体做了什么？  
A: 讲 2-3 个具体模块 + 结果  
- LLM 抽取与评分：`backend/fastApiProject/app/external/DeepSeek.py`  
- 推荐检索：`backend/fastApiProject/app/ai/clustering/Recommend.py`  
- 地图 UI：`frontend/src/components/map/MapContainer.tsx`

Q: 为什么选 ES + FAISS？  
A: ES 适合文本与地理检索，FAISS 适合向量相似度；职责分明，性能好  
- 证据：`backend/fastApiProject/app/services/PlaceService.py`，`backend/fastApiProject/app/ai/vector_database.py`

Q: LLM 不稳定如何保证可靠性？  
A: JSON 解析 + fallback + 可加重试与缓存  
- 证据：`backend/fastApiProject/app/external/DeepSeek.py`

Q: 如果继续做，怎么改进？  
A: 路线优化、缓存、异步、指标评估（NDCG/点击率）  
- 证据：`backend/fastApiProject/app/core/RoutePlanner.py`

---

## 6) 代码地图（快速熟悉仓库）

入口与 API  
- `backend/fastApiProject/app/main.py`  
- `backend/fastApiProject/app/routers/router.py`

LLM / NLP  
- `backend/fastApiProject/app/external/DeepSeek.py`

地理与路线  
- `backend/fastApiProject/app/external/GoogleMap.py`  
- `backend/fastApiProject/app/core/RoutePlanner.py`

搜索与数据层  
- `backend/fastApiProject/app/services/PlaceService.py`  
- `backend/fastApiProject/app/services/PostService.py`  
- `backend/fastApiProject/app/core/ElasticsearchCore.py`

推荐与向量  
- `backend/fastApiProject/app/ai/clustering/Recommend.py`  
- `backend/fastApiProject/app/ai/vector_database.py`  
- `backend/fastApiProject/app/models/text_2_vec.py`  
- `backend/fastApiProject/app/models/clip_image_encoder.py`

数据处理  
- `backend/fastApiProject/app/core/process_data.py`

前端交互  
- `frontend/src/components/SearchPage.tsx`  
- `frontend/src/hooks/useLocations.ts`  
- `frontend/src/components/map/MapContainer.tsx`  
- `frontend/src/components/map/PathDisplay.tsx`  
- `frontend/src/components/map/LocationMarker.tsx`  
- `frontend/src/components/map/LocationCard.tsx`  
- `frontend/src/components/map/NoteCard.tsx`

---

## 7) 展示前准备 Checklist（更细）

- 不展示任何真实 API key（`backend/fastApiProject/app/config.py`）  
- 预先准备 1 个 demo 输入，如 “Seattle food + skyline + 2 days”  
- STAR 讲述控制在 7 分钟以内  
- 准备 1-2 张架构图或流程图  

---

## 8) 需要你补充的个性化信息

- 个人背景：学校/专业/年级/方向  
- 你最想强调的兴趣或经历  
- 你在项目中的真实角色与贡献  
- 量化结果（速度/准确率/体验）  
- 一次真实的冲突或分歧（用于行为题）
