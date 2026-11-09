# Taller 3 - Tres APIs Flask Balanceadas con PostgreSQL

**Curso:** Computación en la Nube e Internet de las Cosas

**Temas**:

- Flask
- Docker Compose
- Nginx
- Load Balancing
- PostgreSQL
- Python y SQL
- Stateless API

---

# Objetivos

Al finalizar este workshop el estudiante será capaz de:

- Ejecutar tres instancias de la misma API.
- Balancear las solicitudes con Nginx.
- Consultar PostgreSQL desde Python.
- Compartir datos entre múltiples instancias.
- Comprender la importancia de separar estado y lógica de negocio.

---

# Arquitectura

```text
                    Cliente
                       |
                       v
                    Nginx
                 /    |    \
                v     v     v
              API1  API2  API3
                \     |     /
                 \    |    /
                 PostgreSQL
```

---

# Parte 1. PostgreSQL

Crear un servicio PostgreSQL:

```yaml
db:
  image: postgres:16
  environment:
    POSTGRES_DB: shop
    POSTGRES_USER: postgres
    POSTGRES_PASSWORD: postgres
```

Crear una tabla:

```sql
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price NUMERIC(10,2) NOT NULL
);
```

Insertar por lo menos cinco productos.

---

# Parte 2. Flask + PostgreSQL

Instalar:

```text
Flask
psycopg[binary]
```

Crear:

```text
GET /products
```

La API debe consultar PostgreSQL y retornar los productos.

Además debe identificar la instancia que procesó la solicitud:

```json
{
  "served_by": "api-2",
  "products": [
    {"id": 1, "name": "Laptop", "price": 3500000}
  ]
}
```

PS C:\Users\Benja\OneDrive\Desktop\IOT\Entregables\03_docker\workshop3> docker compose ps
NAME               IMAGE            COMMAND                  SERVICE   CREATED         STATUS        PORTS
workshop3-api1-1   workshop3-api1   "python app.py"          api1      2 seconds ago   Up 1 second   0.0.0.0:5001->5000/tcp, [::]:5001->5000/tcp
workshop3-db-1     postgres:16      "docker-entrypoint.s…"   db        2 seconds ago   Up 1 second   0.0.0.0:5433->5432/tcp, [::]:5433->5432/tcp
PS C:\Users\Benja\OneDrive\Desktop\IOT\Entregables\03_docker\workshop3> curl.exe -s http://localhost:5001/products
{"products":[{"id":1,"name":"Laptop","price":3500000.0},{"id":2,"name":"Mouse","price":80000.0},{"id":3,"name":"Teclado","price":150000.0},{"id":4,"name":"Monitor","price":900000.0},{"id":5,"name":"Audifonos","price":250000.0}],"served_by":"api-1"}
PS C:\Users\Benja\OneDrive\Desktop\IOT\Entregables\03_docker\workshop3> 

Evidencia de la estructura.

---

# Parte 3. Variables de entorno

Las instancias deben recibir:

```text
INSTANCE
DB_HOST
DB_NAME
DB_USER
DB_PASSWORD
```

La aplicación no debe tener las credenciales escritas directamente en el código fuente.



---

# Parte 4. Tres APIs

```yaml
api1:
  build: ./api
  environment:
    INSTANCE: api-1
    DB_HOST: db
    DB_NAME: shop
    DB_USER: postgres
    DB_PASSWORD: postgres

api2:
  build: ./api
  environment:
    INSTANCE: api-2
    DB_HOST: db
    DB_NAME: shop
    DB_USER: postgres
    DB_PASSWORD: postgres

api3:
  build: ./api
  environment:
    INSTANCE: api-3
    DB_HOST: db
    DB_NAME: shop
    DB_USER: postgres
    DB_PASSWORD: postgres
```
Evidencia de la creacion de las 3 apis

 ✔ Image workshop3-api2       Built                                                                                                         1.7s
 ✔ Image workshop3-api3       Built                                                                                                         1.7s
 ✔ Image workshop3-api1       Built                                                                                                         1.7s
 ✔ Container workshop3-db-1   Running                                                                                                       0.0s
 ✔ Container workshop3-api3-1 Started                                                                                                       3.7s
 ✔ Container workshop3-api1-1 Started                                                                                                       3.7s
 ✔ Container workshop3-api2-1 Started                                                                                                       3.7s
