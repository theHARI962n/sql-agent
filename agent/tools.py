from langchain.tools import tool
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)


@tool
def run_sql_query(query: str):
    """Execute a SQL query on the database and return the results."""
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