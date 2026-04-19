# -*- coding: utf-8 -*-
"""
=====================================================
    资料智能整理 - Flask 后端服务
=====================================================
    文件作用: 提供文件上传、OCR识别、AI分析等API接口
    
    运行方式:
        python app.py
        
    依赖安装:
        pip install flask flask-cors requests pillow pypdf
        
    接口说明:
        POST /api/ocr        - 图片OCR识别
        POST /api/upload     - PDF文件上传解析
        POST /api/analyze    - AI文本分析(章节拆分/关键词/提纲)
"""

import os
import base64
import json
import traceback
from flask import Flask, request, jsonify
from flask_cors import CORS

# ==================== 配置部分 ====================

# Flask应用配置
app = Flask(__name__)
CORS(app)  # 允许跨域请求

# API配置 - 请填入你的API密钥
# 推荐使用硅基流动: https://siliconflow.cn (免费额度大)
API_CONFIG = {
    # 方式1: 硅基流动 (推荐 - 免费额度大)
    'provider': 'siliconflow',
    'api_key': 'YOUR_SILICONFLOW_API_KEY',  # 替换为你的API密钥
    
    # 方式2: 智谱AI (需要申请)
    # 'provider': 'zhipu',
    # 'api_key': 'YOUR_ZHIPU_API_KEY',
    
    # 方式3: OpenAI (需要科学上网)
    # 'provider': 'openai',
    # 'api_key': 'YOUR_OPENAI_API_KEY',
}

# 文件上传配置
UPLOAD_FOLDER = 'uploads'
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}

# 确保上传目录存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ==================== 工具函数 ====================

