from main_app import create_app
import os

# Check if the production directory exists
if os.path.exists("/data/www/RCxn"):
    os.chdir("/data/www/RCxn")  # # Set the working directory to the application's production path
#else:
#    os.chdir(os.path.dirname(os.path.abspath(__file__)))  # Development path

app = create_app()

@app.route("/")
def home():
    return "Hello!"

@app.route("/test_static")
def test_static():
    try:
        return send_file("static/css/styles.css")
    except Exception as e:
        return f"Error: {e}", 500


if __name__ == "__main__":
    app.run(debug=True)
