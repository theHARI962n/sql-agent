from langchain.tools import tool
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

def classify_query(query: str):
    q = query.strip().lower()

    first_word = q.split()[0]

    if first_word == "select":
        return "SAFE"
    elif first_word in ("insert", "update", "alter"):
        return "NEEDS_APPROVAL"
    elif first_word in ("delete", "drop", "truncate"):
        return "BLOCKED"
    return "UNKNOWN"

@tool
def run_sql_query(query: str):
    """Execute SQL query with safety and approval checks."""

    query_type = classify_query(query)

    # BLOCK dangerous queries
    if query_type == "BLOCKED":
        return " This operation (DELETE/DROP/TRUNCATE) is not allowed. Please run manually in DB."

    # NEED APPROVAL
    if query_type == "NEEDS_APPROVAL":
        return {
            "status": "PENDING_APPROVAL",
            "query": query
        }

    # SAFE (SELECT)
    try:
        with engine.connect() as conn:
            result = conn.execute(text(query))
            rows = result.fetchall()
            return [dict(row._mapping) for row in rows]
    except Exception as e:
        return f"Error: {str(e)}"

@tool
def get_schema():
    """Get database schema: tables and columns."""
    schema = {}

    with engine.connect() as conn:
        tables = conn.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema='public';
        """)).fetchall()

        for table in tables:
            table_name = table[0]

            columns = conn.execute(text(f"""
                SELECT column_name, data_type
                FROM information_schema.columns
                WHERE table_name = '{table_name}';
            """)).fetchall()

            schema[table_name] = [
                {"column": col[0], "type": col[1]}
                for col in columns
            ]

    return schema


# import os
# from sqlalchemy import create_engine, text
# from dotenv import load_dotenv

# load_dotenv()

# DATABASE_URL = os.getenv("DATABASE_URL")
# engine = create_engine(DATABASE_URL)


# def run_sql_query(query: str):
#     """Executes a SQL query and returns results."""
#     try:
#         with engine.connect() as conn:
#             result = conn.execute(text(query))
#             rows = result.fetchall()
#             return [dict(row._mapping) for row in rows]
#     except Exception as e:
#         return f"Error: {str(e)}"


# def get_schema():
#     """Returns database schema information."""
#     schema = {}

#     with engine.connect() as conn:
#         # Get tables
#         tables = conn.execute(text("""
#             SELECT table_name 
#             FROM information_schema.tables 
#             WHERE table_schema='public';
#         """)).fetchall()

#         for table in tables:
#             table_name = table[0]

#             columns = conn.execute(text(f"""
#                 SELECT column_name, data_type
#                 FROM information_schema.columns
#                 WHERE table_name = '{table_name}';
#             """)).fetchall()

#             schema[table_name] = [
#                 {"column": col[0], "type": col[1]}
#                 for col in columns
#             ]

#     return schema