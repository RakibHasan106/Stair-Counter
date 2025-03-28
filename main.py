import threading
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
from matplotlib import pyplot as plt
from PIL import Image, ImageTk
import os
import cv2 
from LineDetection import *
from EdgeDetection import *

def show_loading_screen():
    loading_screen = tk.Toplevel(root)
    loading_screen.title("Processing...")
    loading_screen.geometry("300x100")
    loading_label = ttk.Label(loading_screen, text="Processing image, please wait...")
    loading_label.pack(expand=True)
    return loading_screen

def close_loading_screen(loading_screen):
    loading_screen.destroy()

def process_image(file_path, loading_screen):

    img = cv2.imread(file_path)
    if img.shape[0] > 1000 or img.shape[1] > 1000:
        img = cv2.resize(img, (0, 0), fx=0.3, fy=0.3)

    pil_img = Image.fromarray(img)
    img_tk = ImageTk.PhotoImage(pil_img)

    # Display the original image
    root.after(0, lambda: display_image(img_tk, img, "Input Image"))

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    pil_img = Image.fromarray(img)
    img_tk = ImageTk.PhotoImage(pil_img)

    root.after(0, lambda: display_image(img_tk, img, "GrayScale Image"))
    
    EdgeDetector = EdgeDetection(img, sigma=.7, kernelSize=5)
    edged = EdgeDetector.CannyEdgeDetector()

    edged_pil_image = Image.fromarray(edged)
    edged_img_tk = ImageTk.PhotoImage(edged_pil_image)

    # Display the edge-detected image
    root.after(0, lambda: display_image(edged_img_tk, edged, "Edge Detected"))

    LineDetector = LineDetection(edged)
    output, line_number = LineDetector.lineDetection(file_path)

    output_pil_image = Image.fromarray(output)
    output_img_tk = ImageTk.PhotoImage(output_pil_image)

    # Display the line-detected image
    root.after(0, lambda: display_image(output_img_tk, output, "Line Detected"))

    # Close the loading screen
    root.after(0, lambda: close_loading_screen(loading_screen))

def display_image(img_tk, img, title):
    image_viewer = tk.Toplevel(root)
    image_viewer.title(title)
    image_viewer.geometry(f"{img.shape[1]+100}x{img.shape[0]+100}")
    img_label = ttk.Label(image_viewer, image=img_tk)
    img_label.image = img_tk  # Prevent garbage collection
    img_label.pack(padx=10, pady=10)


def on_button1_click():
    file_path = filedialog.askopenfilename(
        title="Select an Image File",
        initialdir='D:/Study/4-1/Lab/Image Lab/Project/Stair-Counter',
        filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp *.svg")]
    )

    if file_path:
        loading_screen = show_loading_screen()

        # Start a new thread for image processing
        threading.Thread(target=process_image, args=(file_path, loading_screen)).start()

def on_button2_click():
    print("Button 2 clicked!")

root = tk.Tk()
root.title("Stair Counter")
root.geometry("500x400")
root.configure(bg='white')

# Define a style for the buttons
style = ttk.Style()
style.configure('TButton', font=('Helvetica', 12), padding=10)
style.map('TButton', foreground=[('pressed', 'red'), ('active', 'blue')],
          background=[('pressed', '!disabled', 'yellow'), ('active', 'white')])

# Add padding around the buttons
button_frame = tk.Frame(root, bg='white')
button_frame.pack(pady=20, padx=20, expand=True)

button1 = ttk.Button(button_frame, text="Choose Image", command=on_button1_click)


button1.pack(side='left', padx=10)

root.mainloop()
