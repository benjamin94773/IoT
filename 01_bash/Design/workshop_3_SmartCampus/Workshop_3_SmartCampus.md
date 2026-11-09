# Workshop 3 - SmartCampus IoT y Cloud: Arquitectura Distribuida y Event-Driven

**Curso:** Computación en la Nube e Internet de las Cosas  
**Proyecto:** SmartCampus — Fase 3: Integración IoT Masiva y Arquitectura Cloud

---

## Contexto y Nuevo Escenario

El campus universitario de **SmartCampus** da el salto hacia una universidad inteligente (*Smart Campus*). Se despliegan miles de dispositivos y sensores físicos distribuidos por facultades, laboratorios, aulas y parqueaderos. 

El sistema ahora recibe una carga continua masiva de **más de 100.000 eventos por minuto** (~1.666 eventos por segundo) generados por hardware en tiempo real.

## Nuevos Dispositivos en el Campus
- **Lectores RFID en puertas y torniquetes:** Control de acceso de estudiantes y docentes a edificios y laboratorios.
- **Sensores de Temperatura y Humedad:** Monitoreo de confort y climatización en aulas de cómputo y auditorios.
- **Sensores de Presencia (PIR / Ultrasonido):** Detección de ocupación en tiempo real de salones de clase.
- **Medidores Inteligentes de Consumo Eléctrico:** Telemetría de gasto energético por facultad y bloque.

---

# Desarrollo de Actividades

## Actividad 1. Análisis de Componentes que Deben Cambiar

### 1.1 ¿Por qué la arquitectura anterior colapsaría con 100.000 eventos/minuto?
1. **Sobrecarga de HTTP en Dispositivos Ligeros:** El protocolo HTTP/REST tiene un encabezado pesado (headers de 500 bytes a 2 KB) y establece una conexión TCP con negociación TLS en cada envío. Para un microcontrolador (ESP32 o Arduino) enviando un número cada 2 segundos, HTTP drena la memoria y satura la red inalámbrica del campus.
2. **Saturación y Bloqueos en PostgreSQL:** Recibir 1.666 peticiones de escritura síncronas por segundo directamente en PostgreSQL provocaría un cuello de botella en los discos (*I/O bottlenecks*), bloqueos de tablas y agotamiento del pool de conexiones (*too many connections*), dejando fuera de servicio las consultas de notas y matrículas.
3. **Acoplamiento Síncrono:** Si el servidor académico se reinicia o entra en mantenimiento por 1 minuto, se perderían 100.000 lecturas de sensores y los torniquetes RFID dejarían de abrir.

### 1.2 Cambios Arquitectónicos Necesarios
* **Sustituir HTTP por MQTT en el borde:** Protocolo ligero de suscripción/publicación optimizado para telemetría.
* **Incorporar un Broker de Mensajería (RabbitMQ):** Para actuar como amortiguador (*buffer de ingesta*) que absorbe los picos de tráfico y desacopla la recepción del procesamiento.
* **Separar el Almacenamiento (Persistencia Políglota):** Mantener los datos académicos en PostgreSQL y mover la telemetría masiva a una base de datos **NoSQL / Time-Series**.
* **Migrar a Microservicios:** Aislar el procesamiento IoT del núcleo académico para que puedan escalar de forma independiente.

---

## Actividad 2. Evaluación de Nuevos Componentes Tecnológicos

| Componente | Rol en la Solución | ¿Por qué es Indispensable? |
| :--- | :--- | :--- |
| **MQTT (Message Queuing Telemetry Transport)** | Protocolo de red para sensores | Diseñado para hardware embebido. Su cabecera pesa apenas **2 bytes**, tiene soporte de Calidad de Servicio (QoS 0, 1, 2) y mantiene conexiones persistentes eficientes sin sobrecargar la red WiFi/LoRaWAN. |
| **Broker de Mensajes (RabbitMQ)** | Colas y enrutamiento de eventos | Resuelve el problema de contrapresión (*backpressure*). Si ingresan 5.000 eventos por segundo en hora pico, RabbitMQ los encola en memoria/disco; los microservicios consumidores los procesan a su propio ritmo sin perder datos. |
| **gRPC (HTTP/2 + Protocol Buffers)** | Comunicación síncrona inter-servicios | Cuando el servicio de acceso RFID necesita validar en menos de 10 ms si el carné escaneado pertenece a un estudiante activo, gRPC ofrece una latencia 7 a 10 veces menor que REST gracias a su serialización binaria compacta. |
| **Base de Datos NoSQL (Time-Series / Documental)** | Persistencia masiva de telemetría | Motores como **MongoDB** o **TimescaleDB / InfluxDB** están optimizados para miles de escrituras concurrentes por segundo sin el costo de mantener integridad referencial ni llaves foráneas en cada lectura de temperatura. |
| **Microservicios** | Desacoplamiento de dominios | Si el servicio IoT procesa millones de datos, sus contenedores se escalan en Docker sin gastar recursos en replicar el módulo de matrículas. Un fallo en el servicio de sensores no tumba el portal de notas. |

