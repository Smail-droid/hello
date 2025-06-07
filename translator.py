import os
import streamlit as st
import pyperclip
import time
import json
import requests
from langdetect import detect
import streamlit.components.v1 as components

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
    .responsive-btns {display: flex; flex-wrap: wrap; gap: 8px; justify-content: center; margin-bottom: 16px;}
    .responsive-btns button {flex: 1 1 120px; min-width: 100px; margin-bottom: 4px;}
    @media (max-width: 600px) {.responsive-btns {flex-direction: column;}}
    .stTextArea [data-testid="stTextArea"] textarea:empty {background: transparent;}
    .centered-loading {
        position: fixed;
        top: 20px;
        left: 50%;
        transform: translateX(-50%);
        z-index: 9999;
        font-size: 1.2rem;
        color: #1976D2;
        background: rgba(255,255,255,0.95);
        padding: 8px 24px;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        display: flex;
        align-items: center;
        font-weight: bold;
    }
    .lds-dual-ring {
      display: inline-block;
      width: 24px;
      height: 24px;
      margin-right: 10px;
    }
    .lds-dual-ring:after {
      content: " ";
      display: block;
      width: 24px;
      height: 24px;
      border-radius: 50%;
      border: 3px solid #1976D2;
      border-color: #1976D2 transparent #1976D2 transparent;
      animation: lds-dual-ring 1.2s linear infinite;
    }
    @keyframes lds-dual-ring {
      0% { transform: rotate(0deg); }
      100% { transform: rotate(360deg); }
    }
    .chat-bubble-user {background:#e6f0fa; color:#222; border-radius:12px 12px 4px 12px; padding:10px 16px; margin:8px 0; max-width:70%; align-self:flex-end;}
    .chat-bubble-result {background:#f5f5f5; color:#222; border-radius:12px 12px 12px 4px; padding:10px 16px; margin:8px 0; max-width:70%; align-self:flex-start;}
    .chat-bubble-pol {background:#fffbe6; color:#222; border-radius:12px 12px 12px 4px; padding:10px 16px; margin:8px 0; max-width:70%; align-self:flex-start; font-style:italic;}
    .chat-history {display:flex; flex-direction:column; gap:0; min-height:60vh; margin-bottom:16px;}
    .chat-bottom-bar {position:fixed; bottom:0; left:0; width:100vw; background:#fff; z-index:100; box-shadow:0 -2px 8px rgba(0,0,0,0.04); padding:12px 0 8px 0;}
    .lang-btn {border:none; background:transparent; font-size:1.5rem; margin:0 4px; cursor:pointer;}
    .send-btn {background:#1976D2; color:#fff; border:none; border-radius:6px; padding:8px 24px; font-size:1.1rem; margin-left:8px; cursor:pointer;}
    @media (max-width:600px) {.chat-bubble-user,.chat-bubble-result,.chat-bubble-pol{max-width:95%;}}
    .lang-btn-bar {display: flex; flex-wrap: wrap; gap: 0; margin-bottom: 18px; justify-content: flex-start;}
    .lang-btn-bar button {
        flex: 1 1 25%;
        min-width: 0;
        max-width: 100%;
        height: 44px;
        font-size: 1.1rem;
        border: none;
        border-radius: 6px;
        background: #1890ff;
        color: #fff;
        box-shadow: 0 2px 8px rgba(24,144,255,0.10);
        transition: transform 0.15s, box-shadow 0.15s, background 0.3s;
        cursor: pointer;
        outline: none;
        margin: 0;
        padding: 0 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 8px;
        margin-bottom: 8px;
    }
    .lang-btn-bar button:hover {
        background: #40a9ff;
        box-shadow: 0 4px 16px rgba(24,144,255,0.18);
        transform: scale(1.06);
    }
    .lang-btn-bar button:last-child {margin-right: 0;}
    @media (max-width: 900px) {
        .lang-btn-bar button {flex: 1 1 50%;}
    }
    @media (max-width: 600px) {
        .lang-btn-bar button {flex: 1 1 100%; min-width: 60px; font-size: 1rem;}
    }
    .custom-btn {
        width: 100%;
        height: 44px;
        font-size: 1.1rem;
        border: none;
        border-radius: 6px;
        background: #1890ff;
        color: #fff;
        box-shadow: 0 2px 8px rgba(24,144,255,0.10);
        transition: transform 0.15s, box-shadow 0.15s, background 0.3s;
        cursor: pointer;
        outline: none;
        margin: 0;
        padding: 0 8px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .custom-btn:hover {
        background: #40a9ff;
        box-shadow: 0 4px 16px rgba(24,144,255,0.18);
        transform: scale(1.06);
    }
</style>
""", unsafe_allow_html=True)

# 从 secrets 获取 API 密钥
API_KEY = "sk-E6jFLa6hABZ56B5rfNpaCrm3haMjkMR3nRQvbc3raq0mrGYZ"
API_URL = "https://k.hdgsb.com/v1/chat/completions"

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
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        }
        data = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": f"You are a professional translator. Translate the following text to {target_language}. Maintain the original formatting and meaning."},
                {"role": "user", "content": text}
            ],
            "temperature": 0.3
        }
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        last_request_time = time.time()
        if isinstance(result, dict):
            choices = result.get('choices', [])
            if choices and isinstance(choices[0], dict):
                message = choices[0].get('message', {})
                if isinstance(message, dict):
                    return message.get('content', 'Error: No content in response')
        return "Error: Unexpected response format from API"
    except requests.exceptions.HTTPError as e:
        if e.response is not None and e.response.status_code == 429:
            st.error('请求过于频繁，请稍后再试。')
            return '翻译失败: 请求过于频繁，请稍后再试。'
        else:
            st.error(f'API请求错误: {str(e)}')
            return f'翻译失败: API请求错误'
    except requests.exceptions.RequestException as e:
        st.error(f"API请求错误: {str(e)}")
        return f"翻译失败: API请求错误"
    except Exception as e:
        st.error(f"翻译出错: {str(e)}")
        return f"翻译失败: {str(e)}"

def generate_polite_response(text):
    """Generate a polite response using OpenAI API, no emoji, no '加油' etc."""
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        }
        data = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "你是一个擅长增进感情和建立良好关系的助手。请根据用户输入的内容，生成一个简短但温暖的回复。回复要求：1. 控制在30字以内 2. 表达真诚的关心和理解 3. 使用温暖友善的语气 4. 不要使用任何表情符号 5. 不要出现'加油'、'祝你好运'等鼓励性口号，只表达理解、关心和支持。6. 保持自然，避免过于做作。7. 重点突出：表达理解和认同，给予真诚的赞美，表达关心和在意。请记住，简短但温暖的回复往往更有力量。"},
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
    except requests.exceptions.HTTPError as e:
        if e.response is not None and e.response.status_code == 429:
            st.error('请求过于频繁，请稍后再试。')
            return '生成回复失败: 请求过于频繁，请稍后再试。'
        else:
            st.error(f'API请求错误: {str(e)}')
            return f'生成回复失败: API请求错误'
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
    # --- 输入框清空机制 ---
    if st.session_state.get('clear_input', False):
        st.session_state['input_area'] = ''
        st.session_state['clear_input'] = False
        st.rerun()

    # 初始化 session_state
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []
    if 'target_language' not in st.session_state:
        st.session_state['target_language'] = '中文'
    if 'input_area' not in st.session_state:
        st.session_state['input_area'] = ''
    if 'loading_message' not in st.session_state:
        st.session_state['loading_message'] = ''
    if 'last_input' not in st.session_state:
        st.session_state['last_input'] = ''
    if 'pending_send' not in st.session_state:
        st.session_state['pending_send'] = False
    if 'auto_translate' not in st.session_state:
        st.session_state['auto_translate'] = False

    # 语言按钮
    languages = {
        '英语': '🇬🇧',
        '波斯语': '🇮🇷',
        '乌兹别克语': '🇺🇿',
        '日语': '🇯🇵'
    }
    
    # 语言按钮区（与发送按钮同样样式，一行4个，铺满宽度）
    st.markdown('''
    <style>
    .custom-btn {
        width: 100%;
        height: 44px;
        font-size: 1.1rem;
        border: none;
        border-radius: 6px;
        background: #1890ff;
        color: #fff;
        box-shadow: 0 2px 8px rgba(24,144,255,0.10);
        transition: transform 0.15s, box-shadow 0.15s, background 0.3s;
        cursor: pointer;
        outline: none;
        margin: 0;
        padding: 0 8px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .custom-btn:hover {
        background: #40a9ff;
        box-shadow: 0 4px 16px rgba(24,144,255,0.18);
        transform: scale(1.06);
    }
    </style>
    ''', unsafe_allow_html=True)
    lang_keys = list(languages.keys())
    lang_cols = st.columns(4)
    for i, lang in enumerate(lang_keys):
        with lang_cols[i]:
            if st.button(lang, key=f'lang_btn_{lang}', use_container_width=True):
                st.session_state['target_language'] = lang
                input_val = st.session_state.get('input_area', '')
                if input_val:
                    st.session_state['last_input'] = input_val
                    st.session_state['chat_history'].append({'role':'user','text':input_val,'lang':'auto'})
                    st.session_state['pending_send'] = True
                st.rerun()

    # 输入框和发送按钮
    st.markdown('<div style="margin-bottom:12px;"></div>', unsafe_allow_html=True)
    col1, col2 = st.columns([5,1])
    with col1:
        if st.session_state.get('clear_input', False):
            user_input = st.text_input("", value="", key='input_area', placeholder="请输入内容并回车或点击发送...", label_visibility='collapsed')
            st.session_state['clear_input'] = False
        else:
            user_input = st.text_input("", key='input_area', placeholder="请输入内容并回车或点击发送...", label_visibility='collapsed')
    with col2:
        send_clicked = st.button('发送', key='send_btn', use_container_width=True)
        if send_clicked:
            st.session_state['target_language'] = '中文'  # 默认翻译为中文
            if st.session_state.get('input_area', ''):
                st.session_state['last_input'] = st.session_state['input_area']
                st.session_state['chat_history'].append({'role':'user','text':st.session_state['input_area'],'lang':'auto'})
                st.session_state['pending_send'] = True
                st.session_state['clear_input'] = True  # 标记清空
            st.rerun()

    # 结果区：输入框下方只显示最新一组，历史组依次往下
    history = st.session_state['chat_history']
    groups = []
    i = 0
    while i < len(history):
        if history[i]['role'] == 'result':
            group = {'result': history[i]['text'], 'polite': ''}
            if i+1 < len(history) and history[i+1]['role'] == 'polite':
                group['polite'] = history[i+1]['text']
                i += 1
            groups.append(group)
        i += 1
    # 最新一组在输入框下方
    if groups:
        group = groups[-1]
        st.markdown(f'<div class="chat-bubble-result">🌐 {group["result"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="chat-bubble-pol">{group["polite"]}</div>', unsafe_allow_html=True)
    # 其余历史依次往下
    for group in reversed(groups[:-1]):
        st.markdown(f'<div class="chat-bubble-result">🌐 {group["result"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="chat-bubble-pol">{group["polite"]}</div>', unsafe_allow_html=True)

    # 自动处理最新一条未翻译的用户消息
    chat_history = st.session_state.get('chat_history', [])
    if st.session_state.get('pending_send', False):
        if chat_history and (not chat_history[-1].get('handled')) and chat_history[-1]['role']=='user':
            try:
                user_msg = chat_history[-1]['text']
                target_lang = st.session_state.get('target_language', '中文')
                st.session_state['loading_message'] = '翻译中...'
                result = translate_text(user_msg, target_lang)
                if result:  # 确保翻译结果不为空
                    st.session_state['chat_history'].append({'role':'result','text':result,'lang':target_lang})
                    st.session_state['loading_message'] = '生成高情商回复...'
                    polite = generate_polite_response(result)
                    if polite:  # 确保高情商回复不为空
                        st.session_state['chat_history'].append({'role':'polite','text':polite,'lang':target_lang})
                        st.session_state['chat_history'][-3]['handled'] = True
                        st.session_state['loading_message'] = ''
                        st.session_state['pending_send'] = False
                        st.session_state['auto_translate'] = False
                        st.session_state['clear_input'] = True  # 翻译成功后清空输入框
                        st.rerun()
            except Exception as e:
                st.error(f"翻译过程中出现错误: {str(e)}")
                st.session_state['pending_send'] = False
                st.session_state['loading_message'] = ''

if __name__ == "__main__":
    main() 