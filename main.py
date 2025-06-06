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

def er_gaeldende(xml_root):
    for elem in xml_root.iter():
        if elem.tag.lower() == "status" and "gældende" in elem.text.lower():
            return True
    return False

@app.post("/search_accession")
def search_accession(request: QueryRequest):
    accession = find_accession_number(request.query)
    if accession:
        xml_url = f"https://www.retsinformation.dk/eli/accn/{accession}/xml"
        xml_res = requests.get(xml_url)
        if xml_res.status_code == 200:
            xml_root = ET.fromstring(xml_res.content)
            if er_gaeldende(xml_root):
                return {"accession": accession}
            return {"error": "Dokument fundet, men ikke gældende"}
    return {"error": "Ingen gældende accessionsnummer fundet"}

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