PS C:\Users\Benja\OneDrive\Desktop\IOT\Entregables\03_docker\workshop3> docker compose ps
NAME               IMAGE            COMMAND                  SERVICE   CREATED         STATUS         PORTS
workshop3-api1-1   workshop3-api1   "python app.py"          api1      5 seconds ago   Up 1 second    5000/tcp
workshop3-api2-1   workshop3-api2   "python app.py"          api2      5 seconds ago   Up 1 second    5000/tcp
workshop3-api3-1   workshop3-api3   "python app.py"          api3      5 seconds ago   Up 1 second    5000/tcp
workshop3-db-1     postgres:16      "docker-entrypoint.s…"   db        2 minutes ago   Up 2 minutes   0.0.0.0:5433->5432/tcp, [::]:5433->5432/tcp
PS C:\Users\Benja\OneDrive\Desktop\IOT\Entregables\03_docker\workshop3> 


Configurar Nginx para distribuir las solicitudes entre `api1`, `api2` y `api3`.

Evidencia Nginx ya creado

 ✔ Container workshop3-api3-1  Running                                                                                                      0.0s
 ✔ Container workshop3-db-1    Running                                                                                                      0.0s
 ✔ Container workshop3-api1-1  Running                                                                                                      0.0s
 ✔ Container workshop3-api2-1  Running                                                                                                      0.0s
 ✔ Container workshop3-nginx-1 Started                                                                                                      0.4s
PS C:\Users\Benja\OneDrive\Desktop\IOT\Entregables\03_docker\workshop3> docker compose ps
NAME                IMAGE            COMMAND                  SERVICE   CREATED         STATUS         PORTS
workshop3-api1-1    workshop3-api1   "python app.py"          api1      2 minutes ago   Up 2 minutes   5000/tcp
workshop3-api2-1    workshop3-api2   "python app.py"          api2      2 minutes ago   Up 2 minutes   5000/tcp
workshop3-api3-1    workshop3-api3   "python app.py"          api3      2 minutes ago   Up 2 minutes   5000/tcp
workshop3-db-1      postgres:16      "docker-entrypoint.s…"   db        4 minutes ago   Up 4 minutes   0.0.0.0:5433->5432/tcp, [::]:5433->5432/tcp
workshop3-nginx-1   nginx:alpine     "/docker-entrypoint.…"   nginx     4 seconds ago   Up 4 seconds   0.0.0.0:8082->80/tcp, [::]:8082->80/tcp
PS C:\Users\Benja\OneDrive\Desktop\IOT\Entregables\03_docker\workshop3> 

---

# Parte 5. Prueba de integración

```bash
docker compose up --build
```

Luego:

```bash
for i in {1..15}; do curl -s http://localhost:8080/products; echo; done
```

Comprobar que:

- Cambia `served_by`.
- Los datos de productos son los mismos.
- Las tres APIs consultan el mismo estado persistente.

