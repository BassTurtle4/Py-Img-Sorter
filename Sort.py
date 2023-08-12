import os
from PIL import ImageTk, Image
import tkinter as tk
from tkinter import filedialog
import shutil

FOLDERNAME = input("Enter Folder Name to sort into: ")

# Function to delete the current image
def delete_image():
    global image_index, image_list, image_label
    if image_index < len(image_list):
        # Get the path of the image file
        image_path = os.path.join(image_folder, image_list[image_index])
        # Create the "Delete" folder if it doesn't exist
        delete_folder = os.path.join(os.path.dirname(image_folder), FOLDERNAME)
        os.makedirs(delete_folder, exist_ok=True)
        # Move the image file to the "Delete" folder
        destination_path = os.path.join(delete_folder, image_list[image_index])
        shutil.move(image_path, destination_path)
        # Update the image list
        image_list = os.listdir(image_folder)
        # Load the next image
        load_image()

# Function to load and display the current image
def load_image():
    global image_index, image_list, image_label
    if image_index < len(image_list):
        # Load the image using Pillow
        image = Image.open(os.path.join(image_folder, image_list[image_index]))
        # Resize the image to fit the window
        #image = image.resize((400, 400))
        # Create a Tkinter-compatible image object
        tk_image = ImageTk.PhotoImage(image)
        # Update the image label
        image_label.configure(image=tk_image)
        image_label.image = tk_image  # Keep a reference to prevent garbage collection

# Function to handle key events
def handle_key(event):
    global image_index, image_list
    if event.keysym == "Left":
        delete_image()
    elif event.keysym == "Right":
        image_index += 1
        load_image()
    elif event.keysym == "Up":
        window.quit()

# Ask for the image folder using the default dialog
image_folder = filedialog.askdirectory()

if image_folder:
    # Create the main window
    window = tk.Tk()
    window.title("Image Viewer")

    # Create a label for displaying the images
    image_label = tk.Label(window)
    image_label.pack()

    # Bind the key event handler function
    window.bind("<Key>", handle_key)

    # Get a list of all image files in the folder
    image_list = [filename for filename in os.listdir(image_folder) if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp'))]

    # Initialize the image index
    image_index = 0

    # Load and display the first image
    load_image()

    # Start the main loop
    window.mainloop()
