from flask import Blueprint, render_template, redirect, url_for
from app import get_db_connection
from app.models.analytics import Analytics

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/')
def index():
    return redirect(url_for('analytics.analytics'))

@analytics_bp.route('/analytics')
def analytics():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT SUM(revenue), SUM(profit), SUM(costs), SUM(fees), COUNT(*), COUNT(DISTINCT product_name)
        FROM orders
    """)
    result = cursor.fetchone()
    analytics = Analytics(*result) if result else Analytics(0, 0, 0, 0, 0, 0)
    cursor.close()
    conn.close()
    return render_template('dashboard.html', analytics=analytics)