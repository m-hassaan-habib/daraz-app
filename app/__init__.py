import os
from flask import Flask
from .utils.db import init_db
from .routes.upload import upload_bp
from .routes.orders import orders_bp
from .routes.products import products_bp
from .routes.dashboard import dashboard_bp
from app.config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Create uploads folder if it doesn't exist
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    app.secret_key = os.getenv("SECRET_KEY", "super-secret-dev-key")


    # Initialize MySQL connection pool
    init_db(app)

    # Register Blueprints
    app.register_blueprint(upload_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(dashboard_bp)

    return app
