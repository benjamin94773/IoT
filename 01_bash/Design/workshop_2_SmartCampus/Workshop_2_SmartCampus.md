# Workshop 2 - La universidad crece: Arquitectura Escalable y Multi-Canal

**Curso:** Computación en la Nube e Internet de las Cosas  
**Proyecto:** SmartCampus — Fase 2: Expansión de Servicios

---

## Contexto y Nuevo Escenario

La Universidad **SmartCampus** ha crecido notablemente. Ahora se incorporan estudiantes que acceden mediante **aplicación móvil** y navegadores web. Además, se requiere un sistema de **autenticación institucional unificada (SSO)** y un canal de **notificaciones en tiempo real** (alertas de notas publicadas, avisos de cambios de aula, cancelaciones).

## Nuevos Requerimientos

### Requerimientos Funcionales
- Soporte para clientes heterogéneos: **Plataforma Web y Aplicación Móvil (Android/iOS)**.
- **Inicio de Sesión Único (SSO):** Un solo punto de autenticación con tokens seguros para todos los servicios.
- **Notificaciones en Tiempo Real:** Envío inmediato de alertas sin necesidad de recargar la página o hacer consultas continuas (*polling*).

### Requerimientos No Funcionales
- **Escalabilidad:** Soportar un salto de 500 a **5.000 usuarios simultáneos** (especialmente en semanas de matrícula y entrega de notas).
- **Eficiencia en Red Móvil:** Minimizar el consumo de ancho de banda y la cantidad de peticiones desde dispositivos móviles.
- **Latencia de Respuesta:** Respuestas de lectura frecuentes en menos de 50 ms.

---

# Desarrollo de Actividades

## Actividad 1. Actualización de la Arquitectura

Para soportar 5.000 usuarios concurrentes y desacoplar las responsabilidades, evolucionamos del monolito inicial hacia una **Arquitectura Orientada a Servicios con API Gateway y Capa de Caché**:

### 1.1 Diagrama de Arquitectura de Alto Nivel

```text
                  +-------------------+     +--------------------+
                  |    Cliente Web    |     |  App Móvil (Móvil) |
                  |   (Navegadores)   |     |   (Android / iOS)  |
                  +---------+---------+     +---------+----------+
                            |                         |
                            | HTTPS / WSS             | HTTPS (JSON)
                            +------------+------------+
                                         |
                                         v
+----------------------------------------------------------------------------------+
|                              PERÍMETRO / ACCESO                                  |
|                                                                                  |
|                        [ API GATEWAY (Kong / Nginx) ]                            |
|             (SSL Termination, Rate Limiting, Enrutamiento, Auth Check)           |
+-------------+--------------------------+-------------------------+---------------+
              |                          |                         |
              | (Ruta /auth)             | (Rutas /academic)       | (Ruta /ws)
              v                          v                         v
+------------------------+  +--------------------------+  +------------------------+
|  Servicio de Auth      |  |   Servicio Académico     |  |   Servicio de          |
|  (SSO - OAuth2 / OIDC) |  |   (Core Académico)       |  |   Notificaciones       |
|  Emisión de JWT        |  |   Matrículas y Notas     |  |   WebSockets / Push    |
+-----------+------------+  +------------+-------------+  +-----------+------------+
            |                            |                            |
            |                            | Consultas frecuentes       |
            |                            v                            |
            |               +--------------------------+              |
            |               |    CACHÉ EN MEMORIA      |              |
            |               |     [ Redis Cache ]      |              |
            |               |  (Catálogos, Horarios)   |              |
            |               +-------------+------------+              |
            |                             | Miss                      |
            v                             v                           v
+------------------------------------------------------+  +------------------------+
|             BASE DE DATOS RELACIONAL                 |  | Servicios Push         |
|              [ PostgreSQL Cluster ]                  |  | Externos (FCM / APNs)  |
|            (Fuente de Verdad - ACID)                 |  | (Celulares)            |
+------------------------------------------------------+  +------------------------+
```

### 1.2 Justificación de los Nuevos Componentes
1. **API Gateway:**
   * **¿Por qué se incorpora?** Con 5.000 usuarios y dos clientes distintos (Web y Móvil), no es viable que los clientes conozcan las IPs internas de múltiples servicios. El Gateway actúa como fachada única (*Single Entry Point*).
   * **Funciones:** Centraliza el cifrado HTTPS, balancea carga, valida la firma del token JWT antes de reenviar la petición a los servicios internos y aplica *Rate Limiting* (protección contra saturación o ataques de fuerza bruta).
