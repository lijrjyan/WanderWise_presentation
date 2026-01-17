# WanderWise — 项目总览 & 代码 Review 指南

目标：用一份文档把项目「是什么 / 怎么跑 / 从哪读起 / 每个文件做什么」说清楚，方便你快速 review 代码与定位入口。

---

## 0) TL;DR（先看这里）

- 项目形态：前端 `React + TS + Vite + Google Maps` + 后端 `FastAPI + Elasticsearch + MySQL + FAISS`。
- 你从哪读起：
  1) 前端入口：`frontend/src/App.tsx`、`frontend/src/components/SearchPage.tsx`、`frontend/src/hooks/useLocations.ts`
  2) 后端入口：`backend/fastApiProject/app/main.py`、`backend/fastApiProject/app/routers/router.py`
  3) 外部依赖：`backend/fastApiProject/app/external/DeepSeek.py`（LLM）、`backend/fastApiProject/app/external/GoogleMap.py`（Google Maps）
- 一句话流程：用户输入 → 后端 LLM 生成候选地点 → Google Places 拉详情 → 路线规划 → 线路采样点附近 ES 检索 → 返回 places + notes + path points → 前端画点/画线/展示卡片。

> 注意：本 repo 目前存在「端口/路径硬编码、部分模块缺失」等问题（见本文末尾“已知问题/技术债”），但不影响你按核心链路 review。

## 1) 系统流程（用户输入 → 结果展示）

主路径（前端搜索 → 后端推荐 → 前端展示）：
1) 用户输入  
   - `frontend/src/components/SearchPage.tsx`
2) 触发搜索  
   - `frontend/src/hooks/useLocations.ts` → `locationService.searchLocations`
3) 后端接口  
   - `backend/fastApiProject/app/routers/router.py`  
   - 使用接口：`/search/ai-recommend`
4) LLM 解析用户需求  
   - `backend/fastApiProject/app/external/DeepSeek.py` → `process_user_query`
5) Google Maps 获取地点详情  
   - `backend/fastApiProject/app/external/GoogleMap.py` → `get_place_detail`
6) 路线规划  
   - `backend/fastApiProject/app/core/RoutePlanner.py` → `plan_route`
7) 路径点与路线详情  
   - `backend/fastApiProject/app/external/GoogleMap.py` → `get_route_details`
8) ES 地理检索 + MySQL 映射  
   - `backend/fastApiProject/app/services/PlaceService.py` → `search_places_mixed`  
   - `backend/fastApiProject/app/services/PlacePostService.py` → `get_notes_by_place_id`  
   - `backend/fastApiProject/app/services/PostService.py` → `get_post_by_id`
9) 前端解析结果并展示  
   - `frontend/src/hooks/useLocations.ts`  
   - `frontend/src/components/map/MapContainer.tsx`  
   - `frontend/src/components/map/PathDisplay.tsx`  
   - `frontend/src/components/map/LocationMarker.tsx`  
   - `frontend/src/components/map/LocationCard.tsx`

---

## 2) 核心模块速览

API 入口与路由  
- `backend/fastApiProject/app/main.py`：FastAPI app + router 挂载（另有一个备用入口 `backend/fastApiProject/main.py`，见文件地图）  
- `backend/fastApiProject/app/routers/router.py`：主要 API 路由与编排（search / data init / export 等）

LLM 与内容理解  
- `backend/fastApiProject/app/external/DeepSeek.py`

路线规划  
- `backend/fastApiProject/app/core/RoutePlanner.py`

地理服务（Google Maps）  
- `backend/fastApiProject/app/external/GoogleMap.py`

检索与索引（ES）  
- `backend/fastApiProject/app/services/PlaceService.py`  
- `backend/fastApiProject/app/services/PostService.py`  
- `backend/fastApiProject/app/core/ElasticsearchCore.py`

向量推荐（FAISS）  
- `backend/fastApiProject/app/ai/clustering/Recommend.py`  
- `backend/fastApiProject/app/ai/vector_database.py`

