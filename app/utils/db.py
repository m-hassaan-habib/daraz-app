import pymysql
from flask import g
from pymysql.cursors import DictCursor

db_pool = {}

def init_db(app):
    db_pool["host"] = app.config["MYSQL_HOST"]
    db_pool["user"] = app.config["MYSQL_USER"]
    db_pool["password"] = app.config["MYSQL_PASSWORD"]
    db_pool["database"] = app.config["MYSQL_DB"]

def get_db():
    if "db" not in g:
        g.db = pymysql.connect(
            host=db_pool["host"],
            user=db_pool["user"],
            password=db_pool["password"],
            database=db_pool["database"],
            cursorclass=DictCursor,
            autocommit=True
        )
    return g.db

def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()
