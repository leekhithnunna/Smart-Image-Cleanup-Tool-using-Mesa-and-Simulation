import os
import time
import cv2  
from PIL import Image
import imagehash
from tkinter import filedialog, messagebox, Listbox
from mesa import Agent, Model
from mesa.time import RandomActivation

# Function to find duplicates
def find_duplicates(image_folder):
    hashes = {}
    duplicates = []
    
    for filename in os.listdir(image_folder):
        if filename.endswith(('jpg', 'jpeg', 'png')):
            img_path = os.path.join(image_folder, filename)
            with Image.open(img_path) as img:
                hash_value = imagehash.average_hash(img)
                
                if hash_value in hashes:
                    print(f'Duplicate found: {filename} is similar to {hashes[hash_value]}')
                    duplicates.append(img_path)
                else:
                    hashes[hash_value] = filename
                
    return duplicates

# Function to remove duplicates
def Duplicates_remover(image_folder):
    if not os.path.exists(image_folder):
        print(f"Error: The specified folder does not exist: {image_folder}")
        return  

    duplicates = find_duplicates(image_folder)
    if duplicates:
        for duplicate in duplicates:
            print(f'Removing duplicate image: {duplicate}')
            try:
                os.remove(duplicate)
                print(f'Successfully removed duplicate: {duplicate}')
            except PermissionError:
                print(f'Permission denied for {duplicate}. Unable to remove.')
                messagebox.showinfo(f'Permission denied for {duplicate}. Unable to remove.')
        messagebox.showinfo("Info", "Duplicates removed successfully!")        
    else:            
        messagebox.showinfo("Info", "Duplicates are not found")    

# Mesa Agent for processing images
class ImageAgent(Agent):
    def __init__(self, unique_id, model, file_path):
        super().__init__(unique_id, model)
        self.file_path = file_path
        self.is_duplicate = False

    def step(self):
        # Use the find_duplicates logic for each agent
        if self.file_path.endswith(('jpg', 'jpeg', 'png')):
            with Image.open(self.file_path) as img:
                hash_value = imagehash.average_hash(img)
                if hash_value in self.model.hashes:
                    self.is_duplicate = True
                    self.model.duplicates.append(self.file_path)
                else:
                    self.model.hashes[hash_value] = self.file_path

# Mesa Model for duplicate management
class ImageCleanupModel(Model):
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.schedule = RandomActivation(self)
        self.hashes = {}
        self.duplicates = []

        # Create agents for each image file
        for idx, filename in enumerate(os.listdir(folder_path)):
            file_path = os.path.join(folder_path, filename)
            agent = ImageAgent(idx, self, file_path)
            self.schedule.add(agent)

    def step(self):
        self.schedule.step()

# Function to integrate Mesa with existing removal logic
def Duplicates_remover_with_mesa(image_folder):
    if not os.path.exists(image_folder):
        messagebox.showerror("Error", f"The specified folder does not exist: {image_folder}")
        return

    # Create and run the model
    model = ImageCleanupModel(image_folder)
    model.step()

    # Remove duplicates
    if model.duplicates:
        for duplicate in model.duplicates:
            print(f'Removing duplicate: {duplicate}')
            try:
                os.remove(duplicate)
            except PermissionError:
                messagebox.showerror("Error", f"Permission denied for {duplicate}. Unable to remove.")
        messagebox.showinfo("Info", "Duplicates removed successfully!")
    else:
        messagebox.showinfo("Info", "No duplicates found.")
