from main import * 
from flask import Flask, render_template, request, send_file
import os

app = Flask(__name__)

OUTPUT_DIR = "static/outputs"
os.makedirs(OUTPUT_DIR, exist_ok = True)

@app.route("/", methods = ["GET", "POST"])
def index():
    if request.method == "POST":
        data = request.form["data"]
        logo = request.files["logo"]

        logo_path = os.path.join(OUTPUT_DIR, logo.filename)
        logo.save(logo_path)

        img = generateQrCode(data, logo_path)

        output_path = os.path.join(OUTPUT_DIR, "qr_code.png")
        img.save(output_path)
        
        return send_file(output_path, as_attachment = True)
    
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug = True)