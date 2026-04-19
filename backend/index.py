"""
阿里云函数计算 - Flask HTTP函数
================================
使用Flask框架，阿里云默认支持，无需额外安装
"""

from flask import Flask, request, jsonify
import os
import json
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
    """首页"""
    return jsonify({
        "name": "校园AI学习助手 API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": ["/", "/api/health", "/api/analyze", "/api/focus/save", "/api/focus/stats"]
    })


@app.route("/api/health")
def health_check():
    """健康检查"""
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
    
    # 支持文本参数
    if not content:
        content = request.args.get("text", "")
    
    # 调用AI分析
    result = call_zhipu_ai(content)
    return jsonify(result)


@app.route("/api/focus/save", methods=["POST"])
def save_focus_record():
    """保存专注记录"""
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form.to_dict()
    
    record = {
        "id": len(focus_records) + 1,
        "duration": int(data.get("duration", 0)),
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
        "total": {
            "total": sum(r["duration"] for r in focus_records),
            "count": len(focus_records)
        }
    })


def call_zhipu_ai(content: str) -> dict:
    """调用智谱GLM-4 API"""
    if not ZHIPU_API_KEY:
        return get_mock_result(content)
    
    import requests
    
    prompt = f"""分析以下学习资料：
{content[:2000] if content else '[无内容]'}

请以JSON格式返回分析结果：
{{"text": "提取文本", "keywords": ["关键词1", "关键词2"], "summary": "摘要内容", "outline": "# 提纲", "mindmap": {{"root": "主题", "branches": ["分支1", "分支2"]}}}}"""

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
    """返回模拟结果（无API Key时使用）"""
    return {
        "text": content[:1000] if content else "[请输入文本内容]",
        "keywords": ["人工智能", "机器学习", "数据分析", "深度学习", "神经网络"],
        "summary": "这是学习资料的摘要总结。AI功能需要在后台配置智谱API Key后使用。",
        "outline": """# 背诵提纲

## 一、核心概念
- 概念一
- 概念二

## 二、重点内容
- 重点一
- 重点二

## 三、实践应用
- 应用一
- 应用二""",
        "mindmap": {
            "root": "学习资料主题",
            "branches": ["核心概念", "重点分析", "实践应用", "总结思考"]
        }
    }


# ============ 阿里云函数计算入口 ============
def handler(environ, start_response):
    """
    阿里云FC HTTP函数入口
    ======================
    """
    return app(environ, start_response)


# 本地测试
if __name__ == "__main__":
    print("🚀 启动本地服务: http://localhost:9000")
    app.run(host="0.0.0.0", port=9000, debug=True)
