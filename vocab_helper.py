import streamlit as st
import os
from openai import OpenAI
import json
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
你是一位英文學習助理，請幫我解釋英文單字「{word}」，並以 JSON 格式回覆下列欄位，不要加入多餘文字：

{{
  "word": "{word}",
  "part_of_speech": "",
  "chinese_meaning": "",
  "example_sentence": "",
  "sentence_translation": "",
  "collocations": []
}}

請務必以標準 JSON 格式回覆，所有欄位都要填寫。
"""

        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
                temperature=0.7
            )
            reply = response.choices[0].text.strip()

            try:
                json_data = json.loads(reply)
                st.write(f"### {json_data['word']}")
                st.write(f"**詞性**：{json_data['part_of_speech']}")
                st.write(f"**中文意思**：{json_data['chinese_meaning']}")
                st.write(f"**英文例句**：{json_data['example_sentence']}")
                st.write(f"**中文翻譯**：{json_data['sentence_translation']}")
                st.write(f"**常見搭配詞**：{', '.join(json_data['collocations'])}")
            except Exception as e:
                st.warning("回覆無法解析為 JSON，以下為原始文字：")
                st.markdown(reply.replace("\n", "  \n"))
        except Exception as e:
            st.error(f"發生錯誤：{str(e)}")
else:
    st.info("請輸入一個英文單字後按下『查詢單字』")
