import os
import logging
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama


def get_llm():
    ai_vendor = os.environ.get("AI_VENDOR", "ollama").lower()
    llm_model = os.environ.get("LLM_MODEL", "mistral").lower()

    if ai_vendor == "ollama":
        base_url = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
        logging.info(f"[LLM] Usando Ollama – modelo: {llm_model} – URL: {base_url}")
        return ChatOllama(model=llm_model, base_url=base_url)
    else:
        llm = ChatOpenAI(model="gpt-4", temperature=0)
        logging.info(f"[LLM] Usando OpenAI – modelo: {llm_model}")
        return ChatOpenAI(model=llm_model, temperature=0)

