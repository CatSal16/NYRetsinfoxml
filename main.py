from fastapi import FastAPI, Request
from pydantic import BaseModel
import requests
import xml.etree.ElementTree as ET

app = FastAPI()

class SearchRequest(BaseModel):
    query: str

class ExtractRequest(BaseModel):
    url: str

@app.post("/search_laws")
def search_laws(request: SearchRequest):
    params = {
        "SearchText": request.query,
        "OnlyActive": "true",
        "PageSize": 5
    }
    res = requests.get("https://retsinformation.dk/api/document", params=params)
    res.raise_for_status()
    data = res.json()
    results = []
    for doc in data.get("Documents", []):
        results.append({
            "titel": doc.get("Title"),
            "eli": doc.get("Eli"),
            "link": f"https://www.retsinformation.dk/api/xml/{doc.get('Eli')}"
        })
    return {"resultater": results}

@app.post("/extract_text")
def extract_text(req: ExtractRequest):
    response = requests.get(req.url)
    response.raise_for_status()
    xml_root = ET.fromstring(response.content)
    paragraphs = []
    for elem in xml_root.iter():
        if elem.text and elem.tag.lower().startswith("p"):
            paragraphs.append(elem.text.strip())
    return {"tekst": "\n\n".join(paragraphs)}
