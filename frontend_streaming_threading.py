import streamlit as st
import os
from uuid import uuid4
from langgraph_chatbot import chatbot, HumanMessage
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Chatbot UI", page_icon="💬", layout="wide")

# --- Utility functions ---
def generate_thread_id() -> str:
    return str(uuid4())

def load_thread(thread_id: str):
    st.session_state.active_thread_id = thread_id

def load_messages(thread_id: str):
    messages = []
    for msg in chatbot.get_state(config={"configurable": {"thread_id": thread_id}}).values.get("messages", []):
        role = "assistant"
        if isinstance(msg, HumanMessage):
            role = "user"
        messages.append({
            "role": role,
            "content": msg.content
        })
    return messages

def handle_new_chat():
    thread_id = generate_thread_id()
    st.session_state.active_thread_id = thread_id
    st.session_state.messages[thread_id] = []
    st.session_state.titles[thread_id] = f"Chat {len(st.session_state.thread_ids) + 1}"
    st.session_state.thread_ids.append(thread_id)

# --- Session state setup ---
if "titles" not in st.session_state:
    st.session_state.titles = {}
if "messages" not in st.session_state:
    st.session_state.messages = {}
if "thread_ids" not in st.session_state:
    new_id = generate_thread_id()
    st.session_state.active_thread_id = new_id
    st.session_state.thread_ids = [new_id]
    st.session_state.titles[new_id] = "Chat 1"
    st.session_state.messages[new_id] = []
if "active_thread_id" not in st.session_state:
    st.session_state.active_thread_id = st.session_state.thread_ids[0]

active_thread_id = st.session_state.active_thread_id

# --- Sidebar ---
with st.sidebar:
    st.markdown("## 💬 Chatbot")
    st.button("➕ New Chat", use_container_width=True, on_click=handle_new_chat)
    st.markdown("### 🕘 Conversation History")
    for thread_id in st.session_state.get("thread_ids", [])[::-1]:
        label = st.session_state.titles[thread_id]
        if thread_id == active_thread_id:
            st.markdown(f"✅ **{label}**")
        else:
            st.button(label, key=thread_id, on_click=lambda t=thread_id: load_thread(t))

    st.markdown("---")
    st.markdown("### ❓ Quick Topics")
    st.markdown("- Account Issues\n- Payment Info\n- Product Help\n- Language Settings")

    st.markdown("### ⚙️ Settings")
    st.selectbox("Language", ["English", "Urdu", "Arabic"], index=0)
    st.checkbox("🔔 Notifications", value=True)

# --- Chat Window Style ---
st.markdown("""
<style>
.chat-container {
    max-width: 900px;
    margin: auto;
}
.chat-bubble {
    padding: 0.8rem 1rem;
    border-radius: 1rem;
    margin-bottom: 1rem;
    max-width: 75%;
    word-wrap: break-word;
}
.user-bubble {
    background-color: #DCF8C6;
    align-self: flex-end;
    text-align: right;
    margin-left: auto;
}
.bot-bubble {
    background-color: #F1F0F0;
    align-self: flex-start;
    text-align: left;
    margin-right: auto;
}
.avatar {
    width: 30px;
    height: 30px;
    border-radius: 50%;
    vertical-align: middle;
    margin-right: 10px;
}
.chat-row {
    display: flex;
    align-items: flex-start;
    margin-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)


for msg in load_messages(active_thread_id):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# --- Chat Input Section ---
user_input = st.chat_input("💬 Type your message here...")

if user_input:
    st.session_state.messages[active_thread_id].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    CONFIG = {"configurable": {"thread_id": active_thread_id}}

    with st.chat_message("assistant"):
        response_container = st.empty()
        full_response = ""
        for chunk, metadata in chatbot.stream(
            {"messages": [HumanMessage(content=user_input)]},
            config=CONFIG,
            stream_mode="messages"
        ):
            content = chunk.content
            full_response += content
            response_container.markdown(full_response + "▌")

        response_container.markdown(full_response)

    st.session_state.messages[active_thread_id].append({
        "role": "assistant",
        "content": full_response
    })
