import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def get_all_links(base_url):
    headers = {"User-Agent": "Mozilla/5.0"}
    visited = set()
    to_visit = [base_url]  # Start with the main URL
    all_links = set()

    while to_visit:
        url = to_visit.pop()
        if url in visited:
            continue
        visited.add(url)
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            # Extract all internal links
            for link in soup.find_all("a", href=True):
                full_link = urljoin(base_url, link["href"])
                parsed_link = urlparse(full_link)

                # Ensure it's an internal link (same domain) and ends with .html
                if base_url in full_link and full_link.endswith(".html"):
                    if full_link not in visited:
                        to_visit.append(full_link)
                        all_links.add(full_link)

        except requests.RequestException:
            continue
    
    return all_links

def extract_and_save_html(url, folder="prashna/scraped_pages"):
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        html_code = soup.prettify()

        # Create folder if it doesn't exist
        os.makedirs(folder, exist_ok=True)

        # Generate filename based on the URL
        page_name = urlparse(url).path.replace("/", "_") or "index"
        file_path = os.path.join(folder, f"{page_name}.txt")

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(html_code)

        print(f"✅ Saved: {file_path}")

    except requests.RequestException as e:
        print(f"❌ Failed to extract {url}: {e}")

# Main function
def scrape_all_pages(base_url):
    all_links = get_all_links(base_url)
    all_links.add(base_url)  # Include the main page

    print(f"🔍 Found {len(all_links)} pages to scrape...")

    for link in all_links:
        extract_and_save_html(link)

# Example usage
base_url = "https://kavachinnovations.com/"  # Replace with your target website
scrape_all_pages(base_url)