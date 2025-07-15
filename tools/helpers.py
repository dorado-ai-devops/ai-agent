# helpers.py

import os
import subprocess
import shutil

def fetch_helm_chart_helper(query: str, branch: str = "main") -> str:
    repo_url = "git@github.com:dorado-ai-devops/devops-ai-lab.git"
    tmp_dir = "/app/tmp_clone"
    charts_out = "/app/tmp_charts"
    charts_dir = os.path.join(tmp_dir, "manifests")
    os.makedirs(charts_out, exist_ok=True)

    if os.path.exists(tmp_dir):
        shutil.rmtree(tmp_dir)
    try:
        env = os.environ.copy()
        env["GIT_SSH_COMMAND"] = "ssh -i /root/.ssh/id_ed25519 -o UserKnownHostsFile=/root/.ssh/known_hosts"
        subprocess.check_call([
            "git", "clone", "--depth=1", "--branch", branch, repo_url, tmp_dir
        ], env=env)

        candidates = [
            d for d in os.listdir(charts_dir)
            if d.startswith("helm-") and query.lower() in d.lower()
        ]
        if not candidates:
            charts = [d for d in os.listdir(charts_dir) if d.startswith("helm-")]
            return f"No encontrado ningún chart que contenga '{query}'. Disponibles: {', '.join(charts)}"
        if len(candidates) > 1:
            return f"Ambiguo: múltiples charts para '{query}': {', '.join(candidates)}. Especifica mejor."
        chart_dir = os.path.join(charts_dir, candidates[0])
        dest_base = os.path.join(charts_out, candidates[0])
        shutil.make_archive(dest_base, 'gztar', chart_dir)
        final_path = dest_base + ".tar.gz"
        if not os.path.exists(final_path):
            return f"Fallo al comprimir el chart en {final_path}."
        return f"Chart '{candidates[0]}' comprimido en: {final_path}"
    except subprocess.CalledProcessError as e:
        return f"Error git: {e}"
    except Exception as e:
        return f"Error general: {e}"
    finally:
        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir)
