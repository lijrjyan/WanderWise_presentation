# WanderWise — Intuit SDE Intern Interview Slides (Detailed Script)

说明：此文档为 10 分钟讲稿与每页内容。建议 7 页（2 页 Intro + 5 页 Proud Project）。每页包含：
1) Slide 上展示的要点
2) 讲稿（Speaker notes）
3) 代码指引（方便你展示/熟悉实现）
4) 对齐 Intuit 价值观的点

如果你要按 Intuit 官方 bullet points 逐条验收（role / trade-offs / outcomes / hindsight），请配合 `intuit_proud_project_checklist.md` 使用。

---

## Slide 1 — Title & Agenda (0:30)

**On-slide 内容**
- WanderWise: AI-Powered Travel Planning
- [你的姓名] | [学校/专业] | SDE Intern Candidate
- Agenda: About Me (3m) + Proud Project (7m)

**讲稿**
“大家好，我是【姓名】。今天会用 10 分钟介绍我自己，然后分享我最自豪的项目 WanderWise。它是一个 AI 驱动的旅行规划平台，目标是把用户一句话的需求变成可执行路线和推荐。”

**代码指引**
- 无需代码

**Intuit 对齐**
- Mission: Power prosperity — 让用户更轻松做旅行决策

---

## Slide 2 — About Me + Beyond Resume (2:30)

**On-slide 内容**
- 学校/专业/年级/方向（【待补充】）
- 不在简历里的亮点：兴趣/跨学科/转折（【待补充】）
- 为什么喜欢做产品型工程：降低用户决策成本

**讲稿**
“我目前在【学校/专业/年级】，关注【方向，如：全栈/推荐/AI/系统】。  
除了课程，我还【兴趣/经历：旅行、地图、摄影、内容创作、开源等】。  
这些兴趣让我意识到：如果用软件把复杂的信息整理成可执行的步骤，用户体验会被明显提升，这也是我选择做 WanderWise 的原因。”

**代码指引**
- 无需代码

**Intuit 对齐**
- Customer Obsession: 从真实用户痛点出发  
- Learn & Grow: 跨领域兴趣推动工程实践

---

## Slide 3 — Problem & Goal (1:00)

**On-slide 内容**
- 痛点：旅行信息分散、路线难规划、个性化不足
- 目标：一句话输入 → 可执行路线 + 周边推荐
- MVP 结果：端到端流程打通

**讲稿**
“旅行规划信息分散在攻略、地图、笔记中，真正难的是把信息变成可执行路线。  
我的目标是让用户用一句话描述需求，系统能自动返回路线和推荐地点，同时在地图上可视化。”

**代码指引**
- 用户入口页面：`frontend/src/components/SearchPage.tsx`

**Intuit 对齐**
- Customer Obsession: 聚焦用户真实痛点  
- Design for Delight: 让“输入一句话就能得到答案”

---

## Slide 4 — Architecture & End-to-End Flow (1:30)

**On-slide 内容**
- 前端：React + Google Maps
- 后端：FastAPI + ES + MySQL + FAISS
- 外部：LLM + Google Maps + Wikipedia
- 数据流：Query → LLM → Places → Route → Search → UI

**讲稿**
“系统分成前端和后端两层。前端用 Google Maps 做交互地图；后端用 FastAPI 提供接口，Elasticsearch 做文本与地理检索，MySQL 存地点-笔记映射，FAISS 做向量推荐。  
核心流程是：用户输入 → LLM 提取地点/关键词 → 获取地点详情 → 规划路线 → 搜索周边 → 返回 UI 展示。”

**代码指引**
- 接口入口：`backend/fastApiProject/app/routers/router.py`  
- 前端拉取：`frontend/src/hooks/useLocations.ts`  
- 地图容器：`frontend/src/components/map/MapContainer.tsx`

**Intuit 对齐**
- Go the Extra Mile: 打通端到端流程  
- Invent and Simplify: 用清晰的模块拆分降低复杂度

---

## Slide 5 — AI & Retrieval (1:30)

**On-slide 内容**
- LLM：抽取地点/关键词 + 打分  
- ES：中文分词 + 地理检索  
- FAISS：文本+图片向量融合推荐

**讲稿**
“在 AI 层，我用 LLM 抽取地点和关键词，并对内容打分过滤噪声。  
检索层用 ES 做中文分词和地理检索，保证召回质量。  
推荐层用 FAISS，把文本向量和图片向量拼接后做相似度检索，提供个性化推荐。”

**代码指引**
- LLM：`backend/fastApiProject/app/external/DeepSeek.py`  
- 数据处理：`backend/fastApiProject/app/core/process_data.py`  
- ES 服务：`backend/fastApiProject/app/services/PlaceService.py`  
- 向量推荐：`backend/fastApiProject/app/ai/clustering/Recommend.py`

**Intuit 对齐**
- Courage to be Bold: 引入 LLM + 向量推荐  
- Dive Deep: 深入到检索与特征融合细节

---

## Slide 6 — Route Planning & UX (1:00)

**On-slide 内容**
- 路线算法：最近邻贪心（简化 TSP）
- 路线点：Google Directions API
- UI：路线折线 + marker + card

**讲稿**
“路线规划采用最近邻贪心，优先保证可执行与稳定输出。  
拿到路线后用 Google Directions 生成路径点，在前端画折线并展示地点详情与相关笔记卡片。  
地图中心和缩放变动用 debounce，保证交互流畅。”

**代码指引**
- 路线算法：`backend/fastApiProject/app/core/RoutePlanner.py`  
- 路线点：`backend/fastApiProject/app/external/GoogleMap.py`  
- 折线显示：`frontend/src/components/map/PathDisplay.tsx`  
- Marker/UI：`frontend/src/components/map/LocationMarker.tsx`  
- 地点卡片：`frontend/src/components/map/LocationCard.tsx`

**Intuit 对齐**
- Customer Obsession: 可视化路线提升体验  
- Invent and Simplify: 用轻量算法快速交付

---

## Slide 7 — Results & Learnings (1:00)

**On-slide 内容**
- 数据规模：1,137 地点 / 603 笔记 / 4,729 映射
- MVP 已打通（可 demo）
- Learnings：LLM 稳定性、路线优化、缓存

**讲稿**
“目前样本规模是 1,137 个地点、603 条笔记、4,729 条地点-笔记映射，端到端流程已打通，可以演示完整体验。  
反思点包括：LLM 输出不稳定，需要结构化校验；路线算法可用 2-opt 优化；外部 API 需要缓存与异步控制成本。”

**代码指引**
- 数据文件：`backend/fastApiProject/app/data/place_es_data.json`  
- LLM：`backend/fastApiProject/app/external/DeepSeek.py`  
- 路线：`backend/fastApiProject/app/core/RoutePlanner.py`

**Intuit 对齐**
- Learn & Grow: 在 AI/检索/地图之间持续学习  
- Integrity without Compromise: 演示时不暴露 API Key

---

## 可选 Slide 8 — Q&A Seed (0:30)

**On-slide 内容**
- 我们最关注的问题：用户输入一句话后，系统如何保证相关性与体验？
- 我能展开：ES 召回 + FAISS 相似度 + UI 可视化

**讲稿**
“如果你们关心检索与推荐的可靠性，我可以从 ES + FAISS 的组合策略解释；如果更关心体验，我可以展开地图交互与路线生成。”

---

## 演示注意点（放在备忘）

- 不展示 `backend/fastApiProject/app/config.py` 中真实 key  
- 准备 demo 输入：“Seattle food + skyline + 2 days”
