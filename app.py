import subprocess
import requests
import edge_tts
import asyncio
import os
from pydub import AudioSegment
import streamlit as st
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class AudioProcessor:
    def __init__(self):
        self.output_dir = "temp"
        os.makedirs(self.output_dir, exist_ok=True)

    def transcribe_audio_to_text(self, audio_path):
        """将音频转换为文本"""
        try:
            result = subprocess.run(
                ['whisper', audio_path, '--output_dir', self.output_dir], 
                capture_output=True, 
                text=True
            )
            if result.returncode != 0:
                st.error(f"转录错误: {result.stderr}")
                return None

            base_name = os.path.splitext(os.path.basename(audio_path))[0]
            text_path = os.path.join(self.output_dir, f"{base_name}.txt")

            if not os.path.isfile(text_path):
                st.error(f"转录失败: 未找到文本文件 {text_path}")
                return None

            with open(text_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            st.error(f"转录失败: {e}")
            return None

    def revise_text_with_model(self, text, model_name):
        """使用AI模型润色文本"""
        url = "http://localhost:11434/api/generate"
        headers = {"Content-Type": "application/json"}
        prompt = (
            "请使用英语修改和润色下面的雅思口语文本，使其用词和句式多样化，"
            "结构完整，补充更多细节，生动一些，符合口语特征，400字左右。\n\n{text}"
        )
        
        data = {
            "model": model_name,
            "prompt": prompt.format(text=text),
            "stream": False
        }

        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            
            response_json = response.json()
            revised_text = response_json.get("response")
            if revised_text.startswith("Here's"):
                revised_text = revised_text.split(':', 1)[1].strip()
            return revised_text
            
        except requests.exceptions.HTTPError as http_err:
            st.error(f"HTTP错误: {http_err}")
        except Exception as err:
            st.error(f"其他错误: {err}")
        return None

    async def text_to_speech(self, text, output_audio_path):
        """将文本转换为语音"""
        try:
            communicate = edge_tts.Communicate(
                text=text,
                voice='en-US-BrianMultilingualNeural',
                rate='-4%',
                volume='+20%'
            )
            await communicate.save(output_audio_path)
            return True
        except Exception as e:
            st.error(f"文本转语音错误: {e}")
            return False

def main():
    st.set_page_config(
        page_title="口语润色助手",
        page_icon="🎯",
        layout="wide"
    )
    
    st.title("🎯 口语润色助手")
    
    processor = AudioProcessor()

    # 文件上传部分
    uploaded_file = st.file_uploader("上传学生音频", type=["mp3", "m4a", "wav"])
    
    if uploaded_file is not None:
        # 保存上传的音频文件
        audio_path = os.path.join("temp", uploaded_file.name)
        with open(audio_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # 转录音频
        original_text = processor.transcribe_audio_to_text(audio_path)
        
        if original_text:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📝 原始转录文本")
                st.text_area("原始文本", original_text, height=200)

            with col2:
                st.subheader("🤖 AI润色设置")
                model_choice = st.selectbox(
                    "选择模型",
                    ["llama3", "qwen2", "mistral"],
                    help="选择用于文本润色的AI模型"
                )

                if st.button("开始润色", type="primary"):
                    with st.spinner("正在润色中..."):
                        revised_text = processor.revise_text_with_model(original_text, model_choice)
                        
                        if revised_text:
                            st.subheader("✨ 润色后的文本")
                            st.text_area("润色文本", revised_text, height=200)

                            # 生成音频
                            output_audio_path = os.path.join(processor.output_dir, f"revised_{model_choice}.mp3")
                            if asyncio.run(processor.text_to_speech(revised_text, output_audio_path)):
                                st.subheader("🎧 生成的音频")
                                audio_file = open(output_audio_path, 'rb')
                                audio_bytes = audio_file.read()
                                st.audio(audio_bytes, format='audio/mp3')
                                st.success("✅ 文本润色和音频生成完成！")

    # 页脚信息
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center;'>"
        "Designed by Toby @2024.6 | "
        "<a href='https://github.com/wallfacer-web/TobyLuoPeng'>GitHub</a>"
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main() 