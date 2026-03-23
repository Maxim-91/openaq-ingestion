import requests
import pandas as pd
import io

def download_data(location_id, year, month, day):
    date = f"{year}{month:02d}{day:02d}"

    url = f"https://openaq-data-archive.s3.amazonaws.com/records/csv.gz/locationid={location_id}/year={year}/month={month:02d}/location-{location_id}-{date}.csv.gz"

    response = requests.get(url)

    if response.status_code == 200:
        df = pd.read_csv(io.BytesIO(response.content), compression='gzip')
        return df

    return None