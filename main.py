from fastapi import FastAPI
from pydantic import BaseModel
import requests
from xml.etree import ElementTree as ET
from find_accession import find_accession_number

app = FastAPI()

class QueryRequest(BaseModel):
    query: str

class ExtractRequest(BaseModel):
    url: str

@app.post("/search_accession")
def search_accession(request: QueryRequest):
    accession = find_accession_number(request.query)
    if accession:
        return {"accession": accession}
    return {"error": "Ingen accessionsnummer fundet"}

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
