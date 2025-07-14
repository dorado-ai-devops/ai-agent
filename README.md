# 🧠 ai-agent

Agente IA razonador construido con **LangChain** + **OpenAI** (GPT-4).\
Orquesta tareas complejas de DevOps mediante razonamiento LLM y llamada modular a herramientas IA propias del ecosistema `devops-ai-lab`.

---

## 🎯 Propósito

Centraliza la lógica de decisión y automatización DevOps basada en LLMs, encapsulando como **tools** los microservicios IA accesibles vía `ai-gateway`.\
Permite analizar logs, validar charts Helm y generar Jenkinsfiles de forma unificada, añadiendo trazabilidad y observabilidad avanzada (MCP).

Este agente es la entrada cognitiva real de la arquitectura.

---

## 🔧 Funcionalidad

El agente expone varias **tools** que actúan como wrappers HTTP a microservicios IA desplegados en Kubernetes:

| Tool                | Endpoint Gateway     | Descripción                                                        |
| ------------------- | -------------------- | ------------------------------------------------------------------ |
| `generate_pipeline` | `/generate-pipeline` | Genera Jenkinsfile a partir de una descripción en lenguaje natural |
| `analyze_log`       | `/analyze-log`       | Diagnóstico y solución de logs Jenkins/CI vía LLM                  |
| `lint_chart`        | `/lint-chart`        | Linting semántico de Helm Charts comprimidos (.tgz)                |

Todas las tools inyectan el campo `caller: ai-agent-langchain` en el payload para trazabilidad.

---

## ⚙️ Estructura del Proyecto

```
ai-agent/
├── main.py                         # Entry point: ejecuta el agente LangChain y orquesta las tools
├── tools/
│   ├── __init__.py
│   ├── ai_gateway_tools.py         # Definición y lógica HTTP de cada tool
├── clients/
│   └── gateway_client.py           # (opcional, para lógica extendida de cliente HTTP)
├── chart_example/
│   └── helm-log-analyzer-0.1.5.tgz # Chart de ejemplo para pruebas de linting
├── config/
│   └── settings.py
├── prompts/
│   └── examples.md
├── README.md
├── requirements.txt
└── Dockerfile
```

---

## 🚀 Ejecución Local

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

Puedes interactuar con el agente vía CLI, o modificar el main para ejecutar pruebas directas sobre las tools.

---

## 🌐 Comunicación con el entorno

El agente se comunica con `ai-gateway` mediante peticiones HTTP internas (Kubernetes service).\
Endpoints activos:

- `POST /generate-pipeline`
- `POST /analyze-log`
- `POST /lint-chart`

Todos los prompts, respuestas y eventos son registrados por el gateway en disco y auditados vía mensajes MCP.

---

## 🧠 Inteligencia y Modelos

- **Modelo por defecto:** OpenAI GPT-4 (puedes adaptar a Mistral/Ollama modificando la config y el microservicio backend).
- Todas las llamadas tools fijan el motor a `ollama` por defecto, pero es configurable.
- Futuro: integración de modelo fine-tuneado propio (`flan-t5` u otros).

---

## 🔎 Observabilidad y Trazabilidad

- **Logs** detallados en cada paso (inicio, input, resultado, error) en stdout (visible en pods Kubernetes).
- **MCP**: Cada ejecución relevante es registrada por `ai-gateway` mediante mensajes MCP, incluyendo metadata (caller, paths, microservicio, etc).

---

## 📦 Dependencias principales

```text
langchain
openai
aiohttp
pydantic
python-dotenv
```

---

## 📌 Estado actual

-

---

## 👨‍💻 Autor

**Dani**\
[github.com/dorado-ai-devops](https://github.com/dorado-ai-devops)

---

## 🛡 Licencia

Licencia Pública General GNU v3.0

