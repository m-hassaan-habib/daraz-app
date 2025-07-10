from flask import Blueprint, render_template
from app.utils.db import get_db
from app.utils.fee_calculator import calculate_order_summary
from collections import defaultdict
from app.decorators import login_required
from app.auth.auth import current_user
from flask import redirect, url_for, flash, request

orders_bp = Blueprint("orders", __name__, url_prefix="/orders")

@orders_bp.route("/")
@login_required
def orders_view():
    db = get_db()
    cursor = db.cursor()
    shop_id = current_user()["shop_id"]

    page = int(request.args.get("page", 1))
    per_page = 20
    offset = (page - 1) * per_page
    q = request.args.get("q", "").strip()

    query = "SELECT * FROM transactions WHERE shop_id = %s"
    params = [shop_id]

    if q:
        query += " AND (order_number LIKE %s OR product_name LIKE %s)"
        like_q = f"%{q}%"
        params.extend([like_q, like_q])

    query += " ORDER BY order_number LIMIT %s OFFSET %s"
    params.extend([per_page, offset])

    cursor.execute(query, params)
    rows = cursor.fetchall()

    count_query = "SELECT COUNT(DISTINCT order_number) AS count FROM transactions WHERE shop_id = %s"
    count_params = [shop_id]

    if q:
        count_query += " AND (order_number LIKE %s OR product_name LIKE %s)"
        count_params.extend([like_q, like_q])

    cursor.execute(count_query, count_params)
    row = cursor.fetchone()
    total_orders = row["count"] if row else 0

    total_pages = (total_orders + per_page - 1) // per_page
    start_page = max(1, page - 2)
    end_page = min(total_pages, page + 2)

    grouped = defaultdict(list)
    for row in rows:
        grouped[row["order_number"]].append(row)

    orders_data = []
    for order_num, items in grouped.items():
        product_name = items[0]["product_name"]

        cursor.execute(
            "SELECT cost_price FROM products WHERE product_name = %s AND shop_id = %s",
            (product_name, shop_id)
        )
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

    return render_template(
        "orders.html",
        orders=orders_data,
        page=page,
        total_pages=total_pages,
        start_page=start_page,
        end_page=end_page,
        q=q
    )


@orders_bp.route("/delete/<order_number>", methods=["POST"])
@login_required
def delete_order(order_number):
    db = get_db()
    cursor = db.cursor()
    shop_id = current_user()["shop_id"]

    cursor.execute("DELETE FROM transactions WHERE order_number = %s AND shop_id = %s", (order_number, shop_id))
    db.commit()
    flash(f"Order {order_number} deleted successfully", "success")
    return redirect(url_for("orders.orders_view"))