---

## Actividad 3. Selección de Tecnología Adecuada por Escenario

| Caso de Uso | Tecnología Seleccionada | Justificación Técnica |
| :--- | :--- | :--- |
| **Comunicación Sensores $\rightarrow$ Servidor** | **MQTT** | Protocolo *Pub/Sub* con bajísimo consumo energético, paquete binario mínimo y reconexión automática tolerante a pérdidas temporales de señal inalámbrica. |
| **Comunicación Interna entre Microservicios** | **gRPC** (Síncrona) / **RabbitMQ** (Asíncrona) | **gRPC** para consultas inmediatas que requieren respuesta en tiempo real (ej. Auth check con contrato estricto `proto3`). **RabbitMQ** para eventos de negocio desacoplados donde no se espera respuesta inmediata (ej. `Event: ClassRoomOccupied`). |
| **Dashboard en Tiempo Real** | **WebSocket** | Permite transmitir métricas de temperatura y mapas de calor de ocupación de aulas directamente al navegador del personal administrativo sin sobrecargar el servidor con peticiones repetitivas. |
| **Consultas Académicas Tradicionales** | **REST** (con caché Redis) | Operaciones CRUD sobre entidades bien estructuradas (estudiantes, docentes, notas). Aprovecha la madurez del ecosistema web y la facilidad de consumo desde navegadores. |

---

## Actividad 4. Persistencia Políglota: Clasificación de Datos (SQL vs NoSQL)

En una arquitectura moderna no existe una única base de datos para todo. Se utiliza el principio de **Persistencia Políglota** (*Polyglot Persistence*):

| Tipo de Base de Datos | Motor Recomendado | Datos Almacenados | Justificación Técnica |
| :--- | :--- | :--- | :--- |
| **Relacional (SQL)** | **PostgreSQL** | • Estudiantes, docentes, usuarios<br>• Cursos, programas académicos<br>• Matrículas y cupos oficiales<br>• Calificaciones y actas de notas | Requiere soporte estricto de **transacciones ACID**, unicidad, integridad referencial y cero tolerancia a inconsistencias o pérdidas de datos. |
| **NoSQL (Time-Series / Documental)** | **MongoDB / TimescaleDB** | • Lecturas de temperatura y humedad<br>• Mediciones de consumo eléctrico (kWh)<br>• Registro histórico de accesos RFID<br>• Estados de presencia por salón | Datos con estructura variable y altísimo volumen de escritura temporal (*append-only*). No requieren joins relacionales; las consultas son por rango de tiempo y agregación estadística (promedios por hora/día). |
| **Caché en Memoria** | **Redis** | • Catálogo de materias en matrícula<br>• Sesiones activas y tokens revocados<br>• Último estado conocido de cada aula (libre/ocupada) | Búsqueda por clave-valor en memoria RAM con latencia sub-milisegundo. Alivia la carga de lectura de los dos motores anteriores. |

---

## Actividad 5. Diseño de la Arquitectura Final de SmartCampus

```text
====================================================================================================
                                      BORDE DE USUARIOS Y CLIENTES
====================================================================================================
           [ Navegadores Web ]                        [ Aplicaciones Móviles (Android / iOS) ]
                   │                                                     │
                   │ HTTPS / WSS                                         │ HTTPS
                   ▼                                                     ▼
====================================================================================================
                                    CAPA DE ACCESO Y BALANCEO (CLOUD)
====================================================================================================
                                 +--------------------------------+
                                 |  LOAD BALANCER (Nginx / ALB)   |
                                 +---------------+----------------+
                                                 │
                                                 ▼
                                 +--------------------------------+
                                 |    API GATEWAY PERIMETRAL      |
                                 |  (Auth, Rate Limit, Routing)   |
                                 +---------------+----------------+
                                                 │
           ┌─────────────────────────────────────┼─────────────────────────────────────┐
           │                                     │                                     │
           ▼                                     ▼                                     ▼
+---------------------+               +---------------------+               +---------------------+
| Microservicio Auth  |               | Microservicio       |               | Microservicio       |
| (SSO / Tokens JWT)  |               | Académico (Core)    |               | Notificaciones      |
+----------+----------+               +----------+----------+               +----------+----------+
           │                                     │                                     ▲
           │                                     │                                     │ WebSockets
           │                                     │ gRPC / REST                         │ / Push
           │                                     │                                     │
           │                                     ▼                                     │
           │                          +---------------------+                          │
           │                          | Microservicio de    |                          │
           │                          | Gestión de Campus   |                          │
           │                          +----------+----------+                          │
           │                                     │                                     │
           │                                     │ Consume eventos procesados          │
           │                                     │                                     │
=================================================│=====================================│============
                                   CAPA ASÍNCRONA Y BROKER DE EVENTOS                  │
=================================================│=====================================│============
                                                 │                                     │
                                    +------------▼-------------------------------------+
                                    |        BROKER DE MENSAJERÍA (RabbitMQ)           |
                                    |   (Colas: events.rfid, events.telemetry, alerts) |
                                    +--------------------+-----------------------------+
                                                         ▲
                                                         │ Encola eventos en tiempo real
                                                         │
                                    +--------------------+-----------------------------+
                                    |     Servicio de Ingesta IoT (Worker Ingest)      |
                                    +--------------------+-----------------------------+
                                                         ▲
                                                         │ Publicaciones MQTT
=========================================================│==========================================
                                       BORDE IoT (DISPOSITIVOS FÍSICOS)
=========================================================│==========================================
                                    +--------------------+-----------------------------+
                                    |       BROKER MQTT (Mosquitto / EMQX)             |
                                    +--------------------+-----------------------------+
                                                         ▲
                             ┌───────────────────────────┴───────────────────────────┐
                             │                           │                           │
                    +--------┴--------+         +--------┴--------+         +--------┴--------+
                    | Torniquetes     |         | Sensores Temp   |         | Medidores de    |
                    | y Lectores RFID |         | Humedad / PIR   |         | Consumo Eléctrico
                    +-----------------+         +-----------------+         +-----------------+
====================================================================================================
                                      CAPA DE PERSISTENCIA POLÍGLOTA
====================================================================================================
    +-----------------------------+   +-----------------------------+   +--------------------------+
    |   POSTGRESQL (Transaccional)|   |   NOSQL / TIME-SERIES       |   |      REDIS CACHE         |
    |   (Usuarios, Cursos, Notas) |   |   (Telemetría IoT, Logs)    |   |   (Sesiones, Catálogos,  |
    |                             |   |   (MongoDB / TimescaleDB)   |   |    Estado de Salones)    |
    +-----------------------------+   +-----------------------------+   +--------------------------+
```

