# 校园AI学习助手 - 产品规范

## 1. 项目概述

**产品名称**：校园AI学习助手  
**产品定位**：面向备考/自习大学生的AI辅助学习工具  
**核心功能**：AI资料智能整理 + 专注时长统计看板  
**技术栈**：Vue3 + Vite（前端）、FastAPI（后端）、智谱GLM-4（AI）

---

## 2. 功能清单

### 2.1 AI资料整理模块

| 功能 | 说明 | 优先级 |
|------|------|--------|
| 文件上传 | 支持PDF、图片（拖拽+点击） | P0 |
| AI OCR识别 | 提取图片中的文字 | P0 |
| AI重点提取 | 自动识别章节、重点关键词 | P0 |
| 思维导图生成 | 可视化展示知识结构 | P1 |
| 背诵提纲生成 | Markdown格式背诵材料 | P0 |

### 2.2 专注计时模块

| 功能 | 说明 | 优先级 |
|------|------|--------|
| 专注计时器 | 15/25/45/60分钟可选 | P0 |
| 今日统计 | 显示今日专注时长、次数 | P0 |
| 本周趋势 | 柱状图展示每日数据 | P1 |
| 防干扰提醒 | 切换标签页时提醒 | P1 |

---

## 3. 技术架构

### 3.1 前端 (Vue3 + Vite)

```
frontend/
├── src/
│   ├── components/
│   │   ├── FileUploader.vue      # 文件上传组件
│   │   ├── AIManager.vue         # AI分析结果展示
│   │   ├── MindMap.vue           # 思维导图组件
│   │   ├── FocusTimer.vue        # 专注计时器
│   │   └── DataDashboard.vue     # 数据看板
│   ├── views/
│   │   ├── HomeView.vue          # 首页
│   │   ├── StudyView.vue         # 资料整理页
│   │   └── FocusView.vue         # 专注计时页
│   ├── stores/
│   │   └── study.js              # Pinia状态管理
│   ├── App.vue
│   └── main.js
├── index.html
├── vite.config.js
└── package.json
```

### 3.2 后端 (FastAPI)

```
backend/
├── main.py                # FastAPI主入口
├── routers/
│   ├── __init__.py
│   ├── ai.py              # AI接口
│   └── files.py          # 文件处理接口
├── services/
│   ├── __init__.py
│   ├── zhipu.py          # 智谱AI服务
│   └── ocr.py            # OCR服务
├── requirements.txt
└── Dockerfile
```

### 3.3 部署架构

```
用户浏览器
    ↓ HTTPS
阿里云函数计算 FC
    ↓
FastAPI 后端
    ↓
智谱GLM-4 API
```

---

## 4. API设计

### 4.1 文件上传
```
POST /api/upload
FormData: file (PDF/图片)
Response: { "file_id": "xxx", "filename": "xxx.pdf" }
```

### 4.2 AI分析
```
POST /api/analyze
Body: { "file_id": "xxx", "type": "image/pdf" }
Response: {
  "text": "提取的文本",
  "keywords": ["关键词1", "关键词2"],
  "summary": "摘要内容",
  "outline": "# 背诵提纲\n...",
  "mindmap": { "nodes": [...], "edges": [...] }
}
```

### 4.3 专注记录
```
POST /api/focus/save
Body: { "duration": 1500, "date": "2026-04-19" }

GET /api/focus/stats
Response: {
  "today": { "total": 3600, "count": 3 },
  "week": [{ "date": "04-13", "total": 1800 }, ...]
}
```

---

## 5. 阿里云Serverless配置

- **计算服务**：阿里云函数计算 FC
- **网关**：API网关
- **前端托管**：OSS静态网站托管
- **免费额度**：每月100万次调用，40万GB-秒

---

## 6. 验收标准

- [ ] 前端页面完整渲染，无报错
- [ ] 文件上传功能正常
- [ ] AI分析接口返回正确结果
- [ ] 专注计时器正常工作
- [ ] 数据看板正确显示统计数据
- [ ] 部署后可通过公网访问
