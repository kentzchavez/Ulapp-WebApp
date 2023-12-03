from scrape_weather import scrape_rappler_links
import requests
from bs4 import BeautifulSoup
import datetime
import time
import pandas as pd

# Get the links from scrape_weather.py
rappler_links = scrape_rappler_links()

# Read the existing Excel file, if it exists
try:
    existing_df = pd.read_excel("articles.xlsx")
except FileNotFoundError:
    existing_df = pd.DataFrame(columns=["Title", "Date", "URL", "Author", "Source", "Logo"])  # Add "Source" and "Logo" columns

# Initialize a list to store the new article information
article_data = []

for link in rappler_links:
    time.sleep(3)  # Introduce a 3-second delay
    response = requests.get(link)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract title, date, and author
        title = soup.find("h1", class_="post-single__title").text
        date_element = soup.find("time", {"class": "entry-date published post__timeago"})
        date_str = date_element["datetime"]

        # Extract only the date part
        date = date_str.split('T')[0]

        author = soup.find("a", class_="post-single__author").text

        # Check if the title is already in the existing DataFrame
        if title not in existing_df["Title"].values:
            # Append the new information to the list
            article_data.append([title, date, link, author, "Rappler", "external/rapppler.png"])  # Add "Rappler" as the source and set the logo
        else:
            print(f"Article with title '{title}' already exists in the Excel file.")
    else:
        print(f"Failed to retrieve the page. Status code for {link}: {response.status_code}")

# Create a DataFrame from the new article data
new_df = pd.DataFrame(article_data, columns=["Title", "Date", "URL", "Author", "Source", "Logo"])  # Add "Source" and "Logo" columns

# Concatenate the existing DataFrame with the new data
combined_df = pd.concat([existing_df, new_df], ignore_index=True)

# Save the combined DataFrame to an Excel file
combined_df.to_excel("articles.xlsx", index=False)