---

## Actividad 6. Justificación Técnica de los 8 Componentes del Sistema

1. **MQTT:** Protocolo binario de comunicación máquina-a-máquina (M2M). Minimiza el ancho de banda y la batería de los sensores del campus con paquetes de transporte de tan solo 2 bytes.
2. **gRPC:** Protocolo de llamadas remotas síncronas basado en HTTP/2 y serialización binaria Protocol Buffers. Garantiza comunicación ultrarrápida y contratos estrictos entre los microservicios internos.
3. **RabbitMQ:** Broker de mensajería empresarial que amortigua los 100.000 eventos por minuto. Previene la pérdida de datos ante picos de concurrencia y desacopla la recepción física del análisis de datos.
4. **WebSockets:** Canal bidireccional continuo que permite a los operadores de seguridad y administración ver tableros de control con datos en vivo (aulas ocupadas, alarmas) con latencia cercana a cero.
5. **API Gateway:** Punto único de entrada para tráfico externo. Realiza la terminación SSL, controla límites de peticiones (*rate limiting*), valida credenciales JWT y enruta el tráfico a los servicios correspondientes.
6. **Caché en Memoria (Redis):** Almacenamiento clave-valor de lectura ultrarrápida. Reduce drásticamente la carga sobre PostgreSQL y guarda el último estado de los salones para consultas instantáneas.
7. **Docker (Contenedores):** Permite empaquetar cada componente (APIs, Nginx, Workers, Bases de datos) con sus dependencias exactas, garantizando portabilidad, reproducibilidad y despliegues estandarizados.
8. **Balanceador de Carga (Load Balancer):** Distribuye las peticiones entrantes entre múltiples réplicas de los contenedores de aplicación, eliminando puntos únicos de falla (*Single Point of Failure*) y permitiendo alta disponibilidad.

---

## Entregables Consolidados

### 1. Resumen de Decisiones Arquitectónicas (ADRs)
* **ADR-01: Separación de Protocolos en el Borde:** Se utiliza MQTT para dispositivos de bajo consumo y HTTPS/WSS exclusivamente para usuarios humanos.
* **ADR-02: Procesamiento Asíncrono de Telemetría:** Ningún sensor escribe directamente en la base de datos; todos los datos pasan por RabbitMQ.
* **ADR-03: Persistencia Políglota:** Separación física estricta entre el almacenamiento transaccional (PostgreSQL) y el histórico masivo (NoSQL).

### 2. Estrategia de Escalabilidad
* **Escalabilidad Horizontal de la Ingesta:** El servicio consumidor de RabbitMQ se despliega en contenedores Docker independientes. Si el tráfico de sensores sube de 100.000 a 500.000 eventos/min, se lanzan más instancias del consumidor (*worker*) sin tocar el servidor de notas ni la base de datos principal.
* **Idempotencia y Manejo de Duplicados:** Cada lectura de sensor incluye un identificador único (`event_id` o combinación de `sensor_id + timestamp`) para evitar duplicaciones en caso de retransmisión por fallo de red.
* **Resiliencia ante Fallos Parciales:** Si la base de datos NoSQL se reinicia, RabbitMQ retiene los mensajes en disco de forma segura hasta que el servicio de almacenamiento se restablezca. El campus físico sigue funcionando sin interrupciones.
