from api import get_bbox, get_openaq_locations_by_bbox
from downloader import download_file_by_location
from db import get_connection

# Connect to database
conn = get_connection()
cur = conn.cursor()

# Step 1: Get Helsinki bbox
bbox = get_bbox("Helsinki")

# Step 2: Get locations
locations = get_openaq_locations_by_bbox(bbox)

if not locations:
    print("No locations found!")
    exit()

# Step 3: Pick first location
location = locations[0]
location_id = location["id"]
location_name = location["name"]

print("Using location:", location_id, location_name)

# Step 4: Insert location (important for FK)
cur.execute("""
    INSERT INTO locations (id, name, city, country)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (id) DO NOTHING
""", (location_id, location_name, "Helsinki", "Finland"))

# Step 5: Download and insert data (1 month)
for day in range(1, 29):
    print(f"Processing day {day}...")

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
            row["location_id"],   # FIXED (was locationId)
            sensor_id,
            row["value"],
            row["datetime"]       # FIXED (correct column)
        ))

# Step 6: Commit changes
conn.commit()

print("Data inserted successfully!")