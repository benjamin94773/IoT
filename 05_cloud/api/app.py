import os
import boto3
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, jsonify, request

app = Flask(__name__)


# Sección 30: Conexión a PostgreSQL usando variables de entorno (DB_HOST=db)
def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "db"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "equipment"),
        user=os.getenv("DB_USER", "equipment"),
        password=os.getenv("DB_PASSWORD", "change-me"),
        cursor_factory=RealDictCursor,
    )


# Sección 31: Cliente S3 con boto3 (usa el IAM Role de la EC2 automáticamente)
s3 = boto3.client("s3", region_name=os.getenv("AWS_REGION", "us-east-1"))


@app.get("/health")
def health():
    return jsonify({
        "status": "ok",
        "service": "equipment-api",
        "version": "2.0"
    })


@app.get("/devices")
def devices():
    return jsonify([
        { "id": 2, "name": "Smartphone Galaxy X", "category": "Celulares", "price": "3500000" },
        { "id": 3, "name": "Monitor Gamer UltraWide 34", "category": "Monitores", "price": "2200000" },
        { "id": 4, "name": "Auriculares Pro Wireless", "category": "Audio", "price": "800000" },
        { "id": 5, "name": "Teclado Mecánico RGB", "category": "Periféricos", "price": "450000" },
        { "id": 6, "name": "Consola PlayStation 5 Pro", "category": "Videojuegos", "price": "4200000" },
        { "id": 7, "name": "Cámara Mirrorless 4K", "category": "Fotografía", "price": "6000000" },
        { "id": 8, "name": "Smartwatch Sport V2", "category": "Relojes", "price": "1200000" },
        { "id": 9, "name": "Tarjeta Gráfica RTX 4070", "category": "Componentes", "price": "3800000" },
        { "id": 10, "name": "Disco Duro Externo 2TB SSD", "category": "Almacenamiento", "price": "650000" },
        { "id": 11, "name": "Tableta Gráfica Pro 13", "category": "Tabletas", "price": "1900000" }
    ])


# --- Sección 3.1: Empleados ---
@app.get("/empleados")
def get_empleados():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name AS nombre, email AS correo, department AS departamento FROM employees ORDER BY id;")
            return jsonify(cur.fetchall())


@app.post("/empleados")
def create_empleado():
    data = request.get_json()
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO employees (name, email, department)
                VALUES (%s, %s, %s)
                RETURNING id, name AS nombre, email AS correo, department AS departamento;
                """,
                (data["nombre"], data["correo"], data.get("departamento")),
            )
            nuevo = cur.fetchone()
            conn.commit()
            return jsonify(nuevo), 201


@app.get("/empleados/<int:empleado_id>")
def get_empleado(empleado_id):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, name AS nombre, email AS correo, department AS departamento FROM employees WHERE id = %s;",
                (empleado_id,),
            )
            emp = cur.fetchone()
            if not emp:
                return jsonify({"error": "Empleado no encontrado"}), 404
            return jsonify(emp)


# --- Sección 3.2: Equipos ---
@app.get("/equipos")
def get_equipos():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, internal_code AS codigo_interno, type AS tipo, brand AS marca,
                       model AS modelo, serial_number AS numero_serie, status AS estado, employee_id
                FROM equipment ORDER BY id;
                """
            )
            return jsonify(cur.fetchall())


@app.post("/equipos")
def create_equipo():
    data = request.get_json()
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO equipment (internal_code, type, brand, model, serial_number, status)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id, internal_code AS codigo_interno, type AS tipo, brand AS marca,
                          model AS modelo, serial_number AS numero_serie, status AS estado;
                """,
                (
                    data["codigo_interno"],
                    data["tipo"],
                    data.get("marca"),
                    data.get("modelo"),
                    data.get("numero_serie"),
                    data.get("estado", "DISPONIBLE"),
                ),
            )
            nuevo = cur.fetchone()
            conn.commit()
            return jsonify(nuevo), 201


@app.get("/equipos/<int:equipo_id>")
def get_equipo(equipo_id):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, internal_code AS codigo_interno, type AS tipo, brand AS marca,
                       model AS modelo, serial_number AS numero_serie, status AS estado, employee_id
                FROM equipment WHERE id = %s;
                """,
                (equipo_id,),
            )
            eq = cur.fetchone()
            if not eq:
                return jsonify({"error": "Equipo no encontrado"}), 404
            return jsonify(eq)


