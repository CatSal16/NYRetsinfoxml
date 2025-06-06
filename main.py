
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import requests
from lxml import etree
import csv

app = FastAPI()

# Load whitelist of allowed ELI links
WHITELIST_PATH = "whitelist.csv"
with open(WHITELIST_PATH, newline='') as csvfile:
    reader = csv.reader(csvfile)
    WHITELIST = {row[0].strip() for row in reader if row}

class SearchRequest(BaseModel):
    query: str

class ExtractRequest(BaseModel):
    url: str

@app.post("/extract_text")
def extract_text(req: ExtractRequest):
    base_url = req.url.strip()
    if not base_url.endswith("/xml"):
        base_url += "/xml"

    if base_url.replace("/xml", "") not in WHITELIST:
        raise HTTPException(status_code=403, detail="URL not whitelisted")

    try:
        response = requests.get(base_url)
        response.raise_for_status()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    tree = etree.fromstring(response.content)
    tekst_afsnit = tree.findall(".//tekstafsnit")
    content = "\n\n".join([etree.tostring(el, encoding="unicode", method="text").strip() for el in tekst_afsnit])
    return {"tekst": content}
