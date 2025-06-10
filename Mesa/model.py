from mesa import Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from agent import ImageAgent
import os
from datetime import datetime

class SmartImageCleanupModel(Model):
    """Model for managing the image cleanup process."""
    def __init__(self, image_folder):
        self.schedule = RandomActivation(self)
        self.datacollector = DataCollector(
            agent_reporters={
                "Path": "image_path",
                "Duplicate": "is_duplicate",
                "Blurred": "is_blurred",
                "Outdated": "is_outdated"
            }
        )
        self.running = True
        self.image_folder = image_folder
        self._load_images()

    def _load_images(self):
        """Load images from the specified folder and create agents."""
        if not os.path.exists(self.image_folder):
            raise FileNotFoundError(f"Image folder {self.image_folder} does not exist.")
        
        valid_extensions = ('.jpg', '.jpeg', '.png')
        for i, filename in enumerate(os.listdir(self.image_folder)):
            if filename.lower().endswith(valid_extensions):
                image_path = os.path.join(self.image_folder, filename)
                last_modified = datetime.fromtimestamp(os.path.getmtime(image_path))
                agent = ImageAgent(i, self, image_path, last_modified)
                self.schedule.add(agent)

    def step(self):
        """Advance the model by one step."""
        self.schedule.step()
        self.datacollector.collect(self)