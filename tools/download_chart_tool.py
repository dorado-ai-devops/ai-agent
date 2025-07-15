from langchain_core.tools import tool
import requests
import os

@tool
def download_helm_chart(repo_url: str, chart_path: str, save_as: str) -> str:
    """
    Descarga un archivo .tgz de Helm Chart desde GitHub.

    repo_url: URL sin `.git` (ej: https://github.com/user/repo)
    chart_path: ruta dentro del repo (ej: charts/helm-log-analyzer-0.1.5.tgz)
    save_as: nombre para guardar el archivo localmente
    """
    download_url = f"{repo_url}/raw/main/{chart_path}"
    local_path = f"/app/tmp_charts/{save_as}"
    os.makedirs("/app/tmp_charts", exist_ok=True)
    
    r = requests.get(download_url)
    if r.status_code != 200:
        return f"Error al descargar el archivo: {r.status_code}"
    
    with open(local_path, "wb") as f:
        f.write(r.content)
    return f"Chart descargado correctamente: {local_path}"
