import sqlite3
import os
import hashlib
from datetime import datetime

DB_PATH = "threadco.db"

def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def init_db():
    conn = get_conn()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'customer',
            created_at TEXT DEFAULT (datetime('now'))
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            original_price REAL,
            category_id INTEGER,
            stock INTEGER DEFAULT 0,
            sizes TEXT DEFAULT 'S,M,L,XL',
            colors TEXT DEFAULT 'Black,White',
            image_url TEXT,
            badge TEXT DEFAULT '',
            is_active INTEGER DEFAULT 1,
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (category_id) REFERENCES categories(id)
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            total REAL NOT NULL,
            status TEXT DEFAULT 'Pending',
            shipping_name TEXT,
            shipping_address TEXT,
            shipping_city TEXT,
            shipping_phone TEXT,
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            product_name TEXT NOT NULL,
            size TEXT,
            color TEXT,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    """)
    conn.commit()
    if c.execute("SELECT COUNT(*) FROM users").fetchone()[0] == 0:
        _seed_data(c, conn)
    conn.close()

def _seed_data(c, conn):
    c.execute("INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)",
              ("Admin", "admin@threadco.com", hash_password("admin123"), "admin"))
    c.execute("INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)",
              ("John Doe", "john@example.com", hash_password("customer123"), "customer"))
    categories = ["T-Shirts", "Shirts", "Jackets", "Jeans", "Hoodies", "Accessories"]
    for cat in categories:
        c.execute("INSERT INTO categories (name) VALUES (?)", (cat,))
    products = [
        ("Classic White Tee", "Premium 100% cotton classic fit t-shirt.", 29.99, None, 1, 50, "S,M,L,XL,XXL", "White,Black,Gray", "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400", "new"),
        ("Oxford Button Shirt", "Slim-fit Oxford shirt for casual and semi-formal.", 59.99, 79.99, 2, 30, "S,M,L,XL", "Blue,White,Pink", "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=400", "sale"),
        ("Varsity Jacket", "Retro-inspired varsity jacket with ribbed cuffs.", 129.99, None, 3, 20, "S,M,L,XL", "Black,Navy,Red", "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400", "featured"),
        ("Slim Fit Jeans", "Modern slim-fit jeans from premium stretch denim.", 79.99, 99.99, 4, 40, "28,30,32,34,36", "Indigo,Black,Light Blue", "https://images.unsplash.com/photo-1542272604-787c3835535d?w=400", "sale"),
        ("Pullover Hoodie", "Ultra-soft fleece hoodie for cooler weather.", 69.99, None, 5, 35, "S,M,L,XL,XXL", "Gray,Black,Navy", "https://images.unsplash.com/photo-1556821840-3a63f15732ce?w=400", "new"),
        ("Graphic Print Tee", "Limited edition graphic tee, 100% organic cotton.", 34.99, None, 1, 25, "S,M,L,XL", "White,Black", "https://images.unsplash.com/photo-1503341504253-dff4815485f1?w=400", "featured"),
        ("Linen Summer Shirt", "Lightweight linen shirt for warm weather.", 54.99, None, 2, 28, "S,M,L,XL", "Beige,White,Sky Blue", "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=400", ""),
        ("Cargo Joggers", "Versatile cargo joggers with multiple pockets.", 64.99, 84.99, 4, 45, "S,M,L,XL,XXL", "Olive,Black,Khaki", "https://images.unsplash.com/photo-1473966968600-fa801b869a1a?w=400", "sale"),
        ("Bomber Jacket", "Classic bomber jacket, lightweight and stylish.", 119.99, None, 3, 15, "S,M,L,XL", "Olive,Black,Navy", "https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=400", "featured"),
        ("Stripe Polo Shirt", "Pique cotton polo with classic stripe pattern.", 44.99, None, 2, 33, "S,M,L,XL", "Navy/White,Red/White", "https://images.unsplash.com/photo-1571945153237-4929e783af4a?w=400", ""),
        ("Zip-Up Hoodie", "Lightweight zip-up hoodie with kangaroo pocket.", 74.99, 89.99, 5, 22, "S,M,L,XL", "Black,Gray,Burgundy", "https://images.unsplash.com/photo-1620799140408-edc6dcb6d633?w=400", "sale"),
        ("Canvas Tote Bag", "Durable canvas tote with interior pocket.", 24.99, None, 6, 60, "One Size", "Natural,Black,Navy", "https://images.unsplash.com/photo-1544816565-aa8c1166648f?w=400", "new"),
    ]
    for p in products:
        c.execute("""INSERT INTO products
            (name, description, price, original_price, category_id, stock, sizes, colors, image_url, badge)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", p)
    conn.commit()

def get_user_by_email(email):
    conn = get_conn()
    user = conn.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
    conn.close()
    return user

def create_user(name, email, password):
    conn = get_conn()
    try:
        conn.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                     (name, email, hash_password(password)))
        conn.commit()
        return True, "Account created successfully!"
    except sqlite3.IntegrityError:
        return False, "Email already registered."
    finally:
        conn.close()

def update_user_profile(user_id, name, email):
    conn = get_conn()
    try:
        conn.execute("UPDATE users SET name=?, email=? WHERE id=?", (name, email, user_id))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def change_password(user_id, old_pw, new_pw):
    conn = get_conn()
    user = conn.execute("SELECT password FROM users WHERE id=?", (user_id,)).fetchone()
    if user and user["password"] == hash_password(old_pw):
        conn.execute("UPDATE users SET password=? WHERE id=?", (hash_password(new_pw), user_id))
        conn.commit()
        conn.close()
        return True, "Password updated!"
    conn.close()
    return False, "Old password is incorrect."

