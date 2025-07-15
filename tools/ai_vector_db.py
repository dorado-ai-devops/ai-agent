from langchain_core.tools import tool
import requests
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

@tool("query_vector_db")
def query_vector_db(query: str) -> str:
    """
    Realiza una búsqueda semántica en ai-vector-db y devuelve resultados relevantes.
    query: consulta en lenguaje natural para recuperar contexto semántico
    """
    url = "http://ai-vector-bd.devops-ai.svc.cluster.local:8888/query"
    logging.info(f"[TOOL CALL] Tool=query_vector_db url={url} query={query}")
    try:
        resp = requests.post(url, json={"query": query})
        if resp.status_code != 200:
            msg = f"No se pudo realizar búsqueda en vector-db: {resp.status_code}"
            logging.error(f"[TOOL ERROR] {msg}")
            return msg

        content = resp.json()

        formatted_content = "\n".join([item['text'] for item in content.get('results', [])])

        max_chars = 4000
        if len(formatted_content) > max_chars:
            formatted_content = formatted_content[:max_chars] + "\n\n[Resultados truncados]"

        logging.info(f"[TOOL RESULT] Resultados obtenidos ({len(formatted_content)} chars)")
        return formatted_content

    except Exception as e:
        msg = f"Error al consultar vector-db: {e}"
        logging.error(f"[TOOL ERROR] {msg}")
        return msg