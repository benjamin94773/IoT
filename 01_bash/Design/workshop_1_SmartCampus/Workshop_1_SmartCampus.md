# Workshop 1 - Modelando el problema y la primera arquitectura

**Curso:** Computación en la Nube e Internet de las Cosas  
**Proyecto:** SmartCampus — Sistema de Gestión Académica

---

## Contexto

La Universidad **SmartCampus** desea reemplazar su antiguo sistema de gestión académica monolítico debido a problemas de mantenimiento, rigidez y falta de documentación. En esta primera fase, se busca diseñar un sistema moderno, mantenible y escalable para las operaciones fundamentales de la universidad.

## Objetivos

- Comprender el problema y delimitar los requerimientos funcionales y no funcionales.
- Identificar actores y casos de uso del sistema académico.
- Proponer una arquitectura de software inicial de alto nivel.
- Diseñar la API y el modelo de base de datos relacional.

## Requerimientos

### Requerimientos Funcionales
- Gestionar estudiantes, docentes, cursos y matrículas.
- Consultar horarios académicos por estudiante y docente.
- Registrar y consultar calificaciones de los estudiantes.

### Requerimientos No Funcionales
- **Concurrencia:** Soportar hasta 500 usuarios simultáneos sin degradación del servicio.
- **Consistencia:** Consistencia estricta (ACID) en transacciones de matrícula y notas.
- **Disponibilidad y Rendimiento:** Tiempos de respuesta inferiores a 200 ms en consultas frecuentes.

---

# Desarrollo de Actividades

## Actividad 1. Identificación de Actores, Casos de Uso y Entidades

### 1.1 Actores del Sistema
1. **Estudiante:** Usuario final que consulta oferta de cursos, realiza su matrícula, revisa su horario y consulta sus calificaciones.
2. **Docente:** Usuario encargado de consultar los cursos y horarios que tiene asignados, listar los estudiantes matriculados en sus grupos y registrar las calificaciones.
3. **Administrador Académico (Coordinador / Registro y Control):** Gestiona el catálogo de materias, habilita períodos académicos, crea grupos/secciones, asigna docentes y administra estudiantes y docentes.

### 1.2 Casos de Uso Principales
* **Módulo de Usuarios y Autenticación:**
  * CU01: Iniciar sesión y autenticar credenciales.
  * CU02: Administrar perfiles de estudiantes y docentes.
* **Módulo de Gestión Curricular:**
  * CU03: Crear y actualizar cursos/asignaturas.
  * CU04: Abrir grupos/secciones para un período académico con cupos máximos y asignación docente.
  * CU05: Asignar bloques de horarios y aulas a cada grupo.
* **Módulo de Matrícula:**
  * CU06: Consultar grupos disponibles y cupos restantes.
  * CU07: Matricular asignaturas (validando cupo y cruce de horarios).
  * CU08: Consultar horario semanal consolidado.
* **Módulo de Calificaciones:**
  * CU09: Registrar y modificar notas por corte/evaluación.
  * CU10: Consultar historial académico y notas finales por estudiante.

### 1.3 Entidades Principales del Dominio
* **Estudiante (`Student`):** Código estudiantil, nombre, correo institucional, documento de identidad, estado académico.
* **Docente (`Teacher`):** Identificación, nombre, correo, departamento académico.
* **Curso / Asignatura (`Course`):** Código de asignatura, nombre, créditos académicos, descripción.
* **Grupo / Sección (`CourseSection`):** Grupo específico abierto en un semestre (ej. Grupo 01 de Cálculo I), cupo máximo, docente asignado.
* **Horario (`Schedule`):** Día de la semana, hora inicio, hora fin, aula/salón asignado a un grupo.
* **Matrícula (`Enrollment`):** Registro de la inscripción de un estudiante en un grupo específico para un período académico.
* **Calificación (`Grade`):** Nota cuantitativa asignada a una matrícula para un corte/hito específico (ej. Parcial 1, 30%).

---

## Actividad 2. Diseño de Arquitectura de Alto Nivel

