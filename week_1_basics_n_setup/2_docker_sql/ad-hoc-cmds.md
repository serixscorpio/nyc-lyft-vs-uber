```bash
# to create a docker network
docker network create pg-network

# to run a postgres instance via docker within a docker network
docker run -it \
    -e POSTGRES_USER="root" \
    -e POSTGRES_PASSWORD="root" \
    -e POSTGRES_DB="ny_taxi" \
    -v $(pwd)/pg_db_file:/var/lib/postgresql/data \
    -p 5432:5432 \
    --network=pg-network \
    --name pg-database \
    postgres:latest

# to run a pgadmin instance via docker within a docker network
docker run -it \
    -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
    -e PGADMIN_DEFAULT_PASSWORD="root" \
    -p 8080:80 \
    --network=pg-network \
    --name pgadmin \
    dpage/pgadmin4
```

```bash
# for subsequent starts after the container exits
docker start -ai pg-database
docker start -ai pgadmin
```

---

```bash
# to connect to the postgres instance using pgcli
pgcli -h localhost -u root -d ny_taxi
```

---
# dockerize ingest_data.py
docker build -t taxi_ingest:v001 .

docker run -it --network=pg-network \
    taxi_ingest:v001 \
    --user=root \
    --password=root \
    --host=pg-database \
    --port=5432 \
    --db=ny_taxi \
    --table_name=yellow_taxi_data \
    --url=${URL}

# Use docker compose for bringing up postgres + pgadmin

```bash
docker compose up
docker compose up -d
docker compose down
```

