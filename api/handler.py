"""
Vercel部署的API入口
使用Flask兼容FastAPI风格
"""

from flask import Flask, request, jsonify, send_file
import os
import json
import base64
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# 创建Flask应用
app = Flask(__name__)

# 智谱AI配置
ZHIPU_API_KEY = os.environ.get("ZHIPU_API_KEY", "")
ZHIPU_API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

# 专注记录存储
focus_records = []


@app.route("/")
def root():
    return jsonify({
        "name": "校园AI学习助手 API",
        "version": "1.0.0",
        "status": "running"
    })


@app.route("/api/health")
def health_check():
    return jsonify({
        "status": "ok",
        "api_provider": "zhipu",
        "api_configured": bool(ZHIPU_API_KEY)
    })


@app.route("/api/analyze", methods=["POST"])
def analyze_content():
    """AI内容分析接口"""
    content = ""
    
    # 支持JSON body
    if request.is_json:
        data = request.get_json()
        content = data.get("text", "")
    
    # 支持表单上传
    if request.files:
        file = request.files.get("file")
        if file:
            content = file.read().decode('utf-8', errors='ignore')
    
    # 调用AI分析
    result = call_zhipu_ai(content)
    return jsonify(result)


@app.route("/api/focus/save", methods=["POST"])
def save_focus_record():
    """保存专注记录"""
    data = request.get_json() or {}
    record = {
        "id": len(focus_records) + 1,
        "duration": data.get("duration", 0),
        "date": data.get("date", ""),
        "timestamp": data.get("timestamp", "")
    }
    focus_records.append(record)
    return jsonify({"success": True, "record": record})


@app.route("/api/focus/stats")
def get_focus_stats():
    """获取专注统计"""
    return jsonify({
        "today": {"total": 0, "count": 0},
        "week": [],
        "total": {"total": sum(r["duration"] for r in focus_records), "count": len(focus_records)}
    })


def call_zhipu_ai(content: str) -> dict:
    """调用智谱GLM-4 API"""
    if not ZHIPU_API_KEY:
        return get_mock_result(content)
    
    import requests
    
    prompt = f"""分析以下学习资料：
{content[:2000]}

请以JSON格式返回分析结果，包含：
- text: 提取文本
- keywords: 关键词列表
- summary: 摘要
- outline: 背诵提纲（Markdown格式）
- mindmap: 思维导图数据（包含root和branches字段）"""

    try:
        response = requests.post(
            ZHIPU_API_URL,
            headers={
                "Authorization": f"Bearer {ZHIPU_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "glm-4-flash",
                "messages": [{"role": "user", "content": prompt}]
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            content_text = result["choices"][0]["message"]["content"]
            try:
                return json.loads(content_text)
            except:
                return get_mock_result(content)
    except Exception as e:
        logger.error(f"API调用失败: {e}")
    
    return get_mock_result(content)


def get_mock_result(content: str) -> dict:
    """返回模拟结果"""
    return {
        "text": content[:1000] if content else "[请上传文件或输入文本]",
        "keywords": ["人工智能", "机器学习", "数据分析", "深度学习", "神经网络"],
        "summary": "资料分析完成，AI功能需要在后台配置智谱API Key后使用。",
        "outline": "# 背诵提纲\n\n## 一、核心要点\n- 要点一\n- 要点二\n\n## 二、重点内容\n- 内容一\n- 内容二",
        "mindmap": {
            "root": "学习资料",
            "branches": ["核心概念", "重点分析", "实践应用", "总结"]
        }
    }


# Vercel handler
def handler(request):
    """Vercel Serverless Function handler"""
    return app(request)
