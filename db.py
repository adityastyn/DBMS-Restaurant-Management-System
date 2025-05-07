import mysql.connector

# MySQL connection details — customize to your setup
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "1234",  # your MySQL password
    "database": "restaurant_db"
}

def get_db():
    return mysql.connector.connect(**db_config)


# Reservations
def reserve_table(name, table_no, time):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            "INSERT INTO reservations (customer_name, table_no, reservation_time) VALUES (%s, %s, %s)",
            (name, table_no, time)
        )
        db.commit()
        return "Reservation successful!"
    except Exception as e:
        return f"Error: {e}"
    finally:
        db.close()


# Menu Management
def add_menu_item(name, price):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO menu (item_name, price) VALUES (%s, %s)", (name, price))
    db.commit()
    db.close()

def get_menu_items():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT item_id, item_name, price FROM menu")
    items = cursor.fetchall()
    db.close()
    return items

def delete_menu_item(item_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM menu WHERE item_id = %s", (item_id,))
    db.commit()
    db.close()


# Orders
def add_order(table_no, item_id, quantity):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO orders (table_no, item_id, quantity) VALUES (%s, %s, %s)", (table_no, item_id, quantity))
    db.commit()
    db.close()

def get_orders(table_no):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT m.item_name, o.quantity, m.price, (o.quantity * m.price) AS total
        FROM orders o
        JOIN menu m ON o.item_id = m.item_id
        WHERE o.table_no = %s
    """, (table_no,))
    rows = cursor.fetchall()
    db.close()
    return rows
