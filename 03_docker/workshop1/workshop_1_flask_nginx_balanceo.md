# Taller 1 - API Flask y Balanceamiento de Carga con Nginx

**Curso:** Computación en la Nube e Internet de las Cosas

**Temas**:

- Python y Flask
- Dockerfile
- Docker Compose
- Nginx
- Reverse Proxy
- Load Balancing
- Escalamiento horizontal

---

# Objetivos

Al finalizar este workshop el estudiante será capaz de:

- Construir una API sencilla con Flask.
- Crear una imagen Docker para una aplicación Python.
- Ejecutar varias instancias de la misma API.
- Configurar Nginx como balanceador.
- Identificar qué instancia respondió a cada solicitud.
- Explicar la relación entre balanceamiento y escalamiento horizontal.

---

# Conceptos que se trabajarán

- API REST
- Contenedor
- Imagen
- Servicio de Docker Compose
- Instancia
- Upstream de Nginx
- Round Robin
- Escalamiento horizontal
- Punto de entrada único

---

# Parte 1. Construcción de la API

Crear `app.py` con un endpoint `GET /`.

La respuesta debe tener el siguiente formato:

```json
{
  "message": "Hola desde Flask",
  "instance": "api-1"
}
```

El valor de `instance` debe venir de una variable de entorno.

```python
import os
from flask import Flask, jsonify

app = Flask(__name__)
INSTANCE = os.getenv("INSTANCE", "api-local")

@app.get("/")
def home():
    return jsonify({
        "message": "Hola desde Flask",
        "instance": INSTANCE
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

Crear `requirements.txt`:

```text
Flask
```

---

# Parte 2. Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]
```

Construir y probar la imagen individualmente antes de crear el balanceamiento.

docker build -t workshop1-api-test .

---

# Parte 3. Docker Compose con tres instancias

Crear tres servicios a partir de la misma imagen:

```yaml
services:
  api1:
    build: ./api
    environment:
      INSTANCE: api-1

  api2:
    build: ./api
    environment:
      INSTANCE: api-2

  api3:
    build: ./api
    environment:
      INSTANCE: api-3

  nginx:
    image: nginx:alpine
    ports:
      - "8080:80"
```

---

# Parte 4. Configuración de Nginx

Crear `nginx/nginx.conf`:

```nginx
upstream flask_backend {
    server api1:5000;
    server api2:5000;
    server api3:5000;
}

server {
    listen 80;

    location / {
        proxy_pass http://flask_backend;
    }
}
```

Completar el servicio Nginx:

```yaml
nginx:
  image: nginx:alpine
  ports:
    - "8080:80"
  volumes:
    - ./nginx/nginx.conf:/etc/nginx/conf.d/default.conf:ro
  depends_on:
    - api1
    - api2
    - api3
```

---

# Parte 5. Evidenciar el balanceamiento

Levantar:

```bash
docker compose up --build
```

Ejecutar:

```bash
for i in {1..12}; do curl -s http://localhost:8080/; echo; done
```

