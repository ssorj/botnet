#!/bin/bash

PGPASSWORD="$POSTGRES_PASSWORD"

# exec pgbench --username "$POSTGRES_USER" --initialize --scale 100

createdb dvdrental
pg_restore -v -d dvdrental /data/dvdrental.tar
