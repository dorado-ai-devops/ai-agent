from langchain.agents import initialize_agent, AgentType
from langchain_core.language_models.chat_models import SimpleChatModel
from langchain_core.messages import AIMessage, HumanMessage
from tools import TOOLS


class DummyLLM(SimpleChatModel):
    def _call(self, messages, stop=None, **kwargs):
        # Extrae el último mensaje del usuario
        last_user_input = [m.content for m in messages if isinstance(m, HumanMessage)][-1]
        return AIMessage(content=f"[Respuesta simulada a]: {last_user_input}")

    @property
    def _llm_type(self) -> str:
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
        if user_input.lower() in ["exit", "quit"]:
            break
        result = agent.run(user_input)
        print(result)