Evidencia de distribucion de solicitudes con Nginx
```
PS C:\Users\Benja\OneDrive\Desktop\IOT\Entregables\03_docker\workshop3> 1..15 | ForEach-Object {
     curl.exe -s -H "Connection: close" http://localhost:8082/products
     Write-Output ""
 }
{"products":[{"id":1,"name":"Laptop","price":3500000.0},{"id":2,"name":"Mouse","price":80000.0},{"id":3,"name":"Teclado","price":150000.0},{"id":4,"name":"Monitor","price":900000.0},{"id":5,"name":"Audifonos","price":250000.0}],"served_by":"api-1"}

{"products":[{"id":1,"name":"Laptop","price":3500000.0},{"id":2,"name":"Mouse","price":80000.0},{"id":3,"name":"Teclado","price":150000.0},{"id":4,"name":"Monitor","price":900000.0},{"id":5,"name":"Audifonos","price":250000.0}],"served_by":"api-2"}

{"products":[{"id":1,"name":"Laptop","price":3500000.0},{"id":2,"name":"Mouse","price":80000.0},{"id":3,"name":"Teclado","price":150000.0},{"id":4,"name":"Monitor","price":900000.0},{"id":5,"name":"Audifonos","price":250000.0}],"served_by":"api-3"}

{"products":[{"id":1,"name":"Laptop","price":3500000.0},{"id":2,"name":"Mouse","price":80000.0},{"id":3,"name":"Teclado","price":150000.0},{"id":4,"name":"Monitor","price":900000.0},{"id":5,"name":"Audifonos","price":250000.0}],"served_by":"api-1"}

{"products":[{"id":1,"name":"Laptop","price":3500000.0},{"id":2,"name":"Mouse","price":80000.0},{"id":3,"name":"Teclado","price":150000.0},{"id":4,"name":"Monitor","price":900000.0},{"id":5,"name":"Audifonos","price":250000.0}],"served_by":"api-2"}

{"products":[{"id":1,"name":"Laptop","price":3500000.0},{"id":2,"name":"Mouse","price":80000.0},{"id":3,"name":"Teclado","price":150000.0},{"id":4,"name":"Monitor","price":900000.0},{"id":5,"name":"Audifonos","price":250000.0}],"served_by":"api-3"}

{"products":[{"id":1,"name":"Laptop","price":3500000.0},{"id":2,"name":"Mouse","price":80000.0},{"id":3,"name":"Teclado","price":150000.0},{"id":4,"name":"Monitor","price":900000.0},{"id":5,"name":"Audifonos","price":250000.0}],"served_by":"api-1"}

{"products":[{"id":1,"name":"Laptop","price":3500000.0},{"id":2,"name":"Mouse","price":80000.0},{"id":3,"name":"Teclado","price":150000.0},{"id":4,"name":"Monitor","price":900000.0},{"id":5,"name":"Audifonos","price":250000.0}],"served_by":"api-2"}

{"products":[{"id":1,"name":"Laptop","price":3500000.0},{"id":2,"name":"Mouse","price":80000.0},{"id":3,"name":"Teclado","price":150000.0},{"id":4,"name":"Monitor","price":900000.0},{"id":5,"name":"Audifonos","price":250000.0}],"served_by":"api-3"}

{"products":[{"id":1,"name":"Laptop","price":3500000.0},{"id":2,"name":"Mouse","price":80000.0},{"id":3,"name":"Teclado","price":150000.0},{"id":4,"name":"Monitor","price":900000.0},{"id":5,"name":"Audifonos","price":250000.0}],"served_by":"api-1"}

{"products":[{"id":1,"name":"Laptop","price":3500000.0},{"id":2,"name":"Mouse","price":80000.0},{"id":3,"name":"Teclado","price":150000.0},{"id":4,"name":"Monitor","price":900000.0},{"id":5,"name":"Audifonos","price":250000.0}],"served_by":"api-2"}

{"products":[{"id":1,"name":"Laptop","price":3500000.0},{"id":2,"name":"Mouse","price":80000.0},{"id":3,"name":"Teclado","price":150000.0},{"id":4,"name":"Monitor","price":900000.0},{"id":5,"name":"Audifonos","price":250000.0}],"served_by":"api-3"}

{"products":[{"id":1,"name":"Laptop","price":3500000.0},{"id":2,"name":"Mouse","price":80000.0},{"id":3,"name":"Teclado","price":150000.0},{"id":4,"name":"Monitor","price":900000.0},{"id":5,"name":"Audifonos","price":250000.0}],"served_by":"api-1"}

{"products":[{"id":1,"name":"Laptop","price":3500000.0},{"id":2,"name":"Mouse","price":80000.0},{"id":3,"name":"Teclado","price":150000.0},{"id":4,"name":"Monitor","price":900000.0},{"id":5,"name":"Audifonos","price":250000.0}],"served_by":"api-2"}

{"products":[{"id":1,"name":"Laptop","price":3500000.0},{"id":2,"name":"Mouse","price":80000.0},{"id":3,"name":"Teclado","price":150000.0},{"id":4,"name":"Monitor","price":900000.0},{"id":5,"name":"Audifonos","price":250000.0}],"served_by":"api-3"}

PS C:\Users\Benja\OneDrive\Desktop\IOT\Entregables\03_docker\workshop3> 

```


