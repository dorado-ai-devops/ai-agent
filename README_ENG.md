# 🧠 ai-agent

AI reasoning agent built with **LangChain** + **OpenAI** (GPT-4).\
Orchestrates complex DevOps tasks using LLM-based reasoning and modular tool invocation from the `devops-ai-lab` ecosystem.

---

## 🎯 Purpose

Centralizes LLM-driven DevOps decision logic and automation by encapsulating internal AI microservices as **tools** via `ai-gateway`.\
Enables unified log analysis, Helm chart validation, and Jenkinsfile generation with advanced traceability and observability (MCP).

This agent serves as the true cognitive entry point of the architecture.

---

## 🔧 Functionality

The agent exposes several **tools** acting as HTTP wrappers to AI microservices deployed on Kubernetes:

| Tool                | Gateway Endpoint      | Description                                                         |
| ------------------- | --------------------- | ------------------------------------------------------------------- |
| `generate_pipeline` | `/generate-pipeline`  | Generates Jenkinsfile from a natural language description           |
| `analyze_log`       | `/analyze-log`        | Diagnoses and solves Jenkins/CI logs using LLM                      |
| `lint_chart`        | `/lint-chart`         | Semantic linting of compressed Helm Charts (.tgz)                   |

All tools inject the field `caller: ai-agent-langchain` into the payload for traceability.

---

## ⚙️ Project Structure

```
ai-agent/
├── main.py                         # Entry point: runs the LangChain agent and orchestrates tools
├── tools/
│   ├── __init__.py
│   ├── ai_gateway_tools.py         # Definition and HTTP logic for each tool
├── clients/
│   └── gateway_client.py           # (optional, for extended HTTP client logic)
├── chart_example/
│   └── helm-log-analyzer-0.1.5.tgz # Example chart for linting tests
├── config/
│   └── settings.py
├── prompts/
│   └── examples.md
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

You can interact with the agent via CLI or modify the main file to run direct tests on the tools.

---

## 🌐 Environment Communication

The agent communicates with `ai-gateway` through internal HTTP requests (Kubernetes service).\
Active endpoints:

- `POST /generate-pipeline`
- `POST /analyze-log`
- `POST /lint-chart`

All prompts, responses, and events are logged by the gateway and audited via MCP messages.

---

## 🧠 Intelligence & Models

- **Default model:** OpenAI GPT-4 (can be switched to Mistral/Ollama by changing the config and backend microservice).
- All tool calls use `ollama` as the default engine (configurable).
- Future: integration of a fine-tuned model (`flan-t5` or others).

---

## 🔎 Observability & Traceability

- **Detailed logs** at each step (start, input, result, error) in stdout (visible in Kubernetes pods).
- **MCP**: All relevant executions are logged by `ai-gateway` through MCP messages, including metadata (caller, paths, microservice, etc).

---

## 📦 Main Dependencies

```text
langchain
openai
aiohttp
pydantic
python-dotenv
```

> Add `ollama-client` only if you need to invoke Ollama models locally.

---

## 📌 Current Status

-

---

## 👨‍💻 Author

**Dani**\
[github.com/dorado-ai-devops](https://github.com/dorado-ai-devops)

---

## 🛡 License

GNU General Public License v3.0
