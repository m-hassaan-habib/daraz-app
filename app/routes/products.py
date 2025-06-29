from flask import Blueprint, render_template, request, redirect, url_for
from app.utils.db import get_db

products_bp = Blueprint("products", __name__, url_prefix="/products")

@products_bp.route("/")
def product_list():
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        SELECT 
            p.product_name,
            p.cost_price,
            COUNT(DISTINCT t.order_number) AS total_orders,
            SUM(CASE WHEN t.fee_name = 'Item Price' THEN t.amount ELSE 0 END) AS revenue,
            SUM(CASE WHEN t.fee_name = 'Item Price' THEN (t.amount - IFNULL(p.cost_price, 0)) ELSE 0 END) AS profit
        FROM products p
        LEFT JOIN transactions t ON p.product_name = t.product_name
        GROUP BY p.product_name, p.cost_price
        ORDER BY p.product_name
    """)
    products = cursor.fetchall()
    return render_template("products.html", products=products)




@products_bp.route("/update", methods=["POST"])
def update_cost():
    idx = request.form.get("row_index")
    product_name = request.form.get(f"product_name_{idx}")
    cost_price = float(request.form.get(f"cost_price_{idx}"))

    db = get_db()
    cursor = db.cursor()
    cursor.execute("UPDATE products SET cost_price = %s WHERE product_name = %s", (cost_price, product_name))
    return redirect(url_for("products.product_list"))
