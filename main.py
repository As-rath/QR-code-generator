import qrcode
from qrcode.constants import ERROR_CORRECT_H
from PIL import Image, ImageDraw, ImageTk
import tkinter as tk
from tkinter import filedialog, messagebox

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

def browseFile():
    path = filedialog.askopenfilename(
        title = "Select Logo Image",
        filetypes = [("Image Files", "*.png;*.jpg;*.jpeg;*.webp;*.bmp;*.gif"), ("All Files", "*.*")]
    )
    logo_entry.delete(0, tk.END)
    logo_entry.insert(0, path)

# def browseSaveLocation():
#     path = filedialog.asksaveasfilename(
#         defaultextension = ".png",
#         filetypes = [("PNG Image", "*.png"), ("All Files", "*.*")],
#         title = "Save QR Code As"
#     )
#     save_entry.delete(0, tk.END)
#     save_entry.insert(0, path)

def onGenerate():
    print("Generating QR code...")
    global current_qr

    data = data_entry.get()
    logo_path = logo_entry.get()

    if not data or not logo_path:
        messagebox.showerror("Error", "Please fill in all fields.")
        return
    
    try:
        img = generateQrCode(data, logo_path)
        current_qr = img
        preview = img.resize((200, 200), Image.LANCZOS)
        tk_img = ImageTk.PhotoImage(preview)
        preview_label.config(image = tk_img)
        preview_label.image = tk_img  # Keep a reference to avoid garbage collection

    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate QR code: {e}")


def saveQrCode():

    if current_qr is None:
        messagebox.showerror("Error", "No QR code to save.")
        return

    save_path = filedialog.asksaveasfilename(
        defaultextension= ".png", 
        filetypes=[("PNG Image", "*.png"), ("All Files", "*.*")], 
        title="Save QR Code As"
        )
    
    if save_path:
        current_qr.save(save_path)
        messagebox.showinfo("Success", f"QR code saved as {save_path}")

#Creating the main window (GUI)
root = tk.Tk()
root.title("QR Code Generator")
root.geometry("800x600")
root.resizable(True, True)

#Data input
data_frame = tk.Frame(root)
data_frame.pack(pady = (20, 5))
tk.Label(data_frame, text="Data/URL:").pack(pady = (20, 5))
data_entry = tk.Entry(data_frame, width = 50)
data_entry.pack()

#Logo input
logo_frame = tk.Frame(root)
logo_frame.pack(pady = (20, 5))
tk.Label(logo_frame, text="Logo Image:").pack(pady = (20, 5))
logo_entry = tk.Entry(logo_frame, width = 50)
logo_entry.pack()
tk.Button(logo_frame, text="Browse", command = browseFile).pack(pady = (10, 0), side = tk.LEFT)

#Save location input
# save_frame = tk.Frame(root)
# save_frame.pack(pady = (20, 5))
# tk.Label(save_frame, text = "Save QR Code as: ").pack(pady = (10, 5))
# save_entry = tk.Entry(save_frame, width = 50)
# save_entry.pack()
# tk.Button(save_frame, text = "Save As", command = browseSaveLocation).pack(pady = (10, 0), side = tk.LEFT)


#Generate Button
tk.Button(root, text = "Generate QR Code", command = onGenerate , bg = "#000000", fg = "white", width = 20).pack(pady = 20)

#Preview of the generated QR
preview_frame = tk.Frame(root)
preview_frame.pack(pady = 10)
preview_label = tk.Label(preview_frame, text = "QR Code Preview will appear here")
preview_label.pack(pady = (10, 5))

#Save Button
tk.Button(root, text = "Save QR Code", command = saveQrCode , bg = "#000000", fg = "white", width = 20).pack(pady = 10)

root.mainloop()
