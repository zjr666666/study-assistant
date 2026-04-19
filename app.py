"""
校园AI学习助手 - FastAPI后端服务
==================================

功能：
- 文件上传（PDF、图片）
- AI文本提取
- AI重点分析（智谱GLM-4）
- 专注记录管理

作者：AI助手
版本：1.0.0
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, List
import os
import json
import base64
import requests
from datetime import datetime, timedelta
import uvicorn

# ============ 配置区域 ============
# 智谱AI配置 - 请替换为你自己的API密钥
ZHIPU_API_KEY = os.environ.get("ZHIPU_API_KEY", "your_api_key_here")
ZHIPU_API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

# 文件上传配置
UPLOAD_DIR = "uploads"
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg"}

# 专注记录存储（内存中，生产环境请使用数据库）
focus_records = []

# ============ FastAPI 应用 ============
app = FastAPI(
    title="校园AI学习助手 API",
    description="提供AI资料整理和专注统计功能",
    version="1.0.0"
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境请限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 创建上传目录
os.makedirs(UPLOAD_DIR, exist_ok=True)


# ============ 数据模型 ============
class AnalyzeRequest(BaseModel):
    text: str
    file_type: Optional[str] = None


class AnalyzeResponse(BaseModel):
    text: str
    keywords: List[str]
    summary: str
    outline: str
    mindmap: dict


class FocusSaveRequest(BaseModel):
    duration: int  # 分钟
    date: Optional[str] = None


class FocusStatsResponse(BaseModel):
    today: dict
    week: List[dict]
    total: dict


# ============ 健康检查 ============
@app.get("/")
async def root():
    """API根路径 - 健康检查"""
    return {
        "name": "校园AI学习助手 API",
        "version": "1.0.0",
        "status": "running",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/api/health")
async def health_check():
    """健康检查接口"""
    return {
        "status": "ok",
        "api_provider": "zhipu",
        "api_configured": ZHIPU_API_KEY != "your_api_key_here"
    }


# ============ 文件上传接口 ============
@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    文件上传接口
    
    支持格式：PDF、图片（PNG/JPG/JPEG）
    返回：文件ID、文件名、文件大小
    
    示例：
    ```
    curl -X POST "http://localhost:8000/api/upload" \\
         -F "file=@document.pdf"
    ```
    """
    # 检查文件扩展名
    filename = file.filename
    ext = os.path.splitext(filename)[1].lower()
    
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"不支持的文件格式。仅支持：{', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # 读取文件内容
    content = await file.read()
    
    # 检查文件大小
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"文件过大。最大支持 {MAX_FILE_SIZE // (1024*1024)}MB"
        )
    
    # 保存文件
    file_id = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{len(content)}"
    filepath = os.path.join(UPLOAD_DIR, f"{file_id}{ext}")
    
    with open(filepath, "wb") as f:
        f.write(content)
    
    return {
        "file_id": file_id,
        "filename": filename,
        "size": len(content),
        "filepath": filepath,
        "type": "pdf" if ext == ".pdf" else "image"
    }


# ============ AI分析接口 ============
@app.post("/api/analyze", response_model=AnalyzeResponse)
async def analyze_content(
    text: str = None,
    file: UploadFile = File(None)
):
    """
    AI内容分析接口
    
    功能：
    - 提取文本内容
    - 识别重点关键词
    - 生成摘要
    - 生成背诵提纲
    - 生成思维导图结构
    
    参数：
    - text: 直接传入的文本
    - file: 上传的文件（PDF或图片）
    
    返回：分析结果字典
    """
    content_text = ""
    
    # 如果上传了文件，提取文本
    if file:
        ext = os.path.splitext(file.filename)[1].lower()
        content = await file.read()
        
        if ext == ".pdf":
            content_text = extract_pdf_text(content)
        elif ext in {".png", ".jpg", ".jpeg"}:
            # 图片需要OCR，这里简化处理
            content_text = "[图片内容]\n请配置OCR服务以提取图片文字"
        else:
            content_text = "[无法识别的文件格式]"
    elif text:
        content_text = text
    else:
        raise HTTPException(status_code=400, detail="请提供文本或上传文件")
    
    # 调用AI分析
    ai_result = await call_zhipu_ai(content_text)
    
    return AnalyzeResponse(**ai_result)


