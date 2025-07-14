from langchain_core.tools import tool
from pydantic import BaseModel, Field, field_validator
import aiohttp

GATEWAY_URL = "http://ai-gateway-service.devops-ai.svc.cluster.local:5002"
VALID_MODES = {"openai", "ollama"}

# --- TOOL 1: generate-pipeline ---
class GeneratePipelineInput(BaseModel):
    description: str = Field(..., description="Breve descripción del pipeline")
    mode: str = Field("ollama", description="Motor de IA: openai u ollama")

    @field_validator("mode")
    @classmethod
    def validate_mode(cls, v):
        if v not in VALID_MODES:
            raise ValueError(f"Mode '{v}' no válido. Usa 'openai' u 'ollama'")
        return v

@tool("generate_pipeline")
async def generate_pipeline_tool(input: GeneratePipelineInput) -> str:
    """Genera un Jenkinsfile a partir de una descripción usando el microservicio de IA."""
    payload = {
        "description": input.description,
        "mode": input.mode
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{GATEWAY_URL}/generate-pipeline", json=payload) as resp:
            return await resp.text()

# --- TOOL 2: analyze-log ---
class AnalyzeLogInput(BaseModel):
    log: str = Field(..., description="Contenido completo del log")
    mode: str = Field("ollama", description="Motor de IA: openai u ollama")

    @field_validator("mode")
    @classmethod
    def validate_mode(cls, v):
        if v not in VALID_MODES:
            raise ValueError(f"Mode '{v}' no válido. Usa 'openai' u 'ollama'")
        return v

@tool("analyze_log")
async def analyze_log_tool(input: AnalyzeLogInput) -> str:
    """Analiza un log de Jenkins y devuelve un diagnóstico generado por IA."""
    payload = {
        "log": input.log,
        "mode": input.mode
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{GATEWAY_URL}/analyze-log", json=payload) as resp:
            return await resp.text()

# --- TOOL 3: lint-chart ---
class LintChartInput(BaseModel):
    chart_path: str = Field(..., description="Ruta local al .tgz del Helm Chart")
    mode: str = Field("ollama", description="Motor de IA: openai u ollama")
    chart_name: str = "unknown"

    @field_validator("mode")
    @classmethod
    def validate_mode(cls, v):
        if v not in VALID_MODES:
            raise ValueError(f"Mode '{v}' no válido. Usa 'openai' u 'ollama'")
        return v

@tool("lint_chart")
async def lint_chart_tool(input: LintChartInput) -> str:
    """Realiza linting de un Helm Chart .tgz usando el microservicio de IA."""
    data = aiohttp.FormData()
    data.add_field("chart", open(input.chart_path, "rb"), filename=input.chart_path, content_type='application/gzip')
    data.add_field("mode", input.mode)
    data.add_field("chart_name", input.chart_name)
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{GATEWAY_URL}/lint-chart", data=data) as resp:
            return await resp.text()
