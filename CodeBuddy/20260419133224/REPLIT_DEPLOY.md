# Replit 部署指南 - 校园AI学习助手

> 零基础也能完成的云端部署教程

---

## 一、为什么选择 Replit？

| 优点 | 说明 |
|------|------|
| 🌐 无需安装任何软件 | 浏览器里完成所有操作 |
| 📦 不用手动配置服务器 | 一键部署，自动配置环境 |
| 🔗 自带公开链接 | 部署完即可分享 |
| 💰 免费额度充足 | 足够个人项目使用 |
| 🇨🇳 国内访问友好 | 比 Vercel 更稳定 |

---

## 二、部署步骤总览

```
Step 1: 注册 Replit 账号
Step 2: 创建新 Repl
Step 3: 上传代码
Step 4: 修改配置文件
Step 5: 一键部署
Step 6: 获取公开链接
```

预计完成时间：**10分钟**

---

## 三、详细操作步骤

### Step 1: 注册 Replit 账号

**1.1 访问 Replit**

在浏览器打开：
```
https://replit.com
```

**1.2 点击注册**

```
┌─────────────────────────────────────────────┐
│                                             │
│     🟢 Welcome to Replit                    │
│                                             │
│   [Sign up with Google]  ← 推荐用这个      │
│   [Sign up with GitHub]                     │
│   [Sign up with Apple]                      │
│                                             │
└─────────────────────────────────────────────┘
```

**1.3 选择「用 Google 注册」**

- 点击 "Sign up with Google"
- 选择你的 Google 账号
- 允许授权

**1.4 设置用户名**

```
Username: study_assistant
(只能包含字母、数字、下划线)
```

---

### Step 2: 创建新 Repl

**2.1 点击「Create Repl」**

页面右上角或首页找到绿色按钮

**2.2 填写信息**

```
┌─────────────────────────────────────────────┐
│  Create a Repl                              │
├─────────────────────────────────────────────┤
│                                             │
│  Template:    [Python]  ← 选择这个          │
│                                             │
│  Title:       [校园AI学习助手]              │
│                                             │
│  Description: [校园AI学习助手MVP]           │
│                                             │
│  Visibility:  [Public ▼]  ← 选择 Public     │
│                                             │
│           [Create Repl]  ← 点击创建         │
│                                             │
└─────────────────────────────────────────────┘
```

---

### Step 3: 上传代码文件

**3.1 界面说明**

```
┌─────────────────────────────────────────────────────┐
│  📁 校园AI学习助手                      [▶ Run]    │
├───────────────┬───────────────────────────────────┤
│               │                                    │
│  📁 Files     │     main.py                       │
│  ├─ main.py   │                                    │
│  ├─ .python   │     print("Hello!")               │
│     replier   │                                    │
│               │                                    │
│  + Add file   │                                    │
│  + Add folder │                                    │
│               │                                    │
├───────────────┴───────────────────────────────────┤
│  [Console]  [Shell]  [Secrets]                    │
│  > _                                          │
└─────────────────────────────────────────────────┘
```

**3.2 删除默认文件**

- 删掉左侧的 `main.py`
- 删掉 `.pythonrepl`

**3.3 添加我们的文件**

点击 `+ Add file` 5次，创建以下文件：

1. `app.py`
2. `index.html`
3. `style.css`
4. `script.js`
5. `requirements.txt`

**3.4 复制粘贴代码**

打开你电脑上的文件，复制内容，粘贴到对应的 Replit 文件中：

| Replit 文件 | 复制自电脑 |
|------------|-----------|
| `app.py` | 你电脑上的 `app.py` |
| `index.html` | 你电脑上的 `index.html` |
| `style.css` | 你电脑上的 `style.css` |
| `script.js` | 你电脑上的 `script.js` |
| `requirements.txt` | 你电脑上的 `requirements.txt` |

**⚠️ 注意事项：**
- 粘贴后记得 Ctrl+S 保存
- 或者点击每个文件右上角的 ✏️ 编辑器会自动保存

---

### Step 4: 修改 app.py 适配 Replit

**4.1 修改端口配置**

在 Replit 中找到 `app.py`，找到文件末尾的：

