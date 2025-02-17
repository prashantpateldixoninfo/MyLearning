from flask import Flask, request, jsonify

app = Flask(__name__)


# Shared data store
shared_data = {}


@app.route("/submit", methods=["POST"])
def submit_data():
    data = request.json
    shared_data["input"] = data.get("input")
    print(f"Received data: {shared_data['input']}")
    return jsonify({"status": "success", "received": shared_data["input"]}), 200


@app.route("/get_data", methods=["GET"])
def get_data():
    if "input" in shared_data:
        print(f"Sending data: {shared_data['input']}")
        return jsonify({"data": shared_data["input"]}), 200
    return jsonify({"status": "error", "message": "No data available"}), 404


if __name__ == "__main__":
    app.run(port=5000)
