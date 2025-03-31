import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

class WebsiteScraper:
    def __init__(self, base_url, output_dir="scraped_data"):
        self.base_url = base_url
        self.output_dir = output_dir
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"}
        os.makedirs(output_dir, exist_ok=True)
    
    def scrape(self):
        print(f"Scraping: {self.base_url}")
        
        try:
            response = requests.get(self.base_url, headers=self.headers, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Failed to scrape {self.base_url}: {e}")
            return
        
        soup = BeautifulSoup(response.text, 'html.parser')
        self.save_page(soup)
    
    def save_page(self, soup):
        file_path = os.path.join(self.output_dir, "index.html")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(soup.prettify())
        print(f"Saved: {file_path}")

if __name__ == "__main__":
    website_url = input("Enter website URL: ")
    scraper = WebsiteScraper(website_url)
    scraper.scrape()
