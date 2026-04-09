from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from tools import run_sql_query, get_schema
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

tools = [run_sql_query, get_schema]

agent = create_react_agent(llm, tools)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

while True:
    query = input("\n🧠 Ask your database: ")

    if query.lower() in ["exit", "quit"]:
        break

    response = agent_executor.invoke({"input": query})
    print("\n🤖 Answer:", response["output"])