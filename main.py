from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import PlainTextResponse
import requests
import pandas as pd

app = FastAPI()

# Indlæs whitelist fra CSV
whitelist_df = pd.read_csv("whitelist.csv")
WHITELIST = set(whitelist_df['url'].tolist())

@app.get("/fetch-from-whitelist", response_class=PlainTextResponse)
def fetch_from_whitelist(url: str = Query(..., description="URL der skal hentes")):
    if url not in WHITELIST:
        raise HTTPException(status_code=403, detail="URL ikke tilladt – ikke i whitelist.")

    try:
        response = requests.get(url)
        response.raise_for_status()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fejl ved hentning: {e}")

    return response.text
