from flask import Flask, request, render_template, send_file, redirect, url_for, session, flash
from waitress import serve
from plotter import generate_plot
import json
import os
import sqlite3
import csv
import subprocess

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
        try:
            if 'db_path' in request.files and request.files['db_path'].filename != '':
                db_path_file = request.files['db_path']
                db_path = os.path.join("/Users/Ben/Documents/Flask_project/Databases", db_path_file.filename)
                db_path_file.save(db_path)
                settings["db_path"] = db_path
                flash("Database path updated successfully.")
            else:
                settings["db_path"] = request.form["current_db_path"]
                
            # Save settings to file
            with open(SETTINGS_FILE, "w") as f:
                json.dump(settings, f)

            return redirect(url_for("index"))
        except Exception as e:
            flash(f"An error occurred while updating the database path: {e}", "error")
            return redirect(url_for("index"))

    return render_template('index.html', settings=settings)

@app.route('/admin/login', methods=["GET", "POST"])
def admin_login():
    """
    Renders the admin login page and handles the login form submission.
    """
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        if username == "admin" and password == "password":  # HARD CODED PASSWORD
            session["admin_logged_in"] = True
            flash("Logged in successfully.")
            return redirect(url_for("admin_dashboard"))
        else:
            flash("Invalid credentials.", "error")
            return render_template("admin_login.html"), 401
    
    return render_template("admin_login.html")

@app.route('/admin/logout')
def admin_logout():
    """
    Logs out the admin user and redirects to the dashboard.
    """
    session.pop("admin_logged_in", None)
    flash("Logged out successfully.")
    return redirect(url_for("dashboard"))

@app.route('/admin', methods=["GET", "POST"])
def admin_dashboard():
    """
    Renders the admin dashboard and handles the form submission for updating settings.
    """
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))
    
    if request.method == "POST":
        try:
            update_time = request.form["update_time"]
            data_period = request.form["data_period"]
            alert_thresholds = request.form["alert_thresholds"]

            if not update_time or not data_period:
                flash("Update time and data period are required.", "error")
                return redirect(url_for("admin_dashboard"))

            settings["update_time"] = int(update_time)
            settings["data_period"] = int(data_period)
            settings["alert_thresholds"] = alert_thresholds

            # Save settings to file
            with open(SETTINGS_FILE, "w") as f:
                json.dump(settings, f)

            flash("Settings updated successfully.")
            return redirect(url_for("admin_dashboard"))
        except ValueError:
            flash("Invalid input. Please enter valid numbers for update time and data period.", "error")
            return redirect(url_for("admin_dashboard"))
        except Exception as e:
            flash(f"An error occurred while updating settings: {e}", "error")
            return redirect(url_for("admin_dashboard"))

    return render_template("admin_dashboard.html", settings=settings)

@app.route('/admin/update_db_path', methods=["POST"])
def update_db_path():
    """
    Handles the form submission for updating the database path.
    """
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))
    try:
        if 'db_path' in request.files and request.files['db_path'].filename != '':
            db_path_file = request.files['db_path']
            db_path = os.path.join("/Users/Ben/Documents/Flask_project/Databases", db_path_file.filename)
            db_path_file.save(db_path)
            settings["db_path"] = db_path
            
            # Save settings to file
            with open(SETTINGS_FILE, "w") as f:
                json.dump(settings, f)

            flash("Database path updated successfully.")
        else:
            flash("No file selected for updating the database path.", "error")
        return redirect(url_for("admin_dashboard"))
    except Exception as e:
        flash(f"An error occurred while updating the database path: {e}", "error")
        return redirect(url_for("admin_dashboard"))

@app.route('/admin/execute_query', methods=["POST"])
def execute_query():
    """
    Handles the form submission for executing SQL queries.
    """
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))
    try:
        sql_query = request.form["sql_query"]
        
        # Connect to the database
        con = sqlite3.connect(settings["db_path"])
        cursor = con.cursor()
        
        # Execute the query
        cursor.execute(sql_query)
        con.commit()
        
        # Fetch the results if it's a SELECT query
        if sql_query.strip().lower().startswith("select"):
            rows = cursor.fetchall()
            columns = [description[0] for description in cursor.description]
            con.close()
            return render_template("query_results.html", rows=rows, columns=columns)
        
        con.close()
        flash("Query executed successfully.")
        return redirect(url_for("admin_dashboard"))
    except sqlite3.Error as e:
        flash(f"An error occurred while executing the query: {e}", "error")
        return redirect(url_for("admin_dashboard"))
    except Exception as e:
        flash(f"An error occurred: {e}", "error")
        return redirect(url_for("admin_dashboard"))