Para este escenario inicial (500 usuarios simultáneos, enfoque centrado en operaciones académicas y consistencia estricta), se propone una arquitectura de tres capas (**3-Tier Architecture**) estructurada como un **Monolito Modular**:

### 2.1 Diagrama de Arquitectura

```text
+--------------------------------------------------------------+
|                    CAPA DE PRESENTACIÓN                      |
|                                                              |
|        [ Cliente Web (SPA - React / HTML5 / CSS3 / JS) ]     |
+------------------------------+-------------------------------+
                               |
                               | HTTPS / JSON (TCP 443 / 80)
                               v
+--------------------------------------------------------------+
|                     CAPA DE APLICACIÓN                       |
|                                                              |
|     +--------------------------------------------------+     |
|     |         Servidor Web / Reverse Proxy (Nginx)     |     |
|     +------------------------+-------------------------+     |
|                              |                               |
|     +------------------------v-------------------------+     |
|     |           API Backend (Python - FastAPI)         |     |
|     |                                                  |     |
|     |   +-------------------+  +-------------------+   |     |
|     |   | Módulo Usuarios   |  | Módulo Cursos     |   |     |
|     |   +-------------------+  +-------------------+   |     |
|     |   +-------------------+  +-------------------+   |     |
|     |   | Módulo Matrículas |  | Módulo Notas      |   |     |
|     |   +-------------------+  +-------------------+   |     |
|     +------------------------+-------------------------+     |
+------------------------------|-------------------------------+
                               |
                               | Protocolo TCP Postgres (Puerto 5432)
                               v
+--------------------------------------------------------------+
|                    CAPA DE PERSISTENCIA                      |
|                                                              |
|             [ Base de Datos Relacional: PostgreSQL ]         |
|              (Transacciones ACID, Tablas Normalizadas)       |
+--------------------------------------------------------------+
```

### 2.2 Descripción de Componentes
1. **Cliente Web:** Interfaz gráfica responsiva ejecutada en el navegador del usuario. Se comunica con el backend mediante peticiones HTTP asíncronas (`fetch` / `axios`) transmitiendo datos en formato JSON.
2. **Nginx (Reverse Proxy):** Servidor perimetral que recibe las peticiones en el puerto 80/443, maneja el cifrado SSL/TLS, sirve archivos estáticos del frontend y reenvía el tráfico dinámico a la API.
3. **API Backend (FastAPI / Python):** Núcleo lógico del sistema implementado como un monolito modular. Contiene la lógica de negocio, validaciones transaccionales (no permitir cupos negativos, evitar cruces de horario) y controladores organizados por dominios.
4. **Base de Datos (PostgreSQL):** Motor de base de datos relacional encargado de la persistencia permanente, integridad referencial y soporte transaccional ACID (`BEGIN...COMMIT / ROLLBACK`).

---

## Actividad 3. Selección de Estilo de API: ¿REST o GraphQL?

### 3.1 Decisión
Para este taller y fase inicial, la elección recomendada es **REST**.

### 3.2 Cuadro Comparativo y Justificación Técnica

| Criterio | REST | GraphQL | Decisión para SmartCampus Fase 1 |
| :--- | :--- | :--- | :--- |
| **Tipo de operaciones** | Basado en recursos y verbos HTTP estándar (`GET`, `POST`, `PUT`, `DELETE`). Ideal para CRUD claro. | Lenguaje de consulta sobre un único endpoint (`POST /graphql`). | **Gana REST:** El sistema académico inicial se compone principalmente de operaciones CRUD directas (crear curso, listar docentes, registrar nota). |
| **Complejidad de implementación** | Muy baja. Soporte nativo universal en frameworks (FastAPI, Flask, Express). | Alta. Requiere definir esquemas, resolvers, tipos y prevenir consultas cíclicas o costosas. | **Gana REST:** Permite desarrollar, probar y desplegar de forma rápida y sin sobrecarga cognitiva innecesaria. |
| **Caché HTTP** | Nativa y sencilla. Aprovecha cabeceras HTTP (`Cache-Control`, `ETag`) en Nginx o navegadores. | Compleja. Todas las consultas son `POST` a `/graphql`, lo que anula la caché HTTP estándar. | **Gana REST:** Permite cachear catálogos que cambian poco (ej. lista de materias o facultades) directamente en Nginx. |
| **Carga de 500 usuarios** | Manejo ligero y directo mediante pool de conexiones y procesos de aplicación. | Sobrecarga de parsing y ejecución del árbol AST por cada query. | **Gana REST:** Procesa peticiones simples con menor consumo de CPU por request. |
| **Over-fetching / Under-fetching** | Puede enviar campos de más si no se usan DTOs específicos. | El cliente pide exactamente los campos requeridos. | Ventaja de GraphQL en clientes móviles, pero en esta fase inicial solo hay Cliente Web. |

