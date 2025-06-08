import streamlit as st
import os
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

load_dotenv()

# Optional: LangSmith tracking
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "Simple Q&A Chatbot With Ollama"

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "system", "content": "You are a helpful assistant. Please respond to the user queries."}
    ]

# App Title
st.title("Enhanced Q&A Chatbot With Open Source Models")

# Sidebar controls
llm_model = st.sidebar.selectbox("Select Open Source model", ["mistral", "llama3", "gemma", "codellama", "phi"])
temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.7)
max_tokens = st.sidebar.slider("Max Tokens", 50, 300, 150)

st.write("Go ahead and ask any question")
user_input = st.text_input("You:")

# Max number of messages to retain in history (4 rounds of user-assistant)
MAX_HISTORY_LEN = 8

# Convert plain dict chat history to LangChain message objects
def format_history(history):
    messages = []
    for msg in history:
        if msg["role"] == "system":
            messages.append(SystemMessage(content=msg["content"]))
        elif msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "assistant":
            messages.append(AIMessage(content=msg["content"]))
    return messages

# Generate response using LangChain's ChatOllama with message history
def generate_response(model_name, temperature, max_tokens):
    chat = ChatOllama(model=model_name, temperature=temperature)
    messages = format_history(st.session_state.chat_history)
    response = chat.invoke(messages)
    return response.content

if user_input:
    # Add user message
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # Trim history (keep system + last N messages)
    if len(st.session_state.chat_history) > MAX_HISTORY_LEN + 1:
        st.session_state.chat_history = [st.session_state.chat_history[0]] + st.session_state.chat_history[-MAX_HISTORY_LEN:]

    # Get bot response
    response = generate_response(llm_model, temperature, max_tokens)

    # Add assistant response
    st.session_state.chat_history.append({"role": "assistant", "content": response})

    # Trim again if needed
    if len(st.session_state.chat_history) > MAX_HISTORY_LEN + 1:
        st.session_state.chat_history = [st.session_state.chat_history[0]] + st.session_state.chat_history[-MAX_HISTORY_LEN:]

# Display chat history
for msg in st.session_state.chat_history[1:]:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    elif msg["role"] == "assistant":
        st.markdown(f"**Bot:** {msg['content']}")

# Optional: Clear chat button
if st.button("Clear Chat"):
    st.session_state.chat_history = [
        {"role": "system", "content": "You are a helpful assistant. Please respond to the user queries."}
    ]
    st.experimental_rerun()
