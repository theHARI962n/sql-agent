import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

def create_tables():
    with engine.connect() as conn:
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100)
        );
        """))

        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS orders (
            id SERIAL PRIMARY KEY,
            user_id INT REFERENCES users(id),
            product VARCHAR(100),
            amount INT
        );
        """))

        conn.commit()

def insert_sample_data():
    with engine.connect() as conn:
        # Insert users
        conn.execute(text("""
        INSERT INTO users (name, email) VALUES
        ('Alice', 'alice@example.com'),
        ('Bob', 'bob@example.com'),
        ('Charlie', 'charlie@example.com')
        ON CONFLICT DO NOTHING;
        """))

        # Insert orders
        conn.execute(text("""
        INSERT INTO orders (user_id, product, amount) VALUES
        (1, 'Laptop', 1200),
        (1, 'Mouse', 25),
        (2, 'Keyboard', 75),
        (3, 'Monitor', 300),
        (2, 'Headphones', 150);
        """))

        conn.commit()

if __name__ == "__main__":
    create_tables()
    insert_sample_data()
    print("✅ Database setup complete!")