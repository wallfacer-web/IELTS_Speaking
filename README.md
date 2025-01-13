# 口语润色助手

本项目旨在帮助口语学习者及教学工作者快速实现音频转录、文本润色及语音合成功能，提升口语表达的准确度和流畅度。通过本工具，用户可便捷地上传音频、获取转录文本，并利用外部 AI 模型进行文本润色，最终生成用于口语练习或课堂教学演示的音频文件。

---

## 功能概述

1. **音频转录**  
   - 利用 [Whisper](https://github.com/openai/whisper) 将音频转换为文本，支持多种音频格式（如 MP3、M4A、WAV）。
   
2. **文本润色**  
   - 接入运行在本地的 AI 模型接口（默认地址 `http://localhost:11434/api/generate`），自动润色转录文本，包括用词优化、句式变换和细节补充，提升口语表达的多样性和准确度。

3. **文本转语音 (TTS)**  
   - 使用 Microsoft Edge TTS 将润色后的文本转化为语音，自动生成可播放的 MP3 音频文件，方便在课堂或个人练习中进一步模仿与学习。

4. **可视化交互界面**  
   - 借助 [Streamlit](https://streamlit.io/) 构建的 Web 界面，用户无需编写任何代码即可完成文件上传、设置及音频播放等操作。

---

## 特性与亮点

- **一站式工作流**：从音频转录到文本润色，再到语音合成，用户只需在同一个界面上进行简单操作，即可获得完整成果。
- **可选AI模型**：支持 `llama3`、`qwen2`、`mistral` 等多种模型，满足不同的润色风格和场景需求。
- **可定制提示词**：通过设置特定提示文本（prompt），灵活调整最终润色效果和目标字数。
- **异步任务处理**：在文本转语音阶段使用异步处理，提升应用响应速度。

---

## 环境准备与安装

### 1. 环境要求

- Python 3.7及以上版本  
- [Streamlit](https://streamlit.io/)  
- [Whisper](https://github.com/openai/whisper)  
- Microsoft Edge TTS 支持  
- 其他依赖库（如 `requests`、`pydub`、`dotenv` 等）

### 2. 克隆项目

```bash
git clone https://github.com/wallfacer-web/IELTS_Speaking.git
cd your_repository

python -m venv venv
source venv/bin/activate  # Linux / macOS
# 或
.\venv\Scripts\activate   # Windows

pip install -r requirements.txt

使用说明
启动服务

在终端中进入项目所在目录后，执行：

bash
复制代码
streamlit run your_script.py
其中 your_script.py 为包含主程序和 Streamlit 界面的脚本文件（示例中默认为 main 函数所在的脚本）。

上传音频文件

打开浏览器访问本地地址（通常是 http://localhost:8501），在页面上方点击“上传学生音频”进行文件上传。支持 mp3、m4a、wav 等格式。

音频转录

程序将自动调用 Whisper 对上传的音频进行识别转录。
转录完成后，左侧区域会显示原始转录文本。
文本润色

在右侧选择需要调用的 AI 模型（llama3、qwen2 或 mistral）。
点击“开始润色”后，程序将向指定的 AI 接口发送润色请求。
等待一段时间即可在界面中查看润色结果。
语音合成与播放

程序会进一步调用 Microsoft Edge TTS 服务，将润色后的文本转换成音频文件 (mp3 格式)。
在界面下方可直接在线播放生成的音频或下载音频文件。
结果输出

转录文本与润色后文本分别显示在页面的左右区域，方便对比和二次编辑。
生成的音频文件默认保存在 temp 文件夹下，便于后续在课堂或其他场景中重复使用。
代码结构
bash
复制代码
├── your_script.py           # 主程序文件，包含main函数与Streamlit界面逻辑
├── temp/                    # 用于存放转录或语音合成的临时文件
├── .env                     # 环境变量配置文件(需自行创建)
├── requirements.txt         # 依赖库列表(如需)
└── README.md                # 项目说明文档
AudioProcessor

transcribe_audio_to_text: 调用 Whisper 对音频进行转录
revise_text_with_model: 利用 AI 模型对文本进行润色
text_to_speech: 使用 Microsoft Edge TTS 将文本转换为音频
main

Streamlit 入口函数，定义页面布局、文件上传接口以及处理流程。
常见问题 (FAQ)
Whisper 未能正确转录音频

请确保已安装并正确配置 Whisper，并检查终端是否能够识别 whisper 命令。
无法连接到 AI 模型接口

检查 .env 文件中的接口地址是否与实际服务地址一致。
确保本地 API 服务已正常启动（默认地址 http://localhost:11434/api/generate）。
文本转语音失败

确认已安装并启用 Microsoft Edge TTS 功能，并在网络环境中能够访问相应服务。
检查程序中选择的语音类型 en-US-BrianMultilingualNeural 是否可用。
生成的音频无法播放或速度过慢

确保浏览器对 MP3 音频格式兼容，或者在播放器设置中启用自动播放功能。
版权与许可
本项目由 Toby 于 2024.6 设计和开发。
本项目仅供学习与研究使用，如需在商业环境中应用，请先征得作者同意并注明来源。
项目地址：
GitHub - wallfacer-web/TobyLuoPeng
