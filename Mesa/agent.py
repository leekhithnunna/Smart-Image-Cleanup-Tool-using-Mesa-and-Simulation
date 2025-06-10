import cv2
import imagehash
from PIL import Image
from mesa import Agent
from datetime import datetime, timedelta

class ImageAgent(Agent):
    """An agent representing an image for cleanup analysis."""
    def __init__(self, unique_id, model, image_path, last_modified):
        super().__init__(unique_id, model)
        self.image_path = image_path
        self.last_modified = last_modified  # datetime object
        self.is_duplicate = False
        self.is_blurred = False
        self.is_outdated = False
        self.image_hash = None  # Store perceptual hash

    def step(self):
        """Perform actions at each step."""
        self.is_outdated = self.check_outdated()
        self.is_duplicate = self.check_duplicate()
        self.is_blurred = self.detect_blur()

    def check_outdated(self):
        """Check if the image is outdated (unused for over a year)."""
        try:
            current_date = datetime.now()
            delta = current_date - self.last_modified
            return delta.days > 365
        except Exception as e:
            print(f"Error checking date for {self.image_path}: {e}. Marking as outdated.")
            return True

    def check_duplicate(self):
        """Check if the image is a duplicate based on perceptual hash."""
        if not self.image_hash:
            try:
                self.image_hash = imagehash.average_hash(Image.open(self.image_path))
            except Exception as e:
                print(f"Error hashing {self.image_path}: {e}. Marking as non-duplicate.")
                return False
        
        for agent in self.model.schedule.agents:
            if agent != self and agent.image_hash:
                if self.image_hash - agent.image_hash < 5:  # Similarity threshold
                    return True
        return False

    def detect_blur(self):
        """Detect if the image is blurred using Laplacian variance."""
        try:
            img = cv2.imread(self.image_path, cv2.IMREAD_GRAYSCALE)
            if img is None:
                print(f"Failed to load {self.image_path}. Marking as blurred.")
                return True
            laplacian_var = cv2.Laplacian(img, cv2.CV_64F).var()
            return laplacian_var < 100  # Adjust threshold based on testing
        except Exception as e:
            print(f"Error processing {self.image_path}: {e}. Marking as blurred.")
            return True