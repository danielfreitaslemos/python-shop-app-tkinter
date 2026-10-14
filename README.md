# Retail Operations & Analytics Manager (Tkinter)

A desktop Point-of-Sale (POS) and inventory management application built using **Python**, **Tkinter (TTK)**, and a localized relational **SQLite** database. 

This application bridges the gap between desktop visual interfaces and persistent data layers. It features an automated checkout flow that instantly recalculates stock metrics and triggers a dynamic business intelligence analytics panel to track your top-selling items.

---

## ⚡ Key Features
- **Tabular Inventory Grid:** Renders real-time warehouse stock, names, and pricing profiles using a decoupled `ttk.Treeview` architecture.
- **Dynamic Point of Sale (POS):** Handles transaction workflows with strict data validations (e.g., stopping checkouts if requested quantity exceeds current warehouse stock).
- **Live Manager Insights:** Runs real-time analytical aggregation queries (`SQL JOIN` and `SUM`) to instantly identify your highest-volume product.
- **Persistent Data Storage:** Runs completely serverless out of a self-contained local `shop.db` file utilizing Python's native `sqlite3` driver.

---

## 🛠️ Tech Stack
- **Language:** Python 3
- **Frontend / UI Framework:** Tkinter & TTK (Themed Widgets)
- **Database Engine:** SQLite3
- **Development Environment:** Zed Editor

---

## 💻 Database Schema Architecture

The relational backend consists of two tables linked via foreign key mapping:

1. **`products` Table:**
   - `product_id` (INTEGER, Primary Key)
   - `name` (TEXT)
   - `price` (REAL)
   - `stock` (INTEGER)

2. **`sales` Table:**
   - `sale_id` (INTEGER, Primary Key)
   - `product_id` (INTEGER, Foreign Key)
   - `quantity_sold` (INTEGER)
   - `sale_date` (TEXT)

---

## 🚀 Installation & Running the Application

1. **Clone the repository:**
   ```bash
   git clone https://github.com
   ```
2. **Navigate into the project directory:**
   ```bash
   cd python-shop-app-tkinter
   ```
3. **Initialize your base database tables and mock data:**
   ```bash
   python3 database.py
   ```
4. **Launch the interactive Point of Sale UI panel:**
   ```bash
   python3 main.py
   ```

*(Note for Linux users: If your Python installation throws an import error on the first line, install the system bindings via your package manager, e.g., `sudo pacman -S tk` or `sudo apt install python3-tk`).*
