from datetime import datetime, timedelta
import os
import random
import sqlite3

DB_NAME = "data/enterprise.db"


def init_db():
  """Initializes the SQLite database with sample e-commerce data."""
  os.makedirs("data", exist_ok=True)

  conn = sqlite3.connect(DB_NAME)
  cursor = conn.cursor()

  # 1. Users Table
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            name TEXT,
            email TEXT,
            city TEXT,
            signup_date DATE
        )
    """)

  # 2. Orders Table
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY,
            user_id INTEGER,
            order_date DATE,
            status TEXT,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """)

  # 3. Order Items Table
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            item_id INTEGER PRIMARY KEY,
            order_id INTEGER,
            product_name TEXT,
            category TEXT,
            price REAL,
            quantity INTEGER,
            FOREIGN KEY (order_id) REFERENCES orders(order_id)
        )
    """)

  # Seed mock data if tables are empty
  cursor.execute("SELECT COUNT(*) FROM users;")
  if cursor.fetchone()[0] == 0:
    cities = ["Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai", "Pune"]
    categories = [
        "Electronics",
        "Clothing",
        "Home Decor",
        "Books",
        "Fitness",
    ]
    products = {
        "Electronics": [
            ("Laptop", 45000),
            ("Smartphone", 25000),
            ("Wireless Earbuds", 3000),
        ],
        "Clothing": [("Jeans", 1500), ("T-Shirt", 700), ("Jacket", 3500)],
        "Home Decor": [("Lamp", 1200), ("Curtains", 2000), ("Wall Art", 1500)],
        "Books": [
            ("Sci-Fi Novel", 400),
            ("Finance Guide", 600),
            ("Biography", 500),
        ],
        "Fitness": [
            ("Yoga Mat", 1000),
            ("Dumbbells", 2500),
            ("Resistance Bands", 500),
        ],
    }

    # Generate 50 Users
    for i in range(1, 51):
      signup = (
          datetime.now() - timedelta(days=random.randint(30, 365))
      ).date()
      cursor.execute(
          "INSERT INTO users VALUES (?, ?, ?, ?, ?)",
          (
              i,
              f"User_{i}",
              f"user{i}@example.com",
              random.choice(cities),
              signup,
          ),
      )

    # Generate 120 Orders & Items
    item_id = 1
    for order_id in range(1, 121):
      uid = random.randint(1, 50)
      order_date = (datetime.now() - timedelta(days=random.randint(1, 30))).date()
      status = random.choice(
          ["Delivered", "Delivered", "Delivered", "Shipped", "Cancelled"]
      )
      cursor.execute(
          "INSERT INTO orders VALUES (?, ?, ?, ?)",
          (order_id, uid, order_date, status),
      )

      for _ in range(random.randint(1, 3)):
        cat = random.choice(categories)
        prod, price = random.choice(products[cat])
        qty = random.randint(1, 2)
        cursor.execute(
            "INSERT INTO order_items VALUES (?, ?, ?, ?, ?, ?)",
            (item_id, order_id, prod, cat, price, qty),
        )
        item_id += 1

    conn.commit()
    print("Database seeded successfully with enterprise mock data.")

  conn.close()


def get_db_schema() -> str:
  """Fetches the schema of the SQLite database tables."""
  conn = sqlite3.connect(DB_NAME)
  cursor = conn.cursor()
  cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
  tables = cursor.fetchall()

  schema_info = []
  for table_name in tables:
    t_name = table_name[0]
    cursor.execute(f"PRAGMA table_info({t_name});")
    columns = cursor.fetchall()
    col_details = ", ".join([f"{col[1]} ({col[2]})" for col in columns])
    schema_info.append(f"Table: {t_name} -> Columns: {col_details}")

  conn.close()
  return "\n".join(schema_info)


if __name__ == "__main__":
  init_db()