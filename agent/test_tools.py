from tools import run_sql_query, get_schema

print("📊 Schema:")
print(get_schema.invoke({}))

print("\n👤 Users:")
print(run_sql_query.invoke({"query": "SELECT * FROM users;"}))

print("\n🛒 Orders:")
print(run_sql_query.invoke({"query": "SELECT * FROM orders;"}))

# from tools import run_sql_query, get_schema

# print("📊 Schema:")
# print(get_schema())

# print("\n👤 Users:")
# print(run_sql_query("SELECT * FROM users;"))

# print("\n🛒 Orders:")
# print(run_sql_query("SELECT * FROM orders;"))