数据清洗与增强  
- `backend/fastApiProject/app/core/process_data.py`  
- `backend/fastApiProject/app/external/WikipediaFinder.py`

前端可视化  
- `frontend/src/components/map/MapContainer.tsx`  
- `frontend/src/components/map/PathDisplay.tsx`  
- `frontend/src/components/map/LocationMarker.tsx`  
- `frontend/src/components/map/LocationCard.tsx`  
- `frontend/src/components/map/NoteCard.tsx`

---

## 3) 两条后端推荐路径（面试可提）

Path A: LLM 驱动推荐（前端默认调用）  
- `GET /search/ai-recommend`  
- 文件：`backend/fastApiProject/app/routers/router.py`
- 逻辑：  
  LLM 提取地点 → Google Places → 路线 → 周边检索 → 返回 places + route + points

Path B: 用户画像 + 向量推荐（更偏个性化）  
- `GET /search/recommend`  
- 文件：`backend/fastApiProject/app/routers/router.py`
- 逻辑：  
  关键词扩展 → ES 搜索 → place/post 向量检索（FAISS） → 路线 → 周边检索

---

## 4) 数据与存储

Elasticsearch  
- 索引创建：`PlaceService` / `PostService`  
- 中文分词：IK Analyzer  
- 数据样本：`backend/fastApiProject/app/data/place_es_data.json`  

MySQL  
- 关联表：地点-笔记映射  
- 服务：`backend/fastApiProject/app/services/PlacePostService.py`  
- 数据样本：`backend/fastApiProject/app/data/place_post_mysql_data.json`

FAISS（向量检索）  
- `backend/fastApiProject/app/ai/vector_database.py`  
- 注意：`Recommend.py` 中数据库路径为绝对路径（可作为技术债说明）

---

## 5) 面试时可提的技术亮点

- LLM 抽取 + ES 检索 + FAISS 推荐的混合架构  
  兼顾语义与地理位置相关性
- 路线规划用贪心算法快速产出可执行路线  
  可扩展到 2-opt 或 OR-Tools
- 地图交互采用 debounce 降低频繁更新  
  `frontend/src/components/map/MapContainer.tsx`

---

## 6) 风险点与取舍（用于反思/追问）

- LLM 输出不稳定 → JSON 解析 + fallback  
  `backend/fastApiProject/app/external/DeepSeek.py`
- 路线算法不是最优解 → 先保证可执行性  
  `backend/fastApiProject/app/core/RoutePlanner.py`
- 向量数据库路径硬编码 → 可优化为配置化  
  `backend/fastApiProject/app/ai/clustering/Recommend.py`
- API Key 风险 → 演示时必须脱敏  
  `backend/fastApiProject/app/config.py`

---

## 7) Demo 复盘路径（如果需要现场演示）

1) 搜索输入：`frontend/src/components/SearchPage.tsx`  
2) 查询触发：`frontend/src/hooks/useLocations.ts`  
3) 后端接口：`/search/ai-recommend`  
4) 地图展示：`frontend/src/components/map/MapContainer.tsx`  
5) 路线折线：`frontend/src/components/map/PathDisplay.tsx`

---

## 8) 面试常见问题的代码证据

Q: 推荐是如何实现的？  
→ `backend/fastApiProject/app/ai/clustering/Recommend.py`

Q: 如何做文本和地理检索？  
→ `backend/fastApiProject/app/services/PlaceService.py`

Q: 路线怎么规划的？  
→ `backend/fastApiProject/app/core/RoutePlanner.py`

Q: 前端地图怎么画路径？  
→ `frontend/src/components/map/PathDisplay.tsx`

---

## 9) Repo 文件地图（按目录逐个解释）

说明：本节以“目录 → 文件 → 用途”方式列出 repo 内主要文件。`.git/` 内部文件不在 review 范围内，故不展开。

### 9.1 根目录

