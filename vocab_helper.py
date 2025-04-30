import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv

# 載入 API 金鑰
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Streamlit UI
st.set_page_config(page_title="Vocabulary Assistant", page_icon="📘")
st.title("📘 Vocabulary Assistant")
st.markdown("輸入一個英文單字，讓 AI 幫你解釋、例句與中文翻譯")

# 使用者輸入
word = st.text_input("請輸入英文單字", "")

# 選擇模型
model = st.selectbox("選擇 GPT 模型", ["gpt-4.1", "gpt-3.5-turbo"])

# 查詢按鈕
if st.button("查詢單字") and word.strip():
    with st.spinner("請稍候，正在請求 GPT 回覆..."):
        prompt = f"""
你是一位英文學習助理，請幫我解釋單字：「{word}」，以以下格式回覆：

- 詞性：
- 中文意思：
- 英文例句：
- 中文翻譯：
- 常見搭配詞（collocations）：
"""

        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            reply = response.choices[0].message.content.strip()
            st.success("GPT 回覆內容如下：")
            st.markdown(reply.replace("\n", "  \n"))
        except Exception as e:
            st.error(f"發生錯誤：{str(e)}")
else:
    st.info("請輸入一個英文單字後按下『查詢單字』")