```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

**替换为：**

```python
if __name__ == '__main__':
    import os
    # Replit 会设置 PORT 环境变量
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
```

**4.2 修改文件上传路径**

找到 `app.py` 中的这行：
```python
UPLOAD_FOLDER = 'uploads'
```

**替换为：**
```python
UPLOAD_FOLDER = '/tmp/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
```

---

### Step 5: 添加 HTML 入口文件

Replit 需要一个入口文件。创建 `.replit` 文件：

**点击 `+ Add file`，创建文件：**

文件名：`REPLIT_DEPLOY.md`（这个文件不用管）

然后再创建：`.replit`

**在 `.replit` 文件中写入：**

```bash
run = "python app.py"
entrypoint = "app.py"
```

---

### Step 6: 一键运行和部署

**6.1 安装依赖**

在 Console（底部终端）输入：

```bash
pip install -r requirements.txt
```

等待安装完成（看到类似 `Successfully installed...`）

**6.2 试运行**

点击右上角的绿色 **▶ Run** 按钮

如果看到类似输出：
```
* Running on http://0.0.0.0:5000
* Running on http://localhost:5000
```

说明运行成功！

**6.3 部署到云端**

在左侧边栏找到 **Deployments** 按钮（或者在顶部菜单找）

```
┌─────────────────────────────────────────────┐
│  ▶ Run        [Deployments ▼]    [Share]   │
└─────────────────────────────────────────────┘
```

点击 **Deployments**，然后点击 **Deploy**

等待部署完成（约 1-2 分钟）

---

### Step 7: 获取公开链接

**7.1 找到你的链接**

部署成功后，你会看到：

```
┌─────────────────────────────────────────────┐
│  ✓ Deployment successful!                  │
│                                             │
│  🔗 https://校园AI学习助手.yourusername.repl.co │
│                                             │
│  [Visit]  [Copy Link]                       │
└─────────────────────────────────────────────┘
```

**7.2 测试链接**

点击 **Visit** 或复制链接在浏览器打开

---

## 四、验证部署成功

### 测试 API

在浏览器打开：
```
https://你的项目名.yourusername.repl.co/
```

应该看到：
```json
{"name": "资料智能整理 API", "version": "1.0.0", ...}
```

### 测试前端页面

```
https://你的项目名.yourusername.repl.co/index.html
```

### 测试功能

1. 上传一张图片
2. 点击「开始智能分析」
3. 查看是否能正常返回结果

---

## 五、常见问题与解决

### 问题1: 点击 Run 没反应

**解决：**
1. 检查 Console 有没有报错
2. 确认 `app.py` 没有语法错误
3. 重新点击 Run 按钮

---

### 问题2: 部署按钮是灰色的

**解决：**
1. 确保你已经安装完依赖（pip install）
2. 确保程序能成功运行（Run 按钮可用）
3. Replit 免费版需要验证邮箱

---

### 问题3: 公开链接打不开

**解决：**
1. 确认部署状态是 "Running"
2. 等待 1-2 分钟再试
3. 检查程序是否在 Console 有报错

---

### 问题4: 页面显示 404

**原因：** 直接访问域名会显示 Flask 默认页面

**解决：** 访问 `/index.html` 路径

---

## 六、后续维护

### 更新代码

1. 修改 Replit 中的文件
2. 重新点击 **Run**
3. 重新 **Deploy**

### 查看日志

在 Deployments 页面点击你的部署，可以查看：
- 运行日志
- 错误信息
- 访问统计

---

## 七、完整操作流程图

```
注册 Replit → 创建 Repl → 上传代码 → 修改配置
      ↓
   安装依赖 → 点击 Run → 验证运行 → Deploy
      ↓
   等待部署 → 获取链接 → 测试验证 → 完成！
```

---

## 八、你的下一步

**请按顺序完成：**

```
[ ] 1. 打开 https://replit.com
[ ] 2. 用 Google 账号注册/登录
[ ] 3. 创建新的 Python Repl
[ ] 4. 上传 5 个文件
[ ] 5. 修改 app.py 配置
[ ] 6. 安装依赖并运行
[ ] 7. 点击 Deploy
[ ] 8. 复制公开链接
```

---

**遇到问题随时告诉我！**

