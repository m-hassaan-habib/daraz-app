# app/models/user.py

from app.utils.db import get_db
from werkzeug.security import generate_password_hash, check_password_hash

def create_user(email, password, shop_name):
    db = get_db()
    cur = db.cursor()

    cur.execute("SELECT id FROM users WHERE email = %s", (email,))
    if cur.fetchone():
        return False, "Email already registered"

    username = email.split("@")[0]
    hashed_password = generate_password_hash(password)

    cur.execute(
        "INSERT INTO users (username, email, password, shop_name) VALUES (%s, %s, %s, %s)",
        (username, email, hashed_password, shop_name)
    )
    user_id = cur.lastrowid

    cur.execute(
        "UPDATE users SET shop_id = %s WHERE id = %s",
        (user_id, user_id)
    )

    db.commit()
    return True, "Signup successful"




def get_user_by_email(email):
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
    return cur.fetchone()

def verify_user(email, password):
    user = get_user_by_email(email)
    if user and check_password_hash(user["password"], password):
        return user
    return None

def get_all_users():
    db = get_db()
    cur = db.cursor()
    cur.execute("""
        SELECT u.id, u.email, u.role, u.status, u.last_login, s.shop_name
        FROM users u
        JOIN shops s ON u.shop_id = s.id
    """)
    return cur.fetchall()

def delete_user(user_id):
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
    db.commit()
