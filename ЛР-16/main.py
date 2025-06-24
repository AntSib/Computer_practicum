import psycopg2
import threading
import time
from datetime import datetime
from dotenv import load_dotenv
import os
from tabulate import tabulate


load_dotenv()

DB_PARAMS = {
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'database': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD')
}


def setup_db():
    with psycopg2.connect(**DB_PARAMS) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS books (
                    id SERIAL PRIMARY KEY,
                    name TEXT UNIQUE NOT NULL
                );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS branches (
                    id SERIAL PRIMARY KEY,
                    name TEXT UNIQUE NOT NULL
                );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS stock (
                    book_id INT REFERENCES books(id),
                    branch_id INT REFERENCES branches(id),
                    quantity INT CHECK (quantity >= 0),
                    PRIMARY KEY (book_id, branch_id)
                );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS movements (
                    id SERIAL PRIMARY KEY,
                    book_id INT REFERENCES books(id),
                    quantity INT CHECK (quantity > 0),
                    from_branch_id INT REFERENCES branches(id),
                    to_branch_id INT REFERENCES branches(id),
                    movement_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            conn.commit()
    print("Таблицы созданы.")


def seed_data():
    books = ['Python Basics', 'Database Systems', 'Operating Systems']
    branches = ['Central Library', 'East Branch', 'West Branch']

    with psycopg2.connect(**DB_PARAMS) as conn:
        with conn.cursor() as cur:
            for book in books:
                cur.execute("INSERT INTO books (name) VALUES (%s) ON CONFLICT DO NOTHING;", (book,))
            for branch in branches:
                cur.execute("INSERT INTO branches (name) VALUES (%s) ON CONFLICT DO NOTHING;", (branch,))
            conn.commit()

        with conn.cursor() as cur:
            cur.execute("SELECT id FROM books WHERE name = 'Python Basics';")
            book_id = cur.fetchone()[0]
            cur.execute("SELECT id FROM branches;")
            branch_ids = [row[0] for row in cur.fetchall()]
            for branch_id in branch_ids:
                cur.execute("""
                    INSERT INTO stock (book_id, branch_id, quantity)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (book_id, branch_id) DO NOTHING;
                """, (book_id, branch_id, 25))
            conn.commit()
    print("Начальные данные добавлены.")


def transfer_books(book_id, from_branch_id, to_branch_id, quantity, isolation_level="READ COMMITTED"):
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        conn.set_session(isolation_level=isolation_level, autocommit=False)
        with conn.cursor() as cur:
            cur.execute("BEGIN;")

            time.sleep(1)

            cur.execute("""
                SELECT quantity FROM stock
                WHERE book_id = %s AND branch_id = %s
                FOR UPDATE;
            """, (book_id, from_branch_id))
            result = cur.fetchone()
            if not result:
                raise Exception("Книга отсутствует в отправляющем филиале.")
            if result[0] < quantity:
                raise Exception("Недостаточно книг для перемещения.")

            cur.execute("""
                UPDATE stock SET quantity = quantity - %s
                WHERE book_id = %s AND branch_id = %s;
            """, (quantity, book_id, from_branch_id))

            cur.execute("""
                INSERT INTO stock (book_id, branch_id, quantity)
                VALUES (%s, %s, %s)
                ON CONFLICT (book_id, branch_id) DO UPDATE SET quantity = stock.quantity + EXCLUDED.quantity;
            """, (book_id, to_branch_id, quantity))

            cur.execute("""
                INSERT INTO movements (book_id, quantity, from_branch_id, to_branch_id)
                VALUES (%s, %s, %s, %s);
            """, (book_id, quantity, from_branch_id, to_branch_id))

            conn.commit()
            print(f"[{datetime.now()}] Перемещено {quantity} книг #{book_id} из филиала #{from_branch_id} в #{to_branch_id}")
    except Exception as e:
        conn.rollback()
        print(f"[{datetime.now()}] Ошибка перемещения: {e}")
    finally:
        conn.close()


def simulate_race_condition(isolation_level="READ COMMITTED"):
    print(f"\n=== Симуляция гонки данных (Isolation: {isolation_level}) ===")
    with psycopg2.connect(**DB_PARAMS) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM books WHERE name = 'Python Basics';")
            book_id = cur.fetchone()[0]
            cur.execute("SELECT id FROM branches WHERE name = 'Central Library';")
            from_id = cur.fetchone()[0]
            cur.execute("SELECT id FROM branches WHERE name = 'East Branch';")
            to1_id = cur.fetchone()[0]
            cur.execute("SELECT id FROM branches WHERE name = 'West Branch';")
            to2_id = cur.fetchone()[0]

    t1 = threading.Thread(target=transfer_books, args=(book_id, from_id, to1_id, 5, isolation_level))
    t2 = threading.Thread(target=transfer_books, args=(book_id, from_id, to2_id, 7, isolation_level))

    t1.start()
    t2.start()
    t1.join()
    t2.join()

    print_table("stock")
    print_table("movements")


def print_table(table_name):
    with psycopg2.connect(**DB_PARAMS) as conn:
        with conn.cursor() as cur:
            cur.execute(f"SELECT * FROM {table_name};")
            rows = cur.fetchall()
            headers = [desc[0] for desc in cur.description]
            print(f"\nТаблица {table_name}:")
            print(tabulate(rows, headers=headers, tablefmt="grid"))


def clear_db():
    with psycopg2.connect(**DB_PARAMS) as conn:
        with conn.cursor() as cur:
            for table in ['movements', 'stock', 'books', 'branches']:
                cur.execute(f"DROP TABLE IF EXISTS {table} CASCADE;")
            conn.commit()
    print("База данных очищена.")


if __name__ == "__main__":
    clear_db()
    setup_db()
    seed_data()
    print_table("stock")
    simulate_race_condition("READ COMMITTED")
    simulate_race_condition("REPEATABLE READ")
