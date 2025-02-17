from flask import Flask, request, render_template, send_file
from waitress import serve
from plotter import generate_plot

# Initialize the Flask application
app = Flask(__name__)

# Define the route for the home page
@app.route('/', methods=["GET", "POST"])
@app.route('/index', methods=["GET", "POST"])
def index():
    """
    Renders the index.html template.
    """
    return render_template('index.html')

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
    img = generate_plot(start_time, end_time, data_types)

    # Check if the plot generation was successful
    if img is None:
        return "No data available for the selected time range.", 400  

    # Send the plot image as a response
    return send_file(img, mimetype="image/png")


@app.route('/dashboard')
def dashboard():
    """
    Renders the dashboard.html template.
    """
    return render_template('dashboard.html')

@app.route("/plot/<data_type>")
def live_plot(data_type):
    """
    Generates a live plot for a specific data type.
    """
    from datetime import datetime, timedelta
    end_time = datetime.now()
    start_time = end_time - timedelta(hours=0.1)  # Show the last 0.1 hour(s) of data

    img = generate_plot(start_time.strftime("%Y-%m-%d %H:%M:%S"), 
                        end_time.strftime("%Y-%m-%d %H:%M:%S"), 
                        [data_type])

    return send_file(img, mimetype="image/png")


# Run the application using the Waitress server
if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8000)