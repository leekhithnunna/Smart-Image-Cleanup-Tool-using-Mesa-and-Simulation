import os
import cv2
import shutil
from mesa import Agent, Model
from mesa.time import RandomActivation
from tkinter import filedialog, messagebox


# Agent for each image
class ImageAgent(Agent):
    def __init__(self, unique_id, model, image_path, threshold=100):
        super().__init__(unique_id, model)
        self.image_path = image_path
        self.threshold = threshold
        self.is_blurry = False

    def is_blurry_image(self):
        img = cv2.imread(self.image_path)
        if img is None:
            print(f"Warning: Unable to read image {self.image_path}. It may be corrupted or not an image.")
            return False
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        variance = cv2.Laplacian(gray, cv2.CV_64F).var()
        return variance < self.threshold

    def step(self):
        if self.is_blurry_image():
            self.is_blurry = True
            print(f'Removing blurry image: {self.image_path}')
            try:
                os.remove(self.image_path)
                print(f'Successfully removed: {self.image_path}')
            except PermissionError:
                print(f'Permission denied for {self.image_path}. Unable to remove.')

# Model for managing image agents
class ImageCleanupModel(Model):
    def __init__(self, folder_path, threshold=100):
        self.folder_path = folder_path
        self.threshold = threshold
        self.schedule = RandomActivation(self)
        self.blurry_images = []

        # Create agents for each image in the folder
        for idx, filename in enumerate(os.listdir(folder_path)):
            file_path = os.path.join(folder_path, filename)
            if filename.endswith(('jpg', 'jpeg', 'png')):
                agent = ImageAgent(idx, self, file_path, self.threshold)
                self.schedule.add(agent)

    def step(self):
        self.schedule.step()

    def get_blurry_images(self):
        for agent in self.schedule.agents:
            if agent.is_blurry:
                self.blurry_images.append(agent.image_path)
        return self.blurry_images


# Function to remove blurry images with Mesa
def remove_blurry_images_with_mesa(folder_path, threshold=100):
    if not os.path.exists(folder_path):
        print(f"Error: The specified folder does not exist: {folder_path}")
        return

    # Initialize the model and run one step
    model = ImageCleanupModel(folder_path, threshold)
    model.step()

    blurry_images = model.get_blurry_images()
    if blurry_images:
        print("Blurry images removed:", blurry_images)
        messagebox.showinfo("Info", "Low-quality images removed successfully!")
    else:
        messagebox.showinfo("Info", "No low-quality images found.")


# Main function to integrate with the GUI
def main(image_folder):
    if not os.path.exists(image_folder):
        print(f"Error: The specified folder does not exist: {image_folder}")
        return

    remove_blurry_images_with_mesa(image_folder)
