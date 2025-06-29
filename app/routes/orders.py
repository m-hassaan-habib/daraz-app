from flask import Blueprint, render_template
from app.utils.db import get_db
from app.utils.fee_calculator import calculate_order_summary
from collections import defaultdict

orders_bp = Blueprint("orders", __name__, url_prefix="/orders")

@orders_bp.route("/")
def orders_view():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM transactions ORDER BY order_number")
    rows = cursor.fetchall()

    grouped = defaultdict(list)
    for row in rows:
        grouped[row["order_number"]].append(row)

    orders_data = []
    for order_num, items in grouped.items():
        product_name = items[0]["product_name"]

        cursor.execute("SELECT cost_price FROM products WHERE product_name = %s", (product_name,))
        cost_row = cursor.fetchone()
        cost_price = cost_row["cost_price"] if cost_row else 0
        
        summary = calculate_order_summary(items, cost_price)
        margin_percent = ((summary["final_profit"] / cost_price) * 100) if cost_price > 0 else 0

        orders_data.append({
            "order_number": order_num,
            "product": product_name,
            "margin_percent": margin_percent,
            **summary
        })

    return render_template("orders.html", orders=orders_data)
