# ai_gateway_tools.py

from langchain_core.tools import tool
from pydantic import BaseModel, Field
import aiohttp

GATEWAY_URL = "http://ai-gateway-service.devops-ai.svc.cluster.local:5002"

# --- TOOL 1: generate-pipeline ---
class GeneratePipelineInput(BaseModel):
    description: str = Field(..., description="Breve descripción del pipeline")
    mode: str = Field(..., description="Motor de IA: openai u ollama")
    prompt_path: str
    response_path: str

@tool("generate_pipeline")
async def generate_pipeline_tool(input: GeneratePipelineInput) -> str:
    """Genera un Jenkinsfile a partir de una descripción usando el microservicio de IA."""
    payload = {
        "description": input.description,
        "mode": input.mode,
        "prompt_path": input.prompt_path,
        "response_path": input.response_path
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{GATEWAY_URL}/generate-pipeline", json=payload) as resp:
            return await resp.text()

# --- TOOL 2: analyze-log ---
class AnalyzeLogInput(BaseModel):
    log: str = Field(..., description="Contenido completo del log")
    mode: str
    prompt_path: str
    response_path: str

@tool("analyze_log")
async def analyze_log_tool(input: AnalyzeLogInput) -> str:
    """Analiza un log de Jenkins y devuelve un diagnóstico generado por IA."""
    payload = {
        "log": input.log,
        "mode": input.mode,
        "prompt_path": input.prompt_path,
        "response_path": input.response_path
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{GATEWAY_URL}/analyze-log", json=payload) as resp:
            return await resp.text()

# --- TOOL 3: lint-chart ---
class LintChartInput(BaseModel):
    chart_path: str = Field(..., description="Ruta local al .tgz del Helm Chart")
    mode: str
    openai_api_key: str | None = None  # Solo si usas OpenAI

@tool("lint_chart")
async def lint_chart_tool(input: LintChartInput) -> str:
    """Realiza linting de un Helm Chart .tgz usando el microservicio de IA."""
    data = aiohttp.FormData()
    data.add_field("chart", open(input.chart_path, "rb"), filename=input.chart_path, content_type='application/gzip')
    data.add_field("mode", input.mode)

    headers = {}
    if input.mode == "openai" and input.openai_api_key:
        headers["Authorization"] = f"Bearer {input.openai_api_key}"

    async with aiohttp.ClientSession() as session:
        async with session.post(f"{GATEWAY_URL}/lint-chart", data=data, headers=headers) as resp:
            return await resp.text()
