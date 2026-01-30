from flask import Blueprint

# Define the blueprint for app_studies
app_studies_blueprint = Blueprint('app_studies', __name__, template_folder='templates')

from . import routes  # Import routes after defining the blueprint
