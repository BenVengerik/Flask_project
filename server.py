from flask import Flask, request, render_template, send_file, redirect, url_for, session
from waitress import serve
from plotter import generate_plot
import json
import os

# Initialize the Flask application
app = Flask(__name__)

app.secret_key = "secret_key"  # Enable session data

SETTINGS_FILE = "settings.json"

# Load settings from file on startup
try:
    with open(SETTINGS_FILE, "r") as f:
        settings = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    settings = {
        "update_time": 3,
        "data_period": 30,
        "alert_thresholds": "placeholder",
        "db_path": "/Users/Ben/Documents/Flask_project/Databases/dblog.db",
        "data_type_colors": {
            "flow": "b",
            "Water_temp": "r",
            "DHT_temp": "g",
            "DHT_hum": "orange"
        }
    }

# Define the route for the home page
@app.route('/', methods=["GET", "POST"])
@app.route('/index', methods=["GET", "POST"])
def index():
    """
    Renders the index.html template and handles the form submission for setting the database path.
    """
    if request.method == "POST":
        if 'db_path' in request.files and request.files['db_path'].filename != '':
            db_path_file = request.files['db_path']
            db_path = os.path.join("/Users/Ben/Documents/Flask_project/Databases", db_path_file.filename)
            db_path_file.save(db_path)
            settings["db_path"] = db_path
        else:
            settings["db_path"] = request.form["current_db_path"]

        # Save settings to file
        with open(SETTINGS_FILE, "w") as f:
            json.dump(settings, f)

        return redirect(url_for("index"))

    return render_template('index.html', settings=settings)

@app.route('/admin/login', methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        if username == "admin" and password == "password":  # Change these later!
            session["admin_logged_in"] = True
            return redirect(url_for("admin_dashboard"))
        else:
            return "Invalid credentials", 401
    
    return render_template("admin_login.html")

@app.route('/admin/logout')
def admin_logout():
    session.pop("admin_logged_in", None)
    return redirect(url_for("admin_login"))

@app.route('/admin', methods=["GET", "POST"])
def admin_dashboard():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))
    
    if request.method == "POST":
        try:
            update_time = request.form["update_time"]
            data_period = request.form["data_period"]
            alert_thresholds = request.form["alert_thresholds"]

            if not update_time or not data_period:
                return "Update time and data period are required.", 400

            settings["update_time"] = int(update_time)
            settings["data_period"] = int(data_period)
            settings["alert_thresholds"] = alert_thresholds

            # Save settings to file
            with open(SETTINGS_FILE, "w") as f:
                json.dump(settings, f)

            return redirect(url_for("admin_dashboard"))
        except ValueError:
            return "Invalid input. Please enter valid numbers for update time and data period.", 400

    return render_template("admin_dashboard.html", settings=settings)

@app.route('/dashboard')
def dashboard():
    """
    Renders the dashboard.html template.
    """

    with open(SETTINGS_FILE, "r") as f:
        settings = json.load(f)

    return render_template("dashboard.html", settings=settings)

@app.route("/plot/<data_type>")
def live_plot(data_type):
    """
    Generates a live plot for a specific data type.
    """
    from datetime import datetime, timedelta
    end_time = datetime.now()
    start_time = end_time - timedelta(minutes=settings["data_period"])  

    img = generate_plot(start_time.strftime("%Y-%m-%d %H:%M:%S"), 
                        end_time.strftime("%Y-%m-%d %H:%M:%S"), 
                        [data_type], 
                        settings["db_path"], 
                        settings["data_type_colors"])

    return send_file(img, mimetype="image/png")

@app.route("/range", methods=["GET","POST"])
def range():
    """
    Renders the range.html template.
    """
    return render_template('range.html')

# Define the route for generating and serving the plot
@app.route("/plot", methods=["GET","POST"])
def plot():
    """
    Generates a plot based on the provided start time, end time, and data types.
    Returns the plot image if successful, otherwise returns an error message.
    """
    # Get the start and end time from the form data
    start_time = request.form["start_time"]
    end_time = request.form["end_time"]
    # Get the selected data types as a list
    data_types = request.form.getlist("data_types")

    # Check if at least one data type is selected
    if not data_types:
        return "Please select at least one data type.", 400  

    # Generate the plot image
    img = generate_plot(start_time, end_time, data_types, settings["db_path"], settings["data_type_colors"])

    # Check if the plot generation was successful
    if img is None:
        return "No data available for the selected time range.", 400  

    # Send the plot image as a response
    return send_file(img, mimetype="image/png")


# Run the application using the Waitress server
if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8000)