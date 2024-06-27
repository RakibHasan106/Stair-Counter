# import tkinter as tk

# root = tk.Tk()

# root.geometry("800x500")
# root.title("My First GUI")

# label = tk.Label(root, text = "Hello World", font=('Arial', 18))
# label.pack(padx=20, pady=20)

# textbox = tk.Text(root, )

# root.mainloop()

import tkinter as tk
from tkinter import ttk

from tkinter import filedialog

import os

from tkinter.filedialog import askopenfilename

# Function to be called when button1 is clicked
def on_button1_click():
    file_path = filedialog.askopenfilename(
        title = "Select an Image File",
        initialdir='/',
        filetypes=[("Image Files","*.png *.jpg *.jpeg *.bmp *.svg")]
    )
    
    if file_path:
        print(f"Selected file: {file_path}")
    

# Function to be called when button2 is clicked
def on_button2_click():
    print("Button 2 clicked!")

# Create the main window
root = tk.Tk()
root.title("Simple Interface")
root.geometry("300x200")
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
button1 = ttk.Button(button_frame, text="Button 1", command=on_button1_click)
button2 = ttk.Button(button_frame, text="Button 2", command=on_button2_click)

# Pack the buttons with some space between them
button1.pack(side='left', padx=10)
button2.pack(side='right', padx=10)

# Run the application
root.mainloop()
