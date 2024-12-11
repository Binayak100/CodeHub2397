import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

# URL of the IMDb Top 250 page
url = "https://www.imdb.com/chart/top/"
headers = {"User-Agent": "Mozilla/5.0"}

# Fetch the page content
response = requests.get(url, headers=headers)
if response.status_code != 200:
    raise Exception("Failed to load page. Status code:", response.status_code)

# Parse the page content
soup = BeautifulSoup(response.text, "html.parser")

# Find the <script> tag containing JSON-LD data
script_tag = soup.find("script", type="application/ld+json")
if not script_tag:
    raise ValueError("JSON-LD script not found on the page.")

# Parse the JSON content
data = json.loads(script_tag.string)

# Initialize lists to store movie data
titles = []
urls = []
descriptions = []
ratings = []
genres = []
durations = []

# Extract movie details
if "itemListElement" in data:
    for item in data["itemListElement"]:
        movie = item["item"]
        titles.append(movie.get("name", "N/A"))
        urls.append(movie.get("url", "N/A"))
        descriptions.append(movie.get("description", "N/A"))
        ratings.append(movie.get("aggregateRating", {}).get("ratingValue", "N/A"))
        genres.append(movie.get("genre", "N/A"))
        durations.append(movie.get("duration", "N/A"))
else:
    raise ValueError("No 'itemListElement' found in JSON data.")

# Create a DataFrame
df = pd.DataFrame({
    "Title": titles,
    "URL": urls,
    "Description": descriptions,
    "Rating": ratings,
    "Genre": genres,
    "Duration": durations
})

# Save the DataFrame to a CSV file
df.to_csv("imdb_top_250.csv", index=False)

print("Data saved to 'imdb_top_250.csv'")
