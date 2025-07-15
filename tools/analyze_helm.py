from langchain_core.tools import tool
import os
import logging
from .helpers import fetch_helm_chart_helper
from .ai_gateway_tools import lint_chart_tool
from tools.ai_gateway_tools import LintChartInput

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

@tool("analyze_helm_chart")
async def analyze_helm_chart(query: str, branch: str = "main") -> str:
    """
    Descarga y comprime un Helm Chart del repo, y ejecuta el lint automáticamente.
    Describe el chart a analizar (ej: 'dorado-ai-devops/ai-agent') y la rama (default: 'main').
    Retorna el resultado del fetch y el lint.
    Si el chart no se encuentra o hay un error al comprimir, retorna un mensaje de error.
    Si hay múltiples charts que coinciden, solicita especificar mejor el nombre.
    Si el chart se encuentra, lo comprime y ejecuta el lint.
    Ejemplo de uso:
    analyze_helm_chart("dorado-ai-devops/ai-agent", "main")     
    """
    logging.info(f"[TOOL CALL] analyze_helm_chart query={query} branch={branch}")
    fetch_result = fetch_helm_chart_helper(query, branch)

    if "comprimido en:" not in fetch_result:
        logging.error(f"[TOOL ERROR] Chart no encontrado o fallo al comprimir: {fetch_result}")
        return f"[ERROR] {fetch_result}"

    try:
        chart_path = fetch_result.split("comprimido en:")[-1].strip().replace("'", "")
        chart_name = os.path.basename(chart_path).replace(".tar.gz", "")

 
        lint_result = await lint_chart_tool.ainvoke({
            "input": {"chart_path": chart_path, "chart_name": chart_name}
        })

        logging.info(f"[TOOL RESULT] Lint completado para {chart_name}: {lint_result}")
        return (
            f"[FETCH RESULT]\n{fetch_result}\n\n"
            f"[LINT RESULT]\n{lint_result}"
        )
    except Exception as e:
        logging.error(f"[TOOL ERROR] analyze_helm_chart: {e}")
        return f"[ERROR] analyze_helm_chart: {e}"
