from flask import Flask, request, jsonify
from backend.ping_logic import run_ping
from backend.db import insert_ping, fetch_history

app = Flask(__name__)

@app.route('/ping', methods=['POST'])
def ping():
    host = request.json.get("host")
    output = run_ping(host)
    insert_ping({"host": host, "output": output})
    return jsonify({"output": output})

@app.route('/history', methods=['GET'])
def history():
    return jsonify(fetch_history())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
