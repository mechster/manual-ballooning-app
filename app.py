import os
import json
from flask import Flask, render_template, request, jsonify, send_file
from pdf2image import convert_from_path
from PIL import Image

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
RENDER_FOLDER = os.path.join(BASE_DIR, "static", "rendered")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RENDER_FOLDER, exist_ok=True)

POPPLER_PATH = r"C:\poppler\Library\bin"

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload_pdf", methods=["POST"])
def upload_pdf():
    file = request.files["file"]
    pdf_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(pdf_path)

    images = convert_from_path(
        pdf_path,
        dpi=200,
        poppler_path=POPPLER_PATH
    )

    img_path = os.path.join(RENDER_FOLDER, "page1.png")
    images[0].save(img_path, "PNG")

    return jsonify({"image_url": "/static/rendered/page1.png"})


@app.route("/save_balloons", methods=["POST"])
def save_balloons():
    with open("exports/balloons.json", "w") as f:
        json.dump(request.json, f)
    return jsonify({"status": "saved"})


if __name__ == "__main__":
    app.run(debug=True)
