from flask import Blueprint

# Define the blueprint for app_form
app_form_blueprint = Blueprint('app_form', __name__, template_folder='templates')

from . import routes  # Import routes after defining the blueprint
