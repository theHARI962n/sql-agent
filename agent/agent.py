# from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
load_dotenv()
print(f"🚀 Using provider: {os.getenv('MODEL_PROVIDER')}")
# from langchain.agents import create_react_agent, AgentExecutor

from langchain.agents import (
    create_tool_calling_agent,
    AgentExecutor
)

# from langchain.prompts import PromptTemplate
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
)
from tools import run_sql_query, get_schema
from llm_factory import get_llm


# llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

llm = get_llm()

tools = [run_sql_query, get_schema]

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an expert SQL assistant.

Rules:
- ALWAYS inspect the schema before generating SQL.
- Use get_schema first.
- Use run_sql_query to execute SQL.
- Never invent tables.
- DELETE/DROP/TRUNCATE are forbidden.
- UPDATE/INSERT require approval.
"""
        ),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

# prompt = PromptTemplate.from_template("""
# You are a SQL agent.

# You have access to the following tools:

# {tools}

# Tool names:
# {tool_names}

# Rules:
# - ALWAYS check database schema using get_schema before writing queries.
# - Use only available tables and columns.
# - SELECT queries are safe.
# - INSERT, UPDATE, ALTER queries require human approval.
# - DELETE, DROP, TRUNCATE queries are strictly forbidden.


# Follow this format:

# Question: {input}
# Thought: think step-by-step
# Action: tool name
# Action Input: input to tool
# Observation: result
# ... (repeat)
# Final Answer: answer to user

# {agent_scratchpad}
# """)

agent = create_tool_calling_agent(
    llm,
    tools,
    prompt
)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

while True:
    query = input("\n🧠 Ask your database: ")

    if query.lower() in ["exit", "quit"]:
        break

    response = agent_executor.invoke({"input": query})
    output = response["output"]

    # 🔥 HANDLE APPROVAL FLOW
    if isinstance(output, dict) and output.get("status") == "PENDING_APPROVAL":
        print("\n⚠️ Query needs approval:")
        print(output["query"])

        decision = input("Approve? (y/n): ")

        if decision.lower() == "y":
            # Execute manually
            try:
                from tools import engine
                from sqlalchemy import text

                with engine.connect() as conn:
                    conn.execute(text(output["query"]))
                    conn.commit()

                print("✅ Query executed successfully!")
            except Exception as e:
                print("❌ Error:", str(e))
        else:
            print("❌ Query rejected.")

    else:
        print("\n🤖 Answer:", output)