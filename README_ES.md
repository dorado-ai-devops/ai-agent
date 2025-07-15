
# 🧠 ai-agent

Agente IA razonador construido con **LangChain** + **OpenAI** (GPT-4).  
Orquesta tareas complejas de DevOps mediante razonamiento LLM y llamada modular a herramientas IA propias del ecosistema `devops-ai-lab`.

---

## 🎯 Propósito

Centraliza la lógica de decisión y automatización DevOps basada en LLMs, encapsulando como **tools** los microservicios IA desplegados vía `ai-gateway`.  
Permite analizar logs, validar charts Helm, generar Jenkinsfiles y recuperar contexto desde una base vectorial documentacional.  
Este agente es la **entrada cognitiva real de la arquitectura**.

---

## 🔧 Funcionalidad

El agente expone varias **tools** conectadas a servicios internos o externos:

| Tool                    | Función                                                                 |
|-------------------------|-------------------------------------------------------------------------|
| `generate_pipeline`     | Genera Jenkinsfile desde texto natural vía `ai-pipeline-gen`            |
| `analyze_log`           | Diagnóstico inteligente de logs CI/CD con `ai-log-analyzer`             |
| `lint_chart`            | Linting semántico de Helm Charts comprimidos (.tgz)                     |
| `analyze_helm_chart`    | Clona, empaqueta y analiza un Helm Chart desde GitHub automáticamente   |
| `list_github_repos`     | Lista todos los repos públicos de `dorado-ai-devops`                    |
| `query_vector_db`       | Recupera contexto semántico desde `ai-vector-db` usando búsqueda LLM    |

Todas las tools inyectan `caller: ai-agent-langchain` para trazabilidad MCP.

---

## ⚙️ Estructura del Proyecto

```
ai-agent/
├── main.py                         # Punto de entrada del agente (FastAPI)
├── tools/                          # Tools expuestas al agente
│   ├── ai_gateway_tools.py         # Wrappers HTTP a los microservicios
│   ├── github_tools.py             # Listado de repositorios desde GitHub
│   ├── helm_chart_tools.py         # Fetch + lint automático de Helm Charts
│   └── vector_db_tools.py          # Consulta semántica al vector DB
├── prompts/
│   └── examples.md                 # Ejemplos y frases de prueba
├── config/
│   └── settings.py                 # Configuración general
├── chart_example/
│   └── helm-log-analyzer-0.1.5.tgz
├── Dockerfile
├── README.md
└── requirements.txt
```

---

## 🌐 API REST

El agente corre en un servidor FastAPI con el endpoint:

- `POST /ask`  
  Payload: `{"prompt": "tu pregunta en lenguaje natural"}`  
  Devuelve: `{"result": "respuesta generada (tool o razonamiento)"}`

El agente identifica si necesita contexto, ejecuta tools, y resume resultados.

---

## 📚 Contexto Semántico (Vector DB)

`query_vector_db` permite que el agente acceda a contexto técnico/documental recuperado semánticamente desde la base vectorial `ai-vector-db`, la cual indexa documentación de todos los microservicios del ecosistema `devops-ai-lab`.

El agente puede consultar conceptos como:

```
¿Qué hace ai-chat-ui?
¿Dónde está implementado el fetch de charts?
```

Y usará la respuesta como contexto antes de contestar.

---

## 🧠 Inteligencia y Modelos

- **Modelo por defecto:** OpenAI GPT-4 (via `langchain_openai.ChatOpenAI`)
- **Motor IA de los tools:** configurable (`ollama`, `openai`) según `AI_VENDOR`

---

## 🚀 Ejecución Local

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

Asegúrate de tener acceso al `ai-gateway`, y de definir las variables de entorno necesarias (`GH_SECRET`, `AI_VENDOR`, etc.).

---

## 🔎 Observabilidad y Trazabilidad

- **Logs** en consola para cada tool: inicio, input, resultado, error.
- **MCP (Message Control Plane)**: mensajes emitidos desde `ai-gateway` con trazabilidad por caller, microservicio y petición.

---

## 📦 Dependencias principales

```text
langchain
langchain-openai
aiohttp
fastapi
openai
requests
uvicorn
pydantic
python-dotenv
```

> Añade `ollama-client` si invocas Ollama localmente.

---

## 📌 Estado actual

✅ Funcional  
🧪 En constante expansión (vector-db, fine-tuning, validación avanzada)

---

## 👨‍💻 Autor

**Dani**  
[github.com/dorado-ai-devops](https://github.com/dorado-ai-devops)

---

## 🛡 Licencia

Licencia Pública General GNU v3.0
