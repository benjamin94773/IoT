# Taller 4 - PostgreSQL con Docker y Docker Compose

**Curso:** Computación en la Nube e Internet de las Cosas

**Temas**:

- PostgreSQL
- Docker
- Docker Compose
- SQL
- Esquemas
- Tablas
- Volúmenes
- Scripts de inicialización

---

# Objetivos

Al finalizar este workshop el estudiante será capaz de:

- Crear PostgreSQL mediante Docker Compose.
- Administrar la base mediante `psql`.
- Construir manualmente una base de datos y su esquema.
- Crear tablas, relaciones y registros.
- Persistir información con volúmenes.
- Automatizar la creación mediante archivos `.sql`.
- Verificar la inicialización del contenido desde cero.

---

# Parte 1. Construcción manual

Crear:

```yaml
services:
  postgres:
    image: postgres:16
    environment:
      POSTGRES_DB: universidad
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: admin
    ports:
      - "5432:5432"
```

Levantar:

```bash
docker compose up -d
```

Entrar:

```bash
docker compose exec postgres psql -U admin -d universidad
```
Listo

```
PS C:\Users\Benja\OneDrive\Desktop\IOT\Entregables\03_docker\workshop4> docker compose up -d
[+] up 2/2
 ✔ Network workshop4_default      Created                                                                                                   0.0s
 ✔ Container workshop4-postgres-1 Started                                                                                                   0.3s
PS C:\Users\Benja\OneDrive\Desktop\IOT\Entregables\03_docker\workshop4> docker compose ps
NAME                   IMAGE         COMMAND                  SERVICE    CREATED         STATUS         PORTS
workshop4-postgres-1   postgres:16   "docker-entrypoint.s…"   postgres   4 seconds ago   Up 3 seconds   0.0.0.0:5432->5432/tcp, [::]:5432->5432/tcp
PS C:\Users\Benja\OneDrive\Desktop\IOT\Entregables\03_docker\workshop4> docker compose exec postgres psql -U admin -d universidad
psql (16.15 (Debian 16.15-1.pgdg13+2))
Type "help" for help.

universidad=# 
```

---

# Parte 2. Crear manualmente la estructura

Ejecutar:

```sql
CREATE SCHEMA academia;
```

Crear:

```sql
CREATE TABLE academia.students (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL
);
```

Crear otra tabla:

```sql
CREATE TABLE academia.courses (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    credits INTEGER NOT NULL
);
```

Insertar datos y consultar:

```sql
SELECT * FROM academia.students;
SELECT * FROM academia.courses;
```
Listo
```
universidad=# CREATE SCHEMA academia;
CREATE SCHEMA
universidad=# CREATE TABLE academia.students (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL
);
CREATE TABLE
universidad=# CREATE TABLE academia.courses (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    credits INTEGER NOT NULL
);
CREATE TABLE
universidad=# INSERT INTO academia.students (name, email) VALUES
('Ana', 'ana@example.com'),
('Luis', 'luis@example.com'),
('Marta', 'marta@example.com');

INSERT INTO academia.courses (name, credits) VALUES
('Cloud Computing', 3),
('Internet of Things', 4);
INSERT 0 3
INSERT 0 2
universidad=# SELECT * FROM academia.students;
 id | name  |       email       
----+-------+-------------------
  1 | Ana   | ana@example.com
  2 | Luis  | luis@example.com
  3 | Marta | marta@example.com
(3 rows)

universidad=# SELECT * FROM academia.courses;
 id |        name        | credits 
----+--------------------+---------
  1 | Cloud Computing    |       3
  2 | Internet of Things |       4
(2 rows)

universidad=# 

```

---

# Parte 3. Automatización

Crear:

```text
postgres/init/01-schema.sql
postgres/init/02-data.sql
```

`01-schema.sql`:

```sql
CREATE SCHEMA IF NOT EXISTS academia;

CREATE TABLE IF NOT EXISTS academia.students (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS academia.courses (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    credits INTEGER NOT NULL
);
```

`02-data.sql`:

```sql
INSERT INTO academia.students (name, email) VALUES
('Ana', 'ana@example.com'),
('Luis', 'luis@example.com'),
('Marta', 'marta@example.com');

INSERT INTO academia.courses (name, credits) VALUES
('Cloud Computing', 3),
('Internet of Things', 4);
```

