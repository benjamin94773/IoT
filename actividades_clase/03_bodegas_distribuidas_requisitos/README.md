# Actividad 3 — Proyecto Integrador: Requerimientos y Refinamiento de Bodegas Distribuidas

**Curso:** Computación en la Nube e Internet de las Cosas  
**Tema:** Arquitectura Distribuida, Autonomía de Servicios, CQRS, Patrón Saga, Mensajería Asíncrona (RabbitMQ), Caché (Redis) e IoT.

---

## 1. Requisitos Funcionales (RF)

* **RF-01 Autonomía de Bodega:** Cada bodega debe administrar de manera autónoma sus productos, inventario, reservas y usuarios u operadores sin depender de la conectividad en tiempo real con la central.
* **RF-02 Movimientos de Inventario:** El sistema debe registrar y gestionar los movimientos de entrada y salida en cada uno de los almacenes con trazabilidad completa.
* **RF-03 Procesamiento Local:** La plataforma debe procesar consultas frecuentes de manera local en cada bodega para asegurar su autonomía y velocidad operativa.
* **RF-04 Transferencias Inter-Bodega:** El sistema debe permitir y coordinar la transferencia de productos entre distintas bodegas garantizando consistencia.
* **RF-05 Consolidación Central:** La plataforma central debe consolidar la información proveniente de todas las bodegas de la empresa.
* **RF-06 Consultas Globales y Reportes:** La plataforma central debe soportar la ejecución de consultas analíticas globales y la generación de reportes consolidados.
* **RF-07 Coordinación de Procesos Distribuidos:** El sistema debe coordinar procesos internos y distribuidos, incluyendo analítica empresarial e integración de datos.

---

## 2. Requisitos No Funcionales (RNF)

* **RNF-01 Rendimiento de Consultas:** Las consultas frecuentes deben ser rápidas utilizando memoria caché (Redis) y el sistema debe soportar cargas variables por bodega (desde 20 hasta 2.000 peticiones por segundo).
* **RNF-02 Consistencia Transaccional Local:** Las operaciones de escritura deben mantener consistencia transaccional (ACID) de forma local dentro de cada bodega.
* **RNF-03 Procesamiento Asíncrono Desacoplado:** Los procesos pesados deben ejecutarse de forma asíncrona mediante *workers* y RabbitMQ para evitar bloquear las APIs del sistema.
* **RNF-04 Escalabilidad y Balanceo:** Las bodegas deben poder escalar horizontalmente de manera independiente y utilizar balanceo de carga.
* **RNF-05 Tolerancia a Fallos Controlada:** Los procesos deben fallar de forma controlada mediante la implementación de idempotencia, reintentos exponenciales y colas de mensajes muertos (DLQ).
* **RNF-06 Trazabilidad Extremo a Extremo:** Debe existir observabilidad integral utilizando logs estructurados, métricas, identificadores de correlación (*correlation IDs*) y pruebas de estado (*health checks*).
* **RNF-07 Consistencia Eventual y Patrón Saga:** El sistema debe soportar consistencia eventual, separación de comandos y consultas (CQRS) y utilizar el patrón Saga para transacciones distribuidas.
* **RNF-08 Estándar Tecnológico:** La solución debe estar basada en contenedores (Docker), construirse con Python (FastAPI/Flask) y PostgreSQL, y estar diseñada para crecer hacia servicios de AWS (EC2, S3, RDS, Lambda) e integrarse con sensores IoT.

---

## 3. Preguntas de Refinamiento: Respuestas Validadas con el Cliente en Clase

Durante la sesión de levantamiento de requisitos con el cliente (Product Owner), se acordaron las siguientes definiciones clave de negocio:

### 1. ¿Qué datos específicos deben registrarse al momento de procesar un movimiento de entrada o salida de inventario?
* **Entrada de productos:** Identificador único del movimiento, trabajador/operador que registra, producto (SKU) y cantidad del producto recibida.
* **Salida de productos:** Identificador único del movimiento, bodega origen, hacia dónde va (destino), fecha de creación, fecha de actualización, estatus del movimiento y persona responsable del despacho.
* **Transferencia entre bodegas:** Identificador único de transferencia, bodega origen, bodega destino, estatus del envío, fecha de creación y fecha de actualización.

### 2. ¿Cómo funciona la lógica de "reservas" de productos y cuánto tiempo dura una reserva antes de expirar o confirmarse?
* **Tiempo límite:** Se definió un tiempo máximo de **4 horas** para mantener la reserva de stock.
* **Regla de negocio:** Una vez cumplidas las 4 horas sin confirmación de despacho, la reserva **expira automáticamente** y los productos vuelven de inmediato al inventario disponible (*stock*).

### 3. ¿Qué roles de usuario operarán dentro de cada bodega y qué permisos requiere cada uno?
* **Admin Global:** Visión central y administración de toda la plataforma de la empresa.
* **Admin de Bodega:** Gestión operativa y control exclusivo dentro de su propio almacén.
* **Encargado de Entrega de Producto:** Responsable de verificar y formalizar los despachos y salidas físicas de mercancía.
* **Líderes de Compras / Cadena:** Gestión de contratos con proveedores y verificación de reportes estadísticos de compras.

