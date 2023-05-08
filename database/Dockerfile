FROM mysql:8.0.33

COPY init.sql /docker-entrypoint-initdb.d/1.sql

ENV MYSQL_ROOT_PASSWORD=admin
ENV MYSQL_DATABASE=db
ENV MYSQL_USER=admin
ENV MYSQL_PASSWORD=admin