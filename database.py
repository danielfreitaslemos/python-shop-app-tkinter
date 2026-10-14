import sqlite3
from datetime import datetime

DB_NAME = "shop.db"

def init_db():
    """Initializes the database and creates the required retail tables."""
    # Connect to the database file (it will be created if it doesn't exist)
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # 1. Create the Products Table (The Inventory)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    """)

    # 2. Create the Sales Table (The Sales Log)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            quantity_sold INTEGER NOT NULL,
            sale_date TEXT NOT NULL,
            FOREIGN KEY (product_id) REFERENCES products (product_id)
        )
    """)

    conn.commit()
    conn.close()
    print("Database and structural tables successfully initialized!")

def seed_data():
    """Populates the database with initial testing items if empty."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Check if we already have products so we don't duplicate them every run
    cursor.execute("SELECT COUNT(*) FROM products")
    if cursor.fetchone()[0] == 0:
        # Mock Inventory: Name, Price, Initial Stock Level
        mock_products = [
            ("Python Programming Book", 45.90, 15),
            ("Mechanical Keyboard", 120.00, 8),
            ("Wireless Ergonomic Mouse", 59.99, 25),
            ("USB-C Hub Adapter", 24.50, 40)
        ]

        cursor.executemany(
            "INSERT INTO products (name, price, stock) VALUES (?, ?, ?)",
            mock_products
        )
        conn.commit()
        print("Initial inventory successfully seeded!")
    else:
        print("Inventory already contains data. Skipping seeding.")

    conn.close()

# This block ensures the code only runs if you execute this file directly
if __name__ == "__main__":
    init_db()
    seed_data()

# FUNCTION FOR THE UI REQUEST THE DATA
def get_all_products():
    """Fetches all items from the inventory table."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT product_id, name, price, stock FROM products")
    products = cursor.fetchall()  # This returns a list of tuples
    conn.close()
    return products


# FUNCTION TO UPDATE THE PRODUCTS DATABASE
def make_sale(product_id, quantity_to_sell):
    """Processes a sale by recording it and subtracting from stock.
    Returns (True, 'Success message') or (False, 'Error message').
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # 1. Check if the product exists and read its current stock level
    cursor.execute("SELECT name, stock FROM products WHERE product_id = ?", (product_id,))
    product = cursor.fetchone()

    if not product:
        conn.close()
        return False, "Product not found!"

    product_name, current_stock = product

    # 2. Safety Check: Verify we actually have enough stock on hand
    if current_stock < quantity_to_sell:
        conn.close()
        return False, f"Not enough stock! Only {current_stock} units left of '{product_name}'."

    # 3. Process Transaction: Subtract from inventory stock levels
    new_stock = current_stock - quantity_to_sell
    cursor.execute("UPDATE products SET stock = ? WHERE product_id = ?", (new_stock, product_id))

    # 4. Process Transaction: Insert a new record into the sales log table
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO sales (product_id, quantity_sold, sale_date) VALUES (?, ?, ?)",
        (product_id, quantity_to_sell, current_time)
    )

    conn.commit()
    conn.close()
    return True, f"Successfully sold {quantity_to_sell}x '{product_name}'!"

# FUNCTION TO GET THE BEST SELLER
def get_best_seller():
    """Analyzes transaction records to find the product with the highest total units sold."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # We use a SQL JOIN to pull the product name while SUMming up quantities
    cursor.execute("""
        SELECT p.name, SUM(s.quantity_sold) as total_sold
        FROM sales s
        JOIN products p ON s.product_id = p.product_id
        GROUP BY s.product_id
        ORDER BY total_sold DESC
        LIMIT 1
    """)
    result = cursor.fetchone()
    conn.close()

    if result:
        return result  # Returns a tuple: ("Product Name", total_units_sold)
    return ("No sales recorded yet", 0)
