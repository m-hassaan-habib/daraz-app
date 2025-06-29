import os
from flask import Blueprint, request, redirect, url_for, current_app, flash, render_template
from werkzeug.utils import secure_filename
from app.utils.csv_parser import parse_csv
from app.utils.db import get_db

upload_bp = Blueprint("upload", __name__, url_prefix="/upload")

@upload_bp.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files.get("file")
        if not file or not file.filename.endswith(".csv"):
            flash("Please upload a valid CSV file", "danger")
            return redirect(request.url)

        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

        orders = parse_csv(filepath)
        db = get_db()
        cursor = db.cursor()

        for order_number, rows in orders.items():
            for row in rows:
                product_name = row.get("Product Name", "").strip()

                if product_name:
                    cursor.execute("SELECT 1 FROM products WHERE product_name = %s", (product_name,))
                    if not cursor.fetchone():
                        cursor.execute(
                            "INSERT INTO products (product_name) VALUES (%s)",
                            (product_name,)
                        )

                cursor.execute(
                    """
                    INSERT INTO transactions (
                        order_number, fee_name, amount, product_name
                    ) VALUES (%s, %s, %s, %s)
                    """,
                    (
                        order_number,
                        row.get("Fee Name", ""),
                        row["Amount(Include Tax)"],
                        product_name
                    )
                )

        flash("File uploaded and processed successfully", "success")
        return redirect(url_for("dashboard.dashboard_view"))

    return render_template("upload.html")
