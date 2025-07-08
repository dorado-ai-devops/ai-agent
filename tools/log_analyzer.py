from langchain.tools import Tool
from clients.gateway_client import MockGatewayClient

client = MockGatewayClient()

def analyze_log(log: str) -> str:
    return client.analyze_log(log)

log_analyzer_tool = Tool(
    name="LogAnalyzerTool",
    func=analyze_log,
    description="Diagnostica errores en logs Jenkins o Kubernetes."
)
