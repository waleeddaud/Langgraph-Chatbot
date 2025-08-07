import streamlit as st
import os , time
from uuid import uuid4
from langgraph_chatbot import chatbot, HumanMessage
from dotenv import load_dotenv
load_dotenv()

def load_thread(thread_id: str):
    st.session_state.update({"active_thread_id":thread_id })
    

def load_messages(thread_id : str):
    my_lst= []
    for msg in chatbot.get_state(config={"configurable" : {"thread_id" : thread_id}}).values.get("messages", []):
        role= "assistant"
        if isinstance(msg, HumanMessage):
            role ="user"
        my_lst.append({"role": role, "content": msg.content})
    return my_lst

def generate_thread_id() -> str:
    """Generate a unique thread ID."""
    return str(uuid4())
def handle_new_chat():
    """Handle the creation of a new chat thread."""
    st.session_state.active_thread_id = generate_thread_id()
    st.session_state.messages[st.session_state.active_thread_id] = []
    st.session_state.thread_ids.append(st.session_state.active_thread_id)
    st.session_state.titles[st.session_state.active_thread_id] = "Untitled Chat"



st.set_page_config(page_title="Streaming output Chatbot", page_icon="💬")

st.title("Chatbot UI")
if "titles" not in st.session_state:
    st.session_state.titles = {}
if "messages" not in st.session_state:
    # Now what is want is Dict [str, list[]]
    st.session_state.messages = {}
# in our session state there will be active thread_id and list of thread_ids , if there is no by default create one
if "active_thread_id" not in st.session_state:
    st.session_state.active_thread_id = generate_thread_id()
    active_thread = st.session_state.active_thread_id
    st.session_state.titles[active_thread] = "Untitled Chat"
    st.session_state.thread_ids = [active_thread]
    st.session_state.messages[active_thread] = []


active_thread_id = st.session_state.active_thread_id

with st.sidebar:
    st.title("All Conversations")
    st.button("New Chat", on_click=handle_new_chat)

    st.header("My Coversations")
    for thread_id in st.session_state.get("thread_ids", [])[::-1]:
        st.button(st.session_state.titles[thread_id],key=f"button_{thread_id}",  on_click=lambda t=thread_id:load_thread(t))


# # Display chat history
for message in load_messages(active_thread_id):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
# for message in st.session_state.messages[active_thread_id]:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])


# User input
user_input = st.chat_input("Say something...")

if user_input:
    # Add user message to chat history
    st.session_state.messages[active_thread_id].append({"role": "user", "content": user_input})
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)
    
    CONFIG = {"configurable" : {"thread_id" : st.session_state.active_thread_id}}
   
    

    # Add bot message to chat history
    with st.chat_message("assistant"):
        bot_response = st.write_stream(
            message_chunk.content for message_chunk, metadata in chatbot.stream(
                {"messages": [HumanMessage(content=user_input)]},
                config=CONFIG,
                stream_mode="messages"  
            )
        )
    st.session_state.messages[active_thread_id].append({"role": "assistant", "content": bot_response})
    
    
