# 🧠 ai-agent

AI reasoning agent built with **LangChain** + **OpenAI GPT-4**.  
Orchestrates complex DevOps tasks through LLM reasoning and modular tool calling from the `devops-ai-lab` ecosystem.

---

## 🎯 Purpose

Centralizes decision-making and DevOps automation powered by LLMs, encapsulating as **tools** the AI microservices accessible via `ai-gateway`.  
Allows unified analysis of logs, Helm chart validation, Jenkinsfile generation, and semantic vector DB querying, with full traceability via MCP messages.

This agent is the real cognitive entry point of the architecture.

---

## 🔧 Functionality

The agent exposes several **tools** that act as HTTP wrappers to AI microservices deployed in Kubernetes:

| Tool                | Endpoint Gateway     | Description                                                           |
| -------------------|----------------------|-----------------------------------------------------------------------|
| `generate_pipeline`| `/generate-pipeline` | Generates a Jenkinsfile from a natural language description           |
| `analyze_log`      | `/analyze-log`       | Diagnoses Jenkins/CI logs using LLM reasoning                         |
| `lint_chart`       | `/lint-chart`        | Semantic linting of compressed Helm Charts (.tgz)                     |
| `analyze_helm_chart` | -                  | Downloads, compresses and runs lint on remote Helm Chart             |
| `list_github_repos`| GitHub API           | Lists public repos from `dorado-ai-devops` for exploration            |
| `query_vector_db`  | `/query`             | Semantic search in `ai-vector-db` to provide enriched context         |

Each tool injects the field `caller: ai-agent-langchain` for audit traceability.

---

## ⚙️ Project Structure

```
ai-agent/
├── main.py                         # Entry point: LangChain agent orchestrating tools
├── tools/
│   ├── __init__.py
│   ├── ai_gateway_tools.py         # Tools calling HTTP endpoints
│   ├── github_tools.py             # GitHub-based tools (e.g. repo listing)
│   ├── vector_db_tool.py           # Vector DB semantic search tool
├── clients/
│   └── gateway_client.py           # (optional) HTTP helper logic
├── prompts/
│   └── examples.md
├── config/
│   └── settings.py
├── README.md
├── requirements.txt
└── Dockerfile
```

---

## 🚀 Local Execution

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

You can invoke the agent via API (`POST /ask`) or adapt the code to test tools directly.

---

## 🌐 Environment Communication

The agent talks to `ai-gateway` via internal Kubernetes service (`http://ai-gateway-service...`).  
Active endpoints:

- `POST /generate-pipeline`
- `POST /analyze-log`
- `POST /lint-chart`
- `POST /query`

All requests include the source caller and mode (default: `ollama`).

---

## 🧠 Intelligence & Models

- **Default model:** OpenAI GPT-4 (can be replaced by Mistral/Ollama or fine-tuned models).
- All backend microservices allow setting `mode=ollama | openai` dynamically.
- In the future: plug-in support for fine-tuned LLMs (e.g., FLAN-T5).

---

## 🔎 Observability & Traceability

- **Verbose logs** for each tool call, inputs, outputs, and errors (stdout).
- **MCP Protocol**: All key agent interactions are reported to `ai-gateway` with full metadata for audit.

---

## 📦 Key Dependencies

```text
langchain
openai
aiohttp
pydantic
python-dotenv
```

> Add `ollama-client` only if running locally against Ollama models.

---

## 📌 Current Status

Actively integrated in the `devops-ai-lab` as the reasoning and control plane for AI-assisted DevOps workflows.

---

## 👨‍💻 Author

**Dani**  
[github.com/dorado-ai-devops](https://github.com/dorado-ai-devops)

---

## 🛡 License

GNU General Public License v3.0