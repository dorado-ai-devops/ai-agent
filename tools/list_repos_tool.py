from langchain_core.tools import tool
import requests

@tool
def list_github_repos(username: str) -> list:
    """Lista repositorios públicos de un usuario u organización de GitHub."""
    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url)
    if response.status_code != 200:
        return f"Error al obtener repositorios: {response.status_code}"
    return [repo["name"] for repo in response.json()]
