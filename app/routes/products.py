from flask import Blueprint, render_template, request, redirect, url_for
from app.utils.db import get_db

products_bp = Blueprint("products", __name__, url_prefix="/products")

@products_bp.route("/")
def product_list():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT DISTINCT sku, product_name FROM transactions")
    products = cursor.fetchall()

    result = []
    for p in products:
        cursor.execute("SELECT cost_price FROM product_costs WHERE sku = %s", (p["sku"],))
        cost = cursor.fetchone()
        result.append({
            "sku": p["sku"],
            "product_name": p["product_name"],
            "cost_price": cost["cost_price"] if cost else 0
        })

    return render_template("products.html", products=result)


@products_bp.route("/update", methods=["POST"])
def update_cost():
    sku = request.form["sku"]
    cost_price = float(request.form["cost_price"])
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT 1 FROM product_costs WHERE sku = %s", (sku,))
    if cursor.fetchone():
        cursor.execute("UPDATE product_costs SET cost_price = %s WHERE sku = %s", (cost_price, sku))
    else:
        cursor.execute("INSERT INTO product_costs (sku, cost_price) VALUES (%s, %s)", (sku, cost_price))

    return redirect(url_for("products.product_list"))
