
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


# Descripción de la infraestructura `DEVOPS-Agent-LAB`

`DEVOPS-Agent-LAB` es una infraestructura modular orientada a automatizar tareas DevOps mediante agentes de lenguaje (`LangChain`) integrados con herramientas personalizadas y capacidades de razonamiento sobre código, logs, y despliegues. El sistema opera en un entorno GitOps (ArgoCD + Kubernetes) y ofrece una experiencia unificada para usuarios humanos, pipelines de CI/CD y agentes LLM.

## Componentes principales

### 1. Entrada natural (AI-CHAT-UI)
Interfaz de lenguaje natural que permite a usuarios humanos interactuar con el agente mediante texto libre.

### 2. Razón y orquestación (ai-agent / LangChain)
Núcleo cognitivo del sistema. Utiliza LangChain para decidir qué herramientas ejecutar, en qué orden, y con qué contexto. Este agente dispone de herramientas registradas como:

- `generate_pipeline`
- `analyze_log`
- `lint_chart`
- `query_vector_db`
- `analyze_helm_chart`
- `list_github_repos`

### 3. Base de contexto (ai-vector-db / Chroma)
Vector DB que almacena documentos técnicos como código, manifiestos de despliegue o logs anteriores. El agente consulta esta base para obtener contexto relevante y enriquecer su razonamiento.

### 4. Herramientas externas personalizadas (EXTERNAL-CUSTOM-TOOLS)
Conjunto de microservicios desplegados en Flask:

- `ai-gateway`: intermediario HTTP para adaptadores externos
- `ai-logs-analyze`: analiza logs CI/CD
- `ai-helm-linter`: valida charts Helm
- `ai-pipeline-gen`: genera Jenkinsfiles desde descripciones

Estas tools pueden trabajar con modelos locales vía `ollama` (ej. Mistral 7B) o con APIs externas como OpenAI si se activa el fallback.

### 5. Integración con Jenkins
Jenkins actúa como emisor de tareas para el agente (`/agentquery`) y también como consumidor de los resultados generados por herramientas del sistema.

### 6. Observabilidad y feedback (FastAPI MCP + Streamlit)
- `ai-mcp-server`: almacena y publica mensajes y eventos en formato estructurado
- `streamlit`: interfaz de visualización para monitorear respuestas, outputs del LLM y estado general del sistema
- Persistencia: los outputs se almacenan en volúmenes `/mnt/data/gateway` y `/mnt/data/mcp` según origen

### 7. Despliegue GitOps (Kubernetes + ArgoCD)
Todos los componentes son desplegados mediante manifiestos Git y gestionados con ArgoCD sobre Kubernetes.

