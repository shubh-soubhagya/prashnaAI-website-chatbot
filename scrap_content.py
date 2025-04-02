import os
import requests
from bs4 import BeautifulSoup

def extract_content(url, output_file=r"prashna/content/website_content.txt"):
    headers = {"User-Agent": "Mozilla/5.0"}
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise error for failed requests
        
        # Parse HTML
        soup = BeautifulSoup(response.text, "html.parser")

        # Remove unnecessary elements
        for tag in soup(["script", "style", "meta", "noscript", "iframe"]):
            tag.decompose()

        # Extract visible text content
        text_content = soup.get_text(separator="\n", strip=True)

        # Save to .txt file
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(text_content)

        print(f"✅ Content extracted and saved in '{output_file}'")
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching the URL: {e}")

# Example usage
url = "https://purezzatechnologies.com/"  # Replace with your target website
extract_content(url)
