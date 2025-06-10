import os
from model import SmartImageCleanupModel
import customtkinter as ctk
from gui import SmartImageCleanupGUI

if __name__ == "__main__":
    # Configure image folder (relative to project directory)
    image_folder = os.path.join(os.path.dirname(__file__), "images")
    
    # Initialize the model with the image folder
    try:
        model = SmartImageCleanupModel(image_folder)
        
        # Run the model for one step (checks are stateless, so one step is enough)
        model.step()
        
        # Fetch results for debugging (optional)
        results = model.datacollector.get_agent_vars_dataframe()
        print("Results from the model:")
        print(results)
        
        # Launch GUI
        root = ctk.CTk()
        gui = SmartImageCleanupGUI(root, model)  # Pass model to GUI
        root.mainloop()
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        exit(1)