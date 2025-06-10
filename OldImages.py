import os
import datetime
from mesa import Agent, Model
from mesa.time import RandomActivation

# Agent for handling individual files
class FileAgent(Agent):
    def __init__(self, unique_id, model, file_path, cutoff_datetime):
        super().__init__(unique_id, model)
        self.file_path = file_path
        self.cutoff_datetime = cutoff_datetime
        self.to_delete = False

    def step(self):
        if os.path.isfile(self.file_path):
            # Get the last modified time of the file
            file_mod_time = datetime.datetime.fromtimestamp(os.path.getmtime(self.file_path))
            # Mark the file for deletion if it's older than the cutoff time
            if file_mod_time < self.cutoff_datetime:
                self.to_delete = True
                self.model.old_files.append(self.file_path)

# Model for managing old file deletion
class FileCleanupModel(Model):
    def __init__(self, folder_path, cutoff_time):
        self.folder_path = folder_path
        self.cutoff_datetime = datetime.datetime.strptime(cutoff_time, "%Y-%m-%d %H:%M:%S")
        self.schedule = RandomActivation(self)
        self.old_files = []  # List of files to delete

        # Create an agent for each file in the folder
        for idx, filename in enumerate(os.listdir(folder_path)):
            file_path = os.path.join(folder_path, filename)
            agent = FileAgent(idx, self, file_path, self.cutoff_datetime)
            self.schedule.add(agent)

    def step(self):
        self.schedule.step()

# Function to delete old images using Mesa
def delete_old_images_with_mesa(folder_path, cutoff_time):
    if not os.path.exists(folder_path):
        print(f"Error: The specified folder does not exist: {folder_path}")
        return

    # Initialize the model
    model = FileCleanupModel(folder_path, cutoff_time)
    model.step()

    # Delete files marked for deletion
    if model.old_files:
        for old_file in model.old_files:
            print(f"Deleting: {old_file}")
            try:
                os.remove(old_file)
            except PermissionError:
                print(f"Permission denied for {old_file}. Unable to remove.")
        print("Old files deleted successfully!")
    else:
        print("No old files found.")

# Example usage
# if __name__ == "__main__":
#     folder_path = r"C:\Users\leekh\Downloads\FAI_project\Gallary"
#     cutoff_time = "2024-10-10 12:00:00"  # Set your desired cutoff time
#     delete_old_images_with_mesa(folder_path, cutoff_time)
