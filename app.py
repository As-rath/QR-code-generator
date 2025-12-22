from main import * 
from flask import Flask, render_template, request, send_file
import os
import uuid

app = Flask(__name__)

OUTPUT_DIR = "QR-code-generator/static/outputs"
os.makedirs(OUTPUT_DIR, exist_ok = True)

@app.route("/", methods = ["GET", "POST"])
def index():
    qr_image_URL = None

    if request.method == "POST":
        data = request.form["data"]
        logo = request.files["logo"]

        #Save Uploaded Logo
        logo_filename = f"{uuid.uuid4()}_{logo.filename}"
        logo_path = os.path.join(OUTPUT_DIR, logo_filename)
        logo.save(logo_path)

        #Generate QR Code
        img = generateQrCode(data, logo_path)

        #Save QR Code Image
        qr_filename = f"{uuid.uuid4()}.png"
        output_path = os.path.join(OUTPUT_DIR, qr_filename)
        img.save(output_path)

        #URL for browser 
        qr_image_URL = f"/{output_path}"
        
    
    return render_template("index.html", qr_image_URL = qr_image_URL)

if __name__ == "__main__":
    app.run(debug = True)