# Retsinfo XML Scraper

Dette projekt gør det muligt for en GPT-handling at tilgå gældende regler fra Retsinformation.dk via deres XML-visning.

## Funktionalitet
- Endpoint: `/extract_text`
- Input: JSON med en URL fra retsinformation.dk
- Output: Tekstudtræk fra dokumentets XML-indhold
- Sikkerhed: Kun URL'er fra `whitelist.csv` accepteres

## Teknologi
- FastAPI
- lxml
- requests
- pandas

## Deployment
Designet til at køre på Render.com

## Forbindelse til GPT
Brug `openapi.yaml` til at forbinde som GPT-handling.
