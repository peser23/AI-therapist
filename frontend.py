import streamlit as st
import requests

BACKEND_url = "http://localhost:8010/ask"

st.set_page_config(page_title="AI Therapist", layout="wide")
st.title("AI Therapist")

# Initialize chat history in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Chat input
user_input = st.chat_input("What's on your mind today?")
if user_input:
    # Append user message
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    # AI Agent exists here
    response = requests.post(BACKEND_url, json={"message": user_input})
    st.session_state.chat_history.append({"role": "assistant", "content": response.json()})

for msg in st.session_state.chat_history:
     with st.chat_message(msg["role"]):
        st.write(msg["content"])