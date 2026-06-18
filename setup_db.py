import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import random

def init_db():
    conn = sqlite3.connect("ecommerce.db")
    cursor = conn.cursor()

    # 1. Create Users Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            name TEXT,
            email TEXT,
            city TEXT,
            signup_date DATE
        )
    ''')

    # 2. Create Orders Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY,
            user_id INTEGER,
            order_date DATE,
            status TEXT,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    ''')

    # 3. Create Order Items Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS order_items (
            item_id INTEGER PRIMARY KEY,
            order_id INTEGER,
            product_name TEXT,
            category TEXT,
            price REAL,
            quantity INTEGER,
            FOREIGN KEY (order_id) REFERENCES orders(order_id)
        )
    ''')

    # Insert Mock Data
    cities = ['Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai', 'Pune']
    categories = ['Electronics', 'Clothing', 'Home Decor', 'Books', 'Fitness']
    products = {
        'Electronics': [('Laptop', 45000), ('Smartphone', 25000), ('Wireless Earbuds', 3000)],
        'Clothing': [('Jeans', 1500), ('T-Shirt', 700), ('Jacket', 3500)],
        'Home Decor': [('Lamp', 1200), ('Curtains', 2000), ('Wall Art', 1500)],
        'Books': [('Sci-Fi Novel', 400), ('Finance Guide', 600), ('Biography', 500)],
        'Fitness': [('Yoga Mat', 1000), ('Dumbbells', 2500), ('Resistance Bands', 500)]
    }

    # Generate 50 Users
    for i in range(1, 51):
        signup = (datetime.now() - timedelta(days=random.randint(30, 365))).date()
        cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?)", 
                       (i, f"User_{i}", f"user{i}@example.com", random.choice(cities), signup))

    # Generate 120 Orders & Items
    item_id = 1
    for order_id in range(1, 121):
        uid = random.randint(1, 50)
        order_date = (datetime.now() - timedelta(days=random.randint(1, 30))).date()
        status = random.choice(['Delivered', 'Delivered', 'Delivered', 'Shipped', 'Cancelled'])
        cursor.execute("INSERT INTO orders VALUES (?, ?, ?, ?)", (order_id, uid, order_date, status))

        # 1 to 3 items per order
        for _ in range(random.randint(1, 3)):
            cat = random.choice(categories)
            prod, price = random.choice(products[cat])
            qty = random.randint(1, 2)
            cursor.execute("INSERT INTO order_items VALUES (?, ?, ?, ?, ?, ?)", 
                           (item_id, order_id, prod, cat, price, qty))
            item_id += 1

    conn.commit()
    conn.close()
    print("Database built successfully with mock relational data!")

if __name__ == "__main__":
    init_db()
