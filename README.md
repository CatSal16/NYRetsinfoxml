# Whitelist Handler API

Denne API er bygget med FastAPI og tillader kun at hente indhold fra URL'er, der er whitelistet i `whitelist.csv`. Den er designet til at blive brugt sammen med GPT Actions eller som en selvstændig sikker proxy for godkendte kilder.

## 🧪 Lokal kørsel

1. Installer afhængigheder:
   ```bash
   pip install -r requirements.txt
   ```

2. Start serveren:
   ```bash
   uvicorn main:app --reload
   ```

3. Prøv i browseren:
   ```
   http://127.0.0.1:8000/fetch-from-whitelist?url=https://www.retsinformation.dk/eli/lta/2025/599
   ```

## 🚀 Deploy til Render

1. Push projektet til GitHub
2. Gå til [https://render.com](https://render.com)
3. Opret et nyt Web Service-projekt
4. Vælg dit repo – `render.yaml` sørger for opsætningen
5. Din API vil blive tilgængelig på en offentlig URL

## 🛡️ Sikkerhed

Alle forespørgsler tjekkes mod `whitelist.csv`. Hvis URL'en ikke er godkendt, returnerer API'en en 403-fejl.

## 🧠 Anvendelse med GPT Actions

Når din API kører offentligt, kan du tilføje den som en Action i en Custom GPT og kun tillade opslag via denne handler.

