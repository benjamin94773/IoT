# Actividades Prácticas y Diseños en Clase

**Curso:** Computación en la Nube e Internet de las Cosas  
**Estudiante:** Benjamín Ortiz

---

## Índice de Actividades

Este módulo agrupa los talleres de diseño de arquitectura de software, especificación de requerimientos y casos de estudio desarrollados a lo largo del curso:

1. **[01 — Diseño de Sistema Escalable: Ticketmaster](./01_diseno_ticketmaster/README.md)**
   - Arquitectura cliente-servidor, alta concurrencia, balanceador de carga, desacoplamiento con Redis (Locks y TTL de 10 min), colas de mensajería (RabbitMQ) y base de datos transaccional ACID (PostgreSQL).

2. **[02 — Sistema de Autenticación mediante API Keys](./02_autenticacion_apikeys/README.md)**
   - Seguridad perimetral en APIs, diagramas de contexto y alto nivel, API Gateway, validación en caché (Redis), hashing SHA-256 de claves y control de cuotas con Rate Limiting.

3. **[03 — Proyecto Integrador: Requerimientos y Refinamiento de Bodegas](./03_bodegas_distribuidas_requisitos/README.md)**
   - Requisitos funcionales y no funcionales de la plataforma de bodegas distribuidas (*Warehouse Cloud Platform*), sesión completa de preguntas y respuestas de refinamiento de negocio, patrón Saga, consistencia eventual (CQRS), workers asíncronos y monitoreo IoT.
