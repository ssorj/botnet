#!/bin/bash

PGPASSWORD="$POSTGRES_PASSWORD"

createdb dvdrental
pg_restore -v -d dvdrental /data/dvdrental.tar
