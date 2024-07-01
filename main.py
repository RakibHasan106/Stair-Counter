import tkinter as tk
from tkinter import ttk

from tkinter import filedialog
from tkinter import messagebox

from matplotlib import pyplot as plt

from PIL import Image, ImageTk

import os

from tkinter.filedialog import askopenfilename

from LineDetection import *
from EdgeDetection import *


# Function to be called when button1 is clicked
def on_button1_click():
    file_path = filedialog.askopenfilename(
        title="Select an Image File",
        initialdir='D:/Study/4-1/Lab/Image Lab/Project/Stair-Counter',
        filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp *.svg")]
    )

    if file_path:
        # image_path = file_path
        # img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        # plt.imshow(img)
        # print(img)

        # print(file_path)
        # root.withdraw()
        
        img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
        print(img)

        if img.shape[0] > 1000 or img.shape[1] > 1000:
            img = cv2.resize(img, (0, 0), fx=0.3, fy=0.3)

        pil_img = Image.fromarray(img)
        
        img_tk = ImageTk.PhotoImage(pil_img) # Creating a ImageTk from a pil_image which is compatible with tkinter
        
        image_viewer = tk.Toplevel(root)
        image_viewer.title("Input Image")
        
        image_viewer.geometry(f"{img.shape[0]+100}x{img.shape[1]+100}")
                

        img_label = ttk.Label(image_viewer, image=img_tk)
        img_label.image = img_tk
        img_label.pack(padx=10, pady=10)
                
        
        EdgeDetector = EdgeDetection(img,sigma=.7,kernelSize=5)
        
        edged = EdgeDetector.CannyEdgeDetector()
        
        edged_pil_image = Image.fromarray(edged)
        edged_img_tk = ImageTk.PhotoImage(edged_pil_image)
        
        edged_viewer = tk.Toplevel(root)
        edged_viewer.title("Edge Detected")
        
        edged_viewer.geometry(f"{edged.shape[0]+100}x{edged.shape[1]+100}")
        
        edged_label = ttk.Label(edged_viewer, image=edged_img_tk)
        edged_label.image = edged_img_tk
        edged_label.pack(padx=10, pady=10)
        
        # edges = np.where(edged>0)
        
        LineDetector = LineDetection(edged)
        
        output,line_number = LineDetector.lineDetection(file_path)
        
        output_pil_image = Image.fromarray(output)
        output_img_tk = ImageTk.PhotoImage(output_pil_image)
        
        output_viewer = tk.Toplevel(root)
        output_viewer.title("Line Detected")
        
        output_viewer.geometry(f"{output.shape[0]+100}x{output.shape[1]+100}")
        
        output_label = ttk.Label(output_viewer, image=output_img_tk)
        output_label.image = output_img_tk
        output_label.pack(padx=10,pady=10)
        
        # messagebox.showinfo("Information", f"Number of steps Detected = {line_number}")
        

# Function to be called when button2 is clicked
def on_button2_click():
    print("Button 2 clicked!")


# Create the main window
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

# Create two buttons and attach functions to them
button1 = ttk.Button(button_frame, text="Open Image", command=on_button1_click)
button2 = ttk.Button(button_frame, text="Button 2", command=on_button2_click)

# Pack the buttons with some space between them
button1.pack(side='left', padx=10)
button2.pack(side='right', padx=10)

# Run the application
root.mainloop()
