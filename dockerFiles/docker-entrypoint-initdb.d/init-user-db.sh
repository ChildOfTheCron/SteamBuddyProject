#!/bin/bash
set -e

#psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
#    CREATE USER docker;
#    CREATE DATABASE docker;
#    GRANT ALL PRIVILEGES ON DATABASE docker TO docker;
#EOSQL

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
CREATE TABLE appIdTable (
	appid 	int PRIMARY KEY,
	productname 	varchar(250),
	discount	int
);
CREATE GROUP restgroup;
CREATE USER restbot WITH PASSWORD 'resty';
ALTER GROUP restgroup ADD USER restbot;
ALTER ROLE restgroup LOGIN;
GRANT SELECT ON TABLE appIdTable TO restgroup;
EOSQL

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" postgres < /appidlist.sql 
