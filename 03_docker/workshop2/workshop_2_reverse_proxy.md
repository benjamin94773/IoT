# Taller 2 - Reverse Proxy con Nginx

**Curso:** Computación en la Nube e Internet de las Cosas

**Temas**:

- Nginx
- Reverse Proxy
- Routing por rutas
- Docker Compose
- Flask

---

# Objetivos

Al finalizar este workshop el estudiante será capaz de:

- Comprender el concepto de reverse proxy.
- Configurar Nginx como punto único de entrada.
- Enrutar diferentes rutas hacia diferentes servicios.
- Ocultar los puertos internos de las aplicaciones.
- Explicar por qué un reverse proxy no implica necesariamente balanceamiento.

---

# Parte 1. Construir dos APIs

Crear dos aplicaciones independientes.

### Servicio users

Ruta interna:

```text
/
```

Respuesta:

```json
{
  "service": "users",
  "message": "Servicio de usuarios"
}
```

### Servicio products

Respuesta:

```json
{
  "service": "products",
  "message": "Servicio de productos"
}
```

---

# Parte 2. Docker Compose

```yaml
services:
  users:
    build: ./users

  products:
    build: ./products

  nginx:
    image: nginx:alpine
    ports:
      - "8080:80"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/conf.d/default.conf:ro
    depends_on:
      - users
      - products
```

Observe que los servicios Flask no publican puertos al host. Nginx será la puerta de entrada.

---

# Parte 3. Reverse Proxy

Crear `nginx.conf`:

```nginx
server {
    listen 80;

    location /api/users/ {
        proxy_pass http://users:5000/;
    }

    location /api/products/ {
        proxy_pass http://products:5000/;
    }
}
```

Probar:

```bash
curl http://localhost:8080/api/users/
curl http://localhost:8080/api/products/

```

PS C:\Users\Benja\OneDrive\Desktop\IOT\Entregables\03_docker\workshop2> curl.exe -s http://localhost:8081/api/users/
{"message":"Servicio de usuarios","service":"users"}
PS C:\Users\Benja\OneDrive\Desktop\IOT\Entregables\03_docker\workshop2> curl.exe -s http://localhost:8081/api/products/
{"message":"Servicio de productos","service":"products"}

Nginx funciona como reverse proxy porque recibe las solicitudes en localhost:8081 y las reenvía a diferentes servicios internos según la ruta solicitada. /api/users/ se dirige al contenedor users, mientras que /api/products/ se dirige al contenedor products. En esta etapa no existe balanceamiento porque cada ruta apunta a un único servicio.

---

# Parte 4. Analizar la diferencia

En este workshop cada ruta es enviada a un backend específico:

```text
/api/users    -> users
/api/products -> products
```

No existe distribución entre varias instancias de `users` o `products`.

Por tanto, el mecanismo principal observado es **reverse proxy + routing**, no balanceamiento.

---

# Parte 5. Transformar el ejercicio en Reverse Proxy + Load Balancer

Crear dos instancias del servicio `users`:

```yaml
users1:
  build: ./users

users2:
  build: ./users
```

Configurar:

```nginx
upstream users_backend {
    server users1:5000;
    server users2:5000;
}

server {
    listen 80;

    location /api/users/ {
        proxy_pass http://users_backend/;
    }
}
```

El estudiante deberá demostrar experimentalmente la diferencia.

Se reconstruyeron los servicios:
docker compose down --remove-orphans
docker compose up --build -d
docker compose ps

Los servicios activos fueron:
workshop2-users1-1
workshop2-users2-1
workshop2-products-1
workshop2-nginx-1

Evidencia del balanceamiento
Se realizaron varias solicitudes:
PS C:\Users\Benja\OneDrive\Desktop\IOT\Entregables\03_docker\workshop2> 1..12 | ForEach-Object {
     curl.exe -s -H "Connection: close" http://localhost:8081/api/users/
     Write-Output ""
 }
{"instance":"users-1","message":"Servicio de usuarios","service":"users"}

{"instance":"users-2","message":"Servicio de usuarios","service":"users"}

{"instance":"users-1","message":"Servicio de usuarios","service":"users"}

{"instance":"users-2","message":"Servicio de usuarios","service":"users"}

{"instance":"users-1","message":"Servicio de usuarios","service":"users"}

{"instance":"users-2","message":"Servicio de usuarios","service":"users"}

{"instance":"users-1","message":"Servicio de usuarios","service":"users"}

{"instance":"users-2","message":"Servicio de usuarios","service":"users"}

{"instance":"users-1","message":"Servicio de usuarios","service":"users"}

{"instance":"users-2","message":"Servicio de usuarios","service":"users"}

{"instance":"users-1","message":"Servicio de usuarios","service":"users"}

{"instance":"users-2","message":"Servicio de usuarios","service":"users"}

Se observa que Nginx distribuye las solicitudes entre users1 y users2.
---

# Reto

Agregar:

```text
/api/orders/
```

y posteriormente crear dos instancias del servicio `orders` y balancearlas.

---

# Entregables

- APIs Flask.
- Dockerfiles.
- `docker-compose.yml`.
- `nginx.conf`.
- Evidencias de routing.
- Evidencias del cambio a load balancing.
- Explicación escrita de la diferencia entre ambos escenarios.
