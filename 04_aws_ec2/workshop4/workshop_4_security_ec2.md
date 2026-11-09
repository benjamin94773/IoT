# Workshop 4 — Seguridad de red en EC2

**Curso:** Computación en la Nube e Internet de las Cosas

**Temas:**

- Security Groups
- Puertos
- SSH
- HTTP
- HTTPS
- Principio de mínimo privilegio
- Network exposure

---

# Objetivos

Al finalizar este workshop el estudiante será capaz de:

- Comprender cómo un Security Group controla el tráfico.
- Diferenciar puertos públicos y privados.
- Aplicar el principio de mínimo privilegio.
- Identificar configuraciones inseguras.
- Reducir la superficie de exposición de una EC2.

---

# Situación inicial

Suponga que la instancia tiene:

```text
22   SSH
80   HTTP
5000 Flask
5432 PostgreSQL
```

La pregunta es:

> **Pregunta:** ¿Deben estar los cuatro puertos (22 SSH, 80 HTTP, 5000 Flask, 5432 PostgreSQL) públicos?  
> **Respuesta:** **No.** Únicamente el puerto **80** (HTTP) debe estar abierto a todo Internet (`0.0.0.0/0`). El puerto **22** (SSH) debe estar restringido exclusivamente a la dirección IP pública del administrador (`/32`), mientras que los puertos **5000** (Flask) y **5432** (PostgreSQL) son servicios de backend y base de datos que deben operar en redes locales/privadas y jamás exponerse directamente a Internet.

---

# Parte 1. Auditar la configuración

Liste los puertos que escucha el servidor:

```bash
sudo ss -tulpn
```

Identifique qué procesos están asociados a cada puerto.

### Evidencia de ejecución:

```text
ubuntu@ip-172-31-26-92:~/app$ sudo ss -tulpn
Netid State  Recv-Q Send-Q     Local Address:Port  Peer Address:Port Process
udp   UNCONN 0      0              127.0.0.1:323        0.0.0.0:*     users:(("chronyd",pid=746,fd=4))
udp   UNCONN 0      0             127.0.0.54:53         0.0.0.0:*     users:(("systemd-resolve",pid=199,fd=18))
udp   UNCONN 0      0          127.0.0.53%lo:53         0.0.0.0:*     users:(("systemd-resolve",pid=199,fd=16))
udp   UNCONN 0      0      172.31.26.92%ens5:68         0.0.0.0:*     users:(("systemd-network",pid=553,fd=32))
udp   UNCONN 0      0                  [::1]:323           [::]:*     users:(("chronyd",pid=746,fd=5))
tcp   LISTEN 0      4096          127.0.0.54:53         0.0.0.0:*     users:(("systemd-resolve",pid=199,fd=19))
tcp   LISTEN 0      4096             0.0.0.0:80         0.0.0.0:*     users:(("docker-proxy",pid=4316,fd=7))
tcp   LISTEN 0      4096           127.0.0.1:44407      0.0.0.0:*     users:(("containerd",pid=2082,fd=14))
tcp   LISTEN 0      4096             0.0.0.0:22         0.0.0.0:*     users:(("sshd",pid=698,fd=3),("systemd",pid=1,fd=233))
tcp   LISTEN 0      4096       127.0.0.53%lo:53         0.0.0.0:*     users:(("systemd-resolve",pid=199,fd=17))
tcp   LISTEN 0      4096                [::]:80            [::]:*     users:(("docker-proxy",pid=4321,fd=7))
tcp   LISTEN 0      4096                [::]:22            [::]:*     users:(("sshd",pid=698,fd=4),("systemd",pid=1,fd=234))
```

### Procesos asociados identificados:
1. **Puerto 22 / TCP (`sshd` y `systemd`):** Servicio OpenSSH escuchando peticiones de acceso remoto por SSH (IPv4 e IPv6).
2. **Puerto 80 / TCP (`docker-proxy`):** Demonio proxy de Docker enlazando el puerto 80 del host con el puerto 80 del contenedor `nginx_proxy`.
3. **Puerto 53 / TCP y UDP (`systemd-resolve`):** Servidor DNS interno local en bucle invertido (`127.0.0.53` y `127.0.0.54`).
4. **Puerto 68 / UDP (`systemd-network`):** Cliente DHCP obteniendo y renovando la configuración IP privada de la interfaz `ens5`.
5. **Puerto 323 / UDP (`chronyd`):** Cliente y servidor NTP local para la sincronización horaria de precisión con los relojes de AWS.
6. **Puerto 44407 / TCP (`containerd`):** Socket interno de comunicación para el runtime de contenedores en `127.0.0.1`.
7. **Puerto 5000 / TCP (Flask):** No aparece expuesto a nivel de host en `0.0.0.0` porque está encapsulado dentro de la red privada virtual de Docker (`bridge`), lo que cumple de inmediato el aislamiento de seguridad frente a Internet.

---

# Parte 2. Analizar el Security Group

| Puerto | Servicio | ¿Necesita ser público (`0.0.0.0/0`)? | Justificación técnica |
| :--- | :--- | :---: | :--- |
| **22** | SSH | **NO** | Es el puerto de administración de la máquina. Debe restringirse exclusivamente a la IP pública del administrador (`IP/32`) o a una VPN corporativa/Bastion Host. Dejarlo abierto al mundo atrae escaneos y ataques de fuerza bruta continuos. |
| **80** | HTTP | **SÍ** | Es el punto de entrada para los usuarios y navegadores en Internet que consumen la aplicación web a través de Nginx. |
| **5000** | Flask | **NO** | Es la lógica de backend interno. Nginx se encarga de recibir el tráfico en el puerto 80 y transferirlo internamente al puerto 5000 de Flask dentro de la red privada de Docker. Abrirlo a Internet saltaría las protecciones de Nginx. |
| **5432** | PostgreSQL | **NO** | Es el motor de base de datos donde residen los datos sensibles. Solo debe permitir conexiones locales (`localhost`) o desde la subred privada de la aplicación. Exponerlo públicamente es una falla grave de seguridad. |

