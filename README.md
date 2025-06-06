# 翻译助手

一个基于 Streamlit 的智能翻译工具，支持多语言翻译和高情商回复功能。

## 功能特点

- 支持多种语言之间的互译
- 实时语言检测
- 一键复制翻译结果
- 高情商回复生成
- 简洁美观的界面

## 本地运行

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 运行应用：
```bash
streamlit run translator.py
```

## 部署到 Streamlit 社区云

1. 在 GitHub 上创建一个新的仓库
2. 将代码推送到仓库
3. 访问 [Streamlit Community Cloud](https://streamlit.io/cloud)
4. 点击 "New app"
5. 选择你的 GitHub 仓库
6. 在 "Secrets" 部分添加你的 API 密钥
7. 点击 "Deploy"

## 注意事项

- 请确保 API 密钥的安全性
- 建议定期更新依赖包
- 本地运行时需要配置 `.streamlit/secrets.toml` 文件

## Features

- Translate text between multiple languages
- User-friendly interface
- Powered by OpenAI's GPT-3.5
- Support for multiple languages including English, Chinese, Japanese, Korean, Spanish, French, German, and Russian

## Setup

1. Clone this repository
2. Create a `.env` file in the project root and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```
   You can obtain an API key from the [OpenAI platform](https://platform.openai.com/api-keys)

## Usage

1. Run the application:
   ```bash
   streamlit run translator.py
   ```
2. Open your web browser and navigate to the URL shown in the terminal (usually http://localhost:8501)
3. Enter the text you want to translate
4. Select the target language
5. Click the "Translate" button

## Notes

- The application uses OpenAI's GPT-3.5-turbo model
- Translation quality depends on the OpenAI model's capabilities
- Make sure you have a stable internet connection
- The API key should be kept secure and not shared publicly

## Requirements

- Python 3.7+
- OpenAI API key
- Internet connection 