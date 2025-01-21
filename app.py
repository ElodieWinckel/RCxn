from main_app import create_app

# Set the working directory to the application's root directory
os.chdir("/data/www/RCxn”)

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