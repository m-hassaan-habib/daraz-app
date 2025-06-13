from flask import Blueprint, render_template
from app.utils.db import get_db
from app.utils.fee_calculator import calculate_order_summary
from collections import defaultdict

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/")
def dashboard_view():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM transactions")
    rows = cursor.fetchall()

    grouped = defaultdict(list)
    for row in rows:
        grouped[row["order_number"]].append(row)

    totals = {
        "revenue": 0,
        "deductions": 0,
        "handling_fee": 0,
        "packing_fee": 0,
        "logistics_fee": 0,
        "final_profit": 0
    }

    for order_rows in grouped.values():
        summary = calculate_order_summary(order_rows)
        for key in totals:
            totals[key] += summary[key]

    return render_template("dashboard.html", totals=totals)

    