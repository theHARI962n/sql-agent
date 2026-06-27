from langchain_core.prompts import ChatPromptTemplate

ANSWER_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are a data analyst assistant.

Your job:
- Convert database query results into natural English answers.
- Be concise and accurate.
- Do NOT mention SQL.
- Do NOT explain your reasoning.
- If result is empty, say: "No data found."
"""
        ),
        (
            "human",
            """
User Question:
{question}

SQL Result:
{result}
"""
        ),
    ]
)


def generate_answer(llm, question, result):
    chain = ANSWER_PROMPT | llm
    response = chain.invoke({
        "question": question,
        "result": result
    })

    return response.content.strip()