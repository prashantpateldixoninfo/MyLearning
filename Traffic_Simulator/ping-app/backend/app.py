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

@app.route('/history', methods=['POST'])
def history():
    data = request.get_json() or {}
    host = data.get("host")
    query = {"host": host} if host else {}
    return jsonify(fetch_history(query))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
