from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI
from tools import tools
import asyncio

llm = ChatOpenAI(model="gpt-4", temperature=0)

async def main():
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.OPENAI_FUNCTIONS,
        verbose=True
    )
    result = await agent.ainvoke("Genera un pipeline básico con test.")
    print(result["output"])

if __name__ == "__main__":
    asyncio.run(main())
