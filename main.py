from langchain.agents import initialize_agent, AgentType
from langchain.llms import OpenAI
from tools import TOOLS

llm = OpenAI(temperature=0)  # Simulación, no se usará si estás mockeando solo

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
