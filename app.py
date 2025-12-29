from main import * 
from flask import Flask, render_template, request, send_file, jsonify
import os
import uuid

app = Flask(__name__)

OUTPUT_DIR = "QR-code-generator/static/outputs"
os.makedirs(OUTPUT_DIR, exist_ok = True)

UPLOAD_DIR = "QR-code-generator/static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok = True)



@app.route("/", methods = ["GET", "POST"])
def index():
    # qr_image_URL = None

    # print("REQUEST METHOD:", request.method)

    # if request.method == "POST":
    #     print("POST RECIEVED.")

    #     data = request.form["data"]
    #     logo = request.files["logo"]

    #     print("DATA:", data)
    #     print("LOGO:", logo)

    #     if not data or not logo:
    #         print("MISSING DATA OR LOGO.")

    #     #Save Uploaded Logo
    #     logo_filename = f"{uuid.uuid4()}_{logo.filename}"
    #     logo_path = os.path.join(OUTPUT_DIR, logo_filename)
    #     logo.save(logo_path)

    #     #Generate QR Code
    #     try:
    #         img = generateQrCode(data, logo_path)
    #         print("QR CODE GENERATED.")

    #     except Exception as e:
    #         print("ERROR GENERATING QR CODE:", str(e))
    #         return "QR generation failed."

    #     #Save QR Code Image
    #     qr_filename = f"{uuid.uuid4()}.png"
    #     output_path = os.path.join(OUTPUT_DIR, qr_filename)
    #     img.save(output_path)

    #     #URL for browser 
    #     qr_image_URL = f"/{output_path}"        
    
    return render_template("index.html")

# @app.route("/generate", methods = ["POST"])
# def generate():
#     data = request.form.get("data")
#     logo = request.files.get("logo")

#     if not data or not logo:
#         return jsonify({"error": "Missing Data"}), 400
    
#     logo_path = os.path.join(OUTPUT_DIR, logo.filename)
#     logo.save(logo_path)

#     img = generateQrCode(data, logo_path)

#     qr_filename = f"{uuid.uuid4()}.png"
#     output_path = os.path.join(OUTPUT_DIR, qr_filename)
#     img.save(output_path)

#     return jsonify({
#         "qr_url": f"/static/outputs/{qr_filename}"
#     })

@app.route("/api/generate", methods = ["POST"])
def api_generate():
    try:
        data = request.form.get("data")
        logo = request.files.get("logo")

        if not data:
            return jsonify({
                "success": False,
                "error": "Missing Data"
            }), 400
        
        logo_path = None
        if logo:
            logo_filename = f"{uuid.uuid4()}_{logo.filename}"
            logo_path = os.path.join(UPLOAD_DIR, logo_filename)
            logo.save(logo_path)

        img = generateQrCode(data, logo_path)

        qr_filename = f"{uuid.uuid4()}.png"
        qr_path = os.path.join(OUTPUT_DIR, qr_filename)
        img.save(qr_path)

        return jsonify({
            "success": True,
            "qr_url": f"/static/outputs/{qr_filename}"
        })
    except Exception as e: 
        print("API ERROR", e)
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

if __name__ == "__main__":
    app.run(debug = True)