- `.gitignore`：全仓库忽略规则（Node 构建产物、env、日志、Python `__pycache__` 等）。
- `README.md`：项目介绍与启动说明（部分端口/细节可能与当前代码不一致，建议以本文为准）。
- `review.md`：本文件，面向 code review 的系统/文件总览。
- `note.md`：面试/演示用笔记（STAR 讲稿、价值观对齐、可讲亮点）。
- `slide.md`：演示 slide 的逐页讲稿（含每页代码指引）。
- `logo/wanderwise_1.png`：README 展示用 Logo 图片。

### 9.2 `backend/`（后端相关）

#### 9.2.1 `backend/docker-compose.yml`

- `backend/docker-compose.yml`：本地起 Elasticsearch(8.11.3) 与 MySQL(8.0) 的 compose；供 FastAPI 连接使用。

#### 9.2.2 `backend/elasticsearch-analysis-ik-8.11.3/`（第三方 IK 分词插件包）

用途：提供 `ik_smart / ik_max_word` 中文分词，用于 ES mapping（见 `PlaceService` / `PostService`）。

- `backend/elasticsearch-analysis-ik-8.11.3.zip`：IK 插件压缩包（通常用于安装到 Elasticsearch 插件目录）。
- `backend/elasticsearch-analysis-ik-8.11.3/elasticsearch-analysis-ik-8.11.3.jar`：插件主 jar。
- `backend/elasticsearch-analysis-ik-8.11.3/config/IKAnalyzer.cfg.xml`：IK 插件配置。
- `backend/elasticsearch-analysis-ik-8.11.3/config/*.dic`：词典/停用词/姓氏等配置文件（扩展词库、停用词等）。
- `backend/elasticsearch-analysis-ik-8.11.3/*.jar`：插件依赖 jar（commons-logging/httpclient 等）。
- `backend/elasticsearch-analysis-ik-8.11.3/plugin-descriptor.properties`：ES 插件描述文件。
- `backend/elasticsearch-analysis-ik-8.11.3/plugin-security.policy`：插件安全策略配置。

#### 9.2.3 `backend/fastApiProject/`（FastAPI 项目主体）

##### 入口与依赖

- `backend/fastApiProject/.env.example`：后端环境变量示例（复制为 `.env` 并填真实值；避免把 key 提交到 repo）。
- `backend/fastApiProject/requirements.txt`：Python 依赖（FastAPI/ES/MySQL/OpenAI SDK/FAISS/ONNXRuntime 等）。
- `backend/fastApiProject/main.py`：FastAPI 入口（把 `app.routers.router` 挂到根 app 上；更像“根目录启动方式”）。
- `backend/fastApiProject/app/main.py`：另一份 FastAPI 入口（从 `routers` 相对导入并打印 routes；端口默认 8082）。
- `backend/fastApiProject/app/__init__.py`：Python package 标记。
- `backend/fastApiProject/app/config.py`：后端配置（MySQL/ES/外部 API key 等；建议用 `.env` 覆盖，避免硬编码）。

##### 路由层（HTTP API）

- `backend/fastApiProject/app/routers/__init__.py`：routers 包初始化。
- `backend/fastApiProject/app/routers/router.py`：核心 API 路由与编排逻辑：
  - `/search/ai-recommend`：LLM → Google Places → 路线 → 采样点附近检索 → 返回前端数据
  - `/search/recommend`：基于关键词扩展 + 向量推荐的路线/推荐
  - `/search/keyword`：仅关键词扩展 + post 推荐
  - `/data/*`：清洗、初始化 ES、导入导出数据等工具型接口

##### service 层（业务封装）

