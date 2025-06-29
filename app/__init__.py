import os
from flask import Flask
from .utils.db import init_db
from .routes.upload import upload_bp
from .routes.orders import orders_bp
from .routes.products import products_bp
from .routes.dashboard import dashboard_bp
from .routes.auth import auth_bp
from app.config import Config
from flask import g, session

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    app.secret_key = os.getenv("SECRET_KEY", "super-secret-dev-key")

    init_db(app)

    app.register_blueprint(upload_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(auth_bp)


    @app.before_request
    def load_user():
        g.current_user = {
            "id": session.get("user_id"),
            "role": session.get("role"),
            "shop_id": session.get("shop_id")
        }
    
    @app.context_processor
    def inject_user():
        return dict(current_user=g.current_user)

    return app
