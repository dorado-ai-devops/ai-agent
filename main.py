from langchain.agents import initialize_agent, AgentType
from langchain_core.language_models.chat_models import SimpleChatModel
from langchain_core.messages import HumanMessage
from tools import TOOLS

class DummyLLM(SimpleChatModel):
    def _call(self, messages, stop=None, **kwargs):
        # HumanMessage más reciente = prompt del agente (incluye “Question: …”)
        raw = [m.content for m in messages if isinstance(m, HumanMessage)][-1]
        # solo la parte que sigue a “Question:”
        user_query = raw.split("Question:")[-1].split("\n")[0].strip()

        return (
            "Thought: Necesito usar una herramienta.\n"
            "Action: LogAnalyzerTool\n"
            f"Action Input: {user_query}"
        )

    @property
    def _llm_type(self):
        return "dummy-chat"

llm = DummyLLM()

agent = initialize_agent(
    tools=TOOLS,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

if __name__ == "__main__":
    while True:
        user_input = input("¿Qué necesitas? > ")
        if user_input.lower() in {"exit", "quit"}:
            break
        print(agent.invoke({"input": user_input})["output"])
