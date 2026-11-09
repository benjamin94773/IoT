import os
from flask import Flask, jsonify

app = Flask(__name__)
INSTANCE = os.getenv("INSTANCE", "orders-local")

@app.get("/")
def home():
    return jsonify({
        "service": "orders",
        "message": "Servicio de pedidos",
        "instance": INSTANCE
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)