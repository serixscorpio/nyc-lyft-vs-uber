FROM python:3.11

RUN pip install pgpq psycopg pyarrow requests 

WORKDIR /app
COPY ingest_data.py ingest_data.py

ENTRYPOINT [ "python", "ingest_data.py" ]