from langchain_core.tools import tool
import requests

@tool
def list_github_repos() -> list:
    """Lista repositorios públicos de la organización dorado-ai-devops."""
    url = f"https://api.github.com/users/dorado-ai-devops/repos"
    response = requests.get(url)
    if response.status_code != 200:
        return f"Error al obtener repositorios: {response.status_code}"
    return [repo["name"] for repo in response.json()]
