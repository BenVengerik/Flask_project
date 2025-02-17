import sqlite3
import time
import random
from datetime import datetime

DB_PATH = "/Users/Ben/Documents/Flask_project/Databases/dblog.db"

def insert_dummy_data():
    con = sqlite3.connect(DB_PATH)
    cursor = con.cursor()

    while True:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        flow = random.uniform(0, 10)
        water_temp = random.uniform(8000, 50000)
        dht_temp = random.uniform(20, 25)
        dht_hum = random.uniform(30, 90)

        cursor.execute("""
            INSERT INTO temlog (timestamp, flow, Water_temp, DHT_temp, DHT_hum) 
            VALUES (?, ?, ?, ?, ?)
        """, (timestamp, flow, water_temp, dht_temp, dht_hum))

        con.commit()
        print(f"Inserted: {timestamp}, {flow}, {water_temp}, {dht_temp}, {dht_hum}")
        
        time.sleep(1)  # Insert new data every 10 seconds

    con.close()

insert_dummy_data()
