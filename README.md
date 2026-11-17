# Laboratorios de Cómputo en la Nube e Internet de las Cosas (IoT)

**Estudiante:** Benjamín Ortiz  
**Repositorio de Entregables del Curso**

---

## Estructura del Repositorio

El repositorio se encuentra organizado por módulos de aprendizaje y actividades:

### 📁 [actividades_clase](./actividades_clase)
- **01_diseno_ticketmaster:** Caso de estudio de la semana 2 sobre arquitectura cliente-servidor para venta masiva de boletos, alta concurrencia, balanceador de carga, locks en Redis con TTL de 10 min, colas RabbitMQ y persistencia ACID en PostgreSQL.
- **02_autenticacion_apikeys:** Diseño del sistema de seguridad perimetral para APIs, diagramas de contexto y alto nivel, API Gateway, validación en caché Redis, hashing SHA-256 y Rate Limiting.
- **03_bodegas_distribuidas_requisitos:** Especificación de requisitos (RF/RNF) y sesión de refinamiento del Proyecto Integrador (*Warehouse Cloud Platform*), patrón Saga para transferencias, CQRS, workers y telemetría IoT.

### 📁 [01_bash](./01_bash)
- **Design:** Arquitectura de software SmartCampus (Capas, REST vs GraphQL, Escalabilidad, Autenticación SSO, Microservicios IoT, Polyglot Persistence con PostgreSQL, NoSQL y Redis).
- **Topic:** Prácticas fundamentales de terminal, scripts de automatización en Bash, tuberías, filtros y gestión de procesos.

### 📁 [02_bash](./02_bash)
- Análisis de logs de servidores web (`access.log`), scripts de monitoreo del sistema, diferencias entre directivas `CMD` y `ENTRYPOINT` en Docker y dockerización inicial con servicios Ubuntu y Nginx.

### 📁 [03_docker](./03_docker)
- Despliegue de arquitecturas multicontenedor con Docker y Docker Compose:
  - Workshop 1: Flask + Nginx con balanceo de carga.
  - Workshop 2: Reverse Proxy para microservicios (`orders`, `products`, `users`).
  - Workshop 3: Backend Flask + Base de datos PostgreSQL + Nginx.
  - Workshop 4: Configuración avanzada de PostgreSQL con scripts de inicialización.
  - Workshop 5: Persistencia NoSQL con MongoDB y Docker Compose.

### 📁 [04_aws_ec2](./04_aws_ec2)
- Infraestructura como Servicio (IaaS) en Amazon Web Services (AWS EC2):
  - Workshop 1: Lanzamiento de instancia, conexión remota por SSH y análisis de hardware.
  - Workshop 2: Administración remota de Linux, inspección de procesos y script `system_info.sh`.
  - Workshop 3: Despliegue de Docker, Docker Compose y Nginx en EC2 con resolución del Reto.
  - Workshop 4: Auditoría de seguridad de red con `ss -tulpn` y principio de mínimo privilegio en Security Groups.
  - Workshop 5: Aprovisionamiento automatizado de servidores con **AWS User Data** (`cloud-init`).
  - Workshop 6: Diseño de arquitecturas cloud escalables, Multi-AZ, Load Balancer, aplicaciones Stateless y Journey to Cloud (J2C).

### 📁 [05_cloud](./05_cloud)
- Proyecto integral de computación en la nube: despliegue multicapa desacoplado con Amazon ECR, Amazon S3, EC2, Nginx, Flask y PostgreSQL con evidencias completas de ejecución.
