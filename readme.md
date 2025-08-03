#  LangGraph Chatbot with Streamlit

A conversational AI chatbot built using [LangGraph](https://github.com/langchain-ai/langgraph) and deployed with a clean [Streamlit](https://streamlit.io/) interface. It uses Large Language Models (LLMs) to process user inputs and provide intelligent, contextual responses — suitable for educational assistance, Q&A systems, and general-purpose conversations.

---

##  Features

-  Streamlit frontend for real-time chat interaction
-  LangGraph-powered stateful conversation logic
-  LLM integration (e.g., OpenAI/Gemini)
-  Modular design — easy to extend with new nodes and workflows
-  Fast and interactive UI

---

## 🛠 Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python, LangGraph
- **AI**: Any supported LLM (OpenAI, Gemini, etc.)
- **Others**: LangChain, Tavily (optional for search)

---

##  Installation

```bash
git clone https://github.com/waleeddaud/Langgraph-Chatbot.git
cd Langgraph-Chatbot

# Create and activate virtual environment (optional)
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# For running streamlit, use command
streamlit run frontend.py