- `backend/fastApiProject/app/services/__init__.py`：services 包初始化（当前为空）。
- `backend/fastApiProject/app/services/PlaceService.py`：Places 索引（ES）封装：建索引、导入导出、地理检索、按名称检索等。
- `backend/fastApiProject/app/services/PostService.py`：Posts 索引（ES）封装：建索引、导入导出、关键词检索、地理检索、function_score 等。
- `backend/fastApiProject/app/services/PlacePostService.py`：地点(place_id) 与笔记(note_id) 映射表（MySQL）封装。
- `backend/fastApiProject/app/services/UserFavoritesService.py`：用户收藏 post 的服务（依赖 `UserNoteService`，当前 repo 中该模块缺失，见“已知问题”）。
- `backend/fastApiProject/app/services/UserPlaceFavoritesService.py`：用户收藏 place 的服务（MySQL 表 `user_place_favorites`）。

##### core 层（基础设施/算法）

- `backend/fastApiProject/app/core/__init__.py`：core 包初始化。
- `backend/fastApiProject/app/core/ElasticsearchCore.py`：ES Client 封装：建索引、CRUD、search、import/export 等基础操作。
- `backend/fastApiProject/app/core/MySqlCore.py`：SQLAlchemy 基础 CRUD + import/export（JSON）通用封装。
- `backend/fastApiProject/app/core/RoutePlanner.py`：简单路线规划（角落点 + 最近邻贪心）。
- `backend/fastApiProject/app/core/process_data.py`：数据清洗/增强流水线：LLM 抽取地点 → Google Places 详情 →（可选）Wikipedia 描述 → 入 ES/MySQL。

##### external 层（外部 API 适配）

- `backend/fastApiProject/app/external/__init__.py`：external 包初始化。
- `backend/fastApiProject/app/external/DeepSeek.py`：LLM 适配（通过 OpenAI SDK + DeepSeek base_url 调用）：地点抽取、评分、关键词扩展、用户 query 解析。
- `backend/fastApiProject/app/external/GoogleMap.py`：Google Maps API 适配：FindPlace/Details/Directions；并做路线点采样供 ES 周边检索使用。
- `backend/fastApiProject/app/external/WikipediaFinder.py`：Wikipedia API 适配：为景点类地点补充简介文本。

##### ai 层（向量检索/特征）

- `backend/fastApiProject/app/ai/__init__.py`：ai 包初始化。
- `backend/fastApiProject/app/ai/vector_database.py`：FAISS 向量库封装（index + meta）。
- `backend/fastApiProject/app/ai/clustering/__init__.py`：clustering 子包初始化。
- `backend/fastApiProject/app/ai/clustering/Recommend.py`：向量推荐入口（拼接 place/post 文本+图片向量；当前有绝对路径硬编码）。
- `backend/fastApiProject/app/ai/clustering/post_feature_calculator.py`：从 posts/places 计算文本/图片 embedding（用 BERT/CLIP；含多进程图片加载）。
- `backend/fastApiProject/app/ai/clustering/utils.py`：clustering 工具函数（图片加载等）。
- `backend/fastApiProject/app/ai/llm/__init__.py`：llm 子包初始化。
- `backend/fastApiProject/app/ai/llm/llm.py`：另一套 LLM 客户端/实验代码（含内网 base_url/示例用 key；更偏实验脚本性质）。

##### models/schemas（MySQL ORM & Pydantic Schema）

- `backend/fastApiProject/app/models/__init__.py`：models 包初始化。
- `backend/fastApiProject/app/models/PlacePost.py`：SQLAlchemy Base/engine/session + PlacePost 映射表（place_id ↔ note_id）。
- `backend/fastApiProject/app/models/Place.py`：Place 表 ORM（places）。
- `backend/fastApiProject/app/models/Post.py`：Post 表 ORM（posts）。
- `backend/fastApiProject/app/models/User.py`：User 表 ORM（users）。
- `backend/fastApiProject/app/models/UserFavorites.py`：UserFavorites 表 ORM（user_favorites：user_id ↔ post_id）。
- `backend/fastApiProject/app/models/UserPlaceFavorites.py`：UserPlaceFavorites 表 ORM（user_place_favorites：user_id ↔ place_id）。
- `backend/fastApiProject/app/models/singleton_meta.py`：SingletonMeta（给 encoder/tokenizer 单例用）。
- `backend/fastApiProject/app/models/text_2_vec.py`：文本向量（BERT）推理封装（直接 torch 推理）。
- `backend/fastApiProject/app/models/clip_image_encoder.py`：图片向量（ONNX CLIP）推理封装（ONNXRuntime）。

