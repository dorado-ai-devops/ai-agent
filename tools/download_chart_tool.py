from langchain_core.tools import tool
import os
import subprocess
import shutil
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

@tool("fetch_helm_chart")
def fetch_helm_chart(query: str, branch: str = "main") -> str:
    """
    Busca, descarga y comprime un Helm Chart 'helm-*' de 'manifests/' en el repo dorado-ai-devops/devops-ai-lab.
    query: nombre completo, fragmento o descripción parcial (ej: 'analyzer', 'dashboard', 'helm-log-analyzer')
    branch: rama del repo (default 'main')
    """
    repo_url = "git@github.com:dorado-ai-devops/devops-ai-lab.git"
    tmp_dir = "/app/tmp_clone"
    charts_out = "/app/tmp_charts"
    charts_dir = os.path.join(tmp_dir, "manifests")
    os.makedirs(charts_out, exist_ok=True)

    # Limpieza previa
    if os.path.exists(tmp_dir):
        shutil.rmtree(tmp_dir)

    logging.info(f"[TOOL CALL] Tool=fetch_helm_chart query={query} branch={branch}")
    try:
        env = os.environ.copy()
        env["GIT_SSH_COMMAND"] = "ssh -i /root/.ssh/id_ed25519 -o UserKnownHostsFile=/root/.ssh/known_hosts"
        subprocess.check_call([
            "git", "clone", "--depth=1", "--branch", branch, repo_url, tmp_dir
        ], env=env)
        logging.info(f"[TOOL RESULT] Repo clonado en {tmp_dir}")

        # Buscar charts matching
        candidates = [
            d for d in os.listdir(charts_dir)
            if d.startswith("helm-") and query.lower() in d.lower()
        ]
        logging.info(f"[TOOL RESULT] Charts candidatos para '{query}': {candidates}")

        if not candidates:
            charts = [d for d in os.listdir(charts_dir) if d.startswith("helm-")]
            msg = f"No encontrado ningún chart que contenga '{query}'. Disponibles: {', '.join(charts)}"
            logging.warning(f"[TOOL RESULT] {msg}")
            return msg
        if len(candidates) > 1:
            msg = f"Ambiguo: múltiples charts para '{query}': {', '.join(candidates)}. Especifica mejor."
            logging.warning(f"[TOOL RESULT] {msg}")
            return msg

        chart_dir = os.path.join(charts_dir, candidates[0])
        dest_base = os.path.join(charts_out, candidates[0])
        shutil.make_archive(dest_base, 'gztar', chart_dir)
        final_path = dest_base + ".tar.gz"
        if not os.path.exists(final_path):
            msg = f"Fallo al comprimir el chart en {final_path}."
            logging.error(f"[TOOL ERROR] {msg}")
            return msg

        msg = f"Chart '{candidates[0]}' comprimido en: {final_path}"
        logging.info(f"[TOOL RESULT] {msg}")
        return msg

    except subprocess.CalledProcessError as e:
        msg = f"Error git: {e}"
        logging.error(f"[TOOL ERROR] {msg}")
        return msg
    except Exception as e:
        msg = f"Error general: {e}"
        logging.error(f"[TOOL ERROR] {msg}")
        return msg
    finally:
        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir)
        logging.info(f"[TOOL END] Limpieza de tmp_dir: {tmp_dir}")

