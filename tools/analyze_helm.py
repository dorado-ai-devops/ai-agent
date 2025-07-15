from langchain_core.tools import tool
import os
import logging
from .helpers import fetch_helm_chart_helper
from .ai_gateway_tools import lint_chart_tool

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

@tool("analyze_helm_chart")
def analyze_helm_chart(query: str, branch: str = "main") -> str:
    """
    Descarga y comprime un Helm Chart del repo, y ejecuta el lint automáticamente.
    """
    fetch_result = fetch_helm_chart_helper(query, branch)

    if "comprimido en:" not in fetch_result:
        return f"[ERROR] {fetch_result}"

    try:
        chart_path = fetch_result.split("comprimido en:")[-1].strip().replace("'", "")
        chart_name = os.path.basename(chart_path).replace(".tar.gz", "")

        # Si lint_chart_tool es async, deberías adaptarlo o llamar vía asyncio
        lint_result = lint_chart_tool(chart_path, chart_name)
        return (
            f"[FETCH RESULT]\n{fetch_result}\n\n"
            f"[LINT RESULT]\n{lint_result}"
        )
    except Exception as e:
        logging.error(f"[TOOL ERROR] analyze_helm_chart: {e}")
        return f"[ERROR] analyze_helm_chart: {e}"
