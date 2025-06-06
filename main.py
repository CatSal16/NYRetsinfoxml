# FastAPI-løsning: returnér samlet tekst fra alle whitelistede bekendtgørelser til GPT

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import PlainTextResponse
import requests
import pandas as pd
from bs4 import BeautifulSoup
import threading

app = FastAPI()

# Indlæs whitelist
whitelist_df = pd.read_csv("whitelist.csv")
WHITELIST_URLS = whitelist_df['url'].tolist()

# Cache til bekendtgørelser
corpus = []  # List[dict] med keys: url, text
lock = threading.Lock()

def fetch_and_extract_text(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Ekstraher hovedindhold: typisk i <section>, <div> eller <p>
        paragraphs = soup.find_all(['p', 'div'])
        text = " ".join(p.get_text(strip=True) for p in paragraphs)
        return text
    except Exception as e:
        return ""

def build_corpus():
    global corpus
    local_corpus = []
    for url in WHITELIST_URLS:
        text = fetch_and_extract_text(url)
        if len(text) > 100:
            local_corpus.append({"url": url, "text": text})
    with lock:
        corpus = local_corpus

@app.on_event("startup")
def on_startup():
    threading.Thread(target=build_corpus).start()

@app.get("/search", response_class=PlainTextResponse)
def search_whitelist(q: str = Query(..., description="Spørgsmål fra GPT")):
    with lock:
        if not corpus:
            raise HTTPException(status_code=503, detail="Bekendtgørelserne indlæses stadig.")

        # Saml alle tekster i én blok
        combined_text = "\n\n".join(
            f"Kilde: {doc['url']}\n{doc['text']}" for doc in corpus
        )

        return combined_text
