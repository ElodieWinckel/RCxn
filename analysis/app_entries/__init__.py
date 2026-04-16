from flask import Blueprint

# Define the blueprint for app_entries
app_entries_blueprint = Blueprint('app_entries', __name__, template_folder='templates')

from . import routes  # Import routes after defining the blueprint
