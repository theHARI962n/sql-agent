from langchain.tools import tool
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)


@tool
def run_sql_query(query: str):
    """
    Executes SQL.
    Assumes validation has already happened.
    """

    try:
        with engine.connect() as conn:

            result = conn.execute(text(query))

            # SELECT queries
            if result.returns_rows:
                rows = result.fetchall()

                return {
                    "status": "SUCCESS",
                    "rows": [dict(row._mapping) for row in rows]
                }

            # INSERT / UPDATE / ALTER
            conn.commit()

            return {
                "status": "SUCCESS",
                "message": "Query executed successfully."
            }

    except Exception as e:
        return {
            "status": "ERROR",
            "message": str(e)
        }

@tool
def get_schema():
    """Return database schema."""

    schema = {}

    with engine.connect() as conn:

        tables = conn.execute(text("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema='public';
        """)).fetchall()

        for table in tables:

            table_name = table[0]

            columns = conn.execute(text("""
                SELECT column_name, data_type
                FROM information_schema.columns
                WHERE table_name = :table
            """), {"table": table_name}).fetchall()

            schema[table_name] = [
                {
                    "column": column,
                    "type": datatype
                }
                for column, datatype in columns
            ]

    return schema

# previous version 
# from langchain.tools import tool
# from validator import validate_sql
# import os
# from sqlalchemy import create_engine, text
# from dotenv import load_dotenv

# load_dotenv()

# DATABASE_URL = os.getenv("DATABASE_URL")
# engine = create_engine(DATABASE_URL)

# def classify_query(query: str):
#     q = query.strip().lower()

#     if not q:
#         return "UNKNOWN"

#     first_word = q.split()[0]

#     if first_word == "select":
#         return "SAFE"
#     elif first_word in ("insert", "update", "alter"):
#         return "NEEDS_APPROVAL"
#     elif first_word in ("delete", "drop", "truncate"):
#         return "BLOCKED"
#     return "UNKNOWN"

# @tool
# def run_sql_query(query: str):
#     """Execute SQL query with safety and approval checks."""

#     validation = validate_sql(query)

#     if not validation["valid"]:
#         return {
#             "status": "ERROR",
#             "message": validation["message"]
#         }

#     query_type = classify_query(query)

#     # BLOCK
#     if query_type == "BLOCKED":
#         return {
#         "status": "BLOCKED",
#         "message": "DELETE, DROP and TRUNCATE operations are not allowed."
#         }
#     # NEED APPROVAL
#     if query_type == "NEEDS_APPROVAL":
#         return {
#             "status": "PENDING_APPROVAL",
#             "query": query
#         }

#     # SAFE (SELECT)

#     if query_type == "UNKNOWN":
#         return {
#         "status": "ERROR",
#         "message": "Unsupported or invalid SQL query."
#         }

#     try:
#         with engine.connect() as conn:
#             result = conn.execute(text(query))
#             rows = result.fetchall()
#             return {
#                 "status": "SUCCESS",
#                 "rows": [dict(row._mapping) for row in rows]
#             }
#     except Exception as e:
#         return {
#         "status": "ERROR",
#         "message": str(e)
#         }

# @tool
# def get_schema():
#     """Get database schema: tables and columns."""
#     schema = {}

#     with engine.connect() as conn:
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










# old ver
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