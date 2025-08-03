import streamlit as st
from langgraph_chatbot import chatbot, HumanMessage
import os , time
from dotenv import load_dotenv
load_dotenv()
thread_id = os.getenv("thread_id")
st.set_page_config(page_title="Streaming output Chatbot", page_icon="💬")

st.title("Chatbot UI")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
user_input = st.chat_input("Say something...")

if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)
    
    config = {"configurable" : {"thread_id" : thread_id}}
   
    

    # Add bot message to chat history
    with st.chat_message("assistant"):
        bot_response = st.write_stream(
            message_chunk.content for message_chunk, metadata in chatbot.stream(
                {"messages": [HumanMessage(content=user_input)]},
                config=config,
                stream_mode="messages"  
            )
        )
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
    
    
