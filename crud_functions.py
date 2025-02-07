import sqlite3


def initiate_db():
    connection = sqlite3.connect("products.db")
    cursor = connection.cursor()

    cursor.execute(" DROP TABLE IF EXISTS Products")
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    price INTEGER NOT NULL
    )
    ''')


    cursor.execute(" INSERT INTO products (title, description, price) VALUES (?, ?, ?)",
            ("Welllab UNCARIA FORTE",'БАД для поддержки иммунитета', 1500 ))
    cursor.execute(" INSERT INTO products (title, description, price) VALUES (?, ?, ?)",
                   ("Welllab ANTISWEET CONTROL", 'БАД для поддержки углеводного обмена', 2500))
    cursor.execute(" INSERT INTO products (title, description, price) VALUES (?, ?, ?)",
                   ("Welllab BRONCHOLUX INTENSIVE", 'БАД для дыхательной системы', 1400))
    cursor.execute(" INSERT INTO products (title, description, price) VALUES (?, ?, ?)",
                   ("Welllab VISION COMPLEX", 'БАД для поддержки зрения', 1300))

    connection.commit()
    connection.close()

p = initiate_db()


def get_all_products():
    connection = sqlite3.connect("products.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Products")
    product = cursor.fetchall()
    connection.commit()
    connection.close()
    return product

