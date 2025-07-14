import uuid
import logging
from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI
from tools import tools
import asyncio

llm = ChatOpenAI(model="gpt-4", temperature=0)

async def main():
    run_id = str(uuid.uuid4())
    logging.info(f"[AGENT RUN START] run_id={run_id}")
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.OPENAI_FUNCTIONS,
        verbose=True,
        max_iterations=1
    )
    prompt = "Genera un pipeline básico usando ollama con la descripción: 'Construir y desplegar una aplicación web simple'."
    logging.info(f"[AGENT PROMPT] run_id={run_id} prompt={prompt}")
    try:
        result = await agent.ainvoke(prompt)
        logging.info(f"[AGENT RESULT] run_id={run_id} output={result['output']}")
        print(result["output"])
    except Exception as e:
        logging.error(f"[AGENT ERROR] run_id={run_id} {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