2. **Servicio de Autenticación (Auth SSO / Identity Provider):**
   * **¿Por qué se incorpora?** Separa la lógica de seguridad y credenciales del código académico. Emite tokens firmados digitalmente (**JWT - JSON Web Tokens**). Los demás servicios confían en el token sin tener que re-autenticar al usuario en cada consulta.
3. **Servicio de Notificaciones (WebSockets + Push):**
   * **¿Por qué se incorpora?** Para no bloquear la API académica manteniendo conexiones abiertas. Mantiene las conexiones persistentes WSS para la Web y delega las notificaciones de celular a Firebase Cloud Messaging (FCM).
4. **Caché en Memoria (Redis):**
   * **¿Por qué se incorpora?** Para resistir el tráfico de 5.000 usuarios simultáneos. Si 4.000 estudiantes consultan el catálogo de materias al mismo tiempo, PostgreSQL colapsaría por exceso de conexiones. Redis atiende esas lecturas desde memoria RAM en 2-5 ms.

---

## Actividad 2. Selección del Tipo de API por Funcionalidad

| Funcionalidad | Tipo de API Seleccionado | Protocolo | Justificación Técnica |
| :--- | :--- | :--- | :--- |
| **Login (Autenticación)** | **REST** | HTTPS (`POST /api/v1/auth/login`) | El proceso de autenticación es un intercambio puntual y seguro: credenciales $\rightarrow$ validación $\rightarrow$ entrega de token JWT con tiempo de expiración. REST es el estándar de facto para flujos OAuth2. |
| **Consulta de Materias** | **GraphQL** (o REST con Redis) | HTTPS (`POST /graphql` o `GET /courses`) | En la aplicación móvil, los estudiantes en redes 4G lentas solo necesitan el nombre de la materia y el código para una vista rápida, mientras que en la web se requiere descripción, créditos y prerequisitos. GraphQL permite que la app móvil solicite únicamente los campos que va a pintar, reduciendo el tamaño del payload y el consumo de datos. |
| **Perfil del Usuario** | **REST** | HTTPS (`GET /api/v1/users/me`) | Consulta puntual sobre un recurso unívoco. La respuesta es pequeña, estandarizada y se puede cachear localmente con encabezados HTTP estándar. |
| **Notificaciones en Tiempo Real** | **WebSocket** | WSS (`wss://smartcampus.edu/ws/notifications`) | Requiere comunicación bidireccional continua y entrega inmediata promovida por el servidor (*push*). HTTP tradicional obligaría al cliente a preguntar cada 5 segundos (*polling*), lo cual generaría 5.000 requests constantes e innecesarios a la infraestructura. |
| **Actualización de Notas** | **REST** | HTTPS (`PUT /api/v1/grades/{id}`) | Operación transaccional ejecutada por los docentes. Requiere semántica clara de verbos HTTP (`PUT`/`PATCH`), código de estado explícito (`200 OK` / `400 Bad Request`) e idempotencia garantizada. |

---

## Actividad 3. Criterios de Selección: REST vs GraphQL vs WebSocket

### 3.1 Cuadro Comparativo

| Característica | REST | GraphQL | WebSocket |
| :--- | :--- | :--- | :--- |
| **Modelo de Comunicación** | Solicitud / Respuesta (Unidireccional por request) | Solicitud / Respuesta (Unidireccional por query) | Dúplex completo (Bidireccional persistente) |
| **Protocolo de Transporte** | HTTP / HTTPS (TCP sin estado) | HTTP / HTTPS (usualmente sobre POST) | Protocolo WebSocket (`ws://` / `wss://`) sobre TCP |
| **Control del Payload** | Fijo en el servidor (diseñado en los DTOs) | Flexible (el cliente pide los campos exactos) | Mensajes de texto o binarios libres (JSON) |
| **Caché en Red / Proxy** | Excelente y nativa (Nginx, CDNs, cabeceras HTTP) | Compleja (al ser POST se requiere caché a nivel de aplicación) | No aplica (la conexión es un flujo de eventos continuo) |
| **Consumo de Recursos en Servidor** | Bajo (conexión efímera que se abre y se cierra) | Medio-Alto (parsing y ejecución del árbol GraphQL) | Alto en memoria (mantiene un socket TCP abierto por cliente) |
| **Ideal para...** | Operaciones CRUD, microservicios estándar, login | Apps móviles, interfaces complejas con muchas relaciones | Chats, tableros en vivo, alertas, telemetría IoT |