def allowed_file(filename):
    """检查文件扩展名是否允许"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_uploaded_file(file):
    """
    保存上传的文件
    返回: 文件保存路径
    """
    filename = file.filename
    # 生成唯一文件名避免冲突
    unique_filename = f"{os.urandom(16).hex()}_{filename}"
    filepath = os.path.join(UPLOAD_FOLDER, unique_filename)
    file.save(filepath)
    return filepath


def delete_file(filepath):
    """删除文件"""
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
    except Exception as e:
        print(f"删除文件失败: {e}")


def call_ai_api(prompt, system_prompt=None):
    """
    调用AI API进行文本处理
    
    Args:
        prompt: 用户提示词
        system_prompt: 系统提示词
        
    Returns:
        AI返回的文本内容
    """
    import requests
    
    if API_CONFIG['provider'] == 'siliconflow':
        # 硅基流动 API
        url = "https://api.siliconflow.cn/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {API_CONFIG['api_key']}",
            "Content-Type": "application/json"
        }
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        data = {
            "model": "Qwen/Qwen2.5-7B-Instruct",  # 免费模型
            # "model": "deepseek-ai/DeepSeek-V2.5",  # 也可尝试这个免费模型
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 2000
        }
        
    elif API_CONFIG['provider'] == 'zhipu':
        # 智谱AI API
        url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
        headers = {
            "Authorization": f"Bearer {API_CONFIG['api_key']}",
            "Content-Type": "application/json"
        }
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        data = {
            "model": "glm-4-flash",  # 免费模型
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 2000
        }
        
    elif API_CONFIG['provider'] == 'openai':
        # OpenAI API
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {API_CONFIG['api_key']}",
            "Content-Type": "application/json"
        }
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        data = {
            "model": "gpt-3.5-turbo",
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 2000
        }
    else:
        raise ValueError(f"不支持的AI提供商: {API_CONFIG['provider']}")
    
    # 发送请求
    try:
        response = requests.post(url, headers=headers, json=data, timeout=60)
        response.raise_for_status()
        result = response.json()
        
        # 提取AI回复
        if 'choices' in result and len(result['choices']) > 0:
            return result['choices'][0]['message']['content']
        else:
            raise Exception(f"API返回格式错误: {result}")
            
    except requests.exceptions.Timeout:
        raise Exception("AI API请求超时，请重试")
    except requests.exceptions.RequestException as e:
        raise Exception(f"AI API请求失败: {str(e)}")
    except Exception as e:
        raise Exception(f"AI处理出错: {str(e)}")


def simple_ocr(image_path):
    """
    简单的图片文字识别
    注意: 这是基础版本，需要配置百度OCR等付费服务才能获得更好的识别效果
    
    当前实现: 返回模拟数据 (仅用于演示)
    实际使用时需要:
    1. 申请百度OCR API (免费额度500次/天)
    2. 或使用其他OCR服务
    
    Returns:
        识别出的文本内容
    """
    # TODO: 接入真实的OCR服务
    # 推荐方案:
    # 1. 百度OCR: https://ai.baidu.com/tech/ocr
    # 2. 腾讯OCR: https://cloud.tencent.com/product/ocr
    # 3. 阿里OCR: https://help.aliyun.com/product/位移/位移/12323
    
    print(f"[OCR] 正在处理图片: {image_path}")
    
    # 这里可以接入百度OCR等API
    # 暂时返回提示信息，实际使用时请替换为真实OCR调用
    
    return None  # 返回None表示需要外部OCR服务


def extract_pdf_text(pdf_path):
    """
    从PDF文件中提取文本
    
    Args:
        pdf_path: PDF文件路径
        
    Returns:
        提取的文本内容
    """
    import PyPDF2
    
    text = []
    try:
        with open(pdf_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            print(f"[PDF] 共 {len(reader.pages)} 页")
            
            for i, page in enumerate(reader.pages):
                page_text = page.extract_text()
                if page_text:
                    text.append(page_text)
                print(f"[PDF] 已处理第 {i+1} 页")
                
    except Exception as e:
        print(f"[PDF] 解析错误: {e}")
        raise Exception(f"PDF解析失败: {str(e)}")
    
    return '\n\n'.join(text)


def analyze_content_with_ai(text):
    """
    使用AI分析文本内容
    
    功能:
    1. 识别章节结构
    2. 提取关键词
    3. 生成背诵提纲
    
    Args:
        text: 待分析的文本
        
    Returns:
        分析结果字典
    """
    # 截断过长的文本 (API有token限制)
    max_chars = 3000
    if len(text) > max_chars:
        text = text[:max_chars] + "\n\n[内容已截断...]"
    
    # 系统提示词
    system_prompt = """你是一个专业的学习助手，擅长整理学习资料。
    请分析用户提供的文本内容，完成以下任务:
    1. 识别并列出主要章节
    2. 提取10个最重要的关键词
    3. 生成一份简洁的背诵提纲
    
    请严格按照以下JSON格式返回结果:
    {
        "chapters": ["章节1", "章节2", ...],
        "keywords": ["关键词1", "关键词2", ...],
        "outline": "背诵提纲内容(使用Markdown格式，条理清晰，便于背诵)"
    }
    
    提纲要求:
    - 使用简洁的语言
    - 重点突出
    - 适合大声朗读背诵
    - 可以添加适当的序号和分层"""
    
    # 用户提示词
    user_prompt = f"请分析以下内容:\n\n{text}"
    
    # 调用AI
    ai_response = call_ai_api(user_prompt, system_prompt)
    
    # 解析AI返回的JSON
    try:
        # 尝试提取JSON部分
        json_str = ai_response
        if '```json' in ai_response:
            json_str = ai_response.split('```json')[1].split('```')[0]
        elif '```' in ai_response:
            json_str = ai_response.split('```')[1].split('```')[0]
        
        result = json.loads(json_str.strip())
        return result
        
    except json.JSONDecodeError as e:
        print(f"[AI] JSON解析失败: {e}")
        print(f"[AI] 原始响应: {ai_response}")
        # 返回默认结构
        return {
            "chapters": [],
            "keywords": [],
            "outline": ai_response if ai_response else "无法生成提纲"
        }


# ==================== API路由 ====================

@app.route('/')
def index():
    """首页"""
    return jsonify({
        "name": "资料智能整理 API",
        "version": "1.0.0",
        "endpoints": {
            "POST /api/ocr": "上传图片进行OCR识别",
            "POST /api/upload": "上传PDF文件进行解析",
            "POST /api/analyze": "分析文本内容，提取章节、关键词、生成提纲",
            "GET /api/health": "健康检查"
        }
    })


@app.route('/api/health')
def health_check():
    """健康检查接口"""
    return jsonify({
        "status": "ok",
        "api_provider": API_CONFIG.get('provider', 'not_configured'),
        "api_configured": API_CONFIG.get('api_key') != 'YOUR_API_KEY'
    })


@app.route('/api/ocr', methods=['POST'])
def ocr_image():
    """
    图片OCR识别接口
    
    请求: multipart/form-data
        - file: 图片文件
        
    响应:
        {
            "success": true/false,
            "text": "识别出的文本",
            "error": "错误信息(如果失败)"
        }
    """
    try:
        # 检查是否有文件
        if 'file' not in request.files:
            return jsonify({
                "success": False,
                "error": "没有上传文件"
            })
        
        file = request.files['file']
        
        # 检查文件名
        if file.filename == '':
            return jsonify({
                "success": False,
                "error": "文件名为空"
            })
        
        # 检查文件类型
        if not allowed_file(file.filename):
            return jsonify({
                "success": False,
                "error": "不支持的文件类型"
            })
        
        # 保存文件
        filepath = save_uploaded_file(file)
        print(f"[OCR] 已保存文件: {filepath}")
        
        try:
            # 调用OCR (当前为演示版本)
            # 实际使用时需要接入百度OCR等API
            text = simple_ocr(filepath)
            
            if text is None:
                # 如果没有配置OCR，返回提示
                return jsonify({
                    "success": False,
                    "error": "OCR服务未配置。请配置百度OCR API或使用PDF解析功能。"
                })
            
            return jsonify({
                "success": True,
                "text": text
            })
            
        finally:
            # 清理临时文件
            delete_file(filepath)
            
    except Exception as e:
        traceback.print_exc()
        return jsonify({
            "success": False,
            "error": str(e)
        })


@app.route('/api/upload', methods=['POST'])
def upload_pdf():
    """
    PDF文件上传和解析接口
    
    请求: multipart/form-data
        - file: PDF文件
        
    响应:
        {
            "success": true/false,
            "text": "提取的文本",
            "error": "错误信息(如果失败)"
        }
    """
    try:
        # 检查是否有文件
        if 'file' not in request.files:
            return jsonify({
                "success": False,
                "error": "没有上传文件"
            })
        
        file = request.files['file']
        
        # 检查文件名
        if file.filename == '':
            return jsonify({
                "success": False,
                "error": "文件名为空"
            })
        
        # 检查文件类型
        if not allowed_file(file.filename):
            return jsonify({
                "success": False,
                "error": "不支持的文件类型"
            })
        
        # 保存文件
        filepath = save_uploaded_file(file)
        print(f"[PDF] 已保存文件: {filepath}")
        
        try:
            # 提取PDF文本
            text = extract_pdf_text(filepath)
            
            if not text or len(text.strip()) < 10:
                return jsonify({
                    "success": False,
                    "error": "PDF内容为空或无法提取文本(可能是扫描版PDF)"
                })
            
            print(f"[PDF] 已提取 {len(text)} 字符")
            
            return jsonify({
                "success": True,
                "text": text
            })
            
        finally:
            # 清理临时文件
            delete_file(filepath)
            
    except Exception as e:
        traceback.print_exc()
        return jsonify({
            "success": False,
            "error": str(e)
        })


@app.route('/api/analyze', methods=['POST'])
def analyze():
    """
    文本分析接口
    
    请求: application/json
        {
            "text": "待分析的文本"
        }
        
    响应:
        {
            "success": true/false,
            "chapters": ["章节列表"],
            "keywords": ["关键词列表"],
            "outline": "生成的背诵提纲",
            "error": "错误信息(如果失败)"
        }
    """
    try:
        # 获取请求数据
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({
                "success": False,
                "error": "缺少text参数"
            })
        
        text = data['text'].strip()
        
        if not text:
            return jsonify({
                "success": False,
                "error": "文本内容为空"
            })
        
        if len(text) < 10:
            return jsonify({
                "success": False,
                "error": "文本内容太短，无法分析"
            })
        
        print(f"[分析] 开始分析文本 ({len(text)} 字符)")
        
        # 调用AI分析
        result = analyze_content_with_ai(text)
        
        print(f"[分析] 完成")
        
        return jsonify({
            "success": True,
            "chapters": result.get('chapters', []),
            "keywords": result.get('keywords', []),
            "outline": result.get('outline', '')
        })
        
    except Exception as e:
        traceback.print_exc()
        return jsonify({
            "success": False,
            "error": str(e)
        })


# ==================== 主程序入口 ====================

if __name__ == '__main__':
    print("=" * 50)
    print("📚 资料智能整理 - Flask后端服务")
    print("=" * 50)
    print(f"\n🔧 API配置: {API_CONFIG['provider']}")
    print(f"   API Key: {'已配置 ✓' if API_CONFIG['api_key'] != 'YOUR_API_KEY' else '未配置 ✗'}")
    print(f"\n📡 服务地址: http://localhost:5000")
    print(f"📖 API文档: http://localhost:5000/")
    print("\n💡 启动前端: 打开 index.html 或启动 http.server")
    print("\n" + "=" * 50)
    
    # 启动Flask服务
    # debug=True 开启调试模式，代码修改会自动重启
    # port=5000 指定端口
    app.run(
        host='0.0.0.0',  # 允许外部访问
        port=5000,
        debug=True
    )
