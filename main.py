import uvicorn
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import pandas as pd
import requests
from lxml import etree
import io

app = FastAPI()

# Indlæs whitelist
try:
    whitelist_df = pd.read_csv("whitelist.csv")
    WHITELIST = set(whitelist_df["url"].dropna().str.replace("/xml", "", regex=False))
except Exception as e:
    print("Fejl ved indlæsning af whitelist:", e)
    WHITELIST = set()

class URLRequest(BaseModel):
    url: str

@app.post("/extract_text")
async def extract_text(req: URLRequest):
    url = req.url.strip()
    clean_url = url.replace("/xml", "")

    if clean_url not in WHITELIST:
        raise HTTPException(status_code=403, detail="URL ikke tilladt (ikke på whitelist)")

    xml_url = clean_url + "/xml"
    try:
        response = requests.get(xml_url)
        response.raise_for_status()
        xml_data = response.content
        tree = etree.parse(io.BytesIO(xml_data))
        tekst = " ".join(tree.xpath("//tekstafsnit//text()"))
        return {"tekst": tekst.strip()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fejl ved hentning eller parsing af XML: {str(e)}")

# For lokal kørsel (valgfri)
# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