def authenticate(email, password):
    user = get_user_by_email(email)
    if user and user["password"] == hash_password(password):
        return dict(user)
    return None

def get_all_products(active_only=True, category_id=None, search=None):
    conn = get_conn()
    sql = "SELECT p.*, c.name as category_name FROM products p LEFT JOIN categories c ON p.category_id = c.id WHERE 1=1"
    params = []
    if active_only:
        sql += " AND p.is_active = 1"
    if category_id:
        sql += " AND p.category_id = ?"
        params.append(category_id)
    if search:
        sql += " AND (p.name LIKE ? OR p.description LIKE ?)"
        params += [f"%{search}%", f"%{search}%"]
    sql += " ORDER BY p.id DESC"
    rows = conn.execute(sql, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_product_by_id(product_id):
    conn = get_conn()
    row = conn.execute("SELECT p.*, c.name as category_name FROM products p LEFT JOIN categories c ON p.category_id = c.id WHERE p.id=?", (product_id,)).fetchone()
    conn.close()
    return dict(row) if row else None

def get_featured_products(limit=6):
    conn = get_conn()
    rows = conn.execute("SELECT p.*, c.name as category_name FROM products p LEFT JOIN categories c ON p.category_id = c.id WHERE p.is_active=1 AND (p.badge='featured' OR p.badge='new') ORDER BY p.id DESC LIMIT ?", (limit,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def create_product(name, description, price, original_price, category_id, stock, sizes, colors, image_url, badge):
    conn = get_conn()
    conn.execute("INSERT INTO products (name, description, price, original_price, category_id, stock, sizes, colors, image_url, badge) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                 (name, description, price, original_price, category_id, stock, sizes, colors, image_url, badge))
    conn.commit()
    conn.close()

def update_product(pid, name, description, price, original_price, category_id, stock, sizes, colors, image_url, badge, is_active):
    conn = get_conn()
    conn.execute("UPDATE products SET name=?, description=?, price=?, original_price=?, category_id=?, stock=?, sizes=?, colors=?, image_url=?, badge=?, is_active=? WHERE id=?",
                 (name, description, price, original_price, category_id, stock, sizes, colors, image_url, badge, is_active, pid))
    conn.commit()
    conn.close()

def delete_product(pid):
    conn = get_conn()
    conn.execute("DELETE FROM products WHERE id=?", (pid,))
    conn.commit()
    conn.close()

def update_stock(product_id, quantity):
    conn = get_conn()
    conn.execute("UPDATE products SET stock = stock - ? WHERE id=?", (quantity, product_id))
    conn.commit()
    conn.close()

def get_all_categories():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM categories ORDER BY name").fetchall()
    conn.close()
    return [dict(r) for r in rows]

def create_category(name):
    conn = get_conn()
    try:
        conn.execute("INSERT INTO categories (name) VALUES (?)", (name,))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def create_order(user_id, cart_items, total, shipping):
    conn = get_conn()
    c = conn.cursor()
    c.execute("INSERT INTO orders (user_id, total, shipping_name, shipping_address, shipping_city, shipping_phone) VALUES (?, ?, ?, ?, ?, ?)",
              (user_id, total, shipping["name"], shipping["address"], shipping["city"], shipping["phone"]))
    order_id = c.lastrowid
    for item in cart_items:
        c.execute("INSERT INTO order_items (order_id, product_id, product_name, size, color, quantity, price) VALUES (?, ?, ?, ?, ?, ?, ?)",
                  (order_id, item["id"], item["name"], item.get("size",""), item.get("color",""), item["qty"], item["price"]))
        update_stock(item["id"], item["qty"])
    conn.commit()
    conn.close()
    return order_id

def get_user_orders(user_id):
    conn = get_conn()
    rows = conn.execute("SELECT * FROM orders WHERE user_id=? ORDER BY created_at DESC", (user_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_order_items(order_id):
    conn = get_conn()
    rows = conn.execute("SELECT * FROM order_items WHERE order_id=?", (order_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_all_orders():
    conn = get_conn()
    rows = conn.execute("SELECT o.*, u.name as customer_name, u.email FROM orders o JOIN users u ON o.user_id = u.id ORDER BY o.created_at DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]

def update_order_status(order_id, status):
    conn = get_conn()
    conn.execute("UPDATE orders SET status=? WHERE id=?", (status, order_id))
    conn.commit()
    conn.close()

def get_dashboard_stats():
    conn = get_conn()
    stats = {
        "total_users": conn.execute("SELECT COUNT(*) FROM users WHERE role='customer'").fetchone()[0],
        "total_products": conn.execute("SELECT COUNT(*) FROM products WHERE is_active=1").fetchone()[0],
        "total_orders": conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0],
        "total_revenue": conn.execute("SELECT COALESCE(SUM(total),0) FROM orders WHERE status!='Cancelled'").fetchone()[0],
        "pending_orders": conn.execute("SELECT COUNT(*) FROM orders WHERE status='Pending'").fetchone()[0],
        "low_stock": conn.execute("SELECT COUNT(*) FROM products WHERE stock < 5 AND is_active=1").fetchone()[0],
    }
    conn.close()
    return stats

def get_all_users():
    conn = get_conn()
    rows = conn.execute("SELECT id, name, email, role, created_at FROM users ORDER BY created_at DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]
