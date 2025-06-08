# Q&A Chatbot with Open-Source Models

This chatbot supports multiple open-source LLMs (Mistral, LLaMA 3, Gemma, CodeLlama, Phi) with conversation memory.

## Features
- Multi-model support
- Conversational history
- Local inference via Ollama
- Streamlit UI for easy interaction

## Requirements
- Python 3.10
- Ollama installed and running

## Setup
bash
pip install -r requirements.txt
streamlit run app.py

##Models
ollama pull mistral
ollama pull llama3
ollama pull gemma
ollama pull codellama
ollama pull phi
