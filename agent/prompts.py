from langchain_core.prompts import ChatPromptTemplate

SQL_GENERATION_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an expert PostgreSQL SQL generator.

Generate ONLY SQL.

Rules:
- Use ONLY the provided schema.
- Never invent tables or columns.
- Return ONLY SQL.
- No markdown.
- No explanation.
- If SQL cannot be generated, return exactly:
CANNOT_GENERATE_SQL
"""
        ),
        (
            "human",
            """
Schema:

{schema}

User Request:

{question}
"""
        ),
    ]
)