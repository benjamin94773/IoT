import os
from flask import Flask, jsonify

app = Flask(__name__)
INSTANCE = os.getenv("INSTANCE", "api-local")

@app.get("/")
def home():
    return jsonify({
        "message": "Hola desde Flask",
        "instance": INSTANCE
    })

@app.get("/health")
def health():
    return jsonify({
        "status": "ok",
        "instance": INSTANCE
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)