1..12 | ForEach-Object { curl.exe -s -H "Connection: close" http://localhost:8080/; Write-Output "" }
aca me toco cambiar el comando al equivalente en windows
resultados:

PS C:\Users\Benja\OneDrive\Desktop\IOT\Entregables\03_docker\workshop1> 1..12 | ForEach-Object { curl.exe -s -H "Connection: close" http://localhost:8080/; Write-Output "" }
{"instance":"api-1","message":"Hola desde Flask"}

{"instance":"api-2","message":"Hola desde Flask"}

{"instance":"api-3","message":"Hola desde Flask"}

{"instance":"api-1","message":"Hola desde Flask"}

{"instance":"api-2","message":"Hola desde Flask"}

{"instance":"api-3","message":"Hola desde Flask"}

{"instance":"api-1","message":"Hola desde Flask"}

{"instance":"api-2","message":"Hola desde Flask"}

{"instance":"api-3","message":"Hola desde Flask"}

{"instance":"api-2","message":"Hola desde Flask"}

{"instance":"api-3","message":"Hola desde Flask"}

{"instance":"api-1","message":"Hola desde Flask"}

PS C:\Users\Benja\OneDrive\Desktop\IOT\Entregables\03_docker\workshop1> 

Identificar qué instancias aparecen.

Detener una instancia:

```bash
docker compose stop api2
```

Volver a probar las solicitudes y documentar el comportamiento.

---

# Parte 6. Preguntas de análisis

1. ¿Por qué el cliente solamente conoce `localhost:8080`?
Porque Nginx funciona como punto de entrada único. El cliente envía todas las solicitudes a localhost:8080, y Nginx las redirige internamente a api1, api2 o api3.

2. ¿Qué función cumple `upstream`?
Define el grupo de servidores Flask que recibirán las solicitudes:

upstream flask_backend {
    server api1:5000;
    server api2:5000;
    server api3:5000;
}

3. ¿Qué estrategia utiliza Nginx por defecto en este escenario?
Utiliza Round Robin. Distribuye las solicitudes sucesivamente entre los servidores disponibles.

4. ¿Qué ocurre al detener `api2`?
Nginx detecta que api2 no responde y deja de enviarle solicitudes temporalmente. Las solicitudes continúan siendo atendidas por api1 y api3.

5. ¿Qué componente podría convertirse en un punto único de falla?
Nginx. Si el contenedor de Nginx se detiene, el cliente ya no puede acceder a ninguna instancia, aunque las APIs Flask sigan funcionando.

6. ¿Por qué este diseño representa escalamiento horizontal?
Porque se ejecutan varias copias iguales de la API, cada una en un contenedor independiente. Se aumenta la capacidad agregando más instancias, en lugar de hacer más potente una sola instancia.

7. ¿Qué tendría que cambiar para tener cinco instancias?
Agregar api4 y api5 en docker-compose.yml:
api4:
  build: ./api
  environment:
    INSTANCE: api-4

api5:
  build: ./api
  environment:
    INSTANCE: api-5

Y agregarlas al upstream de Nginx:

upstream flask_backend {
    server api1:5000;
    server api2:5000;
    server api3:5000;
    server api4:5000;
    server api5:5000;
}


Después se reconstruye el entorno:
docker compose up --build -d

---

# Reto

Agregar un endpoint `/health` que responda:

```json
{
  "status": "ok",
  "instance": "api-1"
}
```

Agregamos esto a app.py
```py
@app.get("/health")
def health():
    return jsonify({
        "status": "ok",
        "instance": INSTANCE
    })
```
Reconstruimos 

docker compose up --build -d

probamos:

1..6 | ForEach-Object {
    curl.exe -s -H "Connection: close" http://localhost:8080/health
    Write-Output ""
}

PS C:\Users\Benja\OneDrive\Desktop\IOT\Entregables\03_docker\workshop1> 1..6 | ForEach-Object {
     curl.exe -s -H "Connection: close" http://localhost:8080/health
     Write-Output ""
 }
{"instance":"api-1","status":"ok"}

{"instance":"api-1","status":"ok"}

{"instance":"api-1","status":"ok"}

{"instance":"api-1","status":"ok"}

{"instance":"api-1","status":"ok"}

{"instance":"api-1","status":"ok"}

Luego investigar cómo podría usarse en una estrategia de health check.

El endpoint sirve como health check porque un sistema externo puede consultar periódicamente /health. Si recibe status: "ok", la instancia está funcionando; si recibe error o no responde, Nginx o el sistema de monitoreo puede dejar de enviarle tráfico y alertar sobre la instancia.

---

# Entregables

- `app.py`
- `requirements.txt`
- `Dockerfile`
- `docker-compose.yml`
- `nginx.conf`
- Evidencias del balanceamiento.
- Respuestas a las preguntas.
