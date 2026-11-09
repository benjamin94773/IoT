# Workshop 3 - Docker: Introducción a los Contenedores

**Curso:** Computación en la Nube e Internet de las Cosas

**Temas**:
    - Docker

---

# Objetivos

Al finalizar este workshop el estudiante será capaz de:

- Comprender el concepto de contenedor.
- Diferenciar imágenes y contenedores.
- Descargar imágenes desde Docker Hub.
- Ejecutar y administrar contenedores.
- Inspeccionar recursos Docker.

---

# Conceptos que se trabajarán

- Docker
- Imagen
- Contenedor
- Docker Hub
- Dockerfile
- Redes
- Volúmenes
- Logs
- Persistencia

---

# Comandos que se utilizarán

| Comando | Descripción |
|----------|-------------|
| docker --version | Verificar instalación |
| docker pull | Descargar imágenes |
| docker images | Listar imágenes |
| docker run | Crear contenedores |
| docker ps | Mostrar contenedores |
| docker stop | Detener contenedores |
| docker start | Iniciar contenedores |
| docker rm | Eliminar contenedores |
| docker rmi | Eliminar imágenes |
| docker exec | Ejecutar comandos |
| docker logs | Ver registros |
| docker inspect | Información detallada |
| docker network ls | Redes |
| docker volume ls | Volúmenes |
| docker system df | Uso de disco |
| docker system prune | Limpiar recursos |

---

# Parte 1. Introducción a Docker

## Conceptos fundamentales

- Imagen
- Contenedor
- Dockerfile
- Docker Hub

## ¿Por qué utilizar Docker?

- Portabilidad.
- Escalabilidad.
- Aislamiento.
- Integración con CI/CD.
- Despliegue de microservicios.

---

# Parte 2. Explorando Docker

Ejecute:

```bash
docker --version
docker images
docker system df
```

Analice la salida obtenida.

---

# Parte 3. Descarga de imágenes

Descargue:

```bash
docker pull ubuntu
docker pull nginx
```

Verifique:

```bash
docker images
```

---

# Parte 4. Primer contenedor

Ejecute:

```bash
docker run -it ubuntu bash
```

Dentro del contenedor:

```bash
pwd
ls
whoami
exit
```

---

# Parte 5. Contenedor Web

Ejecute:

```bash
docker run -d -p 8080:80 nginx
```

Verifique:

```bash
docker ps
```

Acceda desde el navegador:

```
http://localhost:8080
```

---

# Parte 6. Administración

Practique los siguientes comandos:

```bash
docker stop
docker start
docker logs
docker exec
docker inspect
docker rm
docker rmi
```

Explique qué hace cada uno.

Comando,¿Qué hace?
docker stop,"Envía una señal (SIGTERM, y luego SIGKILL si no responde) a un contenedor en ejecución para detener sus procesos de forma ordenada sin borrarlo."
docker start,"Inicia uno o varios contenedores que previamente se encontraban detenidos, preservando su configuración y estado de disco previo."
docker logs,Muestra en la terminal los flujos de salida estándar (STDOUT) y error estándar (STDERR) generados por los procesos dentro del contenedor.
docker exec,Ejecuta un comando nuevo dentro de un contenedor que ya está en ejecución (frecuentemente usado para abrir una terminal interactiva tipo bash o sh).
docker inspect,"Devuelve toda la información detallada de bajo nivel de un contenedor, imagen, volumen o red en formato estructurado JSON (direcciones IP, puertos, variables de entorno, rutas montadas)."
docker rm,Elimina uno o más contenedores del sistema de archivos local (por defecto solo funciona en contenedores detenidos).
docker rmi,"Elimina una o más imágenes de Docker del almacenamiento local (siempre que ningún contenedor, activo o detenido, dependa de ella)."

---

# Parte 7. Recursos Docker

Explore:

```bash
docker network ls
docker volume ls
docker system df
docker system prune
```

Analice qué recursos administra cada comando.

### Análisis de Recursos Administrados en Docker

