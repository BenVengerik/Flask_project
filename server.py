from flask import Flask, request, render_template, send_file
from waitress import serve
from plotter import generate_plot


app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
@app.route('/index', methods=["GET", "POST"])
def index():
    return render_template('index.html')

@app.route("/plot", methods=["GET","POST"])
def plot():
    start_time = request.form["start_time"]
    end_time = request.form["end_time"]
    data_types = request.form.getlist("data_types")  # Get selected data types as a list

    if not data_types:
        return "Please select at least one data type.", 400  

    img = generate_plot(start_time, end_time, data_types)

    if img is None:
        return "No data available for the selected time range.", 400  

    return send_file(img, mimetype="image/png")

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8000)