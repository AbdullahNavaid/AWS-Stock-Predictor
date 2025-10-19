from flask import Flask, jsonify, send_from_directory
from lambda_package.lambda_functions import lambda_handler
import os

app = Flask(__name__, static_folder="frontend")

# API route to sample Lambda
@app.route("/api/stocks")
def get_stocks():
    event = {"httpMethod": "GET"}
    response = lambda_handler(event, None)
    return jsonify(response)

# Serve frontend HTML files
@app.route("/")
def serve_start():
    return send_from_directory(app.static_folder, "start.html")

@app.route("/index.html")
def serve_index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/results.html")
def serve_results():
    return send_from_directory(app.static_folder, "results.html")

# Serve other static assets if you add JS/CSS/images
@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory(app.static_folder, path)

if __name__ == "__main__":
    app.run(debug=True)