@app.route('/admin/execute_cli', methods=["POST"])
def execute_cli():
    """
    Handles the form submission for executing CLI commands.
    """
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))
    try:
        cli_command = request.form["cli_command"]
        
        # Execute the CLI command
        result = subprocess.run(cli_command, shell=True, capture_output=True, text=True)
        
        # Capture the output and errors
        output = result.stdout
        error = result.stderr
        
        return render_template("cli_results.html", command=cli_command, output=output, error=error)
    except Exception as e:
        flash(f"An error occurred while executing the CLI command: {e}", "error")
        return redirect(url_for("admin_dashboard"))

@app.route('/dashboard')
def dashboard():
    """
    Renders the dashboard.html template.
    """
    try:
        with open(SETTINGS_FILE, "r") as f:
            settings = json.load(f)
    except Exception as e:
        flash(f"An error occurred while loading settings: {e}", "error")
        return redirect(url_for("dashboard"))

    return render_template("dashboard.html", settings=settings)

@app.route("/plot/check")
def check_data():
    """
    Checks if data is available for the selected time range.
    """
    from datetime import datetime, timedelta
    try:
        end_time = datetime.now()
        start_time = end_time - timedelta(minutes=settings["data_period"])

        # Check if data is available
        con = sqlite3.connect(settings["db_path"])
        cursor = con.cursor()
        query = f"""
        SELECT COUNT(*) 
        FROM temlog 
        WHERE timestamp BETWEEN '{start_time.strftime("%Y-%m-%d %H:%M:%S")}' AND '{end_time.strftime("%Y-%m-%d %H:%M:%S")}'
        """
        cursor.execute(query)
        count = cursor.fetchone()[0]
        con.close()

        if count == 0:
            return "No data available", 400
        return "Data available", 200
    except sqlite3.Error as e:
        flash(f"An error occurred while accessing the database: {e}", "error")
        return "Database error", 500
    except Exception as e:
        flash(f"An error occurred while checking data availability: {e}", "error")
        return "Error checking data availability", 500

@app.route("/plot/<data_type>")
def live_plot(data_type):
    """
    Generates a live plot for a specific data type.
    """
    from datetime import datetime, timedelta
    try:
        end_time = datetime.now()
        start_time = end_time - timedelta(minutes=settings["data_period"])  

        img = generate_plot(start_time.strftime("%Y-%m-%d %H:%M:%S"), 
                            end_time.strftime("%Y-%m-%d %H:%M:%S"), 
                            [data_type], 
                            settings["db_path"], 
                            settings["data_type_colors"])

        if img is None:
            flash("No data available for the selected time range.", "error")
            return "No data available for the selected time range.", 400  

        return send_file(img, mimetype="image/png")
    except sqlite3.Error as e:
        flash(f"An error occurred while accessing the database: {e}", "error")
        return "Database error", 500
    except Exception as e:
        flash(f"An error occurred while generating the plot: {e}", "error")
        return "Error generating plot", 500

@app.route("/range", methods=["GET","POST"])
def range():
    """
    Renders the range.html template.
    """
    return render_template('range.html')

@app.route("/plot", methods=["POST"])
def plot():
    """
    Generates a plot based on the provided start time, end time, and data types.
    Returns the plot image if successful, otherwise returns an error message.
    """
    try:
        # Get the start and end time from the form data
        start_time = request.form["start_time"]
        end_time = request.form["end_time"]
        # Get the selected data types as a list
        data_types = request.form.getlist("data_types")

        # Check if at least one data type is selected
        if not data_types:
            flash("Please select at least one data type.", "error")
            return "Please select at least one data type.", 400  

        # Generate the plot image
        img = generate_plot(start_time, end_time, data_types, settings["db_path"], settings["data_type_colors"])

        if img is None:
            flash("No data available for the selected time range.", "error")
            return "No data available for the selected time range.", 400  

        return send_file(img, mimetype="image/png")
    except sqlite3.Error as e:
        flash(f"An error occurred while accessing the database: {e}", "error")
        return "Database error", 500
    except Exception as e:
        flash(f"An error occurred while generating the plot: {e}", "error")
        return "Error generating plot", 500

