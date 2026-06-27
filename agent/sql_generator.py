from prompts import SQL_GENERATION_PROMPT


def generate_sql(llm, schema, question):

    chain = SQL_GENERATION_PROMPT | llm

    response = chain.invoke(
        {
            "schema": schema,
            "question": question
        }
    )

    return response.content.strip()