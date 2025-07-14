# 🧠 ai-agent

Agente IA razonador construido con LangChain. Orquesta tareas complejas de DevOps mediante razonamiento simbólico e invocación modular de herramientas IA ya existentes en el ecosistema `devops-ai-lab`.

---

## 🎯 Propósito

Centraliza la lógica de razonamiento y decisión basada en LLMs, encapsulando como herramientas (`tools`) los microservicios IA accesibles vía `ai-gateway`. Permite analizar logs, validar charts, generar pipelines y realizar consultas libres desde un único punto de entrada cognitivo.

Este componente marca el inicio de la capa de inteligencia real en la arquitectura.

---

## 🔧 Funcionalidad

El agente combina múltiples herramientas como funciones invocables desde lenguaje natural. Cada tool actúa como wrapper HTTP a uno de los siguientes endpoints:

| Tool              | Microservicio        | Descripción |
|------------------|----------------------|-------------|
| `LogAnalyzerTool` | `ai-logs-analyze`     | Diagnóstico de logs CI/CD con LLM |
| `HelmLinterTool`  | `ai-helm-linter`      | Validación semántica de charts Helm |
| `PipelineGenTool` | `ai-pipeline-gen`     | Generación de Jenkinsfile desde texto |


---

## ⚙️ Estructura del Proyecto

```
ai-agent/
├── main.py                       # Entry point: ejecuta el agente LangChain
├── tools/
│   ├── __init__.py
│   ├── ai_gateway_tools.py
├── clients/
│   └── gateway_client.py
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

Interactuar vía CLI directamente con el agente:

```
> ¿Qué necesitas? > Diagnostica este log: (...)
> Resultado: Parece un error de volumen persistente en tu pod de Kubernetes...
```

---

## 🌐 Comunicación con el entorno

El agente se conecta a `ai-gateway` para acceder a las herramientas IA existentes. Los endpoints utilizados son:

- `POST /analyze-log`
- `POST /lint-chart`
- `POST /generate-pipeline`
- `POST /query-ollama`
- `POST /query-flan`

(Ver configuración en `config/settings.py`)

---

## 🧠 Inteligencia y Modelos

- Modelo principal: `Mistral` vía Ollama
- Soporte para OpenAI (fallback opcional)
- Soporte futuro: LLM fine-tuneado (FlanT5)

---

## 📦 Dependencias

```text
langchain
requests
python-dotenv
ollama-client  # si se usa cliente específico
```

---

## 📌 Estado actual

- [x] Estructura del agente definida
- [ ] Tools implementadas (en progreso)
- [ ] CLI operativa
- [ ] Integración completa con `ai-gateway`
- [ ] Orquestación simbólica multi-tool

---

## 👨‍💻 Autor

**Dani** – [@dorado-ai-devops](https://github.com/dorado-ai-devops)

---

## 🛡 Licencia

Licencia Pública General GNU v3.0
