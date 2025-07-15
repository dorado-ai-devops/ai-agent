from langchain_core.tools import tool
import os
import subprocess
import shutil
import logging
from .ai_gateway_tools import lint_chart_tool
from .download_chart_tool import fetch_helm_chart
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

@tool("analyze_helm_chart")
def analyze_helm_chart(query: str, branch: str = "main") -> str:
    """
    Descarga y comprime un Helm Chart del repo, y ejecuta el lint automáticamente.
    query: nombre, fragmento o descripción parcial del chart.
    branch: rama del repo.
    """
    # Paso 1: Descarga el chart (reusa tu tool)
    fetch_result = fetch_helm_chart(query, branch)

    # Maneja errores de fetch
    if "comprimido en:" not in fetch_result:
        return f"[ERROR] {fetch_result}"

    try:
        # Extrae la ruta del archivo comprimido
        chart_path = fetch_result.split("comprimido en:")[-1].strip().replace("'", "")
        chart_name = os.path.basename(chart_path).replace(".tar.gz", "")

        # Paso 2: Lint chart (ajusta args si tu lint_chart_tool los requiere distinto)
        lint_result = lint_chart_tool(chart_path, chart_name)
        # Si lint_chart_tool es async, deberías adaptarlo (o usar run_in_executor)
        result = (
            f"[FETCH RESULT]\n{fetch_result}\n\n"
            f"[LINT RESULT]\n{lint_result}"
        )
        return result

    except Exception as e:
        logging.error(f"[TOOL ERROR] analyze_helm_chart: {e}")
        return f"[ERROR] analyze_helm_chart: {e}"

