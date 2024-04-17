# Utilizamos la imagen oficial de MySQL como base
FROM mysql:latest

# Establecemos las variables de entorno para configurar la base de datos
ENV MYSQL_ROOT_PASSWORD=123
ENV MYSQL_DATABASE=AmenazasNaturales
ENV MYSQL_USER=chortax
ENV MYSQL_PASSWORD=db_password

# Copiamos el script SQL que creará la tabla y los datos de ejemplo
COPY init.sql /docker-entrypoint-initdb.d/

# Cambiamos el nombre del archivo a un número de secuencia válido
# Esto asegura que se ejecute después de que se inicialice la base de datos
RUN mv /docker-entrypoint-initdb.d/init.sql /docker-entrypoint-initdb.d/001_init.sql
