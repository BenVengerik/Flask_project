import sqlite3

import matplotlib
matplotlib.use("Agg")  # Use non-GUI backend (fixes Mac OS GUI error)

import matplotlib.pyplot as plt
import datetime
import io

import numpy as np
from scipy.optimize import curve_fit

# Given calibration data
resistance_values = np.array([332776, 96481, 32566, 12486, 10000, 5331, 2490, 1071, 678.1, 387.3])  # Ohms
temperature_values = np.array([-40, -20, 0, 20, 25, 40, 60, 85, 100, 120])  # Celsius

# Define logarithmic model
def log_fit(R, A, B):
    return A + B * np.log(R)

# Fit the curve to find A and B
params, _ = curve_fit(log_fit, resistance_values, temperature_values)
A_fit, B_fit = params

def resistance_to_temperature(resistance):
    """Convert resistance to temperature using the logarithmic model."""
    return A_fit + B_fit * np.log(resistance)

def generate_plot(start_time, end_time, data_types, db_path, data_type_colors):
    """
    Generates a plot for the given data types within the specified time range.

    Parameters:
    start_time (str): The start time for the data range in 'YYYY-MM-DD HH:MM:SS' format.
    end_time (str): The end time for the data range in 'YYYY-MM-DD HH:MM:SS' format.
    data_types (list): A list of data types to plot.
    db_path (str): The path to the SQLite database file.
    data_type_colors (dict): A dictionary mapping data types to colors.

    Returns:
    BytesIO: A BytesIO object containing the plot image in PNG format, or None if no data is available.
    """
    try:
        # Connect to the SQLite database
        con = sqlite3.connect(db_path)
        cursor = con.cursor()

        # Convert list of selected data types into a SQL column selection
        columns = ", ".join(data_types)
        query = f"""
        SELECT timestamp, {columns} 
        FROM temlog 
        WHERE timestamp BETWEEN '{start_time}' AND '{end_time}' 
        ORDER BY timestamp;
        """
        cursor.execute(query)
        data = cursor.fetchall()
        con.close()

        # Return None if no data is available
        if not data:
            return None

        # Parse timestamps from the data
        timestamps = [datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S") for row in data]

        # Create a new figure and axis for the plot
        fig, ax1 = plt.subplots(figsize=(10, 5))

        # The first axis (ax1) is for the first selected data type
        primary_axis = True
        ax_objects = {}

        # Plot each data type on the graph
        for i, data_type in enumerate(data_types):
            values = [row[i + 1] for row in data]  # Offset by 1 because row[0] is timestamp
            color = data_type_colors.get(data_type, f"C{i}")  # Use default Matplotlib colors if not found
        
            if data_type == "Water_temp":
                values = resistance_to_temperature(values)  # Convert using log model
        
            if primary_axis:
                ax = ax1  # First plot uses the main axis
                primary_axis = False
            else:
                ax = ax1.twinx()  # Create a secondary axis
                ax.spines["right"].set_position(("outward", 60 * (len(ax_objects) - 1)))  # Space out multiple Y-axes
        
            # Plot the data on the axis
            line, = ax.plot(timestamps, values, linestyle="-", color=color, label=data_type)
            ax.set_ylabel(data_type, color=color)
            ax.yaxis.label.set_color(color)  # Set axis label color
            ax_objects[data_type] = ax  # Store axis for later reference

        # Set the x-axis label and title
        ax1.set_xlabel("Timestamp")
        ax1.set_title("Sensor Data Over Time")
        ax1.tick_params(axis='x', rotation=45)
        ax1.grid()

        # Combine legends from all axes
        handles, labels = [], []
        for ax in ax_objects.values():
            h, l = ax.get_legend_handles_labels()
            handles.extend(h)
            labels.extend(l)
        ax1.legend(handles, labels, loc="upper left")

        # Save the plot to a BytesIO object
        img = io.BytesIO()
        fig.savefig(img, format="png", bbox_inches="tight")
        img.seek(0)
        plt.close(fig)

        return img
    except Exception as e:
        print(f"An error occurred while generating the plot: {e}")
        return None
