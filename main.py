from api import get_bbox, get_openaq_locations_by_bbox
from downloader import download_file_by_location
from db import get_connection

# Connect to database
conn = get_connection()
cur = conn.cursor()

# Get Helsinki bounding box
bbox = get_bbox("Helsinki")

# Get locations from OpenAQ API
locations = get_openaq_locations_by_bbox(bbox)

# Pick first location
location = locations[0]
location_id = location["id"]
location_name = location["name"]

# Insert location into database (important for FK)
cur.execute("""
    INSERT INTO locations (id, name, city, country)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (id) DO NOTHING
""", (location_id, location_name, "Helsinki", "Finland"))

# Download one month of data
for day in range(1, 29):
    df = download_file_by_location(location_id, 2023, 1, day)

    if df is None:
        continue

    for _, row in df.iterrows():
        sensor_name = row["parameter"]

        # Insert sensor if not exists
        cur.execute("""
            INSERT INTO sensors (name)
            VALUES (%s)
            ON CONFLICT (name) DO NOTHING
        """, (sensor_name,))

        # Get sensor id
        cur.execute("SELECT id FROM sensors WHERE name=%s", (sensor_name,))
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

# Commit all changes
conn.commit()

print("Data inserted successfully!")
