from fastapi import FastAPI, Request
import asyncio
import uvicorn
from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI
from tools import tools
import os

ssh_dir = "/app/.ssh"
os.makedirs(ssh_dir, exist_ok=True)

# Si no existe el archivo pero la clave está en env, escríbela
if not os.path.exists(f"{ssh_dir}/id_ed25519") and os.environ.get("GH_SECRET"):
    with open(f"{ssh_dir}/id_ed25519", "w") as f:
        f.write(os.environ["GH_SECRET"])
    os.chmod(f"{ssh_dir}/id_ed25519", 0o600)

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
    uvicorn.run("server:app", host="0.0.0.0", port=6001, reload=True)
