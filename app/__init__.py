from flask import Flask
from instance.config import app_config
from manage import DbSetup


def create_app(config):
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.config.from_object(app_config[config])

    myDb = DbSetup()
    myDb.createTables()
    myDb.create_default_admin()

    return app
