import qrcode
from qrcode.constants import ERROR_CORRECT_H

def generate_qr_code(data, filename):
    # Creating a QR code instance 
    qr = qrcode.QRCode(
            version = 1, 
            error_correction = qrcode.ERROR_CORRECT_H, 
            box_size = 10, 
            border = 4
    )

    # Adding data to the QR code
    qr.add_data(data)
    qr.make(fit = True)

    # Creating an image from the QR Code instance
    img = qr.make_image(fill_color = "blue", back_color = "white")
    
    # Saving the image to a file
    img.save(filename)

    print(f"QR code generated and saved as {filename}")


# if __name__ == "__main__":
#     data = "https://www.google.com"
#     filename = "google_qr.png"
#     generate_qr_code(data, filename)