### 4. ¿Cuál es el flujo de negocio exacto cuando se solicita transferir productos entre dos bodegas independientes?
* El producto en la bodega origen cambia su estado de disponible a **Reservado**.
* Al iniciarse el transporte, pasa a estado **En camino** (en tránsito) hasta llegar a la bodega de destino.
* A los líderes y compras les interesa garantizar el cumplimiento y recepción formal de los pedidos solicitados.

### 5. ¿Cómo debe alertar el sistema a los administradores cuando un proceso falla repetidamente y los mensajes caen en la cola de mensajes muertos (DLQ)?
* El sistema debe disparar automáticamente **notificaciones por correo electrónico** dirigidas a los administradores del sistema, detallando el fallo y la información del mensaje que no pudo ser procesado.

---

## 4. Definiciones y Supuestos Técnicos del Sistema (Basados en la Arquitectura del Proyecto)

Para las preguntas que no fueron abordadas directamente en la sesión con el cliente, se establecieron las siguientes definiciones de ingeniería basadas en la arquitectura técnica del Proyecto Integrador:

### 6. ¿Cuáles son las "consultas frecuentes" exactas que los operadores realizan a diario y que deben ser aceleradas mediante la caché (Redis)?
* Consulta de stock disponible por SKU en la bodega local.
* Ubicación física del producto en el almacén (pasillo, estantería y nivel).
* Consulta del estado de una reserva u orden de entrega activa.
* Validación rápida de permisos y tokens de sesión de operadores.

### 7. Si una transferencia falla en el sistema de la bodega de destino, ¿cuál debe ser el mecanismo de compensación en la bodega de origen (Saga)?
* Se implementa una **transacción de compensación** bajo el patrón Saga: si la bodega destino no puede procesar el ingreso o rechaza el lote, se emite un evento de compensación que revierte la reserva en la bodega de origen, devolviendo las unidades al stock disponible local y registrando la incidencia en auditoría.

### 8. ¿Existen procesos internos o "pesados" que actualmente bloquean el trabajo de los operadores y que deban moverse a workers asíncronos con prioridad?
* Generación de reportes de inventario y cierres contables mensuales en formato PDF.
* Carga e importación masiva de catálogos mediante hojas de cálculo CSV de proveedores.
* Sincronización en segundo plano de eventos acumulados hacia la plataforma central.

### 9. ¿Qué indicadores, métricas o reportes globales necesita ver la gerencia en la plataforma central de consolidación?
* Stock consolidado global por producto sumando todas las bodegas.
* Tasa de rotación de inventarios y productos de baja demanda por región.
* Tiempos promedio de tránsito en transferencias inter-bodega.
* Reportes de mermas, pérdidas e inconsistencias de inventario.

### 10. Para los modelos de lectura (CQRS), ¿es aceptable que la información en la plataforma central tenga un ligero retraso (consistencia eventual), o hay datos que requieren actualización en tiempo real estricto?
* **En la plataforma central:** Es **100% aceptable consistencia eventual** (retraso de 5 a 60 segundos) para analítica gerencial y reportes consolidados.
* **En cada bodega local:** Las transacciones de despacho y reservas **requieren consistencia estricta en tiempo real** para evitar despachar producto inexistente.

### 11. ¿Qué tipo de información histórica o archivos pesados se espera procesar mediante procesos Batch y almacenar en AWS S3?
* Copias de seguridad periódicas (*backups*) de las bases de datos PostgreSQL de cada bodega.
* Reportes mensuales consolidados de movimientos y facturación.
* Archivos comprimidos de registros y logs estructurados de auditoría.

### 12. Sabiendo que existen bodegas con hasta 2.000 peticiones por segundo, ¿cuáles son los tiempos de respuesta máximos aceptables (latencia) para estas operaciones críticas?
* Consultas de inventario en caché en memoria (Redis): **menor a 10 milisegundos**.
* Escrituras transaccionales locales en base de datos (PostgreSQL): **menor a 150 milisegundos**.
* Uptime y disponibilidad operativa de la API local: **mínimo 99.9%**.

### 13. En caso de que se pierda la conexión entre una bodega y la central, ¿cuál es el protocolo operativo mientras el sistema local sigue funcionando de manera autónoma?
* **Patrón Transactional Outbox (Modo Autónomo Local):** La bodega continúa operando normalmente registrando transacciones en su base de datos local. Los eventos que deben enviarse a la central se guardan en una tabla local de eventos pendientes. Al restablecerse la conectividad, un proceso en segundo plano los retransmite a RabbitMQ central de forma ordenada e idempotente.

### 14. ¿Qué variables físicas se planean monitorear dentro de las bodegas con dispositivos IoT?
* Temperatura y humedad ambiental para bodegas de productos perecederos o farmacéuticos.
* Sensores de apertura de puertas y control de acceso físico en zonas restringidas.
* Pórticos con lectores RFID en muelles de carga para detectar el ingreso y salida automática de estibas (*pallets*).

### 15. ¿Qué volumen de datos emitirán estos sensores y con qué frecuencia deben comunicarse con la plataforma?
* **Sensores de temperatura y humedad:** 1 lectura cada **30 segundos** por sensor en formato ligero JSON (~100 bytes) utilizando protocolo **MQTT**.
* **Lectores RFID:** Comunicación reactiva basada en eventos (se emite una lectura únicamente cuando una estiba cruza el portal del muelle).
