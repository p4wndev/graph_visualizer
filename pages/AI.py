import streamlit as st
import google.generativeai as genai
import time
import random

st.set_page_config(layout="centered",
                   page_title="GraphCoach",
                   page_icon="🤖",
                   initial_sidebar_state="expanded")

st.title("Graph:violet[Coach] 🤖")
st.caption("Được hỗ trợ bởi :violet[Gemini]")

if "history" not in st.session_state:
    st.session_state.history = []

genai.configure(api_key="AIzaSyBkrqxHG2q0vyF1TdFLrpdJOnBEiZbAxxk")
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=st.session_state.history)

with st.sidebar:
    if st.button("Cuộc hội thoại mới", use_container_width=True, type="primary"):
        st.session_state.history = []
        st.rerun()

for message in chat.history:
    role = "assistant" if message.role == 'model' else message.role
    with st.chat_message(role):
        st.markdown(message.parts[0].text)


if prompt := st.chat_input(""):
    prompt = prompt.replace('\n', ' \n')
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Suy nghĩ...")
        try:
            full_response = ""
            prompt = f"Hãy trong vai một giảng viên dạy về Lý thuyết đồ thị và trả lời câu hỏi sau đây thật rõ ràng và dễ hiểu: {prompt}"
            for chunk in chat.send_message(prompt, stream=True):
                word_count = 0
                random_int = random.randint(5, 10)
                for word in chunk.text:
                    full_response += word
                    word_count += 1
                    if word_count == random_int:
                        time.sleep(0.05)
                        message_placeholder.markdown(full_response + "_")
                        word_count = 0
                        random_int = random.randint(5, 10)
            message_placeholder.markdown(full_response)
        except genai.types.generation_types.BlockedPromptException as e:
            st.exception(e)
        except Exception as e:
            st.exception(e)
        st.session_state.history = chat.history
st.sidebar.caption(
    "Gemini có thể đưa ra thông tin không chính xác, kể cả thông tin về con người, vì vậy, hãy xác minh các câu trả lời của Gemini.")
