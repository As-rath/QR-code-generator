import qrcode
from qrcode.constants import ERROR_CORRECT_H
from PIL import Image, ImageDraw


current_qr = None  

def generateQrCode(data, logo_path):
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
    img = qr.make_image(fill_color = "black", back_color = "white").convert("RGBA")

    #Opening the logo image
    logo = Image.open(logo_path).convert("RGBA")

    #Resizing the logo
    qr_width, qr_height = img.size
    logo_size = qr_width // 5
    logo = logo.resize((logo_size, logo_size), Image.LANCZOS)

    #Buffer 
    padding = 12
    bg_size = logo_size + padding*2 

    #Creating a background for the logo
    logo_bg = Image.new("RGBA", (bg_size, bg_size), (255, 255, 255, 255))
    mask = Image.new("L", (bg_size, bg_size), 0)

    #Drawing a rounded rectangle as mask
    draw = ImageDraw.Draw(mask)
    radius = bg_size // 6
    draw.rounded_rectangle((0, 0, bg_size, bg_size), radius, fill=255)

    logo_bg.putalpha(mask)  

    #Calculating the position to paste the logo
    bg_pos = ((qr_width - logo_size) //2, (qr_height - logo_size) //2)
    logo_pos = (bg_pos[0] + padding, bg_pos[1] + padding)

    #Pasting the logo onto the QR code
    img.paste(logo_bg, bg_pos, logo_bg)
    img.paste(logo, logo_pos, logo)
    
    # Saving the image to a file
    return img

