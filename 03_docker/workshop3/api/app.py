import os
from flask import Flask, jsonify, request
import psycopg

app = Flask(__name__)

INSTANCE = os.getenv("INSTANCE", "api-local")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "shop")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")


def get_connection():
    return psycopg.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )


@app.get("/products")
def get_products():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id, name, price FROM products ORDER BY id"
            )
            rows = cursor.fetchall()

    products = [
        {
            "id": row[0],
            "name": row[1],
            "price": float(row[2])
        }
        for row in rows
    ]

    return jsonify({
        "served_by": INSTANCE,
        "products": products
    })

@app.get("/products/<int:product_id>")
def get_product(product_id):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id, name, price FROM products WHERE id = %s",
                (product_id,)
            )
            row = cursor.fetchone()

    if row is None:
        return jsonify({
            "error": "Producto no encontrado"
        }), 404

    return jsonify({
        "served_by": INSTANCE,
        "product": {
            "id": row[0],
            "name": row[1],
            "price": float(row[2])
        }
    })

@app.post("/products")
def create_product():
    data = request.get_json()

    if not data or "name" not in data or "price" not in data:
        return jsonify({
            "error": "name y price son obligatorios"
        }), 400

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO products (name, price)
                VALUES (%s, %s)
                RETURNING id, name, price
                """,
                (data["name"], data["price"])
            )
            row = cursor.fetchone()

    return jsonify({
        "served_by": INSTANCE,
        "product": {
            "id": row[0],
            "name": row[1],
            "price": float(row[2])
        }
    }), 201

@app.put("/products/<int:product_id>")
def update_product(product_id):
    data = request.get_json()

    if not data or "name" not in data or "price" not in data:
        return jsonify({
            "error": "name y price son obligatorios"
        }), 400

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE products
                SET name = %s, price = %s
                WHERE id = %s
                RETURNING id, name, price
                """,
                (data["name"], data["price"], product_id)
            )
            row = cursor.fetchone()

    if row is None:
        return jsonify({
            "error": "Producto no encontrado"
        }), 404

    return jsonify({
        "served_by": INSTANCE,
        "product": {
            "id": row[0],
            "name": row[1],
            "price": float(row[2])
        }
    })

@app.delete("/products/<int:product_id>")
def delete_product(product_id):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM products
                WHERE id = %s
                RETURNING id, name, price
                """,
                (product_id,)
            )
            row = cursor.fetchone()

    if row is None:
        return jsonify({
            "error": "Producto no encontrado"
        }), 404

    return jsonify({
        "served_by": INSTANCE,
        "deleted": {
            "id": row[0],
            "name": row[1],
            "price": float(row[2])
        }
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)