# 🚀 校园AI学习助手 - 阿里云Serverless部署教程

本教程详细介绍如何将校园AI学习助手部署到阿里云函数计算（FC），获得可公开访问的链接。

---

## 📋 目录

1. [方案概述](#方案概述)
2. [本地测试](#本地测试)
3. [阿里云部署](#阿里云部署)
4. [前端部署](#前端部署)
5. [验证访问](#验证访问)
6. [常见问题](#常见问题)

---

## 一、方案概述

### 部署架构

```
用户浏览器
    ↓ HTTPS
┌─────────────────┐
│  阿里云API网关   │  ← 公开访问入口
└────────┬────────┘
         ↓
┌─────────────────┐
│  函数计算 FC     │  ← 后端Python服务
│  (Serverless)   │
└────────┬────────┘
         ↓
┌─────────────────┐
│  智谱GLM-4 API   │  ← AI能力
└─────────────────┘
```

### 费用说明

| 服务 | 免费额度 | 说明 |
|------|----------|------|
| 函数计算 FC | 100万次调用/月 | 按调用计费 |
| API网关 | 100万次调用/月 | 免费套餐 |
| 对象存储 OSS | 5GB存储 | 免费额度 |

**总计：完全免费！**

---

## 二、本地测试

### Step 1: 安装Python依赖

```bash
# 进入项目目录
cd c:/Users/Administrator/CodeBuddy/20260419133224

# 安装依赖
pip install -r requirements.txt
```

### Step 2: 配置API密钥

**获取智谱AI密钥：**

1. 访问 https://open.bigmodel.cn
2. 注册/登录账号
3. 进入「API Keys」页面
4. 创建新密钥，复制保存

**设置环境变量：**

```bash
# Windows PowerShell
$env:ZHIPU_API_KEY = "your_api_key_here"

# 或创建 .env 文件
echo ZHIPU_API_KEY=your_api_key_here > .env
```

### Step 3: 启动本地服务

```bash
# 启动后端
python app.py

# 服务地址：http://localhost:8000
```

### Step 4: 测试前端

**方式A：直接打开**

```bash
# 双击打开 index.html 文件
```

**方式B：启动静态服务器**

```bash
# Python 3
python -m http.server 8080

# 访问 http://localhost:8080
```

---

## 三、阿里云部署

### 3.1 注册阿里云账号

```
1. 访问 https://www.aliyun.com
2. 点击「免费注册」
3. 完成实名认证（必需）
4. 绑定支付宝/银行卡
```

### 3.2 开通函数计算服务

```
1. 登录阿里云控制台
2. 搜索「函数计算 FC」
3. 点击「开通服务」
4. 选择「按量付费」或「免费套餐」
5. 确认开通
```

### 3.3 安装Serverless CLI

```bash
# 安装Serverless Devs
npm install -g @serverless-devs/s

# 验证安装
s --version
```

### 3.4 配置阿里云凭证

```
1. 访问 RAM 访问控制
   https://ram.console.aliyun.com/overview

2. 创建 AccessKey
   「个人头像」→「AccessKey管理」
   「创建AccessKey」→ 保存 AK/SK

3. 配置凭证
   s config add
   # 选择 aliyun
   # 输入 AccessKey ID
   # 输入 AccessKey Secret
```

### 3.5 修改配置文件

编辑 `s.yaml`：

```yaml
vars:
  region: cn-hangzhou  # 你的区域
  serviceName: campus-ai-study

services:
  backend:
    component: fc3
    inputs:
      function:
        environmentVariables:
          ZHIPU_API_KEY: your_api_key_here  # ← 填入你的密钥
```

### 3.6 部署后端

```bash
# 进入项目目录
cd c:/Users/Administrator/CodeBuddy/20260419133224

# 部署后端服务
s backend deploy

# 等待部署完成（约1-3分钟）
# 成功后会显示API地址
```

### 3.7 获取API地址

部署成功后，记下API地址：

```
✅ 部署成功！
📡 API地址: https://campus-ai-study.cn-hangzhou.fc.aliyuncs.com/2016-08-15/proxy/campus-ai-study/study-assistant-api/
```

---

## 四、前端部署

### 方案A：阿里云OSS静态网站（推荐）

```bash
# 1. 创建OSS Bucket
# 控制台 → 对象存储OSS → 创建Bucket
# Bucket名称：campus-ai-study-frontend

# 2. 上传文件
# 直接在OSS控制台上传 index.html
# 或者使用ossutil工具

# 3. 配置静态网站
# Bucket → 基础设置 → 静态网站
# 索引文档：index.html

# 4. 获取访问地址
# Bucket → 域名管理
# 外网访问地址：https://campus-ai-study-frontend.oss-cn-hangzhou.aliyuncs.com
```

### 方案B：Vercel免费托管（更简单）

```bash
# 1. 安装Vercel CLI
npm i -g vercel

# 2. 创建 vercel.json（项目已包含）

# 3. 部署
vercel --prod

# 4. 获取公开链接
# https://your-project.vercel.app
```

### 4.1 修改前端API地址

部署前端前，需要修改 `index.html` 中的API地址：

找到（约第530行）：
```javascript
const apiBase = 'http://localhost:8000';
```

替换为你的API地址：
```javascript
// 阿里云部署
const apiBase = 'https://你的API地址';

// Vercel部署（如果后端也用Vercel）
const apiBase = 'https://your-backend.vercel.app';
```

---

## 五、验证访问

### 5.1 测试后端API

```bash
# 健康检查
curl https://你的API地址/api/health

# 预期返回
{"status": "ok", "api_provider": "zhipu", "api_configured": true}
```

### 5.2 测试前端页面

```
1. 在浏览器打开前端地址
2. 尝试上传图片或PDF
3. 点击「开始智能分析」
4. 检查是否正常返回结果
```

### 5.3 功能测试清单

```
☐ 页面正常加载
☐ 文件上传功能正常
☐ AI分析返回结果
☐ 思维导图正确显示
☐ 背诵提纲正确显示
☐ 专注计时器正常工作
☐ 数据看板正常显示
```

---

## 六、常见问题

### Q1: 部署失败，显示权限不足？

```
解决：确保RAM用户有AliyunFCFullAccess权限

1. 访问 RAM 控制台
2. 找到你的用户
3. 添加权限：AliyunFCFullAccess
```

### Q2: 函数计算调用超时？

```
解决：增加超时时间

在 s.yaml 中：
function:
  timeout: 120  # 改为120秒
```

### Q3: 内存不足？

```
解决：增加内存配置

在 s.yaml 中：
function:
  memorySize: 1024  # 改为1GB
```

### Q4: CORS跨域错误？

```
解决：检查CORS配置

确保后端设置了允许跨域：
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 或指定具体域名
    ...
)
```

### Q5: 如何绑定自定义域名？

```
1. 函数计算控制台 → 函数 → 触发器管理
2. 点击「绑定域名」
3. 添加你的域名
4. 配置DNS解析
5. 申请SSL证书（阿里云免费提供）
```

---

## 七、快速检查清单

```
部署前检查：
☐ 阿里云账号已注册并实名认证
☐ 函数计算FC已开通
☐ RAM AccessKey已创建
☐ Serverless Devs CLI已安装
☐ 智谱AI API密钥已获取
☐ 代码已推送到GitHub

部署后检查：
☐ 后端API可访问
☐ 前端页面正常加载
☐ AI分析功能正常
☐ 专注计时功能正常
☐ 数据保存正常
```

---

## 八、后续优化建议

1. **添加用户认证**
   - 使用阿里云API网关认证
   - 或集成阿里云日志服务

2. **添加数据持久化**
   - 开通RDS数据库存储专注记录
   - 使用Redis缓存热门分析结果

3. **添加监控告警**
   - 配置函数计算日志
   - 设置错误率告警

4. **性能优化**
   - 使用API网关缓存
   - 添加CDN加速

---

## 📞 获取帮助

- 阿里云文档：https://help.aliyun.com/zh/fc/
- Serverless Devs：https://www.serverless-devs.com/
- 智谱AI：https://open.bigmodel.cn/doc

---

**祝你部署成功！🎉**
