from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


class DatabaseInterface:
    DB = SQLAlchemy()
    MA = Marshmallow()

    def __init__(self, app):
        DatabaseInterface.DB.init_app(app)
        DatabaseInterface.MA.init_app(app)
