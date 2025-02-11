import sqlite3

import matplotlib
matplotlib.use("Agg")  # Use non-GUI backend (fixes Mac OS GUI error)

import matplotlib.pyplot as plt
import datetime
import io

# Database file path
DB_PATH = "/Users/Ben/Documents/Flask_project/Databases/dblog.db"

# Assign colors to each data type for consistency
DATA_TYPE_COLORS = {
    "flow": "b",       # Blue
    "Water_temp": "r",       # Red
    "DHT_temp": "g",         # Green
    "DHT_hum": "orange" # Orange
}

def generate_plot(start_time, end_time, data_types):
    con = sqlite3.connect(DB_PATH)
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

    if not data:
        return None

    timestamps = [datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S") for row in data]

    fig, ax1 = plt.subplots(figsize=(10, 5))

    # The first axis (ax1) is for the first selected data type
    primary_axis = True
    ax_objects = {}

    for i, data_type in enumerate(data_types):
        values = [row[i + 1] for row in data]  # Offset by 1 because row[0] is timestamp
        color = DATA_TYPE_COLORS.get(data_type, f"C{i}")  # Use default Matplotlib colors if not found
    
        if primary_axis:
            ax = ax1  # First plot uses the main axis
            primary_axis = False
        else:
            ax = ax1.twinx()  # Create a secondary axis
            ax.spines["right"].set_position(("outward", 60 * (len(ax_objects) - 1)))  # Space out multiple Y-axes
    
        # Explicitly set color of both the line and axis labels
        line, = ax.plot(timestamps, values, linestyle="-", color=color, label=data_type)
        ax.set_ylabel(data_type, color=color)
        ax.yaxis.label.set_color(color)  # Set axis label color
        ax_objects[data_type] = ax  # Store axis for later reference

        
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

    img = io.BytesIO()
    fig.savefig(img, format="png", bbox_inches="tight")
    img.seek(0)
    plt.close(fig)

    return img
