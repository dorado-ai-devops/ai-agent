from langchain_core.tools import tool
import requests
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

@tool("get_github_r")
def get_github_r(repo: str) -> str:
    """
    Descarga y devuelve el contenido del README.md de un repositorio público.
    repo: nombre del repo (ej: 'ai-agent')
    """
    url = f"https://raw.githubusercontent.com/dorado-ai-devops/{repo}/main/README_ES.md"
    logging.info(f"[TOOL CALL] Tool=get_github_readme url={url}")
    try:
        resp = requests.get(url)
        if resp.status_code != 200:
            msg = f"No se pudo obtener README.md de {repo}: {resp.status_code}"
            logging.error(f"[TOOL ERROR] {msg}")
            return msg
        content = resp.text
       
        max_chars = 4000
        if len(content) > max_chars:
            content = content[:max_chars] + "\n\n[README truncado]"
        logging.info(f"[TOOL RESULT] README.md obtenido para {repo} ({len(content)} chars)")
        return content
    except Exception as e:
        msg = f"Error al obtener README.md: {e}"
        logging.error(f"[TOOL ERROR] {msg}")
        return msg
