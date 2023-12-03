import requests
from bs4 import BeautifulSoup
import time

def scrape_rappler_links():
    url = "https://www.rappler.com/nation/weather/"
    response = requests.get(url)
    rappler_links = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        article_cards = soup.find_all("article", class_="post-card")

        for card in article_cards:
            rappler_links.append(card.find("h3").find("a").get("href"))
            
            # Introduce a delay of 3 seconds
            time.sleep(3)
    else:
        print("Failed to retrieve the page. Status code:", response.status_code)

    return rappler_links

if __name__ == '__main__':
    links = scrape_rappler_links()
    print(links)
