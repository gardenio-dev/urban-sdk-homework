#!/usr/bin/env bash

# TODO: NEVER PUT SENSITIVE INFORMATION IN YOUR CODE.
# This is just an example, do not use this in production.
export PGHOST=localhost
export PGPORT=5432
export PGDATABASE=urbansdk
export PGUSER=postgres
export PGPASSWORD=postgres

ogr2ogr \
  -f "PostgreSQL" \
  "PG:host=${PGHOST} port=${PGPORT} dbname=${PGDATABASE} user=${PGUSER} password=${PGPASSWORD}" \
  -nln "staging.duval_jan1_2024" \
  -overwrite \
  -progress \
  ./data/duval_jan1_2024.parquet.gz \
  duval_jan1_2024.parquet

ogr2ogr \
  -f "PostgreSQL" \
  "PG:host=${PGHOST} port=${PGPORT} dbname=${PGDATABASE} user=${PGUSER} password=${PGPASSWORD}" \
  -nln "staging.link_info" \
  -lco "GEOMETRY_NAME=geom" \
  -a_srs "EPSG:4326" \
  -overwrite \
  -progress \
  ./data/link_info.parquet.gz \
  link_info.parquet

# Ensure libpq is in your PATH.
export PATH="$PATH:/usr/local/Cellar/libpq/17.5/bin"
psql -f ./scripts/etl.sql