### 3.2 Regla de Decisión Arquitectónica
* **Use REST** cuando necesite operaciones transaccionales, endpoints CRUD bien definidos, simplicidad y facilidad de integración.
* **Use GraphQL** cuando tenga múltiples clientes (web, móvil, tablets) que demandan vistas de datos con formas muy distintas y donde el tráfico de red móvil deba optimizarse al mínimo.
* **Use WebSocket** cuando el servidor necesite empujar datos hacia el cliente de forma instantánea sin que el cliente los pida explícitamente.

---

## Actividad 4. Estrategia de Caché: Dónde, Qué y Por Qué

### 4.1 ¿Dónde se ubica la caché?
Se implementa una instancia de **Redis** ubicada entre el API Gateway / Servicios y la base de datos PostgreSQL, implementando el patrón **Cache-Aside (Lazy Loading)**.

```text
Cliente ---> API ---> ¿Está en Redis?
                        |-- SÍ (Cache Hit) --> Retorna dato (3 ms)
                        +-- NO (Cache Miss) -> Lee de PostgreSQL (60 ms)
                                                Guarda copia en Redis (TTL)
                                                Retorna dato
```

### 4.2 ¿Qué información SÍ se debe cachear y por qué?
1. **Catálogo de Cursos y Pensum Académico:**
   * *Razón:* Durante las semanas de matrícula, 5.000 estudiantes consultan las mismas materias una y otra vez. Los cursos casi nunca cambian durante el semestre.
   * *Estrategia:* TTL largo (ej. 4 horas) o invalidación dirigida cuando el coordinador edita una materia.
2. **Horarios y Aulas de Secciones:**
   * *Razón:* Altísima tasa de lectura en la primera semana de clases.
   * *Estrategia:* TTL de 30 minutos.
3. **Información de Sesión y Datos Básicos de Perfil:**
   * *Razón:* Cada petición entrante debe verificar el rol del usuario (estudiante o profesor). Consultar PostgreSQL en cada click satura la base de datos.
   * *Estrategia:* Guardar el perfil mínimo en Redis indexado por `user_id` con un TTL igual a la vigencia del token (ej. 1 hora).

### 4.3 ¿Qué información NO se debe cachear en Redis?
1. **El Cupo Restante en Matrícula Concurrente:**
   * *Razón:* Si se cachea el cupo de un curso con 1 vacante, dos estudiantes podrían ver "Cupo disponible = 1" en caché simultáneamente y ambos matricularse, generando sobrecupo (*overselling*). Debe validarse directamente en PostgreSQL con bloqueo transaccional (`SELECT ... FOR UPDATE`).
2. **Registro y Modificación de Calificaciones:**
   * *Razón:* Son operaciones de escritura críticas que deben persistir de inmediato en PostgreSQL para garantizar durabilidad y no perder notas ante un reinicio de memoria.

---

## Entregables Consolidados

### 1. Resumen de Justificación de Componentes
* **API Gateway:** Reduce acoplamiento, protege los servicios internos y evita exponer la topología del backend a Internet.
* **Auth SSO (JWT):** Hace que los servicios sean *stateless* (sin estado de sesión en memoria), facilitando el escalamiento horizontal.
* **Redis:** Disminuye en un 80% las consultas de solo lectura hacia PostgreSQL, permitiendo atender a los 5.000 usuarios con una sola base de datos.
* **WebSockets:** Proporciona reactividad instantánea con un coste de red mínimo comparado con *polling*.

### 2. Flujo de una Notificación en Tiempo Real
1. El docente publica las notas de un examen (`POST /api/v1/grades`).
2. El Servicio Académico guarda las notas en PostgreSQL en una transacción segura.
3. El Servicio Académico emite un evento interno hacia el Servicio de Notificaciones.
4. El Servicio de Notificaciones localiza las sesiones activas de los estudiantes matriculados y envía el paquete JSON a través del canal **WebSocket** abierto en sus navegadores.
5. En la pantalla del estudiante aparece de inmediato el aviso: *"Tu nota de Cálculo I ha sido publicada"*.