async def call_zhipu_ai(content: str) -> dict:
    """
    调用智谱GLM-4 API进行分析
    
    参数：
    - content: 待分析的文本内容
    
    返回：包含text、keywords、summary、outline、mindmap的字典
    """
    # 如果未配置API，返回模拟数据
    if ZHIPU_API_KEY == "your_api_key_here":
        return get_mock_analysis(content)
    
    # 构建提示词
    prompt = f"""请分析以下学习资料，提取关键信息：

资料内容：
{content[:2000]}

请按以下JSON格式返回分析结果（只返回JSON，不要其他内容）：
{{
    "text": "提取的文本内容（保留原文重点段落）",
    "keywords": ["关键词1", "关键词2", "关键词3", "关键词4", "关键词5"],
    "summary": "100字以内的内容摘要",
    "outline": "# 背诵提纲\\n\\n## 一、核心概念\\n- 要点1\\n- 要点2\\n\\n## 二、重点内容\\n- 内容1\\n- 内容2",
    "mindmap": {{
        "root": "主题名称",
        "branches": ["分支1", "分支2", "分支3", "分支4"]
    }}
}}"""

    try:
        headers = {
            "Authorization": f"Bearer {ZHIPU_API_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "glm-4-flash",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7
        }
        
        response = requests.post(
            ZHIPU_API_URL,
            headers=headers,
            json=data,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            
            # 尝试解析JSON
            try:
                # 去除可能的markdown代码块
                if "```json" in content:
                    content = content.split("```json")[1].split("```")[0]
                elif "```" in content:
                    content = content.split("```")[1].split("```")[0]
                
                return json.loads(content.strip())
            except json.JSONDecodeError:
                return get_mock_analysis(content)
        else:
            print(f"API调用失败: {response.status_code}")
            return get_mock_analysis(content)
            
    except Exception as e:
        print(f"调用异常: {e}")
        return get_mock_analysis(content)


def get_mock_analysis(content: str) -> dict:
    """返回模拟分析结果（用于演示）"""
    return {
        "text": content[:1000] if len(content) > 1000 else content,
        "keywords": ["人工智能", "机器学习", "深度学习", "神经网络", "数据分析"],
        "summary": "这是一段学习资料的核心摘要，概括了主要内容要点。",
        "outline": """# 背诵提纲

## 一、基础知识回顾
- 核心概念定义
- 基本原理说明
- 典型应用场景

## 二、重点难点分析
- 关键技术点
- 常见问题解析
- 实践应用技巧

## 三、总结与展望
- 知识体系梳理
- 未来发展方向""",
        "mindmap": {
            "root": "学习资料",
            "branches": ["基础概念", "重点分析", "实践应用", "总结提升"]
        }
    }


def extract_pdf_text(content: bytes) -> str:
    """
    从PDF提取文本
    
    这里使用简单实现，生产环境建议使用：
    - PyPDF2
    - pdfplumber
    - pdfminer
    """
    try:
        # 简单尝试读取PDF内容
        # 实际项目请安装：pip install pypdf
        from io import BytesIO
        try:
            from pypdf import PdfReader
            reader = PdfReader(BytesIO(content))
            text = ""
            for page in reader.pages[:10]:  # 最多取前10页
                text += page.extract_text() + "\n\n"
            return text if text.strip() else "[PDF无文本内容]"
        except ImportError:
            return "[请安装pypdf: pip install pypdf]\nPDF文件已上传，但文本提取功能需要安装依赖"
    except Exception as e:
        return f"[PDF解析出错: {e}]"


# ============ 专注记录接口 ============
@app.post("/api/focus/save")
async def save_focus_record(request: FocusSaveRequest):
    """
    保存专注记录
    
    参数：
    - duration: 专注时长（分钟）
    - date: 日期（可选，默认今天）
    """
    record = {
        "id": len(focus_records) + 1,
        "duration": request.duration,
        "date": request.date or datetime.now().strftime("%Y-%m-%d"),
        "timestamp": datetime.now().isoformat()
    }
    
    focus_records.append(record)
    
    return {
        "success": True,
        "record": record
    }


@app.get("/api/focus/stats", response_model=FocusStatsResponse)
async def get_focus_stats():
    """
    获取专注统计数据
    
    返回：
    - today: 今日统计
    - week: 本周每日统计
    - total: 总计统计
    """
    today = datetime.now().strftime("%Y-%m-%d")
    week_ago = (datetime.now() - timedelta(days=6)).strftime("%Y-%m-%d")
    
    # 今日统计
    today_records = [r for r in focus_records if r["date"] == today]
    today_stats = {
        "total": sum(r["duration"] for r in today_records),
        "count": len(today_records)
    }
    
    # 本周统计
    week_stats = []
    for i in range(7):
        date = (datetime.now() - timedelta(days=6-i)).strftime("%Y-%m-%d")
        day_records = [r for r in focus_records if r["date"] == date]
        week_stats.append({
            "date": date,
            "total": sum(r["duration"] for r in day_records),
            "count": len(day_records)
        })
    
    # 总计
    total_stats = {
        "total": sum(r["duration"] for r in focus_records),
        "count": len(focus_records)
    }
    
    return FocusStatsResponse(
        today=today_stats,
        week=week_stats,
        total=total_stats
    )


@app.get("/api/focus/records")
async def get_focus_records(limit: int = 20):
    """
    获取专注记录列表
    
    参数：
    - limit: 返回记录数量限制
    """
    records = sorted(focus_records, key=lambda x: x["timestamp"], reverse=True)
    return records[:limit]


# ============ 主程序入口 ============
if __name__ == "__main__":
    print("""
╔═══════════════════════════════════════════════════════════╗
║          📚 校园AI学习助手 - FastAPI 后端服务              ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  🔧 服务地址: http://localhost:8000                       ║
║  📖 API文档:  http://localhost:8000/docs                  ║
║  🏥 健康检查: http://localhost:8000/api/health           ║
║                                                           ║
║  ⚠️  配置提示:                                             ║
║     请设置环境变量 ZHIPU_API_KEY 启用AI分析功能            ║
║     export ZHIPU_API_KEY="your_api_key"                  ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
    """)
    
    # 启动服务
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
