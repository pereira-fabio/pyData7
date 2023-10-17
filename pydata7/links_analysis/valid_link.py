import requests
import json
from pydata7.links_analysis.link_filter import data_filtering

with open("../data/filtered_data_2023-10-04_15-09-07.json", "r") as f:
    data = json.load(f)

for item in data:
    url = item.get("url")

    if url:
        try:
            response = requests.head(url)
            if response.status_code == 200:
                print("200")
            elif response.status_code == 404:
                print("404")
        except requests.exceptions.RequestException as err:
            raise SystemExit(err)
    else:
        print("No URL found")