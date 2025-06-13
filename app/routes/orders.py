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
        summary = calculate_order_summary(items)
        orders_data.append({
            "order_number": order_num,
            "product": items[0]["product_name"],
            "sku": items[0]["sku"],
            **summary
        })

    return render_template("orders.html", orders=orders_data)
