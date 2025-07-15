from langchain_core.tools import tool
import requests
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

@tool("list_github_repos")
def list_github_repos() -> list:
    """Lista repositorios públicos de la organización dorado-ai-devops."""
    url = "https://api.github.com/users/dorado-ai-devops/repos"
    logging.info(f"[TOOL CALL] Tool=list_github_repos url={url}")
    try:
        response = requests.get(url)
        if response.status_code != 200:
            msg = f"Error al obtener repositorios: {response.status_code}"
            logging.error(f"[TOOL ERROR] {msg}")
            return msg
        repo_names = [repo["name"] for repo in response.json()]
        logging.info(f"[TOOL RESULT] Repos encontrados: {repo_names}")
        return repo_names
    except Exception as e:
        msg = f"Error general: {e}"
        logging.error(f"[TOOL ERROR] {msg}")
        return msg
