import os
import socket
from datetime import datetime
from flask import Flask, jsonify

app = Flask(__name__)

@app.get("/")
def home():
    return jsonify({
        "message": "Hola desde EC2 con Docker y Nginx",
        "container_hostname": socket.gethostname(),
        "ec2_hostname": os.environ.get("EC2_HOSTNAME", "ip-172-31-26-92"),
        "current_time": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    })

@app.get("/health")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
