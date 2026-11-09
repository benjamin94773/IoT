# Workshop 3 — Docker en EC2 y despliegue de una aplicación

**Curso:** Computación en la Nube e Internet de las Cosas

**Temas:**

- EC2
- Docker
- Docker Compose
- Nginx
- Flask
- Puertos
- Publicación de aplicaciones

---

# Objetivos

Al finalizar este workshop el estudiante será capaz de:

- Instalar Docker en una instancia EC2.
- Ejecutar contenedores dentro de EC2.
- Publicar una aplicación hacia Internet.
- Comprender la diferencia entre puerto del contenedor y puerto del host.
- Integrar EC2 con los conocimientos anteriores de Docker y Flask.
- Utilizar un Security Group para permitir tráfico HTTP.

---

# Arquitectura

```text
Internet
   |
   v
EC2
 |
 +-- Docker
      |
      +-- Nginx
      |
      +-- Flask
```

---

# Parte 1. Instalar Docker

Siga la documentación oficial de Docker para la distribución utilizada o el método recomendado por ella.

Verifique:

```bash
docker --version
sudo docker run hello-world
```

---

# Parte 2. Crear una API Flask

Cree:

```text
app/
├── app.py
├── requirements.txt
└── Dockerfile
```

`app.py`:

```python
from flask import Flask

app = Flask(__name__)

@app.get("/")
def home():
    return {"message": "Hola desde EC2"}

@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

`requirements.txt`:

```text
flask
```

`Dockerfile`:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]
```

---

# Parte 3. Construir la imagen

```bash
docker build -t ec2-flask-api .
docker images
```

---

# Parte 4. Ejecutar el contenedor

```bash
docker run -d --name api -p 5000:5000 ec2-flask-api
docker ps
curl http://localhost:5000/health
```

---

# Parte 5. Publicar la aplicación

Configure el Security Group para permitir temporalmente el puerto requerido para el laboratorio.

Pruebe desde su computador:

```text
http://13.218.87.210:5000
```

---

# Parte 6. Docker Compose

Cree:

```yaml
services:
  api:
    build: .
    container_name: api
    ports:
      - "5000:5000"
```

Ejecute:

```bash
docker compose up -d --build
docker compose ps
```

---

# Parte 7. Nginx

Como extensión, agregue Nginx y haga que actúe como reverse proxy hacia Flask:

```text
Internet
   |
  :80
   |
 Nginx
   |
  :5000
   |
 Flask
```

El usuario final debería entrar solamente por:

```text
http://<IP_PUBLICA>
```

---

# Reto

Cambie la respuesta de Flask para incluir:

- Hostname del contenedor.
- Hostname de EC2.
- Hora actual.

Explique la diferencia entre el host EC2 y el contenedor.

Diferencia entre el Host EC2 y el Contenedor:
* **Host EC2:** Es una Máquina Virtual completa provista sobre la infraestructura de AWS (hipervisor Nitro/KVM). Posee su propio kernel Linux en memoria, un sistema de inicio completo (`systemd` / PID 1), interfaces físicas/virtuales de red asignadas por la VPC (`eth0`), tabla de enrutamiento y administración directa de los recursos de hardware virtual (vCPU, memoria, volúmenes EBS).
* **Contenedor Docker:** Es un proceso aislado que se ejecuta directamente **sobre el kernel del Host EC2**. No virtualiza hardware ni ejecuta su propio kernel; utiliza mecanismos nativos del kernel Linux como:
  * **Namespaces:** Aísla el identificador de procesos (PID), red (NET), nombres de máquina (UTS, por eso su hostname es el Container ID y no el de EC2), y sistemas de archivos (MNT).
  * **Control Groups (cgroups):** Limita y controla el uso de CPU, RAM y E/S asignados.
* **En resumen:** El host es el sistema operativo completo que provee los recursos y el kernel; el contenedor es un entorno de ejecución de procesos empaquetado, liviano y desacoplado del sistema base.

---

# Entregable

- Dockerfile.
- `docker-compose.yml`.
- Configuración Nginx.
- Evidencia de la API accesible desde Internet.
- Explicación del flujo:

```text
Internet -> Security Group -> EC2 -> Docker -> Nginx -> Flask
```

1. **Internet (Cliente):** El usuario escribe `http://13.218.87.210` en su navegador web, emitiendo una petición HTTP estándar dirigida al puerto `80`.
2. **Security Group de AWS:** Actúa como firewall virtual perimetral y con estado (stateful). Inspecciona el paquete antes de que toque la interfaz de red de la máquina. Al encontrar la regla permitiendo el tráfico TCP al puerto `80` desde `0.0.0.0/0`, autoriza el paso del paquete hacia la instancia.
3. **EC2 (Host):** El paquete llega a la tarjeta de red de la máquina virtual (`eth0`). La pila de red de Linux y las reglas de `iptables` / `nftables` administradas por Docker detectan que hay un socket en modo escucha en el puerto `0.0.0.0:80`.
4. **Docker Engine (Mapeo de puertos y red bridge):** Docker recibe el paquete en el host y, mediante NAT (Network Address Translation) en su red virtual (`bridge`), reenvía el tráfico del puerto `80` del host al puerto `80` del contenedor `nginx_proxy`.
5. **Nginx (Reverse Proxy):** Nginx recibe la petición en el puerto 80, evalúa el bloque `location /`, y actúa como proxy inverso. Reenvía internamente la petición a través de la red DNS interna de Docker hacia el nombre de servicio `http://api:5000`.
6. **Flask (API Backend):** La aplicación Python en el contenedor `api` recibe la solicitud en el puerto `5000`, procesa la función `home()`, obtiene el hostname del contenedor y la hora actual, y devuelve la respuesta en formato JSON.
7. **Retorno:** Nginx recibe la respuesta de Flask y la transmite de vuelta al cliente en Internet a través del túnel TCP establecido.
