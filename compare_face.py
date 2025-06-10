import face_recognition
import os
import shutil
from mesa import Agent, Model
from mesa.time import RandomActivation
from tkinter import messagebox

# Agent to compare faces in an image
class FaceComparisonAgent(Agent):
    def __init__(self, unique_id, model, image_path, folder_path, reference_encoding, output_folder="matched_images", tolerance=0.5):
        super().__init__(unique_id, model)
        self.image_path = image_path
        self.folder_path = folder_path
        self.reference_encoding = reference_encoding
        self.output_folder = output_folder
        self.tolerance = tolerance
        self.has_matched = False
    
    def compare_face(self):
        """Compare the agent's image with the reference image"""
        # Load current image and get face encodings
        current_image = face_recognition.load_image_file(self.image_path)
        current_encodings = face_recognition.face_encodings(current_image)

        if not current_encodings:
            print(f"No face found in {self.image_path}. Skipping.")
            return False

        # Compare the faces with specified tolerance
        match_result = face_recognition.compare_faces([self.reference_encoding], current_encodings[0], tolerance=self.tolerance)
        return match_result[0]

    def move_image(self):
        """Move the image to the output folder if matched"""
        if self.compare_face():
            print(f"Face matched with {self.image_path}")
            if not os.path.exists(self.output_folder):
                os.makedirs(self.output_folder)
            shutil.copy(self.image_path, os.path.join(self.output_folder, os.path.basename(self.image_path)))
            self.has_matched = True
        else:
            print(f"No match for {self.image_path}")

    def step(self):
        """Run the agent's logic: compare and move the image if a match is found"""
        self.move_image()

# Model to manage the face comparison process
class FaceComparisonModel(Model):
    def __init__(self, folder_path, reference_image_path, output_folder="matched_images", tolerance=0.5):
        self.folder_path = folder_path
        self.reference_image_path = reference_image_path
        self.output_folder = output_folder
        self.tolerance = tolerance
        self.schedule = RandomActivation(self)

        # Load reference image and get face encoding
        reference_image = face_recognition.load_image_file(self.reference_image_path)
        reference_encodings = face_recognition.face_encodings(reference_image)
        
        if not reference_encodings:
            print("No face found in the reference image.")
            return

        self.reference_encoding = reference_encodings[0]

        # Create agents for each image in the folder
        for idx, filename in enumerate(os.listdir(self.folder_path)):
            file_path = os.path.join(self.folder_path, filename)
            agent = FaceComparisonAgent(idx, self, file_path, self.folder_path, self.reference_encoding, self.output_folder, self.tolerance)
            self.schedule.add(agent)

    def step(self):
        """Run a step for all agents"""
        self.schedule.step()

# Function to run the model and compare faces
def compare_faces_with_mesa(reference_image_path, folder_path, output_folder="matched_images", tolerance=0.5):
    model = FaceComparisonModel(folder_path, reference_image_path, output_folder, tolerance)
    has_matches = False

    # Run the model for several steps (to process each agent)
    for _ in range(len(os.listdir(folder_path))):
        model.step()
    
    # Check if any images were matched and copied
    for agent in model.schedule.agents:
        if agent.has_matched:
            has_matches = True

    if has_matches:
        messagebox.showinfo("Info", "Successfully completed")
    else:
        messagebox.showinfo("Info", "No images were found that match the reference.")

# Example usage (using file paths as arguments)
if __name__ == "__main__":
    folder_path = "path_to_folder_with_images"
    reference_image_path = "path_to_reference_image.jpg"
    compare_faces_with_mesa(reference_image_path, folder_path)
