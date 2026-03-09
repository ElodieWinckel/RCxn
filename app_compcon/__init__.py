from flask import Blueprint

# Define the blueprint for app_comcon
app_compcon_blueprint = Blueprint('app_compcon', __name__, template_folder='templates')

from . import routes  # Import routes after defining the blueprint