**Conclusión:** REST cumple de manera óptima con el principio de simplicidad arquitectónica (*KISS - Keep It Simple, Stupid*). No introduce capas de complejidad prematura y resuelve el 100% de los requerimientos de la Fase 1.

---

## Actividad 4. Diseño del Modelo de Base de Datos

Dado que el sistema gestiona notas oficiales, matrículas y cupos de cursos, la integridad de los datos es crítica. Se emplea un modelo relacional normalizado en Tercera Forma Normal (3FN) con claves foráneas e índices.

### 4.1 Diagrama Entidad - Relación (Relacional)

```text
 +-----------------+          +---------------------+          +-----------------+
 |    STUDENTS     |          |   COURSE_SECTIONS   |          |     COURSES     |
 +-----------------+          +---------------------+          +-----------------+
 | id (PK)         |<---+     | id (PK)             |<----+    | id (PK)         |
 | student_code    |    |     | course_id (FK)      |-----+--->| code (UNIQUE)   |
 | first_name      |    |     | teacher_id (FK)     |---+ |    | name            |
 | last_name       |    |     | term (e.g. 2026-1)  |   | |    | credits         |
 | email (UNIQUE)  |    |     | section_number      |   | |    +-----------------+
 +-----------------+    |     | max_capacity        |   | |
                        |     +---------------------+   | |    +-----------------+
                        |                |              | |    |    TEACHERS     |
                        |                | 1            | |    +-----------------+
                        |                |              | +--->| id (PK)         |
                        |                v N            |      | employee_code   |
                        |     +---------------------+   |      | first_name      |
                        |     |      SCHEDULES      |   |      | last_name       |
                        |     +---------------------+   |      | email (UNIQUE)  |
                        |     | id (PK)             |   |      +-----------------+
                        |     | section_id (FK)     |   |
                        |     | day_of_week         |   |
                        |     | start_time          |   |
                        |     | end_time            |   |
                        |     | classroom           |   |
                        |     +---------------------+   |
                        |                               |
                        +---------------+               |
                                        |               |
                                        v               v
                             +-----------------------------+
                             |         ENROLLMENTS         |
                             +-----------------------------+
                             | id (PK)                     |
                             | student_id (FK)             |
                             | section_id (FK)             |
                             | status (ENROLLED/DROPPED)   |
                             | enrolled_at                 |
                             +-----------------------------+
                                            |
                                            | 1
                                            v N
                             +-----------------------------+
                             |           GRADES            |
                             +-----------------------------+
                             | id (PK)                     |
                             | enrollment_id (FK)          |
                             | evaluation_name             |
                             | percentage (e.g. 30.0)      |
                             | score (e.g. 4.5)            |
                             | registered_at               |
                             +-----------------------------+
```

### 4.2 Script DDL SQL (PostgreSQL)

