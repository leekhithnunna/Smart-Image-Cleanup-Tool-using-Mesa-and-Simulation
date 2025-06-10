import os
import cv2
import tkinter as tk
from tkinter import filedialog, messagebox, Listbox, Scrollbar, simpledialog, Label
import Duplicates as dupi
import lowQuality
from captureFace import *
from compare_face import *
from OldImages import *
import re
import customtkinter as ctk
from PIL import Image, ImageTk
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'Mesa'))  # Add Mesa folder to path
from gui import SmartImageCleanupGUI  # Import MESA GUI

# Function to animate the title
def animate_title():
    colors = ["#FF5733", "#33FF57", "#3357FF", "#F1C40F", "#E74C3C", "#8E44AD"]
    current_color = title_label.cget("fg")
    next_color = colors[(colors.index(current_color) + 1) % len(colors)]
    title_label.config(fg=next_color)
    root.after(500, animate_title)  # Change color every 500ms

# Function to toggle dark mode
def toggle_dark_mode():
    if dark_mode_var.get():
        root.config(bg="#121212")
        frame.config(bg="#121212")
        selected_folder_label.config(bg="#121212", fg="white")
        listbox.config(bg="#1e1e1e", fg="white")
        scrollbar.config(bg="#121212")
    else:
        root.config(bg="white")
        frame.config(bg="white")
        selected_folder_label.config(bg="white", fg="black")
        listbox.config(bg="white", fg="black")
        scrollbar.config(bg="white")

# Function to remove duplicate images
def remove_duplicates(folder_path):
    listbox.delete(0, tk.END)
    if not folder_path or folder_path == "Selected Folder: None":
        messagebox.showerror("Error", "Please select a folder first.")
        return
    duplicates = dupi.find_duplicates(folder_path)
    for d in duplicates:
        path = d
        match = re.search(r'[^\\]+$', path)
        if match:
            listbox.insert(tk.END, match.group(0))
    dupi.Duplicates_remover(folder_path)
    messagebox.showinfo("Info", "Duplicate images processed.")

# Function to remove blurry images
def Remove_blurry_images(folder_path, threshold=100):
    listbox.delete(0, tk.END)
    if not folder_path or folder_path == "Selected Folder: None":
        messagebox.showerror("Error", "Please select a folder first.")
        return
    img, a = lowQuality.remove_blurry_images_with_mesa(folder_path)
    for d in img:
        path = d
        match = re.search(r'[^\\]+$', path)
        if match:
            listbox.insert(tk.END, match.group(0))
    if a:
        messagebox.showinfo("Info", "Low quality images are removed successfully!")
    else:
        messagebox.showinfo("Info", "No low quality images")

# Function to remove images before a certain time
def remove_old_images(folder_path):
    if not folder_path or folder_path == "Selected Folder: None":
        messagebox.showerror("Error", "Please select a folder first.")
        return
    cutoff_time = simpledialog.askstring("Input", "Enter cutoff time (YYYY-MM-DD HH:MM:SS):")
    if cutoff_time:
        try:
            delete_old_images_with_mesa(folder_path, cutoff_time)
            messagebox.showinfo("Info", "Outdated images removed successfully!")
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD HH:MM:SS.")

# Open folder dialog and run compare function
def select_folder_and_compare():
    folder_path = filedialog.askdirectory()
    if folder_path:
        compare_faces_with_mesa(folder_path=folder_path, captured_image="captured_frame.jpg")

# Function to manage face capture and comparison
def face_management():
    face_window = tk.Toplevel(root)
    face_window.geometry("400x400")
    face_window.title("Face Capture and Compare")
    
    # Frame for layout consistency
    frame = ctk.CTkFrame(face_window, corner_radius=15)
    frame.pack(pady=20, padx=20, fill="both", expand=True)

    def capture_image_and_display():
        capture_face_with_mesa("captured_frame.jpg")
        if os.path.exists("captured_frame.jpg"):
            image = Image.open("captured_frame.jpg")
            image.thumbnail((200, 200))
            img = ImageTk.PhotoImage(image)
            image_label.config(image=img)
            image_label.image = img

    # Capture button
    capture_button = ctk.CTkButton(
        frame, 
        text="Capture Image", 
        command=capture_image_and_display,
        fg_color="green",
        text_color="white",
        hover_color="darkgreen"
    )
    capture_button.pack(pady=10)

    # Image display label
    image_label = tk.Label(frame)
    image_label.pack(pady=10)

    # Compare button
    compare_button = ctk.CTkButton(
        frame, 
        text="Compare Images", 
        command=select_folder_and_compare,
        fg_color="blue",
        text_color="white",
        hover_color="darkblue"
    )
    compare_button.pack(pady=10)

# Function to select folder and enable_buttons()
def select_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        selected_folder_label.config(text=folder_path)
        enable_buttons()

