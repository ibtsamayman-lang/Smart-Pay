import sqlite3
from datetime import datetime


DB_NAME = "smartbuy.db"


def create_database():

    connection = sqlite3.connect(DB_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS price_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT NOT NULL,
            store TEXT NOT NULL,
            price REAL NOT NULL,
            date TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def save_price(product_name, store, price):

    connection = sqlite3.connect(DB_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO price_history
        (product_name, store, price, date)
        VALUES (?, ?, ?, ?)
    """, (
        product_name,
        store,
        price,
        datetime.now().strftime("%Y-%m-%d %H:%M")
    ))

    connection.commit()
    connection.close()


def get_price_history(product_name):

    connection = sqlite3.connect(DB_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT store, price, date
        FROM price_history
        WHERE product_name LIKE ?
        ORDER BY date
    """, (f"%{product_name}%",))

    results = cursor.fetchall()

    connection.close()

    return results