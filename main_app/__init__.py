from flask import Flask
from main_app.routes import main_blueprint
from app_form import app_form_blueprint
from app_entries import app_entries_blueprint
import os

def create_app():

    # Dynamically determine the absolute path to the static folder
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    static_folder_path = os.path.join(project_root, "static")

    app = Flask(
        __name__,
        static_folder=static_folder_path
    )

    # Register blueprints
    app.register_blueprint(main_blueprint)
    app.register_blueprint(app_form_blueprint, url_prefix='/app_form')
    app.register_blueprint(app_entries_blueprint, url_prefix='/app_entries')

    return app
