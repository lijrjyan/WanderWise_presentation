# WanderWise — Code Guide & System Flow (Review)

目标：帮助你快速熟悉系统流程与关键代码路径；面试时可用作技术问答支撑。

---

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
- `backend/fastApiProject/app/main.py`  
- `backend/fastApiProject/app/routers/router.py`

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