```sql
-- 1. Tabla de Estudiantes
CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    student_code VARCHAR(20) UNIQUE NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Tabla de Docentes
CREATE TABLE teachers (
    id SERIAL PRIMARY KEY,
    employee_code VARCHAR(20) UNIQUE NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    department VARCHAR(100) NOT NULL
);

-- 3. Tabla de Cursos
CREATE TABLE courses (
    id SERIAL PRIMARY KEY,
    code VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(120) NOT NULL,
    credits INTEGER NOT NULL CHECK (credits > 0),
    description TEXT
);

-- 4. Tabla de Secciones / Grupos
CREATE TABLE course_sections (
    id SERIAL PRIMARY KEY,
    course_id INTEGER NOT NULL REFERENCES courses(id) ON DELETE RESTRICT,
    teacher_id INTEGER NOT NULL REFERENCES teachers(id) ON DELETE RESTRICT,
    term VARCHAR(10) NOT NULL, -- Ej: '2026-1'
    section_number INTEGER NOT NULL,
    max_capacity INTEGER NOT NULL CHECK (max_capacity > 0),
    CONSTRAINT uk_course_term_section UNIQUE (course_id, term, section_number)
);

-- 5. Tabla de Horarios de la Sección
CREATE TABLE schedules (
    id SERIAL PRIMARY KEY,
    section_id INTEGER NOT NULL REFERENCES course_sections(id) ON DELETE CASCADE,
    day_of_week VARCHAR(10) NOT NULL CHECK (day_of_week IN ('LUNES','MARTES','MIERCOLES','JUEVES','VIERNES','SABADO')),
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    classroom VARCHAR(50) NOT NULL,
    CHECK (end_time > start_time)
);

-- 6. Tabla de Matrículas (Inscripción de estudiante a sección)
CREATE TABLE enrollments (
    id SERIAL PRIMARY KEY,
    student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE RESTRICT,
    section_id INTEGER NOT NULL REFERENCES course_sections(id) ON DELETE RESTRICT,
    status VARCHAR(20) NOT NULL DEFAULT 'ENROLLED' CHECK (status IN ('ENROLLED', 'DROPPED', 'COMPLETED')),
    enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uk_student_section UNIQUE (student_id, section_id)
);

-- 7. Tabla de Calificaciones
CREATE TABLE grades (
    id SERIAL PRIMARY KEY,
    enrollment_id INTEGER NOT NULL REFERENCES enrollments(id) ON DELETE CASCADE,
    evaluation_name VARCHAR(50) NOT NULL, -- Ej: 'Parcial 1', 'Taller 1', 'Final'
    percentage NUMERIC(5,2) NOT NULL CHECK (percentage > 0 AND percentage <= 100),
    score NUMERIC(3,2) NOT NULL CHECK (score >= 0.0 AND score <= 5.0),
    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## Entregables Consolidados

### 1. Especificación de Endpoints de la API REST

| Método | Endpoint | Descripción | Body / Parámetros | Código Respuesta |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/api/v1/health` | Verificación de estado del servicio | Ninguno | `200 OK` |
| `GET` | `/api/v1/students/{id}/schedule` | Consultar horario del estudiante | Path param: `id` | `200 OK` |
| `POST` | `/api/v1/enrollments` | Matricular asignatura en un grupo | `{ "student_id": 1, "section_id": 4 }` | `201 Created` / `400 Bad Request` |
| `GET` | `/api/v1/sections/{id}/students` | Listar estudiantes matriculados en grupo (Docente) | Path param: `id` | `200 OK` |
| `POST` | `/api/v1/grades` | Registrar o actualizar calificación de un estudiante | `{ "enrollment_id": 12, "evaluation": "Parcial 1", "percentage": 30, "score": 4.5 }` | `201 Created` |
| `GET` | `/api/v1/students/{id}/grades` | Consultar historial de notas del estudiante | Path param: `id`, Query: `term=2026-1` | `200 OK` |

### 2. Ejemplo de Payload: Matrícula de Asignatura
**Petición (`POST /api/v1/enrollments`):**
```json
{
  "student_id": 105,
  "section_id": 12
}
```

**Respuesta (`201 Created`):**
```json
{
  "enrollment_id": 341,
  "student_code": "EST-2026105",
  "course": "Sistemas Distribuidos",
  "term": "2026-1",
  "section": 1,
  "status": "ENROLLED",
  "enrolled_at": "2026-02-01T08:30:00Z"
}
```
