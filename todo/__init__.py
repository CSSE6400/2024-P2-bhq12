from flask import Flask
from .views.routes import api
from .models.todo import ToDoDatabaseHelper
import os

def create_app(config_overrides: dict = None):
    print('Create_app')
    app = Flask(__name__)    
    print('Flasked')
    app.register_blueprint(api)
    print('registered blueprint')

    if config_overrides:
        app.config.update(config_overrides)
    
    # Initialise the Database connection,
    # set up tables if not exists
    database_helper = ToDoDatabaseHelper()
    database_helper.instantiate_database_tables()

    return app