---

# Parte 6. Prueba de tolerancia ante fallo

Detener una API:

```bash
docker compose stop api2
```

Repetir las solicitudes.

Después detener dos APIs y observar qué ocurre.

Se realiza el balanceo correctamente, se quita la api2 y sigue funcionando con api1 y api3

```

PS C:\Users\Benja\OneDrive\Desktop\IOT\Entregables\03_docker\workshop3> docker compose stop api2
[+] stop 1/1
 ✔ Container workshop3-api2-1 Stopped                                                                                                       3.2s
PS C:\Users\Benja\OneDrive\Desktop\IOT\Entregables\03_docker\workshop3> docker compose ps
NAME                IMAGE            COMMAND                  SERVICE   CREATED         STATUS         PORTS
workshop3-api1-1    workshop3-api1   "python app.py"          api1      7 minutes ago   Up 7 minutes   5000/tcp
workshop3-api3-1    workshop3-api3   "python app.py"          api3      7 minutes ago   Up 7 minutes   5000/tcp
workshop3-db-1      postgres:16      "docker-entrypoint.s…"   db        9 minutes ago   Up 9 minutes   0.0.0.0:5433->5432/tcp, [::]:5433->5432/tcp
workshop3-nginx-1   nginx:alpine     "/docker-entrypoint.…"   nginx     5 minutes ago   Up 5 minutes   0.0.0.0:8082->80/tcp, [::]:8082->80/tcp
PS C:\Users\Benja\OneDrive\Desktop\IOT\Entregables\03_docker\workshop3> 1..10 | ForEach-Object {
>>     curl.exe -s -H "Connection: close" http://localhost:8082/products
>>     Write-Output ""
>> }
{"products":[{"id":1,"name":"Laptop","price":3500000.0},{"id":2,"name":"Mouse","price":80000.0},{"id":3,"name":"Teclado","price":150000.0},{"id":4,"name":"Monitor","price":900000.0},{"id":5,"name":"Audifonos","price":250000.0}],"served_by":"api-1"}

{"products":[{"id":1,"name":"Laptop","price":3500000.0},{"id":2,"name":"Mouse","price":80000.0},{"id":3,"name":"Teclado","price":150000.0},{"id":4,"name":"Monitor","price":900000.0},{"id":5,"name":"Audifonos","price":250000.0}],"served_by":"api-3"}

{"products":[{"id":1,"name":"Laptop","price":3500000.0},{"id":2,"name":"Mouse","price":80000.0},{"id":3,"name":"Teclado","price":150000.0},{"id":4,"name":"Monitor","price":900000.0},{"id":5,"name":"Audifonos","price":250000.0}],"served_by":"api-3"}

{"products":[{"id":1,"name":"Laptop","price":3500000.0},{"id":2,"name":"Mouse","price":80000.0},{"id":3,"name":"Teclado","price":150000.0},{"id":4,"name":"Monitor","price":900000.0},{"id":5,"name":"Audifonos","price":250000.0}],"served_by":"api-3"}

{"products":[{"id":1,"name":"Laptop","price":3500000.0},{"id":2,"name":"Mouse","price":80000.0},{"id":3,"name":"Teclado","price":150000.0},{"id":4,"name":"Monitor","price":900000.0},{"id":5,"name":"Audifonos","price":250000.0}],"served_by":"api-1"}

{"products":[{"id":1,"name":"Laptop","price":3500000.0},{"id":2,"name":"Mouse","price":80000.0},{"id":3,"name":"Teclado","price":150000.0},{"id":4,"name":"Monitor","price":900000.0},{"id":5,"name":"Audifonos","price":250000.0}],"served_by":"api-3"}

{"products":[{"id":1,"name":"Laptop","price":3500000.0},{"id":2,"name":"Mouse","price":80000.0},{"id":3,"name":"Teclado","price":150000.0},{"id":4,"name":"Monitor","price":900000.0},{"id":5,"name":"Audifonos","price":250000.0}],"served_by":"api-1"}

{"products":[{"id":1,"name":"Laptop","price":3500000.0},{"id":2,"name":"Mouse","price":80000.0},{"id":3,"name":"Teclado","price":150000.0},{"id":4,"name":"Monitor","price":900000.0},{"id":5,"name":"Audifonos","price":250000.0}],"served_by":"api-3"}

{"products":[{"id":1,"name":"Laptop","price":3500000.0},{"id":2,"name":"Mouse","price":80000.0},{"id":3,"name":"Teclado","price":150000.0},{"id":4,"name":"Monitor","price":900000.0},{"id":5,"name":"Audifonos","price":250000.0}],"served_by":"api-1"}

{"products":[{"id":1,"name":"Laptop","price":3500000.0},{"id":2,"name":"Mouse","price":80000.0},{"id":3,"name":"Teclado","price":150000.0},{"id":4,"name":"Monitor","price":900000.0},{"id":5,"name":"Audifonos","price":250000.0}],"served_by":"api-3"}

PS C:\Users\Benja\OneDrive\Desktop\IOT\Entregables\03_docker\workshop3> 

```

