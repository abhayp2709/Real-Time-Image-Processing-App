import cv2
import tkinter as tk
from tkinter import filedialog, Label, Button, StringVar
from PIL import Image, ImageTk

# Function to apply filters to the image
def apply_filter(img, filter_type):
    if filter_type == "Grayscale":
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    elif filter_type == "Blur":
        return cv2.GaussianBlur(img, (15, 15), 0)
    elif filter_type == "Edge Detection":
        return cv2.Canny(img, 100, 200)
    elif filter_type == "Pencil Sketch":
        gray, sketch = cv2.pencilSketch(img, sigma_s=60, sigma_r=0.07, shade_factor=0.05)
        return sketch
    else:
        return img

# Function to display the processed image in the GUI
def display_image(image):
    # Convert BGR (OpenCV format) to RGB
    if len(image.shape) == 2:  # Grayscale image
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    else:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    image = Image.fromarray(image)
    imgtk = ImageTk.PhotoImage(image=image)
    display_label.imgtk = imgtk
    display_label.configure(image=imgtk)

# Function to open and process the selected image
def open_file():
    global original_image, processed_image
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png;*.jpeg")])
    if not file_path:
        return

    # Load and display the original image
    original_image = cv2.imread(file_path)
    processed_image = original_image.copy()
    display_image(original_image)

# Function to apply the selected filter
def apply_selected_filter():
    global processed_image
    if original_image is None:
        print("Please select an image first.")
        return

    filter_type = selected_filter.get()
    processed_image = apply_filter(original_image, filter_type)
    display_image(processed_image)

# Function to save the processed image
def save_image():
    if processed_image is None:
        print("No image to save.")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png")])
    if file_path:
        cv2.imwrite(file_path, processed_image)
        print(f"Image saved to {file_path}")

# Initialize Tkinter window
app = tk.Tk()
app.title("Image Processing App")

# Add dropdown for filter selection
Label(app, text="Select a filter:", font=("Arial", 12)).pack(pady=5)

selected_filter = StringVar(value="Grayscale")
filters = ["Grayscale", "Blur", "Edge Detection", "Pencil Sketch"]
dropdown = tk.OptionMenu(app, selected_filter, *filters)
dropdown.pack(pady=10)

# Add other buttons and widgets
Button(app, text="Open Image", command=open_file).pack(pady=5)
Button(app, text="Apply Filter", command=apply_selected_filter).pack(pady=5)
Button(app, text="Save Image", command=save_image).pack(pady=5)

# Run the application
app.mainloop()
