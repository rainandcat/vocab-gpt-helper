import streamlit as st
from vocab_helper import get_vocab_response
import json

st.set_page_config(page_title="Vocabulary Assistant")

st.title("Vocabulary Assistant")
st.markdown("Enter an English word to get its meaning, example, and usage.")

word = st.text_input("Word", "")

if st.button("🔍 Lookup"):
    if not word.strip():
        st.warning("Please enter a word.")
    else:
        try:
            with st.spinner("Thinking..."):
                response_text = get_vocab_response(word)
                result = json.loads(response_text)
                st.success("Here's what I found:")
                st.json(result)
        except json.JSONDecodeError:
            st.error("The response format was incorrect. Please try again.")
        except Exception as e:
            st.error(f"An error occurred: {e}")
