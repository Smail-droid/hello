import os
import streamlit as st
import pyperclip
import time
import json
import requests
from langdetect import detect

# 设置页面配置
st.set_page_config(
    page_title="翻译助手",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 自定义CSS样式
st.markdown("""
<style>
    .main {
        padding: 1rem;
        max-width: 1600px;
        margin: 0 auto;
    }
    .stButton>button {
        width: 100%;
        background-color: #2196F3;
        color: white;
        padding: 0.5rem;
        border-radius: 5px;
        border: none;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #1976D2;
        transform: translateY(-1px);
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }
    .stTextArea>div>div>textarea {
        font-size: 1rem;
        border-radius: 5px;
        border: 1px solid #ddd;
        cursor: text;
        min-height: 200px;
    }
    .stTextArea>div>div>textarea:disabled {
        background-color: #f8f9fa;
        cursor: text;
    }
    .stSelectbox>div>div>select {
        font-size: 1rem;
        border-radius: 5px;
    }
    .stMarkdown h3 {
        color: #1976D2;
        margin-bottom: 0.5rem;
    }
    .stSpinner > div {
        border-color: #2196F3;
    }
    .success-message {
        color: #4CAF50;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    .quick-translate-btn {
        margin-top: 0.5rem;
    }
    .detected-lang {
        color: #666;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    .quick-buttons {
        margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# 从 secrets 获取 API 密钥
API_KEY = "sk-GR6XoKKYfrsfhBvKDj2FFELSgsRJ65IMdsDMLDODyt43ibtR"
API_URL = "https://api.chatanywhere.tech/v1/chat/completions"

# 请求限制控制
last_request_time = 0
min_request_interval = 0.1  # 100ms between requests (10 requests per second)

# 语言代码到中文名称的映射
LANGUAGE_NAMES = {
    'af': '南非荷兰语',
    'ar': '阿拉伯语',
    'bg': '保加利亚语',
    'bn': '孟加拉语',
    'ca': '加泰罗尼亚语',
    'cs': '捷克语',
    'cy': '威尔士语',
    'da': '丹麦语',
    'de': '德语',
    'el': '希腊语',
    'en': '英语',
    'es': '西班牙语',
    'et': '爱沙尼亚语',
    'fa': '波斯语',
    'fi': '芬兰语',
    'fr': '法语',
    'gu': '古吉拉特语',
    'he': '希伯来语',
    'hi': '印地语',
    'hr': '克罗地亚语',
    'hu': '匈牙利语',
    'id': '印尼语',
    'it': '意大利语',
    'ja': '日语',
    'kn': '卡纳达语',
    'ko': '韩语',
    'lt': '立陶宛语',
    'lv': '拉脱维亚语',
    'mk': '马其顿语',
    'ml': '马拉雅拉姆语',
    'mr': '马拉地语',
    'ne': '尼泊尔语',
    'nl': '荷兰语',
    'no': '挪威语',
    'pa': '旁遮普语',
    'pl': '波兰语',
    'pt': '葡萄牙语',
    'ro': '罗马尼亚语',
    'ru': '俄语',
    'sk': '斯洛伐克语',
    'sl': '斯洛文尼亚语',
    'so': '索马里语',
    'sq': '阿尔巴尼亚语',
    'sv': '瑞典语',
    'sw': '斯瓦希里语',
    'ta': '泰米尔语',
    'te': '泰卢固语',
    'th': '泰语',
    'tl': '他加禄语',
    'tr': '土耳其语',
    'uk': '乌克兰语',
    'ur': '乌尔都语',
    'vi': '越南语',
    'yi': '意第绪语',
    'zh-cn': '中文',
    'zh-tw': '中文',
    'zh': '中文'
}

def detect_language(text):
    """Detect the language of the input text"""
    try:
        lang_code = detect(text)
        return LANGUAGE_NAMES.get(lang_code, lang_code)
    except:
        return "未知语言"

def translate_text(text, target_language):
    """Translate text using OpenAI API"""
    global last_request_time
    
    try:
        # 控制请求频率
        current_time = time.time()
        time_since_last_request = current_time - last_request_time
        if time_since_last_request < min_request_interval:
            time.sleep(min_request_interval - time_since_last_request)
        
        # 构建请求数据
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        }
        
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": f"You are a professional translator. Translate the following text to {target_language}. Maintain the original formatting and meaning."},
                {"role": "user", "content": text}
            ],
            "temperature": 0.3
        }
        
        # 发送请求
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        
        last_request_time = time.time()
        
        # 检查响应格式
        if isinstance(result, dict):
            choices = result.get('choices', [])
            if choices and isinstance(choices[0], dict):
                message = choices[0].get('message', {})
                if isinstance(message, dict):
                    return message.get('content', 'Error: No content in response')
        return "Error: Unexpected response format from API"
            
    except requests.exceptions.RequestException as e:
        st.error(f"API请求错误: {str(e)}")
        return f"翻译失败: API请求错误"
    except Exception as e:
        st.error(f"翻译出错: {str(e)}")
        return f"翻译失败: {str(e)}"

def generate_polite_response(text):
    """Generate a polite response using OpenAI API"""
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        }
        
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": """你是一个擅长增进感情和建立良好关系的助手。请根据用户输入的内容，生成一个简短但温暖的回复。
                回复要求：
                1. 控制在30字以内
                2. 表达真诚的关心和理解
                3. 使用温暖友善的语气
                4. 可以适当使用1-2个表情符号
                5. 保持自然，避免过于做作
                6. 避免过于正式或客套的表达
                7. 重点突出：
                   - 表达理解和认同
                   - 给予真诚的赞美
                   - 表达关心和在意
                请记住，简短但温暖的回复往往更有力量。"""},
                {"role": "user", "content": text}
            ],
            "temperature": 0.7
        }
        
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        
        if isinstance(result, dict):
            choices = result.get('choices', [])
            if choices and isinstance(choices[0], dict):
                message = choices[0].get('message', {})
                if isinstance(message, dict):
                    return message.get('content', 'Error: No content in response')
        return "Error: Unexpected response format from API"
            
    except Exception as e:
        return f"生成回复失败: {str(e)}"

def copy_to_clipboard(text):
    """Copy text to clipboard with error handling"""
    try:
        pyperclip.copy(text)
        return True
    except Exception as e:
        st.warning("无法访问剪贴板，但翻译已完成。")
        return False

def main():
    # 初始化session state
    if 'translated_text' not in st.session_state:
        st.session_state.translated_text = ""
    if 'detected_language' not in st.session_state:
        st.session_state.detected_language = ""
    if 'last_copied' not in st.session_state:
        st.session_state.last_copied = 0
    if 'copy_success' not in st.session_state:
        st.session_state.copy_success = False

    # 语言选择
    target_language = st.selectbox(
        "选择目标语言",
        list(LANGUAGE_NAMES.values()),
        index=list(LANGUAGE_NAMES.values()).index("中文")
    )

    # 输入文本
    input_text = st.text_area("输入要翻译的文本", height=200)

    # 翻译按钮
    if st.button("翻译", key="translate_button"):
        with st.spinner("正在翻译..."):
            translated_text = translate_text(input_text, target_language)
            st.session_state.translated_text = translated_text
            st.session_state.detected_language = detect_language(input_text)
            
    # 显示翻译结果
    if st.session_state.translated_text:
        st.markdown("### 翻译结果")
        st.text_area("", st.session_state.translated_text, height=200, key="result_area")
        
        # 复制按钮
        if st.button("复制结果", key="copy_button"):
            if copy_to_clipboard(st.session_state.translated_text):
                st.session_state.copy_success = True
                st.session_state.last_copied = time.time()
                st.success("已复制到剪贴板！")
            else:
                st.info("翻译已完成，但无法访问剪贴板。")

if __name__ == "__main__":
    main() 