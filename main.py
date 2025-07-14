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

    # 1. Generación de pipelines
    prompt_pipeline = "Genera un pipeline de Jenkins básico usandocon la descripción: 'Construir y desplegar una aplicación web simple'. Devuelve solo el texto del Jenkinsfile."
    logging.info(f"[AGENT PROMPT] run_id={run_id} prompt={prompt_pipeline}")
    try:
        result_pipeline = await agent.ainvoke(prompt_pipeline)
        logging.info(f"[AGENT RESULT] run_id={run_id} output={result_pipeline['output']}")
        print("Pipeline output:", result_pipeline["output"])
    except Exception as e:
        logging.error(f"[AGENT ERROR pipeline] run_id={run_id} {e}")
        raise

    # 2. Análisis de logs 
    log_contenido = "[2025-07-05] ERROR: something exploded"
    prompt_logs = f"Analiza el siguiente log de Jenkins y proporciona diagnóstico y solución:\n{log_contenido}"
    logging.info(f"[AGENT PROMPT] run_id={run_id} prompt={prompt_logs}")
    try:
        result_logs = await agent.ainvoke(prompt_logs)
        logging.info(f"[AGENT RESULT] run_id={run_id} output={result_logs['output']}")
        print("Log analysis output:", result_logs["output"])
    except Exception as e:
        logging.error(f"[AGENT ERROR logs] run_id={run_id} {e}")
        raise

    # 3. Linting de Helm Chart (vía prompt natural)
    prompt_lint = (
        "Haz lint del Helm Chart comprimido que está en /app/chart_example/helm-log-analyzer-0.1.5.tgz "
        "y cuyo nombre es helm-log-analyzer."
    )
    logging.info(f"[AGENT PROMPT] run_id={run_id} prompt={prompt_lint}")
    try:
        result_lint = await agent.ainvoke(prompt_lint)
        logging.info(f"[AGENT RESULT] run_id={run_id} output={result_lint['output']}")
        print("Lint chart output:", result_lint["output"])
    except Exception as e:
        logging.error(f"[AGENT ERROR lint_chart] run_id={run_id} {e}")
        raise

    logging.info(f"[AGENT RUN END] run_id={run_id}")

if __name__ == "__main__":
    asyncio.run(main())
