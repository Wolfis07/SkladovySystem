FROM python:3.10-slim

WORKDIR /app

# Instalace závislostí pro MSSQL (FreeTDS)
RUN apt-get update && apt-get install -y \
    freetds-dev \
    freetds-bin \
    build-essential \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

COPY . .

# Instalace Python knihovny pro MSSQL
RUN pip install pymssql

CMD ["python", "main.py"]