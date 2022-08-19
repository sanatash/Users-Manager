FROM mysql:latest
COPY ./database_users.sql /docker-entrypoint-initdb.d/
COPY ./database_config.sql /docker-entrypoint-initdb.d/