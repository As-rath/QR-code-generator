import qrcode
from qrcode.constants import ERROR_CORRECT_H
from PIL import Image

def generate_qr_code(data, filename):
    # Creating a QR code instance 
    qr = qrcode.QRCode(
            version = 1, 
            error_correction = qrcode.constants.ERROR_CORRECT_H, 
            box_size = 10, 
            border = 4
    )

    # Adding data to the QR code
    qr.add_data(data)
    qr.make(fit = True)

    # Creating an image from the QR Code instance
    img = qr.make_image(fill_color = "blue", back_color = "white").convert("RGBA")

    #Opening the logo image
    logo_path = input("Enter the path to the logo image (e.g., logo.webp): ")
    logo = Image.open(logo_path).convert("RGBA")

    #Resizing the logo
    qr_width, qr_height = img.size
    logo_size = qr_width // 5
    logo = logo.resize((logo_size, logo_size), Image.LANCZOS)

    #Calculating the position to paste the logo
    logo_pos = ((qr_width - logo_size) //2, (qr_height - logo_size) //2)

    #Pasting the logo onto the QR code
    img.paste(logo, logo_pos, logo)
    
    # Saving the image to a file
    img.save(filename)

    print(f"QR code generated and saved as {filename}")


if __name__ == "__main__":
    data = "https://www.google.com"
    filename = "google_qr.png"
    generate_qr_code(data, filename)