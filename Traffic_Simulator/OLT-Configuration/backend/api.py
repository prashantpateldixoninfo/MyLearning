from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/api/data")
def get_data():
    return jsonify({"key": "Hello from the backend!"})


if __name__ == "__main__":
    app.run(debug=True)
