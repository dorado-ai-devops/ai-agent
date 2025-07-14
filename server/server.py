from fastapi import FastAPI, Request
import asyncio
import uvicorn
from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI
from tools import tools

app = FastAPI()
llm = ChatOpenAI(model="gpt-4", temperature=0)

# Solo necesitas un agente global (thread-safe para peticiones independientes)
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True,
    max_iterations=1
)

@app.post("/ask")
async def ask(request: Request):
    data = await request.json()
    prompt = data.get("prompt")
    if not prompt:
        return {"error": "Missing prompt"}
    try:
        # El LLM decide la tool, igual que en tus pruebas sueltas
        result = await agent.ainvoke(prompt)
        return {"result": result["output"]}
    except Exception as e:
        return {"error": str(e)}

# Opcional: correr directamente con python main_api.py
if __name__ == "__main__":
    uvicorn.run("main_api:app", host="0.0.0.0", port=6001, reload=True)