---

# Parte 4. Montar los scripts

```yaml
services:
  postgres:
    image: postgres:16
    environment:
      POSTGRES_DB: universidad
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: admin
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./postgres/init:/docker-entrypoint-initdb.d:ro

volumes:
  postgres_data:
```

---

# Parte 5. Regla importante de inicialización

Los scripts de `/docker-entrypoint-initdb.d` son ejecutados por la imagen oficial durante la inicialización de un directorio de datos vacío.

Para probar nuevamente la carga automática desde cero:

```bash
docker compose down -v
```

Luego:

```bash
docker compose up -d
```

Verificar esquemas:

```bash
docker compose exec postgres psql -U admin -d universidad -c "\\dn"
```

Verificar tablas:

```bash
docker compose exec postgres psql -U admin -d universidad -c "\\dt academia.*"
```

Consultar datos:

```bash
docker compose exec postgres psql -U admin -d universidad -c "SELECT * FROM academia.students;"
```
Evidencia ejecucion
```

PS C:\Users\Benja\OneDrive\Desktop\IOT\Entregables\03_docker\workshop4> docker compose config
name: workshop4
services:
  postgres:
    environment:
      POSTGRES_DB: universidad
      POSTGRES_PASSWORD: admin
      POSTGRES_USER: admin
    image: postgres:16
    networks:
      default: null
    ports:
      - mode: ingress
        target: 5432
        published: "5432"
        protocol: tcp
    volumes:
      - type: volume
        source: postgres_data
        target: /var/lib/postgresql/data
        volume: {}
      - type: bind
        source: C:\Users\Benja\OneDrive\Desktop\IOT\Entregables\03_docker\workshop4\postgres\init
        target: /docker-entrypoint-initdb.d
        read_only: true
        bind: {}
networks:
  default:
    name: workshop4_default
volumes:
  postgres_data:
    name: workshop4_postgres_data
PS C:\Users\Benja\OneDrive\Desktop\IOT\Entregables\03_docker\workshop4> docker compose down -v
[+] down 2/2
 ✔ Container workshop4-postgres-1 Removed                                                                                                   0.3s
 ✔ Network workshop4_default      Removed                                                                                                   0.2s
PS C:\Users\Benja\OneDrive\Desktop\IOT\Entregables\03_docker\workshop4> docker compose up -d
[+] up 3/3
 ✔ Network workshop4_default      Created                                                                                                   0.0s
 ✔ Volume workshop4_postgres_data Created                                                                                                   0.0s
 ✔ Container workshop4-postgres-1 Started                                                                                                   0.2s
PS C:\Users\Benja\OneDrive\Desktop\IOT\Entregables\03_docker\workshop4> docker compose ps
NAME                   IMAGE         COMMAND                  SERVICE    CREATED         STATUS         PORTS
workshop4-postgres-1   postgres:16   "docker-entrypoint.s…"   postgres   3 seconds ago   Up 3 seconds   0.0.0.0:5432->5432/tcp, [::]:5432->5432/tcp
PS C:\Users\Benja\OneDrive\Desktop\IOT\Entregables\03_docker\workshop4> docker compose exec postgres psql -U admin -d universidad -c "\dn"
       List of schemas
   Name   |       Owner       
----------+-------------------
 academia | admin
 public   | pg_database_owner
(2 rows)

PS C:\Users\Benja\OneDrive\Desktop\IOT\Entregables\03_docker\workshop4> docker compose exec postgres psql -U admin -d universidad -c "\dt academia.*"
          List of relations
  Schema  |   Name   | Type  | Owner 
----------+----------+-------+-------
 academia | courses  | table | admin
 academia | students | table | admin
(2 rows)

PS C:\Users\Benja\OneDrive\Desktop\IOT\Entregables\03_docker\workshop4> docker compose exec postgres psql -U admin -d universidad -c "SELECT * FROM academia.students;"
 id | name  |       email       
----+-------+-------------------
  1 | Ana   | ana@example.com
  2 | Luis  | luis@example.com
  3 | Marta | marta@example.com
(3 rows)

PS C:\Users\Benja\OneDrive\Desktop\IOT\Entregables\03_docker\workshop4> docker compose exec postgres psql -U admin -d universidad -c "SELECT * FROM academia.courses;"
 id |        name        | credits 
----+--------------------+---------
  1 | Cloud Computing    |       3
  2 | Internet of Things |       4
(2 rows)


```


