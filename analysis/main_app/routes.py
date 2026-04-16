from flask import Blueprint, render_template

# Create the blueprint for the main app
main_blueprint = Blueprint('main', __name__, template_folder='../templates')

# Define the route for the landing page
@main_blueprint.route("/")
def home():
    return render_template("index.html")
