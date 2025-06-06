import requests
from bs4 import BeautifulSoup
import re

def find_accession_number(query):
    """
    Søger via Google efter XML-dokumenter på retsinformation.dk.
    Returnerer det første gyldige accessionsnummer, fx 'B20220122005'.
    """
    headers = {"User-Agent": "Mozilla/5.0"}
    google_search_url = f"https://www.google.com/search?q=site:retsinformation.dk+inurl:accn+inurl:xml+{query}"

    response = requests.get(google_search_url, headers=headers)
    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    results = soup.find_all("a")

    for link in results:
        href = link.get("href")
        if href and "/eli/accn/" in href and href.endswith("/xml"):
            # Match accessionsnummer fra URL
            match = re.search(r"/eli/accn/([A-Z0-9]+)/xml", href)
            if match:
                return match.group(1)  # fx B20220122005

    return None