- `backend/fastApiProject/app/schemas/__init__.py`：schemas 包初始化。
- `backend/fastApiProject/app/schemas/PlaceSchema.py`：Place 相关 Pydantic schema。
- `backend/fastApiProject/app/schemas/PostSchema.py`：Post 相关 Pydantic schema。
- `backend/fastApiProject/app/schemas/PlacePostSchema.py`：PlacePost 相关 schema。
- `backend/fastApiProject/app/schemas/UserSchema.py`：User 相关 schema。
- `backend/fastApiProject/app/schemas/UserFavoritesSchema.py`：UserFavorites 相关 schema。
- `backend/fastApiProject/app/schemas/UserPlaceFavoritesSchema.py`：UserPlaceFavorites 相关 schema（含 count view）。

##### 数据/资产（样本数据、向量库文件）

- `backend/fastApiProject/app/data/*.json`：样本数据与导入导出文件：
  - `place_es_data.json`：places 索引样本数据（Google Places-like 结构）
  - `post_es_data.json`：posts 索引样本数据（笔记/帖子结构）
  - `place_post_mysql_data.json`：place↔post 映射数据（MySQL 导入导出）
  - `merged_posts.json`：原始/合并后的 posts 原料数据（供 `process_data` 清洗）
  - `processed_search_contents.json`：清洗后的 posts（供搜索/索引）
  - `user000*_posts.txt` / `user000*_places.txt`：用户样本偏好/行为数据（用于向量推荐/画像实验）
- `backend/fastApiProject/app/data/*.db.index` / `*.db.meta`：FAISS index 与元数据（向量检索离线产物）。
- `backend/fastApiProject/app/images/.gitkeep`：占位文件，保证 images 目录被 git 跟踪。

##### 迁移/测试/脚本（多为开发期脚手架）

- `backend/fastApiProject/app/db_migration.py`：DB 初始化/重置/迁移脚本（当前引用了缺失的 `models.UserNote`）。
- `backend/fastApiProject/app/test_favorites.py`：收藏相关功能的手动测试脚本（依赖 services 导出，当前不完整）。
- `backend/fastApiProject/app/test_user_place_favorites.py`：UserPlaceFavoritesService 的 DB 层测试脚本。
- `backend/fastApiProject/app/test_user_place_favorites_api.py`：UserPlaceFavorites API 的 TestClient 测试脚本（依赖实际路由实现，可能需要调整）。

- `backend/fastApiProject/add_test_data.py`：向 user_notes 表灌测试数据（依赖缺失的 `UserNoteService`）。
- `backend/fastApiProject/api_test_commands.txt`：curl 测试 user_notes API 的命令集合（同样依赖缺失模块）。
- `backend/fastApiProject/simple_db_test.py`：SQLite 的独立 demo（不接入当前 MySQL/SQLAlchemy 主流程）。
- `backend/fastApiProject/test_api_endpoints.py`：requests 方式的 API 测试脚本（路径/端口需与实际一致）。
- `backend/fastApiProject/example.txt`：杂项说明/占位文本。
- `backend/fastApiProject/test model.ipynb`：实验 notebook（训练/向量等，非生产）。
- `backend/fastApiProject/test/*.py`：实验/离线脚本（向量库构建、内网 LLM 调用示例等）。
- `backend/fastApiProject/*.db.index` / `*.db.meta`：与 app/data 类似的向量库产物（历史/备用路径）。

##### 生成物（不建议参与 code review）

以下文件/目录通常是 Python 运行生成的缓存（本 repo 已提交，但建议 review 时忽略）：
- `backend/fastApiProject/**/__pycache__/*`
- `backend/fastApiProject/**/.ipynb_checkpoints/*`

