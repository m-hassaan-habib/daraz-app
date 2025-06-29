# app/routes/auth.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.auth.auth import login_user, logout_user
from app.models.user import create_user, verify_user
from app.utils.db import get_db

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = verify_user(request.form["email"], request.form["password"])
        if user:
            login_user(user)
            return redirect(url_for("dashboard.dashboard_view"))
        flash("Invalid credentials")
    return render_template("login.html")

@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        success, msg = create_user(
            request.form["email"],
            request.form["password"],
            request.form["shop_name"]
        )
        flash(msg, "success" if success else "error")
        if success:
            return redirect(url_for("auth.login"))
    return render_template("signup.html")


@auth_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
