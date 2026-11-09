# Taller 3 - Docker Compose y Nginx

**Curso:** Computación en la Nube e Internet de las Cosas

**Temas**:

- Docker Compose
- Servicios
- Nginx
- Puertos
- Volúmenes
- Build
- Imágenes
- Redes entre servicios

---

# Objetivos

Al finalizar este workshop el estudiante será capaz de:

- Definir un servicio mediante `docker-compose.yml`.
- Ejecutar Nginx usando Docker Compose.
- Publicar un puerto del contenedor hacia el host.
- Montar contenido mediante volúmenes.
- Construir un servicio a partir de un `Dockerfile`.
- Levantar y detener un conjunto de servicios utilizando Compose.

---

# Conceptos que se trabajarán

- `docker-compose.yml`
- YAML
- `services`
- `image`
- `build`
- `ports`
- `volumes`
- `environment`
- `depends_on`
- Redes Docker
- Persistencia
- Orquestación local

---

# Comandos que se utilizarán

| Comando | Descripción |
|----------|-------------|
| `docker compose up` | Crear e iniciar los servicios |
| `docker compose up -d` | Iniciar servicios en segundo plano |
| `docker compose down` | Detener y eliminar los servicios |
| `docker compose ps` | Mostrar estado de servicios |
| `docker compose logs` | Mostrar logs |
| `docker compose build` | Construir imágenes de los servicios |
| `docker compose exec` | Ejecutar comandos dentro de un servicio |

---

# Parte 1. Primer servicio Nginx

Crear `docker-compose.yml`:

```yaml
services:
  web:
    image: nginx:alpine
    ports:
      - "8080:80"
```

Levantar el servicio:

```bash
docker compose up -d
```

Verificar:

```bash
docker compose ps
```

Abrir en el navegador:

```text
http://localhost:8080
```

Consultar logs:

```bash
docker compose logs web
```

Detener:

```bash
docker compose down
```

---

# Parte 2. Nginx con contenido propio

Crear:

```text
proyecto/
├── docker-compose.yml
└── html/
    └── index.html
```

Contenido de `index.html`:

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Mi primer servicio Docker</title>
</head>
<body>
    <h1>Hola desde Nginx y Docker Compose</h1>
    <p>Este contenido está siendo servido desde un contenedor.</p>
</body>
</html>
```

Modificar `docker-compose.yml`:

```yaml
services:
  web:
    image: nginx:alpine
    ports:
      - "8080:80"
    volumes:
      - ./html:/usr/share/nginx/html:ro
```

Levantar:

```bash
docker compose up -d
```

Abrir:

```text
http://localhost:8080
```

Modificar `index.html` y comprobar el cambio en el navegador.

## Preguntas

1. ¿Por qué el cambio aparece sin reconstruir la imagen?
Porque el contenido de la página se monta mediante un volumen:
volumes:
  ./html:/usr/share/nginx/html:ro
Eso significa que Nginx está sirviendo archivos que están en tu carpeta del host, no en la imagen construida. Cuando cambias index.html, Docker refleja ese cambio inmediatamente, sin necesidad de volver a ejecutar docker build o reconstruir la imagen.

2. ¿Qué función cumple `:ro`?
ro significa “read-only” (solo lectura).
en el contexto quiere decir que:
./html = carpeta del host
/usr/share/nginx/html = carpeta dentro del contenedor
:ro = el contenedor puede leer ese contenido, pero no puede modificarlo
Esto sirve para evitar que el servicio interno altere el contenido del proyecto del host.

3. ¿Cuál es la diferencia entre el puerto `8080` y el `80`?
80 es el puerto interno del contenedor, donde Nginx escucha por defecto.
8080 es el puerto del host (tu máquina), que expones para acceder desde el navegador.
ports:
   "8080:80"
se está indicando:
que en la computadora es: localhost:8080
dentro del contenedor: nginx escucha en 80

4. ¿Qué parte representa el host y qué parte representa el contenedor?
  ./html:/usr/share/nginx/html:ro
se distinguen dos partes:

./html = host
/usr/share/nginx/html = contenedor
Es decir:

del lado del host está la carpeta del proyecto en tu computadora
del lado del contenedor está la carpeta donde Nginx busca el contenido que va a servir

---

# Parte 3. Compose utilizando un Dockerfile

Crear esta estructura:

```text
proyecto/
├── docker-compose.yml
├── Dockerfile
└── html/
    └── index.html
```

`Dockerfile`:

```dockerfile
FROM nginx:alpine
COPY html/ /usr/share/nginx/html/
```

`docker-compose.yml`:

```yaml
services:
  web:
    build: .
    ports:
      - "8080:80"
```

Construir y levantar:

```bash
docker compose up --build -d
```

---

# Parte 4. Reto integrador

Construir un pequeño proyecto con dos servicios:

```text
Servicio 1: Nginx
Servicio 2: Ubuntu/Bash
```

Requisitos:

- Nginx debe estar disponible en `localhost:8080`.
- El servicio Ubuntu debe contener `monitor.sh` y `analiza.sh`.
- Los scripts deben poder ejecutarse dentro del contenedor.
- Debe existir un volumen para compartir una carpeta de logs.
- El estudiante debe demostrar que los dos servicios pueden ejecutarse simultáneamente.

## Pregunta de diseño

Explique por qué Docker Compose resulta más conveniente que ejecutar manualmente varios `docker run` cuando un sistema comienza a tener múltiples servicios.

Porque Compose permite definir todos los servicios de la aplicación en un solo archivo, con sus redes, puertos y volúmenes. En lugar de lanzar cada contenedor manualmente, puedes levantar todo el sistema con un solo comando:

docker compose up -d
Y si necesitamos detenerlo:
docker compose down

Esto es mucho más práctico cuando la aplicación tiene varios servicios, porque:

organiza mejor la configuración
facilita la repetición
evita errores de comandos largos
centraliza la infraestructura del proyecto
permite que servicios se vean entre sí por red Docker
Cuando el sistema crece, docker run manual se vuelve difícil de mantener; Compose lo hace mucho más simple y escalable.

---

# Entregables

- `docker-compose.yml`.
- `Dockerfile` para Nginx.
- Página `index.html` personalizada.
- Servicios funcionando correctamente.
- Evidencia de `docker compose ps`.
- Evidencia de acceso a Nginx.
- Respuestas a las preguntas de análisis.