---

# Parte 3. Principio de mínimo privilegio

Proponga una configuración donde:

```text
Internet
   |
   +--> 80/443 --> aplicación
   |
Administración
   |
   +--> 22 --> solo IP autorizada
```

Y la base de datos no sea accesible desde Internet:

```text
Internet -X-> 5432
```

El principio de mínimo privilegio establece que cada componente debe tener acceso únicamente a los recursos e información estrictamente necesarios para cumplir su función.

### Modelo de arquitectura segura propuesto:

```text
Usuarios en Internet
        |
        +-----> [ TCP :80 / :443 ] -----> Nginx (Reverse Proxy)
                                                |
                                      (Red Privada Interna)
                                                |
                                                +-----> [ TCP :5000 ] -----> Flask API
                                                                                |
                                                                      (Subred Privada / Local)
                                                                                |
                                                                                +-----> [ TCP :5432 ] -----> PostgreSQL
Administrador
        |
        +-----> [ TCP :22 ] (Solo IP Administrador: 200.x.x.x/32) -----> SSH Host EC2

Internet -----X (BLOQUEADO en SG) -----> Puertos 5000 y 5432
```

---

# Parte 4. Análisis de Seguridad

### 1. ¿Qué riesgo existe al abrir SSH al mundo (`0.0.0.0/0`)?
Exponer el puerto 22 a todo Internet hace que la instancia sea inmediatamente detectada por bots automatizados y escáneres globales. Los riesgos principales son:
* Ataques constantes de fuerza bruta y diccionario contra cuentas del sistema.
* Explotación de vulnerabilidades de día cero (*zero-day*) en OpenSSH.
* Consumo innecesario de recursos de CPU y saturación de registros (`/var/log/auth.log`).

### 2. ¿Qué diferencia existe entre Security Group y un firewall dentro del sistema operativo (UFW/iptables)?
* **Security Group (AWS):** Opera en la capa de hipervisor (Nitro/KVM) de AWS, **antes de que los paquetes alcancen la instancia**. Es un firewall *stateful* que filtra el tráfico sin consumir recursos (CPU/RAM) de la EC2 y no puede ser manipulado ni desactivado desde el sistema operativo en caso de un compromiso.
* **Firewall del Sistema Operativo (`iptables` / `ufw`):** Opera dentro del kernel de la máquina invitada. La tarjeta de red ya tuvo que recibir y procesar el paquete para que el kernel decida descartarlo, consumiendo recursos de cómputo. Si un atacante obtiene permisos `root`, puede desactivar el firewall local.

### 3. ¿Por qué no debemos exponer PostgreSQL públicamente si no es necesario?
Las bases de datos contienen la información más crítica del sistema. Exponer el puerto 5432 públicamente incrementa el riesgo de:
* Ataques de inyección y autenticación débil.
* Filtración o exfiltración masiva de datos sensibles.
* Ataques de ransomware que cifran o eliminan bases de datos expuestas.
* Denegación de servicio por agotamiento de conexiones disponibles en el pool de Postgres.

### 4. ¿Por qué Nginx puede ser el único punto público de entrada?
Nginx actúa como **Proxy Inverso y DMZ perimetral**:
* **Ocultación de topología:** El cliente nunca sabe qué lenguaje, puerto o servidor interno procesa la lógica de negocio (Flask, Node, Go, etc.).
* **Gestión centralizada de TLS/SSL:** Permite cifrar el tráfico con certificados HTTPS en un único punto.
* **Protección y rendimiento:** Permite aplicar *Rate Limiting* (control de tasa de peticiones), compresión gzip, caché de respuestas y filtrado de cabeceras maliciosas antes de que impacten al backend.


---

# Reto

Documente una propuesta de Security Group para una API Flask detrás de Nginx.

Debe incluir:

- Regla.
- Puerto.
- Protocolo.
- Origen.
- Justificación.

---

# Reto — Propuesta de Security Group

Para una arquitectura de API Flask detrás de Nginx y acceso administrativo seguro:

### Reglas de Entrada (Inbound Rules):

| Regla | Tipo | Protocolo | Puerto | Origen (Source) | Justificación |
| :--- | :--- | :---: | :---: | :--- | :--- |
| **1** | **HTTP** | TCP | `80` | `0.0.0.0/0` | Permite el tráfico web no cifrado de los clientes hacia Nginx (redirección a HTTPS). |
| **2** | **HTTPS** | TCP | `443` | `0.0.0.0/0` | Permite el tráfico web seguro y cifrado de los usuarios hacia Nginx. |
| **3** | **SSH** | TCP | `22` | `201.244.x.x/32` (My IP) | Acceso de administración remota restringido estrictamente a la IP pública del administrador. |

### Reglas de Salida (Outbound Rules):

| Tipo | Protocolo | Puerto | Destino | Justificación |
| :--- | :---: | :---: | :--- | :--- |
| **All traffic** | Todos | Todos | `0.0.0.0/0` | Permite a la instancia descargar actualizaciones del sistema (`apt update`), imágenes de Docker y consultar repositorios externos. |

---


# Entregable

- Tabla de puertos.
- Capturas de Security Group.
- Propuesta de configuración segura.
- Respuestas de análisis.
