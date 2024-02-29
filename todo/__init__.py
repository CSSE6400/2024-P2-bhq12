from flask import Flask
from .views.routes import api
from .models.todo import ToDoDatabaseHelper
import os

def create_app(config_overrides: dict = {}):
    print('Create_app')
    app = Flask(__name__)    
    print('Flasked')
    app.register_blueprint(api)
    print('registered blueprint')

    if config_overrides:
        app.config.update(config_overrides)
    
    # Initialise the Database connection,
    # set up tables if not exists
    print('instantiating database from create_app')
    database_helper = ToDoDatabaseHelper()
    print(f'CONFIG OVERRIDES: {config_overrides}')
    if config_overrides['TESTING'] is True:
        database_helper._instantiate_database_tables_from_scratch_CAREFUL()
    else:
        database_helper.instantiate_database_tables()

    return app