@app.route("/generate_plot", methods=["POST"])
def generate_plot_route():
    """
    Generates a plot based on the provided start and end time, and data types.
    Renders the plot_result.html template with the plot image and download options.
    """
    try:
        # Get the start and end time from the form data
        start_time = request.form["start_time"]
        end_time = request.form["end_time"]
        # Get the selected data types as a list
        data_types = request.form.getlist("data_types")

        # Check if at least one data type is selected
        if not data_types:
            flash("Please select at least one data type.", "error")
            return redirect(url_for("range"))

        # Generate the plot image
        img = generate_plot(start_time, end_time, data_types, settings["db_path"], settings["data_type_colors"])

        if img is None:
            flash("No data available for the selected time range.", "error")
            return redirect(url_for("range"))

        # Save the plot image to the static folder
        plot_path = os.path.join(app.static_folder, "plot.png")
        with open(plot_path, "wb") as f:
            f.write(img.getbuffer())

        # Render the plot_result.html template with the plot image and download options
        return render_template("plot_result.html", plot_url=url_for('static', filename='plot.png'), start_time=start_time, end_time=end_time, data_types=",".join(data_types))
    except sqlite3.Error as e:
        flash(f"An error occurred while accessing the database: {e}", "error")
        return redirect(url_for("range"))
    except Exception as e:
        flash(f"An error occurred while generating the plot: {e}", "error")
        return redirect(url_for("range"))

@app.route("/export_plot", methods=["POST"])
def export_plot():
    """
    Exports the plot image based on the provided start time, end time, and data types.
    """
    try:
        # Get the start and end time from the form data
        start_time = request.form["start_time"]
        end_time = request.form["end_time"]
        # Get the selected data types as a list
        data_types = request.form["data_types"].split(',')

        # Generate the plot image
        img = generate_plot(start_time, end_time, data_types, settings["db_path"], settings["data_type_colors"])

        if img is None:
            flash("No data available for the selected time range.", "error")
            return redirect(url_for("range"))

        return send_file(img, mimetype="image/png", as_attachment=True, download_name="plot.png")
    except sqlite3.Error as e:
        flash(f"An error occurred while accessing the database: {e}", "error")
        return redirect(url_for("range"))
    except Exception as e:
        flash(f"An error occurred while exporting the plot: {e}", "error")
        return redirect(url_for("range"))

@app.route("/download_data", methods=["POST"])
def download_data():
    """
    Downloads the raw data based on the provided start time, end time, and data types.
    """
    try:
        # Get the start and end time from the form data
        start_time = request.form["start_time"]
        end_time = request.form["end_time"]
        # Get the selected data types as a list
        data_types = request.form["data_types"].split(',')

        # Connect to the database
        con = sqlite3.connect(settings["db_path"])
        cursor = con.cursor()

        # Query to get the raw data
        query = f"""
        SELECT timestamp, {', '.join(data_types)}
        FROM temlog
        WHERE timestamp BETWEEN '{start_time}' AND '{end_time}'
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        con.close()

        # Create a CSV file with the raw data
        csv_file = "/tmp/raw_data.csv"
        with open(csv_file, "w") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp"] + data_types)
            writer.writerows(rows)

        return send_file(csv_file, mimetype="text/csv", as_attachment=True, download_name="raw_data.csv")
    except sqlite3.Error as e:
        flash(f"An error occurred while accessing the database: {e}", "error")
        return redirect(url_for("range"))
    except Exception as e:
        flash(f"An error occurred while downloading the data: {e}", "error")
        return redirect(url_for("range"))

@app.route("/update_settings", methods=["POST"])
def update_settings():
    """
    Updates the data period and update time settings.
    """
    try:
        data = request.get_json()
        settings["data_period"] = int(data["data_period"])
        settings["update_time"] = int(data["update_time"])

        # Save settings to file
        with open(SETTINGS_FILE, "w") as f:
            json.dump(settings, f)

        return "Settings updated successfully", 200
    except Exception as e:
        flash(f"An error occurred while updating settings: {e}", "error")
        return "Error updating settings", 500

# Run the application using the Waitress server
if __name__ == '__main__':
    print("\033[92mStarting the Flask application...\033[0m")
    print("\033[94mServer running at \033[4mhttp://localhost:8000\033[0m")
    serve(app, host='0.0.0.0', port=8000)