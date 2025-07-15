from fastapi import FastAPI, Request
import asyncio
import uvicorn
from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI
from tools import tools
import os

ssh_dir = "/app/.ssh"
os.makedirs(ssh_dir, exist_ok=True)


if not os.path.exists(f"{ssh_dir}/id_ed25519") and os.environ.get("GH_SECRET"):
    with open(f"{ssh_dir}/id_ed25519", "w") as f:
        f.write(os.environ["GH_SECRET"])
    os.chmod(f"{ssh_dir}/id_ed25519", 0o600)

app = FastAPI()
llm = ChatOpenAI(model="gpt-4", temperature=0)

# Agente global
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True,
    max_iterations=3
)

@app.post("/ask")
async def ask(request: Request):
    data = await request.json()
    prompt = data.get("prompt")
    if not prompt:
        return {"error": "Missing prompt"}
    try:
        result = await agent.ainvoke(prompt)
        # --- DEVOLVER RESPUESTA DE TOOL SI EXISTE ---
        if "intermediate_steps" in result and result["intermediate_steps"]:
            # Coge el resultado de la última tool ejecutada
            last_tool_result = result["intermediate_steps"][-1][1]
            return {"result": last_tool_result}
        # Si no hay steps (p.ej. solo reasoning), devuelve output
        return {"result": result.get("output", "Sin respuesta")}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=6001, reload=True)
