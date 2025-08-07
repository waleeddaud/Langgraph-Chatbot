import os 
from uuid import uuid4
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import START , END, StateGraph
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import add_messages
from typing import TypedDict, Annotated, Literal

from pydantic import BaseModel , Field
import time
load_dotenv()
model = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.7)

class ChatState(TypedDict):
    messages : Annotated[list[BaseMessage],add_messages]

def chatnode(state: ChatState) :
    response = model.invoke(state["messages"])
    return {
        "messages" : [response]
    }

checkpointer = MemorySaver()
graph = StateGraph(ChatState)
graph.add_node("chatnode", chatnode)
graph.add_edge(START, "chatnode")
graph.add_edge("chatnode", END)
chatbot = graph.compile(checkpointer = checkpointer)


# # For streaming code example
# thread_id = os.getenv("thread_id")
# config = {"configurable" : {"thread_id" : thread_id}}
# for message_chunk , metadata in chatbot.stream(
#     {"messages" : [HumanMessage(content="Hello my name is Waleed")]},
#       config = config,
#      stream_mode="messages"):
#     if message_chunk.content:
#         print(message_chunk.content, end=" ", flush=True)




