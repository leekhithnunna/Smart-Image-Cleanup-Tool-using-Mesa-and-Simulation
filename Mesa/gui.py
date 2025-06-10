import customtkinter as ctk
import threading
import random
import os
from tkinter import filedialog, messagebox, ttk
from model import SmartImageCleanupModel
import pandas as pd
import tkinter as tk

class SmartImageCleanupGUI:
    """GUI for the Smart Image Cleanup Tool using MESA simulation."""
    def __init__(self, root, model=None, folder_path=None):
        self.root = root
        self.model = model  # Model passed from main.py or None
        self.image_folder = folder_path  # Pre-selected folder
        self.root.title("MESA Image Cleanup Simulation")
        self.root.geometry("1000x800")
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        # Main frame
        self.main_frame = ctk.CTkFrame(self.root, corner_radius=10)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Title
        self.title_label = ctk.CTkLabel(
            self.main_frame, text="MESA Image Cleanup Simulation", font=("Arial", 24, "bold")
        )
        self.title_label.pack(pady=10)

        # Folder selection
        self.folder_frame = ctk.CTkFrame(self.main_frame, corner_radius=5)
        self.folder_frame.pack(pady=10, fill="x", padx=20)
        self.folder_label = ctk.CTkLabel(
            self.folder_frame, 
            text=f"Image Folder: {folder_path if folder_path else 'Not selected'}", 
            font=("Arial", 12)
        )
        self.folder_label.pack(side="left", padx=10)
        self.select_folder_button = ctk.CTkButton(
            self.folder_frame, text="Select Folder", command=self.select_folder
        )
        self.select_folder_button.pack(side="left", padx=10)

        # Canvas for agent visualization
        self.canvas = ctk.CTkCanvas(self.main_frame, width=700, height=400, bg="white")
        self.canvas.pack(pady=10)

        # Legend
        self.legend_frame = ctk.CTkFrame(self.main_frame, corner_radius=5)
        self.legend_frame.pack(pady=10)
        ctk.CTkLabel(self.legend_frame, text="Legend: ", font=("Arial", 14)).grid(
            row=0, column=0, padx=10
        )
        legend_items = [
            {"color": "blue", "text": "Active"},
            {"color": "red", "text": "Duplicate"},
            {"color": "yellow", "text": "Blurred"},
            {"color": "gray", "text": "Outdated"},
        ]
        for i, item in enumerate(legend_items):
            ctk.CTkLabel(
                self.legend_frame, width=20, height=20, bg_color=item["color"], text=""
            ).grid(row=0, column=i * 2 + 1, padx=5)
            ctk.CTkLabel(self.legend_frame, text=item["text"], font=("Arial", 12)).grid(
                row=0, column=i * 2 + 2, padx=5
            )

        # Control buttons
        self.control_frame = ctk.CTkFrame(self.main_frame, corner_radius=5)
        self.control_frame.pack(pady=10)
        self.run_button = ctk.CTkButton(
            self.control_frame, text="Run Cleanup", command=self.run_model, 
            state="normal" if folder_path else "disabled"
        )
        self.run_button.grid(row=0, column=0, padx=5)
        self.delete_button = ctk.CTkButton(
            self.control_frame, text="Delete Flagged Images", command=self.delete_images, state="disabled"
        )
        self.delete_button.grid(row=0, column=1, padx=5)

        # Result table
        self.result_frame = ctk.CTkFrame(self.main_frame, corner_radius=5)
        self.result_frame.pack(pady=10, fill="both", expand=True, padx=20)
        self.result_tree = ttk.Treeview(
            self.result_frame,
            columns=("Path", "Duplicate", "Blurred", "Outdated"),
            show="headings",
            height=10
        )
        self.result_tree.heading("Path", text="Image Path")
        self.result_tree.heading("Duplicate", text="Duplicate")
        self.result_tree.heading("Blurred", text="Blurred")
        self.result_tree.heading("Outdated", text="Outdated")
        self.result_tree.column("Path", width=400)
        self.result_tree.column("Duplicate", width=100)
        self.result_tree.column("Blurred", width=100)
        self.result_tree.column("Outdated", width=100)
        self.result_tree.pack(side="left", fill="both", expand=True)
        scrollbar = ctk.CTkScrollbar(self.result_frame, command=self.result_tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.result_tree.configure(yscrollcommand=scrollbar.set)

        self.agents = []
        self.agent_positions = set()

        # Initialize model if folder_path provided
        if folder_path:
            try:
                self.model = SmartImageCleanupModel(folder_path)
            except FileNotFoundError:
                messagebox.showerror("Error", f"Invalid folder: {folder_path}")
                self.folder_label.configure(text="Image Folder: Not selected")
                self.image_folder = None
                self.run_button.configure(state="disabled")

    def select_folder(self):
        """Open a dialog to select the image folder."""
        folder = filedialog.askdirectory(title="Select Image Folder")
        if folder:
            self.image_folder = folder
            self.folder_label.configure(text=f"Image Folder: {folder}")
            try:
                self.model = SmartImageCleanupModel(folder)
                self.run_button.configure(state="normal")
                self.clear_canvas()
            except FileNotFoundError:
                messagebox.showerror("Error", f"Invalid folder: {folder}")
                self.folder_label.configure(text="Image Folder: Not selected")
                self.image_folder = None
                self.run_button.configure(state="disabled")

    def clear_canvas(self):
        """Clear the canvas and reset agent visualizations."""
        self.canvas.delete("all")
        self.agents = []
        self.agent_positions = set()

    def run_model(self):
        """Run the cleanup process in a separate thread."""
        if not self.model:
            messagebox.showerror("Error", "No image folder selected.")
            return
        self.run_button.configure(state="disabled")
        self.delete_button.configure(state="disabled")
        self.result_tree.delete(*self.result_tree.get_children())
        threading.Thread(target=self.run_cleanup, daemon=True).start()

    def run_cleanup(self):
        """Run the model and update the GUI."""
        self.clear_canvas()
        for agent in self.model.schedule.agents:
            while True:
                x = random.randint(50, 650)
                y = random.randint(50, 350)
                if (x, y) not in self.agent_positions:
                    self.agent_positions.add((x, y))
                    break
            agent_graphic = self.canvas.create_oval(x, y, x + 20, y + 20, fill="blue", outline="black")
            self.agents.append(agent_graphic)

        self.model.step()
        self.update_agents()

        results = self.model.datacollector.get_agent_vars_dataframe()
        for _, row in results.iterrows():
            self.result_tree.insert(
                "",
                "end",
                values=(
                    row["Path"],
                    "Yes" if row["Duplicate"] else "No",
                    "Yes" if row["Blurred"] else "No",
                    "Yes" if row["Outdated"] else "No"
                )
            )

        self.delete_button.configure(state="normal")
        self.run_button.configure(state="normal")
        self.root.after(0, self.root.update)

    def update_agents(self):
        """Update agent visualizations based on their states."""
        for i, agent in enumerate(self.model.schedule.agents):
            if i >= len(self.agents):
                continue
            color = (
                "red" if agent.is_duplicate else
                "yellow" if agent.is_blurred else
                "gray" if agent.is_outdated else
                "blue"
            )
            self.canvas.itemconfig(self.agents[i], fill=color)

    def delete_images(self):
        """Delete flagged images after user confirmation."""
        if not self.model:
            return
        flagged = [
            agent.image_path
            for agent in self.model.schedule.agents
            if agent.is_duplicate or agent.is_blurred or agent.is_outdated
        ]
        if not flagged:
            messagebox.showinfo("Info", "No images flagged for deletion.")
            return
        if messagebox.askyesno(
            "Confirm Deletion",
            f"Delete {len(flagged)} flagged images?\nThis action cannot be undone."
        ):
            for path in flagged:
                try:
                    os.remove(path)
                except Exception as e:
                    print(f"Error deleting {path}: {e}")
            messagebox.showinfo("Success", f"Deleted {len(flagged)} images.")
            self.clear_canvas()
            self.result_tree.delete(*self.result_tree.get_children())
            self.model = None
            self.image_folder = None
            self.folder_label.configure(text="Image Folder: Not selected")
            self.run_button.configure(state="disabled")
            self.delete_button.configure(state="disabled")