| Comando | Recurso Administrado | Función y Propósito |
| :--- | :--- | :--- |
| **`docker network ls`** | Redes virtuales (*Networks*) | Lista las redes disponibles (`bridge`, `host`, `overlay`). Permite auditar la conectividad, topología y aislamiento entre contenedores. |
| **`docker volume ls`** | Almacenamiento persistente (*Volumes*) | Lista los volúmenes de datos locales gestionados por Docker. Controla la persistencia de datos independientes del ciclo de vida del contenedor. |
| **`docker system df`** | Almacenamiento global en disco | Muestra un resumen del espacio ocupado y reutilizable en imágenes, contenedores, volúmenes locales y caché de compilación (*build cache*). |
| **`docker system prune`** | Mantenimiento y espacio (*Garbage Collector*) | Elimina de forma masiva recursos huérfanos o en desuso: contenedores detenidos, redes sin uso, imágenes colgantes (*dangling*) y caché de compilación. *(No borra volúmenes por defecto para proteger los datos)*. |

---

# Reto Integrador

Implemente un entorno compuesto por:

- Un contenedor Ubuntu.
- Un contenedor Nginx.
- Acceda al contenedor Ubuntu mediante `docker exec`.
- Consulte los logs del contenedor Nginx.
- Detenga ambos contenedores.
- Elimine los contenedores.
- Elimine las imágenes descargadas.

Documente cada comando utilizado y describa el propósito de cada uno.

### Tabla resumen de comandos

| Comando | Sintaxis utilizada | Propósito principal | Resultado esperado |
| :--- | :--- | :--- | :--- |
| `docker run` **(Ubuntu)** | `docker run -d -it --name servidor-ubuntu ubuntu` | Crear e inicializar el contenedor Ubuntu en segundo plano manteniendo una sesión interactiva activa. | Contenedor en ejecución continua (`Up`) sin cerrarse tras la inicialización. |
| `docker run` **(Nginx)** | `docker run -d --name servidor-nginx -p 8080:80 nginx` | Desplegar el servidor web Nginx en segundo plano y vincular puertos de red entre host y contenedor. | Servidor web operativo accesible en `http://localhost:8080`. |
| `docker exec` | `docker exec -it servidor-ubuntu bash` | Abrir una consola interactiva dentro de un contenedor en ejecución sin interrumpir su servicio. | Acceso al shell `root` interno de Ubuntu. |
| `docker logs` | `docker logs servidor-nginx` | Consultar los registros de salida estándar (`STDOUT`) y errores (`STDERR`) del contenedor. | Despliegue en pantalla del historial de arranque y peticiones HTTP de Nginx. |
| `docker stop` | `docker stop servidor-ubuntu servidor-nginx` | Enviar una señal `SIGTERM` para detener de forma limpia la ejecución de ambos contenedores. | Contenedores en estado detenido (`Exited`). |
| `docker rm` | `docker rm servidor-ubuntu servidor-nginx` | Eliminar de forma definitiva los contenedores detenidos y su capa de escritura temporal. | Liberación de los nombres y eliminación de las instancias en disco. |
| `docker rmi` | `docker rmi ubuntu nginx` | Borrar las imágenes base almacenadas localmente en el host. | Recuperación del espacio en disco ocupado por las capas de las imágenes. |

---

# Preguntas de reflexión

1. ¿Cuál es la diferencia entre una imagen y un contenedor?
Una imagen es una plantilla inmutable de solo lectura con el código y dependencias; un contenedor es su instancia viva y aislada en ejecución con una capa de lectura/escritura.
2. ¿Por qué Docker facilita el despliegue en la nube?
Garantiza portabilidad ("funciona en cualquier entorno"), estandariza pipelines de CI/CD y se integra de forma nativa con orquestadores para escalado automático.
3. ¿Qué ventajas ofrece Docker frente a instalar aplicaciones directamente en el sistema operativo?
Evita conflictos entre versiones de librerías, aísla procesos sin alterar el sistema operativo host y permite despliegues rápidos y desechables.
4. ¿En qué situaciones utilizaría un volumen Docker?
Se utilizan para persistencia de datos independiente del ciclo de vida del contenedor (bases de datos, subida de archivos de usuario) y para mejorar el rendimiento de I/O.
5. ¿Qué riesgos existen al ejecutar `docker system prune` en un servidor de producción?
Puede eliminar contenedores detenidos temporalmente (con datos no persistidos), redes personalizadas en reposo y, con flags como `--volumes`, provocar la pérdida irreversible de volúmenes de datos.
