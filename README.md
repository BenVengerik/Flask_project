# Flask Project

This is a Flask-based web application that generates and serves plots based on user-selected time ranges and data types.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Endpoints](#endpoints)

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

## Project Structure

- [Databases]: Contains the SQLite database file.
- [styles]: Contains the CSS stylesheets.
- [templates]): Contains the HTML templates.
- [server.py]: The main Flask application file.
- [plotter.py]: Contains the function to generate plots.
- `requirements.txt`: Lists the project dependencies.

## Endpoints

- `/`: Home page where users can select the time range and data types.
- `/plot`: Endpoint to generate and serve the plot based on user input.
