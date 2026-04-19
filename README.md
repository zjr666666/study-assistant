# 📚 校园AI学习助手

面向备考/自习大学生的AI辅助学习工具，核心功能：**AI资料智能整理** + **专注时长统计**。

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## ✨ 功能特点

### 📖 AI资料智能整理
| 功能 | 说明 |
|------|------|
| 📤 文件上传 | 支持PDF、图片（拖拽+点击） |
| 🔤 AI OCR识别 | 提取图片中的文字 |
| 🏷️ 重点提取 | 自动识别章节、关键词 |
| 📝 背诵提纲 | Markdown格式背诵材料 |
| 🧠 思维导图 | 可视化知识结构图 |

### ⏱️ 专注时长统计
| 功能 | 说明 |
|------|------|
| 计时器 | 15/25/45/60分钟可选 |
| 📊 数据看板 | 今日/本周统计 |
| 📈 趋势图表 | 柱状图展示数据 |
| 🚫 防干扰 | 切换标签页提醒 |
| 💾 本地存储 | LocalStorage持久化 |

---

## 🛠️ 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | Vue3 + Vite + Chart.js |
| 后端 | FastAPI (Python) |
| AI | 智谱GLM-4 API |
| 部署 | 阿里云函数计算FC |

---

## 🚀 快速开始

### 本地运行

```bash
# 1. 安装Python依赖
pip install -r requirements.txt

# 2. 配置API密钥
export ZHIPU_API_KEY=your_api_key

# 3. 启动后端
python app.py

# 4. 打开前端
# 双击 index.html 或
python -m http.server 8080
# 访问 http://localhost:8080
```

### 公开部署

详细教程请查看 [DEPLOY.md](./DEPLOY.md)

```
阿里云Serverless免费部署流程：
1. 注册阿里云账号 → https://www.aliyun.com
2. 开通函数计算FC
3. 安装Serverless CLI: npm i -g @serverless-devs/s
4. 配置凭证: s config add
5. 部署: s backend deploy
```

---

## 📁 项目结构

```
├── index.html              # 前端主页面（可直接打开）
├── app.py                  # FastAPI后端服务
├── requirements.txt        # Python依赖
├── s.yaml                  # 阿里云Serverless配置
├── vercel.json             # Vercel配置（备选部署）
├── backend/
│   ├── index.py            # 阿里云FC入口
│   └── requirements.txt    # 后端依赖
├── DEPLOY.md               # 部署教程
├── SPEC.md                 # 产品规范
├── REPLIT_DEPLOY.md        # Replit部署指南
└── README.md               # 项目说明
```

---

## 🔑 API申请

### 智谱AI（推荐）

1. 访问 https://open.bigmodel.cn
2. 注册并登录
3. 创建API Key
4. 免费额度：100万Tokens/月

### 环境变量配置

```bash
# Linux/Mac
export ZHIPU_API_KEY=your_api_key

# Windows PowerShell
$env:ZHIPU_API_KEY=your_api_key
```

---

## 🎨 界面预览

```
┌─────────────────────────────────────────────────┐
│  📚 校园AI学习助手                               │
│  ─────────────────────────────────────────────  │
│  [📖 AI资料整理]  [⏱️ 专注计时]                  │
│                                                 │
│  ┌─────────────────────────────────────────┐   │
│  │     📤 拖拽文件到此处，或点击选择文件     │   │
│  │         支持 PDF、图片（PNG/JPG）       │   │
│  └─────────────────────────────────────────┘   │
│                                                 │
│  [🚀 开始智能分析]                               │
│                                                 │
│  📝 提取的文本                                  │
│  ┌─────────────────────────────────────────┐   │
│  │  这是从文档中提取的文本内容...          │   │
│  └─────────────────────────────────────────┘   │
│                                                 │
│  🔑 重点关键词                                  │
│  [人工智能] [机器学习] [深度学习] [神经网络]     │
│                                                 │
└─────────────────────────────────────────────────┘
```

---

## ⚙️ 功能配置

### 修改API地址

编辑 `index.html`，找到（约第530行）：

```javascript
const apiBase = 'http://localhost:8000';
```

替换为你的API地址：

```javascript
const apiBase = 'https://your-api.aliyuncs.com';
```

### 启用真实AI功能

1. 获取智谱AI API Key
2. 设置环境变量 `ZHIPU_API_KEY`
3. 重启后端服务

---

## 📝 开发指南

### API接口

| 端点 | 方法 | 说明 |
|------|------|------|
| `/` | GET | 健康检查 |
| `/api/health` | GET | API状态 |
| `/api/analyze` | POST | AI内容分析 |
| `/api/focus/save` | POST | 保存专注记录 |
| `/api/focus/stats` | GET | 获取统计数据 |

### 测试API

```bash
# 健康检查
curl http://localhost:8000/api/health

# AI分析
curl -X POST http://localhost:8000/api/analyze \
  -F "file=@test.pdf"

# 保存专注记录
curl -X POST http://localhost:8000/api/focus/save \
  -H "Content-Type: application/json" \
  -d '{"duration": 25, "date": "2026-04-19"}'
```

---

## 🔧 常见问题

**Q: 提示"API未配置"？**
> 请设置 `ZHIPU_API_KEY` 环境变量

**Q: 文件上传失败？**
> 检查文件大小是否超过10MB，或文件格式是否支持

**Q: 部署后无法访问？**
> 检查CORS配置，确保允许跨域访问

---

## 📄 许可证

MIT License

---

## 🙏 致谢

- [Vue.js](https://vuejs.org/) - 前端框架
- [FastAPI](https://fastapi.tiangolo.com/) - 后端框架
- [智谱AI](https://open.bigmodel.cn/) - 大语言模型
- [阿里云](https://www.aliyun.com/) - 云计算服务
