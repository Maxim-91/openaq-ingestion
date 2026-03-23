from api import get_bbox, get_locations
from downloader import download_data
from db import get_connection

conn = get_connection()
cur = conn.cursor()

bbox = get_bbox("Helsinki")
locations = get_locations(bbox)

location_id = locations[0]["id"]

# Download one month
for day in range(1, 29):
    df = download_data(location_id, 2023, 1, day)

    if df is None:
        continue

    for _, row in df.iterrows():
        sensor = row["parameter"]

        # Insert sensor if not exists
        cur.execute("""
            INSERT INTO sensors (name)
            VALUES (%s)
            ON CONFLICT (name) DO NOTHING
        """, (sensor,))

        cur.execute("SELECT id FROM sensors WHERE name=%s", (sensor,))
        sensor_id = cur.fetchone()[0]

        # Insert measurement
        cur.execute("""
            INSERT INTO measurements (location_id, sensor_id, value, timestamp)
            VALUES (%s, %s, %s, %s)
        """, (
            row["locationId"],
            sensor_id,
            row["value"],
            row["date"]
        ))

conn.commit()
print("Data inserted")