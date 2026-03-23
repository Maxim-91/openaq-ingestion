import requests
import pandas as pd
import io

def download_file_by_location(location_id, year, month, day):
    date_str = f"{year}{month:02d}{day:02d}"
    base_url = "https://openaq-data-archive.s3.amazonaws.com"
    key = f"records/csv.gz/locationid={location_id}/year={year}/month={month:02d}/location-{location_id}-{date_str}.csv.gz"
    full_url = f"{base_url}/{key}"

    # 2. Use requests to get the file
    response = requests.get(full_url)

    if response.status_code == 200:
        # pandas osaa avata gzip-pakatun csv
        df = pd.read_csv(io.BytesIO(response.content), compression='gzip')
        df.to_csv(f"{location_id}-{date_str}.csv", index=False) # Save locally (optional)
        return df
    else:
        print(f"Failed to fetch. Status: {response.status_code}")
        return None


# DEBUG -----------------------------------------------------------------------------------------------------
#if __name__ == "__main__":
#    df = download_file_by_location(2975, 2023, 1, 1)

#    if df is not None:
#        print(df.head())
#        print(df.columns)
