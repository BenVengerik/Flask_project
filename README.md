# Flask Project

This is a Flask-based web application that generates and serves plots based on user-selected time ranges and data types.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Endpoints](#endpoints)
- [How to Use](#how-to-use)

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/BenVengerik/Flask_project.git
    cd Flask_project
    ```

2. Create a virtual environment and activate it:
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Run the Flask application:
    ```sh
    python server.py
    ```

2. Open your web browser and navigate to `http://localhost:8000`.

3.	You can navigate the different pages by using the banner at the top of the page.

4.	The main page will display the live dashboard. You can change the period of displayed data and the frequency of graph updates using the form at the bottom of the page.

5.	If you navigate to the “Generate Plots” page, you will be able to generates plots for any data type and from any period where data is available. Choose which the start and end time and what data types you want to display and click generate plot. A plot will be generated, displaying the data. This plot can be exported as image or as raw data (csv file).

6.	If you navigate to the “Admin Dashboard” you will be prompted with a log-in page. To log in, input ‘admin’ as username and ‘password’ as password. In the admin dashboard, you will be able to make many changes. You will be able to update the live dashboard settings, including the alert threshold, which currently is only a place holder. You will also be able to update the database path in case the database is in a different location. You will also be able to interface directly with the terminal using the SQL query and command line interfaces.

## Project Structure

- [Databases](https://github.com/BenVengerik/Flask_project/tree/main/Databases): Contains the SQLite database file.
- [styles](https://github.com/BenVengerik/Flask_project/tree/main/static/styles): Contains the CSS stylesheets.
- [templates](https://github.com/BenVengerik/Flask_project/tree/main/templates): Contains the HTML templates.
- [server.py](https://github.com/BenVengerik/Flask_project/blob/main/server.py): The main Flask application file.
- [plotter.py](https://github.com/BenVengerik/Flask_project/blob/main/plotter.py): Contains the function to generate plots.
- `requirements.txt`: Lists the project dependencies.

## Endpoints

- `/dashboard`: Live sensor data dashboard.
- `/plot/check`: Endpoint to check data availability.
- `/plot/<data_type>`: Endpoint to generate a live plot for a specific data type.
- `/range`: Page to select time range and data types for generating plots.
- `/plot`: Endpoint to generate and serve the plot based on user input.
- `/generate_plot`: Endpoint to generate a plot based on the provided start and end time, and data types.
- `/export_plot`: Endpoint to export the plot image.
- `/download_data`: Endpoint to download the raw data.
- `/update_settings`: Endpoint to update the data period and update time settings.
- `/admin/login`: Admin login page.
- `/admin/logout`: Admin logout endpoint.
- `/admin`: Admin dashboard.
- `/admin/update_settings`: Endpoint to update live dashboard settings.
- `/admin/update_db_path`: Endpoint to update the database path.
- `/admin/execute_query`: Endpoint to execute SQL queries.
- `/admin/execute_cli`: Endpoint to execute CLI commands.

## How to Use

1. **Live Dashboard**::
    - Navigate to the home page (`http://localhost:8000/dashboard`) to view live sensor data plots.
    - Update live dashboard settings using the provided form.

2. **Generate Plots**:
    - Navigate to the range selection page (`http://localhost:8000/range`).
    - Select the start and end time, and the data types you want to plot.
    - Click "Generate Plot" to generate and view the plot.
    - After generating a plot, use the provided forms to export the plot image or download the raw data.

4. **Admin Dashboard**:
    - After logging in, navigate to the admin dashboard (`http://localhost:8000/admin`).
    - Update live dashboard settings, database path, execute SQL queries, and CLI commands using the provided forms.