### 9.3 `frontend/`（前端相关）

#### 9.3.1 构建/配置

- `frontend/package.json`：依赖与脚本（dev/build/lint/preview）。
- `frontend/vite.config.ts`：Vite 配置与 dev proxy（`/api` → 后端 base）。
- `frontend/tsconfig*.json`：TS 编译配置（app/node）。
- `frontend/eslint.config.js`：ESLint 配置。
- `frontend/index.html`：Vite 入口 HTML。
- `frontend/.env.example`：前端环境变量示例（Google Maps key、后端 base URL）。
- `frontend/public/vite.svg`、`frontend/src/assets/react.svg`：Vite/React 默认资源。
- `frontend/.gitignore`：前端子项目的忽略规则。
- `frontend/README.md`：前端说明文档（可与本文件互补）。

#### 9.3.2 `frontend/src/`（核心业务代码）

- `frontend/src/main.tsx`：React 挂载入口。
- `frontend/src/App.tsx`：全局布局（左侧导航 + SearchPage + MapContainer）与 Provider 挂载。
- `frontend/src/context/LocationContext.tsx`：全局状态（locations / selected / route / pathPoints / mapSettings / loading/error）。
- `frontend/src/hooks/useLocations.ts`：核心数据流 hook：调用后端 search、解析返回数据、落到 context。
- `frontend/src/services/api.ts`：Axios 实例 + locationService/routeService（并接 Vite proxy）。
- `frontend/src/types/index.ts`：前端 TypeScript 类型（API 返回结构、Location/Route 等）。
- `frontend/src/utils/locationUtils.ts`：排序/距离/时间估算等工具函数。
- `frontend/src/utils/imageUtils.ts`：图片相关工具函数（若使用）。
- `frontend/src/components/SearchPage.tsx`：输入查询的页面（目前用于触发 `searchLocations`）。
- `frontend/src/components/map/MapContainer.tsx`：GoogleMap 容器 + markers/polyline 渲染 + debounce 同步 map 状态。
- `frontend/src/components/map/PathDisplay.tsx`：绘制后端返回的采样路径点（Polyline）。
- `frontend/src/components/map/RouteDisplay.tsx`：展示 route（DirectionsRenderer 或简单 Polyline）。
- `frontend/src/components/map/LocationMarker.tsx`：Marker + InfoWindow；根据 zoom/category 展示不同样式/卡片。
- `frontend/src/components/map/LocationCard.tsx`：地点详情卡片（地址/评分/营业时间/电话/图片轮播/关联笔记）。
- `frontend/src/components/map/NoteCard.tsx`：笔记卡片（封面/标题/作者/收藏按钮 UI）。
- `frontend/src/components/map/NavigationPanel.tsx`：选点/排序/创建路线的侧边控制面板（部分依赖后端 `/routes`）。
- `frontend/src/components/map/SearchBar.tsx`：旧版侧边搜索栏（App 里 sidebar 当前隐藏）。
- `frontend/src/App.css`、`frontend/src/index.css`、`frontend/src/components/map/*.css`：样式文件。
- `frontend/src/vite-env.d.ts`：Vite TS 类型声明。

---

## 10) 已知问题 / 技术债（review 时建议关注）

- 端口/代理约定：前端 dev proxy 目标在 `frontend/vite.config.ts`，后端启动端口需与其一致（默认按 8082）。
- 硬编码/绝对路径：`backend/fastApiProject/app/ai/clustering/Recommend.py` 使用 `/home/gophers/...` 绝对路径加载向量库。
- 缺失模块：多处引用 `UserNoteService` / `models.UserNote`，但 repo 未包含对应实现（相关测试/脚本会失败）。
- 生成物被提交：`__pycache__`、`.ipynb_checkpoints`、`.pyc` 等不应进 git（会干扰 review）。
- Secrets 风险：配置/脚本里出现 API key/内网地址时，建议全部迁移到 `.env` 并避免提交到远端。
