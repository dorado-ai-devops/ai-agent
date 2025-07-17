from fastapi import FastAPI, Request
import asyncio
import uvicorn
from langchain.agents import initialize_agent, AgentType
from llm_provider import get_llm
from langchain.memory import ConversationBufferWindowMemory
from tools import tools
from langchain_openai import ChatOpenAI
import os

ssh_dir = "/app/.ssh"
os.makedirs(ssh_dir, exist_ok=True)


if not os.path.exists(f"{ssh_dir}/id_ed25519") and os.environ.get("GH_SECRET"):
    with open(f"{ssh_dir}/id_ed25519", "w") as f:
        f.write(os.environ["GH_SECRET"])
    os.chmod(f"{ssh_dir}/id_ed25519", 0o600)

app = FastAPI()

llm = get_llm()

memory = ConversationBufferWindowMemory(k=5, return_messages=True)
# Agente global
if isinstance(llm, ChatOpenAI):
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        memory=memory,
        agent=AgentType.OPENAI_FUNCTIONS,  
        verbose=True,
        max_iterations=3
    )
else:
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        memory=memory,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,  
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
        print(result)
        if "intermediate_steps" in result and result["intermediate_steps"]:
            action, last_tool_result = result["intermediate_steps"][-1]

            # Lógica explícita según nombre de la herramienta usada:
            if action.tool == "query_vector_db":
                context_prompt = (
                    f"Utiliza el siguiente contexto para responder a la pregunta del usuario.\n\n"
                    f"Contexto:\n{last_tool_result}\n\n"
                    f"Pregunta del usuario:\n{prompt}\n\n"
                    f"Respuesta:"
                )
                explanation = await llm.ainvoke(context_prompt)
                print(explanation)
                return {"result": explanation.content if hasattr(explanation, "content") else explanation}

            elif action.tool == "list_repositories":
                expl_prompt = (
                    "Esta es la lista de repositorios públicos del proyecto dorado-ai-devops:\n\n"
                    + "\n".join(f"- {r}" for r in last_tool_result)
                    + "\n\nResume brevemente para un usuario DevOps: ¿qué tipo de proyectos hay y para qué sirve cada uno?"
                )
                explanation = await llm.ainvoke(expl_prompt)
                print(explanation)
                return {"result": explanation.content if hasattr(explanation, "content") else explanation}

            # Caso por defecto: devolver resultado directamente
            else:
                return {"result": str(last_tool_result)}

        # Si no hay steps (solo reasoning), devuelve output
        return {"result": result.get("output", "Sin respuesta")}

    except Exception as e:
        return {"error": str(e)}



if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=6001, reload=True)
