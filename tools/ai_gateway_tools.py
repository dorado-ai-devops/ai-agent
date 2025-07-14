from langchain_core.tools import tool
from pydantic import BaseModel, Field
import aiohttp
import logging

GATEWAY_URL = "http://ai-gateway-service.devops-ai.svc.cluster.local:5002"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# --- TOOL 1: generate-pipeline ---
class GeneratePipelineInput(BaseModel):
    description: str = Field(..., description="Breve descripción del pipeline")


@tool("generate_pipeline")
async def generate_pipeline_tool(input: GeneratePipelineInput) -> str:
    """Genera un Jenkinsfile a partir de una descripción usando el microservicio de IA."""
    logging.info(f"[TOOL CALL] Tool=generate_pipeline input={input}")
    payload = {
        "description": input.description,
        "mode": "ollama"
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{GATEWAY_URL}/generate-pipeline", json=payload) as resp:
                result = await resp.text()
        logging.info(f"[TOOL RESULT] Tool=generate_pipeline output={result}")
        return result
    except Exception as e:
        logging.error(f"[TOOL ERROR] Tool=generate_pipeline {e}")
        raise
# --- TOOL 2: analyze-log ---
class AnalyzeLogInput(BaseModel):
    log: str = Field(..., description="Contenido completo del log")


@tool("analyze_log")
async def analyze_log_tool(input: AnalyzeLogInput) -> str:
    """Analiza un log de Jenkins y devuelve un diagnóstico generado por IA."""
    payload = {
        "log": input.log,
        "mode": "ollama"  # <-- Siempre fijo
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{GATEWAY_URL}/analyze-log", json=payload) as resp:
            return await resp.text()

# --- TOOL 3: lint-chart ---
class LintChartInput(BaseModel):
    chart_path: str = Field(..., description="Ruta local al .tgz del Helm Chart")
    chart_name: str = "unknown"

@tool("lint_chart")
async def lint_chart_tool(input: LintChartInput) -> str:
    """Realiza linting de un Helm Chart .tgz usando el microservicio de IA."""
    data = aiohttp.FormData()
    data.add_field("chart", open(input.chart_path, "rb"), filename=input.chart_path, content_type='application/gzip')
    data.add_field("mode", "ollama")  # <-- Siempre fijo
    data.add_field("chart_name", input.chart_name)
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{GATEWAY_URL}/lint-chart", data=data) as resp:
            return await resp.text()