---

# Parte 7. Reto CRUD

Agregar:

```text
GET /products/<id>
POST /products
PUT /products/<id>
DELETE /products/<id>
```

El alumno debe demostrar que un registro creado desde una instancia puede ser consultado desde otra.

### Demostración de estado compartido

El producto `id: 6` fue creado mediante una solicitud atendida por `api-1`. Posteriormente, el mismo registro fue consultado mediante solicitudes atendidas por `api-2` y `api-3`, conservando los mismos datos.

Esto demuestra que el registro no se almacenó dentro de una instancia específica de Flask, sino en PostgreSQL, que es compartido por las tres APIs.

---

# Análisis

1. ¿Dónde se encuentra el estado del negocio?
El estado del negocio se encuentra en PostgreSQL. Allí se almacenan los productos y sus cambios, como creaciones, actualizaciones y eliminaciones.

2. ¿Por qué las APIs pueden ser stateless?
Porque las APIs no almacenan los productos dentro de sus contenedores. Cada solicitud consulta o modifica PostgreSQL, que es la fuente central de datos. Por eso cualquier instancia puede atender cualquier solicitud.

3. ¿Qué ocurre si una API reinicia?
La instancia que reinicia deja de atender solicitudes temporalmente. Nginx puede redirigir las solicitudes hacia las otras APIs disponibles. Cuando la instancia vuelve a estar activa, puede consultar nuevamente los mismos datos de PostgreSQL.

4. ¿Qué ocurre si PostgreSQL reinicia?
Durante el reinicio, las APIs no podrán consultar ni modificar productos. Cuando PostgreSQL vuelva a estar disponible, las APIs recuperarán el acceso a los datos. El volumen postgres_data permite conservar la información.

5. ¿Dónde existen puntos únicos de falla?
Nginx y PostgreSQL pueden convertirse en puntos únicos de falla. Si Nginx se detiene, los clientes no pueden acceder a las APIs. Si PostgreSQL falla, ninguna API puede consultar ni modificar el estado del negocio.

6. ¿El balanceamiento de API soluciona el escalamiento de la base de datos?
No. El balanceamiento distribuye las solicitudes entre las APIs, pero todas siguen utilizando la misma base de datos. PostgreSQL puede convertirse en un cuello de botella y necesitar réplicas, particionamiento, optimización o escalamiento propio.

7. ¿Qué mecanismos podrían añadirse en una arquitectura de producción?
Podrían agregarse:

Réplicas de PostgreSQL y alta disponibilidad.
Backups automáticos.
Pool de conexiones.
Health checks.
HTTPS y autenticación.
Monitoreo y registro centralizado.
Límites de solicitudes.
Caché, por ejemplo Redis.
Migraciones de base de datos.
Contenedores administrados u orquestación con Kubernetes.


---

# Entregables

- API Flask.
- Dockerfile.
- `docker-compose.yml`.
- `nginx.conf`.
- Script SQL.
- Evidencia del balanceamiento.
- Evidencia de consulta a PostgreSQL.
- Respuestas de análisis.
