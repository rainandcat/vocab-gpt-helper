import streamlit as st
import os
from openai import OpenAI
import json
from dotenv import load_dotenv

# 載入 API 金鑰
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

system_prompt = """
You are a friendly and professional English vocabulary tutor.
Your job is to explain any English word the user inputs.
Always respond in this structured JSON format:
{
    "word": "<input word>",
    "part_of_speech": "",
    "chinese_meaning": "",
    "example_sentence": "",
    "sentence_translation": "",
    "collocations": [""]
}
Do not add any comments or explanations outside the JSON format.
"""

def get_vocab_response(word: str) -> str:
    response = client.chat.completions.create(
                    model="gpt-4.1",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f'Word: "{word}"'}],
                    max_tokens=200,
                    temperature=0.5
                )
    return response.choices[0].text.strip()