# Enable action buttons after folder selection
def enable_buttons():
    remove_duplicates_button.config(state="normal")
    remove_blurry_button.config(state="normal")
    remove_old_button.config(state="normal")
    mesa_button.config(state="normal")
    face_management_button.config(state="normal")

# Disable action buttons initially
def disable_buttons():
    remove_duplicates_button.config(state="disabled")
    remove_blurry_button.config(state="disabled")
    remove_old_button.config(state="disabled")
    mesa_button.config(state="disabled")
    face_management_button.config(state="disabled")

# Function to run MESA simulation GUI
def run_mesa_simulation_gui():
    folder_path = selected_folder_label.cget("text")
    if not folder_path or folder_path == "Selected Folder: None":
        messagebox.showerror("Error", "Please select a folder first.")
        return
    # Create new customtkinter root for MESA GUI
    mesa_root = ctk.CTk()
    # Initialize MESA GUI with selected folder
    gui = SmartImageCleanupGUI(mesa_root, folder_path=folder_path)
    # Update folder label in MESA GUI
    gui.folder_label.configure(text=f"Image Folder: {folder_path}")
    gui.run_button.configure(state="normal")
    mesa_root.mainloop()

# GUI Setup
root = tk.Tk()
root.title("Smart Image Cleanup Tool")
root.geometry("600x700")
root.config(bg="white")

# Dark mode variable
dark_mode_var = tk.BooleanVar()

# Title label with animation
title_label = tk.Label(root, text="Smart Image Cleanup Tool", font=("Arial", 18, "bold"), fg="#FF5733", bg="white")
title_label.pack(pady=20)
animate_title()

# Frame for folder selection
folder_frame = tk.Frame(root, padx=20, pady=10, bg="white")
folder_frame.pack(pady=10)

# Select folder button
select_folder_button = tk.Button(
    folder_frame, 
    text="Select Folder",
    command=select_folder,
    bg="#3F51B5", fg="white", relief="raised",
    activebackground="#3949AB"
)
select_folder_button.pack(pady=5)

# Selected folder label
selected_folder_label = tk.Label(folder_frame, text="Selected Folder: None", wraplength=400, bg="white", fg="black")
selected_folder_label.pack(pady=10)

# Frame for action buttons
frame = tk.Frame(root, padx=20, pady=20, bg="white")
frame.pack(pady=20)

# Remove duplicates button
remove_duplicates_button = tk.Button(
    frame, 
    text="Remove Duplicates",
    command=lambda: remove_duplicates(selected_folder_label.cget("text")),
    bg="#4CAF50", fg="white", relief="raised",
    activebackground="#45a049",
    state="disabled"
)
remove_duplicates_button.pack(pady=5)

# Remove blurry images button
remove_blurry_button = tk.Button(
    frame, 
    text="Remove Blurry Images",
    command=lambda: Remove_blurry_images(selected_folder_label.cget("text")),
    bg="#2196F3", fg="white", relief="raised",
    activebackground="#1e88e5",
    state="disabled"
)
remove_blurry_button.pack(pady=5)

# Remove old images button
remove_old_button = tk.Button(
    frame, 
    text="Remove Old Images",
    command=lambda: remove_old_images(selected_folder_label.cget("text")),
    bg="#FF5722", fg="white", relief="raised",
    activebackground="#e64a19",
    state="disabled"
)
remove_old_button.pack(pady=5)

# MESA simulation button
mesa_button = tk.Button(
    frame, 
    text="Run MESA Simulation",
    command=run_mesa_simulation_gui,
    bg="#FFC107", fg="black", relief="raised",
    activebackground="#FFB300",
    state="disabled"
)
mesa_button.pack(pady=5)

# Face Management button
face_management_button = tk.Button(
    frame, 
    text="Face Management",
    command=face_management,
    bg="#9C27B0", fg="white", relief="raised",
    activebackground="#8e24aa",
    state="disabled"
)
face_management_button.pack(pady=10)

# Dark mode toggle button
dark_mode_toggle = tk.Checkbutton(
    root, 
    text="Dark Mode",
    variable=dark_mode_var,
    onvalue=True,
    offvalue=False,
    command=toggle_dark_mode,
    bg="#e0e0e0",
    fg="black",
    activebackground="#c0c0c0"
)
dark_mode_toggle.pack(pady=10)

# Scrollable Listbox
listbox_frame = tk.Frame(root)
listbox_frame.pack(fill=tk.BOTH, expand=True)

scrollbar = Scrollbar(listbox_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

listbox = Listbox(listbox_frame, yscrollcommand=scrollbar.set, width=50, height=10)
listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar.config(command=listbox.yview)

# Disable action buttons initially
disable_buttons()

# Start the GUI loop
root.mainloop()