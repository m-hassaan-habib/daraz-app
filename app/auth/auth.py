# app/auth/auth.py

from flask import session

def login_user(user):
    session["user_id"] = user["id"]
    session["role"] = user["role"]
    session["shop_id"] = user["shop_id"]

def logout_user():
    session.clear()

def current_user():
    return {
        "id": session.get("user_id"),
        "role": session.get("role"),
        "shop_id": session.get("shop_id")
    }

def is_admin():
    return session.get("role") == "admin"
