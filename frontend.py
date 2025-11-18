import streamlit as st

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
    fixed_dummy_response = "What Would you like to talk about?"
    st.session_state.chat_history.append({"role": "assistant", "content": fixed_dummy_response})

for msg in st.session_state.chat_history:
     with st.chat_message(msg["role"]):
        st.write(msg["content"])