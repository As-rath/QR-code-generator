import qrcode
from qrcode.constants import ERROR_CORRECT_H
from PIL import Image, ImageDraw
import tkinter as tk
from tkinter import filedialog, messagebox


def generateQrCode(data, save_path, logo_path):
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
    img.save(save_path)

    print(f"QR code generated and saved as {save_path}")

def browseFile():
    path = filedialog.askopenfilename(
        title = "Select Logo Image",
        filetypes = [("Image Files", "*.png;*.jpg;*.jpeg;*.webp;*.bmp;*.gif"), ("All Files", "*.*")]
    )
    logo_entry.delete(0, tk.END)
    logo_entry.insert(0, path)

def browseSaveLocation():
    path = filedialog.asksaveasfilename(
        defaultextension = ".png",
        filetypes = [("PNG Image", "*.png"), ("All Files", "*.*")],
        title = "Save QR Code As"
    )
    save_entry.delete(0, tk.END)
    save_entry.insert(0, path)

def onGenerate():
    data = data_entry.get()
    logo_path = logo_entry.get()
    save_path = save_entry.get()

    if not data or not logo_path or not save_path:
        messagebox.showerror("Error", "Please fill in all fields.")
        return
    
    try:
        generateQrCode(data, save_path, logo_path)
        messagebox.showinfo("Success", f"QR code generated and saved as {save_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate QR code: {e}")


#Creating the main window (GUI)
root = tk.Tk()
root.title("QR Code Generator")
root.geometry("420x420")
root.resizable(False, False)

#Data input
tk.Label(root, text="Data/URL:").pack(pady = (20, 5))
data_entry = tk.Entry(root, width = 50)
data_entry.pack()

#Logo input
tk.Label(root, text="Logo Image:").pack(pady = (20, 5))
logo_entry = tk.Entry(root, width = 50)
logo_entry.pack()
tk.Button(root, text="Browse", command = browseFile).pack(side = tk.LEFT)

#Save location input
tk.Label(root, text = "Save QR Code as: ").pack(pady = (20, 5))
save_entry = tk.Entry(root, width = 50)
save_entry.pack()
tk.Button(root, text = "Save As", command = browseSaveLocation).pack(side = tk.LEFT)

#Generate Button
tk.Button(root, text = "Generate QR Code", command = onGenerate , bg = "#000000", fg = "white", width = 20).pack(pady = 20)

root.mainloop()
