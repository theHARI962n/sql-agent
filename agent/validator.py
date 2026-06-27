# validator.py

import re


def validate_sql(query: str):
    """
    Validate SQL before execution.
    Returns:
        {"valid": True}
    or
        {"valid": False, "message": "..."}
    """

    query = query.strip()

    # Empty query
    if not query:
        return {
            "valid": False,
            "message": "SQL query is empty."
        }

    # Valid starting keywords
    allowed = (
        "select",
        "insert",
        "update",
        "delete",
        "alter",
        "drop",
        "truncate",
    )

    if not query.lower().startswith(allowed):
        return {
            "valid": False,
            "message": "Invalid SQL statement."
        }

    return {
        "valid": True
    }