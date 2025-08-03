import os 
from uuid import uuid4
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import START , END, StateGraph
from langchain_core.messages import BaseMessage, HumanMessage
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


# thread_id = uuid4().hex
# chatbot.invoke({"messages" : [HumanMessage(content="Hello, my name is Waleed?") ]}, config = config)

# while True:
#     user_input = input("You: ")
#     if user_input.strip().lower() in { "exit" , "quit", "end" }:
#         break
#     response = chatbot.invoke({"messages" : [HumanMessage(content=user_input)]}, config = config)
#     print(f"Chatbot: {response['messages'][-1].content}")
