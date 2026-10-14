import tkinter as tk
from tkinter import messagebox, ttk

import database

root = tk.Tk()
root.title("Retail Operations & Inventory Manager")
root.geometry("700x680")  # Expanded height to neatly fit the analytics block
root.configure(bg="#f3f4f6")

# --- 📦 INVENTORY SECTION ---
header_label = tk.Label(
    root,
    text="📦 Current Inventory Levels",
    font=("Arial", 16, "bold"),
    bg="#f3f4f6",
    fg="#1f2937",
)
header_label.pack(pady=15)

frame = tk.Frame(root, bg="#f3f4f6")
frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)

columns = ("id", "name", "price", "stock")
tree = ttk.Treeview(frame, columns=columns, show="headings", selectmode="browse")

tree.heading("id", text="Product ID")
tree.heading("name", text="Product Name")
tree.heading("price", text="Selling Price")
tree.heading("stock", text="Stock Quantity")

tree.column("id", width=80, anchor=tk.CENTER)
tree.column("name", width=250, anchor=tk.W)
tree.column("price", width=120, anchor=tk.E)
tree.column("stock", width=100, anchor=tk.CENTER)
tree.pack(fill=tk.BOTH, expand=True)

# --- 🛒 CHECKOUT PANEL SECTION ---
checkout_frame = tk.LabelFrame(
    root,
    text="🛒 Point of Sale Checkout",
    font=("Arial", 11, "bold"),
    bg="#f3f4f6",
    fg="#374151",
    padx=15,
    pady=15,
)
checkout_frame.pack(fill=tk.X, padx=20, pady=10)

tk.Label(
    checkout_frame, text="Selected Product ID:", font=("Arial", 10), bg="#f3f4f6"
).grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
selected_id_entry = tk.Entry(
    checkout_frame, width=10, font=("Arial", 10), state="readonly"
)
selected_id_entry.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)

tk.Label(
    checkout_frame, text="Quantity to Sell:", font=("Arial", 10), bg="#f3f4f6"
).grid(row=0, column=2, sticky=tk.W, padx=20, pady=5)
quantity_entry = tk.Entry(checkout_frame, width=10, font=("Arial", 10))
quantity_entry.insert(0, "1")
quantity_entry.grid(row=0, column=3, sticky=tk.W, padx=5, pady=5)

# ----------------------------------------------------
# 📊 NEW: ANALYTICS & INSIGHTS FRAME
# ----------------------------------------------------
analytics_frame = tk.LabelFrame(
    root,
    text="📊 Manager Insights & Business Reporting",
    font=("Arial", 11, "bold"),
    bg="#f3f4f6",
    fg="#374151",
    padx=15,
    pady=15,
)
analytics_frame.pack(fill=tk.X, padx=20, pady=15)

# Visual Readout Components
best_seller_label = tk.Label(
    analytics_frame,
    text="Top Performing Product: Loading...",
    font=("Arial", 11, "italic"),
    bg="#f3f4f6",
    fg="#2563eb",  # Royal blue highlight color
)
best_seller_label.pack(anchor=tk.W, pady=5)


def update_analytics_view():
    """Queries historical transaction trends to dynamically refresh data fields."""
    name, volume = database.get_best_seller()
    if volume > 0:
        best_seller_label.config(
            text=f"🔥 Top Performing Product: {name} ({volume} units sold total)",
            font=("Arial", 11, "bold"),
        )
    else:
        best_seller_label.config(
            text="📊 Top Performing Product: No sales recorded yet."
        )


# --- Row Selection Mechanism ---
def on_row_select(event):
    selected_item = tree.selection()
    if not selected_item:
        return
    row_values = tree.item(selected_item, "values")
    product_id = row_values[0]

    selected_id_entry.config(state="normal")
    selected_id_entry.delete(0, tk.END)
    selected_id_entry.insert(0, product_id)
    selected_id_entry.config(state="readonly")


tree.bind("<<TreeviewSelect>>", on_row_select)


# --- Sale Submission Mechanism ---
def execute_sale():
    prod_id = selected_id_entry.get()
    qty_text = quantity_entry.get()

    if not prod_id:
        messagebox.showwarning(
            "Validation Error", "Please select a product from the table first!"
        )
        return

    try:
        qty = int(qty_text)
        if qty <= 0:
            raise ValueError()
    except ValueError:
        messagebox.showwarning(
            "Validation Error",
            "Please enter a valid positive whole number for Quantity!",
        )
        return

    success, message = database.make_sale(int(prod_id), qty)

    if success:
        messagebox.showinfo("Transaction Complete", message)
        load_inventory_data()  # Update inventory values row text
        update_analytics_view()  # Dynamically updates your analytics values instantly!
        quantity_entry.delete(0, tk.END)
        quantity_entry.insert(0, "1")
    else:
        messagebox.showerror("Transaction Failed", message)


sell_button = tk.Button(
    checkout_frame,
    text="Complete Checkout Sale 💸",
    font=("Arial", 10, "bold"),
    bg="#10b981",
    fg="white",
    activebackground="#059669",
    padx=10,
    command=execute_sale,
)
sell_button.grid(row=0, column=4, padx=30, pady=5)


# --- Load Dynamic Layouts ---
def load_inventory_data():
    for item in tree.get_children():
        tree.delete(item)
    inventory_items = database.get_all_products()
    for row in inventory_items:
        formatted_row = (row[0], row[1], f"${row[2]:.2f}", row[3])
        tree.insert("", tk.END, values=formatted_row)


# Initialize data and reporting logs on application startup
load_inventory_data()
update_analytics_view()

root.mainloop()