---

# Parte 6. Reto

Automatizar:

- `teachers`.
- `courses`.
- `enrollments`.
- Llaves foráneas.
- Datos de prueba.

El esquema debe quedar completamente reconstruible eliminando el volumen y levantando nuevamente Compose.
Evidencia del Reto
```
PS C:\Users\Benja\OneDrive\Desktop\IOT\Entregables\03_docker\workshop4> docker compose down -v
[+] down 3/3
 ✔ Container workshop4-postgres-1 Removed                                                                                                   0.3s
 ✔ Volume workshop4_postgres_data Removed                                                                                                   0.0s
 ✔ Network workshop4_default      Removed                                                                                                   0.2s
PS C:\Users\Benja\OneDrive\Desktop\IOT\Entregables\03_docker\workshop4> docker compose up -d
[+] up 3/3
 ✔ Volume workshop4_postgres_data Created                                                                                                   0.0s
 ✔ Network workshop4_default      Created                                                                                                   0.0s
 ✔ Container workshop4-postgres-1 Started                                                                                                   0.3s
PS C:\Users\Benja\OneDrive\Desktop\IOT\Entregables\03_docker\workshop4> docker compose ps
NAME                   IMAGE         COMMAND                  SERVICE    CREATED          STATUS          PORTS
workshop4-postgres-1   postgres:16   "docker-entrypoint.s…"   postgres   20 seconds ago   Up 19 seconds   0.0.0.0:5432->5432/tcp, [::]:5432->5432/tcp
PS C:\Users\Benja\OneDrive\Desktop\IOT\Entregables\03_docker\workshop4> docker compose exec postgres psql -U admin -d universidad -c "\dt academia.*"
           List of relations
  Schema  |    Name     | Type  | Owner 
----------+-------------+-------+-------
 academia | courses     | table | admin
 academia | enrollments | table | admin
 academia | students    | table | admin
 academia | teachers    | table | admin
(4 rows)

PS C:\Users\Benja\OneDrive\Desktop\IOT\Entregables\03_docker\workshop4> docker compose exec postgres psql -U admin -d universidad -c "SELECT * FROM academia.teachers;"
 id |     name     |       email        
----+--------------+--------------------
  1 | Carlos Perez | carlos@example.com
  2 | Laura Gomez  | laura@example.com
(2 rows)

PS C:\Users\Benja\OneDrive\Desktop\IOT\Entregables\03_docker\workshop4> docker compose exec postgres psql -U admin -d universidad -c "SELECT * FROM academia.courses;"
 id |        name        | credits | teacher_id 
----+--------------------+---------+------------
  1 | Cloud Computing    |       3 |          1
  2 | Internet of Things |       4 |          2
(2 rows)

PS C:\Users\Benja\OneDrive\Desktop\IOT\Entregables\03_docker\workshop4> docker compose exec postgres psql -U admin -d universidad -c "SELECT * FROM academia.enrollments;"
 student_id | course_id | enrollment_date 
------------+-----------+-----------------
          1 |         1 | 2026-09-05
          1 |         2 | 2026-09-05
          2 |         1 | 2026-09-05
          3 |         2 | 2026-09-05
(4 rows)

PS C:\Users\Benja\OneDrive\Desktop\IOT\Entregables\03_docker\workshop4> docker compose exec postgres psql -U admin -d universidad -c "SELECT s.name AS student, c.name AS course, t.name AS teacher FROM academia.enrollments e JOIN academia.students s ON e.student_id = s.id JOIN academia.courses c ON e.course_id = c.id JOIN academia.teachers t ON c.teacher_id = t.id;"
 student |       course       |   teacher    
---------+--------------------+--------------
 Ana     | Cloud Computing    | Carlos Perez
 Ana     | Internet of Things | Laura Gomez
 Luis    | Cloud Computing    | Carlos Perez
 Marta   | Internet of Things | Laura Gomez
(4 rows)

PS C:\Users\Benja\OneDrive\Desktop\IOT\Entregables\03_docker\workshop4> 


```



---

# Entregables

- `docker-compose.yml`.
- Directorio `postgres/init/`.
- Scripts `.sql`.
- Evidencia manual.
- Evidencia automática.
- Evidencia de esquemas, tablas y datos.
