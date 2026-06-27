import os
from dotenv import load_dotenv
from answer_generator import generate_answer
load_dotenv()

from llm_factory import get_llm
from tools import get_schema, run_sql_query
from classifier import classify_query
from sql_generator import generate_sql

llm = get_llm()

print(f"🚀 Using provider: {os.getenv('MODEL_PROVIDER')}")

while True:

    question = input("\n🧠 Ask your database: ")

    if question.lower() in ["exit", "quit"]:
        break

    schema = get_schema.invoke({})

    sql = generate_sql(
        llm,
        schema,
        question
    )

    print("\nGenerated SQL:")
    print(sql)

    if sql == "CANNOT_GENERATE_SQL":
        print("\n❌ I cannot generate SQL for that request.")
        continue

    query_type = classify_query(sql)

    if query_type == "BLOCKED":
        print("\n❌ DELETE/DROP/TRUNCATE are forbidden.")
        continue

    if query_type == "NEEDS_APPROVAL":
        print("\n⚠️ This query will modify the database.")
        print(sql)

        choice = input("\nApprove? (y/n): ")

        if choice.lower() != "y":
            print("\n❌ Cancelled.")
            continue

    result = run_sql_query.invoke(
        {
            "query": sql
        }
    )

    if result["status"] == "ERROR":
        print(result["message"])
        continue

    # Generate natural language answer
    final_answer = generate_answer(
        llm,
        question,
        result
    )

    print("\n🤖 Answer:")
    print(final_answer)

    # if "rows" in result:
    #     print("\nResult:")

    #     for row in result["rows"]:
    #         print(row)
    # else:
    #     print(result["message"])
    


# Previous version
# # from langchain_openai import ChatOpenAI
# import os
# from dotenv import load_dotenv
# load_dotenv()
# print(f"🚀 Using provider: {os.getenv('MODEL_PROVIDER')}")
# # from langchain.agents import create_react_agent, AgentExecutor

# from langchain.agents import (
#     create_tool_calling_agent,
#     AgentExecutor
# )

# # from langchain.prompts import PromptTemplate
# from langchain_core.prompts import (
#     ChatPromptTemplate,
#     MessagesPlaceholder,
# )
# from tools import run_sql_query, get_schema
# from llm_factory import get_llm


# # llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# llm = get_llm()

# tools = [run_sql_query, get_schema]


# prompt = ChatPromptTemplate.from_messages(
#     [
#         (
#             "system",
#             """
# You are an expert SQL assistant.

# You have access to two tools:

# 1. get_schema
# 2. run_sql_query

# Rules:

# - ALWAYS call get_schema before generating SQL unless you already know the schema.
# - Use ONLY the tables and columns returned by get_schema.
# - Never invent table names or column names.

# The run_sql_query tool returns structured responses.

# Interpret them as follows:

# SUCCESS
# ---------
# The SQL executed successfully.
# Use the returned rows to answer the user's question.

# ERROR
# ---------
# The SQL failed.
# Read the error message.
# If possible, correct the SQL and try again.
# Do not repeat the exact same incorrect query more than once.

# PENDING_APPROVAL
# ---------
# The query requires user approval.
# DO NOT call run_sql_query again.
# Inform the user that approval is required and stop.

# BLOCKED
# ---------
# The requested SQL operation is forbidden.
# Inform the user that the operation is not allowed.
# Do not retry.

# Always produce clear and concise answers.
# """
#         ),
#         ("human", "{input}"),
#         MessagesPlaceholder(variable_name="agent_scratchpad"),
#     ]
# )

# # prompt = ChatPromptTemplate.from_messages(
# #     [
# #         (
# #             "system",
# #             """
# # You are an expert SQL assistant.

# # Rules:
# # - ALWAYS inspect the schema before generating SQL.
# # - Use get_schema first.
# # - Use run_sql_query to execute SQL.
# # - Never invent tables.
# # - DELETE/DROP/TRUNCATE are forbidden.
# # - UPDATE/INSERT require approval.
# # """
# #         ),
# #         ("human", "{input}"),
# #         MessagesPlaceholder(variable_name="agent_scratchpad"),
# #     ]
# # )

# # prompt = PromptTemplate.from_template("""
# # You are a SQL agent.

# # You have access to the following tools:

# # {tools}

# # Tool names:
# # {tool_names}

# # Rules:
# # - ALWAYS check database schema using get_schema before writing queries.
# # - Use only available tables and columns.
# # - SELECT queries are safe.
# # - INSERT, UPDATE, ALTER queries require human approval.
# # - DELETE, DROP, TRUNCATE queries are strictly forbidden.


# # Follow this format:

# # Question: {input}
# # Thought: think step-by-step
# # Action: tool name
# # Action Input: input to tool
# # Observation: result
# # ... (repeat)
# # Final Answer: answer to user

# # {agent_scratchpad}
# # """)

# agent = create_tool_calling_agent(
#     llm,
#     tools,
#     prompt
# )

# agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True,max_iterations=5,
#     handle_parsing_errors=True,)

# while True:
#     query = input("\n🧠 Ask your database: ")

#     if query.lower() in ["exit", "quit"]:
#         break

#     response = agent_executor.invoke({"input": query})

#     print("\n========== RAW RESPONSE ==========")
#     print(response)
#     print("==================================\n")

#     output = response["output"]

#     # 🔥 HANDLE APPROVAL FLOW
#     if isinstance(output, dict) and output.get("status") == "PENDING_APPROVAL":
#         print("\n⚠️ Query needs approval:")
#         print(output["query"])

#         decision = input("Approve? (y/n): ")

#         if decision.lower() == "y":
#             # Execute manually
#             try:
#                 from tools import engine
#                 from sqlalchemy import text

#                 with engine.connect() as conn:
#                     conn.execute(text(output["query"]))
#                     conn.commit()

#                 print("✅ Query executed successfully!")
#             except Exception as e:
#                 print("❌ Error:", str(e))
#         else:
#             print("❌ Query rejected.")

#     else:
#         print("\n🤖 Answer:", output)