import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = input("Enter the URL of the pastpapers.co page. for eg: 'https://pastpapers.co/cie/?dir=IGCSE/Mathematics-0580: '")
SAVE_DIR = input("Enter the name of the folder to save the PDFs to. for eg: 'math', will save it in the current directory")

# Headers to mimic a real browser
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/115.0.0.0 Safari/537.36",
    "Referer": "https://pastpapers.co/"
}

os.makedirs(SAVE_DIR, exist_ok=True)

# Create a session to persist cookies
session = requests.Session()
session.headers.update(HEADERS)

def get_soup(url):
    r = session.get(url)
    r.raise_for_status()
    return BeautifulSoup(r.text, "html.parser")

def download_file(url, folder):
    filename = url.split("/")[-1]
    filepath = os.path.join(folder, filename)
    if not os.path.exists(filepath):
        print(f"Downloading {filename}...")
        r = session.get(url)
        r.raise_for_status()
        with open(filepath, "wb") as f:
            f.write(r.content)

def scrape_pdfs():
    soup = get_soup(BASE_URL)
    
    # Find year folders (>= 2019)
    year_links = []
    for link in soup.find_all("a"):
        href = link.get("href")
        if href and any(str(year) in href for year in range(2019, 2026)):
            year_links.append(urljoin(BASE_URL, href))

    for folder_url in year_links:
        print(f"Scanning: {folder_url}")
        sub_soup = get_soup(folder_url)

        for file_link in sub_soup.find_all("a"):
            file_href = file_link.get("href")
            if file_href and file_href.lower().endswith(".pdf"):
                file_url = urljoin(folder_url, file_href)
                download_file(file_url, SAVE_DIR)

if __name__ == "__main__":
    scrape_pdfs()