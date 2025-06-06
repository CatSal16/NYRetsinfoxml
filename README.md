# NYRetsinfoxml

Denne webservice gør det muligt for en GPT at tilgå og læse gældende danske bekendtgørelser direkte fra XML-dokumenter på retsinformation.dk.

## Funktionalitet

- 🔍 **Søgning i whitelistede bekendtgørelser** via `whitelist.csv`
- 📄 **Indholdsanalyse af XML-dokumenter** for at finde relevante bestemmelser
- 📑 **OpenAPI-integration** til GPT Actions

## Projektstruktur

```
NYRetsinfoxml/
│
├── main.py               # FastAPI app med scraper og API endpoints
├── requirements.txt      # Afhængigheder til projektet
├── openapi.yaml          # OpenAPI specifikation til GPT-integration
├── whitelist.csv         # Liste over tilladte XML-dokumenter
└── README.md             # Denne fil
```

## Sådan deployer du på Render

1. Gør dit GitHub-repo **Public**.
2. Opret en ny Web Service på [https://render.com](https://render.com).
3. Peg på dit GitHub-repository.
4. Vælg:
   - **Environment**: Python
   - **Build command**: `pip install -r requirements.txt`
   - **Start command**: `uvicorn main:app --host 0.0.0.0 --port 10000`
5. Gå live og brug linket i GPT’s “Server URL”.

## API Endpoints

### `POST /search_whitelist`

Søger efter relevante bekendtgørelser i whitelistede XML-links baseret på tekstindhold.

**Body:**
```json
{
  "query": "diabetes kørekort"
}
```

**Returnerer:**
Liste med matches og URL’er.

---

### `POST /extract_paragraph`

Henter en specifik paragraf i et dokument via accessionsnummer og paragrafnavn (§ 2, § 56 osv.).

**Body:**
```json
{
  "accession": "LTA2024-875",
  "paragraph": "§ 2"
}
```

---

## XML-struktur og parsing

Parseren anvender `lxml` til at læse strukturerede afsnit og §-opdelinger fra xml-versionen af bekendtgørelser. Al tekst samles og gennemsøges med fuzzy matching og keyword scoring.

## Vedligeholdelse

Kontakt: [Ministerbetjening – Færdselsstyrelsen](mailto:min@fstyr.dk)