@app.put("/equipos/<int:equipo_id>")
def update_equipo(equipo_id):
    data = request.get_json()
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE equipment
                SET type = COALESCE(%s, type),
                    brand = COALESCE(%s, brand),
                    model = COALESCE(%s, model),
                    status = COALESCE(%s, status)
                WHERE id = %s
                RETURNING id, internal_code AS codigo_interno, type AS tipo, brand AS marca,
                          model AS modelo, serial_number AS numero_serie, status AS estado;
                """,
                (data.get("tipo"), data.get("marca"), data.get("modelo"), data.get("estado"), equipo_id),
            )
            eq = cur.fetchone()
            conn.commit()
            if not eq:
                return jsonify({"error": "Equipo no encontrado"}), 404
            return jsonify(eq)


# --- Sección 3.3: Asignación ---
@app.post("/equipos/<int:equipo_id>/asignar")
def asignar_equipo(equipo_id):
    data = request.get_json()
    empleado_id = data.get("empleado_id")
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, status FROM equipment WHERE id = %s;", (equipo_id,))
            eq = cur.fetchone()
            if not eq:
                return jsonify({"error": "Equipo no encontrado"}), 404
            if eq["status"] != "DISPONIBLE":
                return jsonify({"error": "El equipo no está disponible"}), 400

            cur.execute("SELECT id, name FROM employees WHERE id = %s;", (empleado_id,))
            emp = cur.fetchone()
            if not emp:
                return jsonify({"error": "Empleado no encontrado"}), 404

            cur.execute(
                "UPDATE equipment SET employee_id = %s, status = 'ASIGNADO' WHERE id = %s;",
                (empleado_id, equipo_id),
            )
            conn.commit()
            return jsonify({"mensaje": "Equipo asignado", "equipo_id": equipo_id, "empleado": emp["name"]})


# --- Sección 3.4: Mantenimiento ---
@app.post("/equipos/<int:equipo_id>/mantenimientos")
def crear_mantenimiento(equipo_id):
    data = request.get_json()
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO maintenance (equipment_id, type, description, cost)
                VALUES (%s, %s, %s, %s)
                RETURNING id, equipment_id, maintenance_date, type AS tipo, description AS descripcion, cost AS costo;
                """,
                (equipo_id, data.get("tipo"), data.get("descripcion"), data.get("costo")),
            )
            mant = cur.fetchone()
            conn.commit()
            return jsonify(mant), 201


# --- Sección 3.5: Historial ---
@app.get("/equipos/<int:equipo_id>/historial")
def historial_equipo(equipo_id):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT e.internal_code, emp.name AS empleado_nombre
                FROM equipment e
                LEFT JOIN employees emp ON e.employee_id = emp.id
                WHERE e.id = %s;
                """,
                (equipo_id,),
            )
            eq = cur.fetchone()
            if not eq:
                return jsonify({"error": "Equipo no encontrado"}), 404

            eventos = []
            if eq["empleado_nombre"]:
                eventos.append({"evento": "Asignación", "detalle": eq["empleado_nombre"]})

            cur.execute(
                "SELECT maintenance_date, type, description FROM maintenance WHERE equipment_id = %s ORDER BY maintenance_date;",
                (equipo_id,),
            )
            for m in cur.fetchall():
                eventos.append({
                    "fecha": str(m["maintenance_date"].date()),
                    "evento": "Mantenimiento",
                    "detalle": m["type"],
                })

            cur.execute(
                "SELECT created_at, file_name, s3_key FROM documents WHERE equipment_id = %s ORDER BY created_at;",
                (equipo_id,),
            )
            for d in cur.fetchall():
                eventos.append({
                    "fecha": str(d["created_at"].date()),
                    "evento": "Documento S3",
                    "detalle": d["s3_key"],
                })

            return jsonify({"equipo": eq["internal_code"], "historial": eventos})


# --- Sección 32: Endpoint para documentos en S3 + metadata en PostgreSQL ---
@app.post("/equipos/<int:equipment_id>/documentos")
def upload_document(equipment_id):
    file = request.files["file"]
    key = f"equipos/{equipment_id}/{file.filename}"

    # 1. Subir archivo físico a Amazon S3
    s3.upload_fileobj(
        file,
        os.environ["S3_BUCKET"],
        key,
    )

    # 2. Guardar metadata en PostgreSQL
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO documents (equipment_id, file_name, s3_key)
                VALUES (%s, %s, %s)
                RETURNING id;
                """,
                (equipment_id, file.filename, key),
            )
            conn.commit()

    return jsonify({
        "equipment_id": equipment_id,
        "s3_key": key,
    }), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)