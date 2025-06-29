# app/routes/admin.py

from flask import Blueprint, render_template, redirect, url_for
from app.models.user import get_all_users, delete_user
from app.auth import is_admin
from app.decorators import login_required


admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@admin_bp.route("/users")
@login_required
def users():
    if not is_admin():
        return redirect(url_for("auth.login"))
    return render_template("admin_users.html", users=get_all_users())

@admin_bp.route("/users/delete/<int:user_id>")
@login_required
def delete(user_id):
    if not is_admin():
        return redirect(url_for("auth.login"))
    delete_user(user_id)
    return redirect(url_for("admin.users"))
