```bash
# to run a postgres instance via docker
docker run -it \
    -e POSTGRES_USER="root" \
    -e POSTGRES_PASSWORD="root" \
    -e POSTGRES_DB="ny_taxi" \
    -v $(pwd)/pg_db_file:/var/lib/postgresql/data \
    -p 5432:5432 \
    postgres:latest
```

```bash
# to connect to the postgres instance using pgcli
pgcli -h localhost -u root -d ny_taxi
```