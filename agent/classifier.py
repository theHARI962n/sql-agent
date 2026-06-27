def classify_query(query: str):

    query = query.strip().lower()

    first = query.split()[0]

    if first == "select":
        return "SAFE"

    if first in ("insert", "update", "alter"):
        return "NEEDS_APPROVAL"

    if first in ("delete", "drop", "truncate"):
        return "BLOCKED"

    return "UNKNOWN"