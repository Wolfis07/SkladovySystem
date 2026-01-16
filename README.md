Implementace skladového systému s využitím relační databáze a **Repository Pattern (D1)**.

## Popis projektu
Aplikace slouží pro správu skladu, objednávek a generování reportů. Řešení je plně kontejnerizované.

**Funkcionalita:**
* **CRUD:** Produkty, Kategorie, Zákazníci
* **Transakce:** Vytváření objednávek (Atomické operace)
* **Reporting:** Agregované přehledy tržeb
* **Import:** CSV parser pro naskladnění

## Spuštění (Docker)
Není nutná lokální instalace Pythonu ani SQL Serveru.

1.  **Spuštění aplikace:**
    ```bash
    docker-compose run --rm app
    ```
    *(Příkaz automaticky sestaví image, spustí DB kontejner a připojí aplikaci)*

## Konfigurace
Soubor: `config.json`
* **Default:** Připojení k Docker kontejneru (`mssql`).
* **Externí DB:** Změňte hodnoty `server`, `username`, `password`.

## Struktura
* `/src` – Zdrojové kódy (Repositories, Models, Services)
* `/doc` – Dokumentace a testovací scénáře (PDF)
* `data.csv` – Data pro import
* `docker-compose.yml` – Orchestrace kontejnerů
