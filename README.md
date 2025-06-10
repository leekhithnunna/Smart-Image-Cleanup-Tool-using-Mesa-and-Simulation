# Smart-Image-Cleanup-Tool-using-Mesa-and-Simulation
Smart Image Cleanup, Tkinter GUI, Image Management, imageHash: Perceptual Hashing, Duplicate Detection, Blurry Image Removal, Laplacian Variance, Metadata Extraction, Dlib: Face Detection, OpenCV, Image Filtering,Image Gallery Management, mesa simulation Analaysis

# Smart Image Cleanup Tool

A **Python-based desktop application** for organizing and cleaning up image collections. This tool combines traditional image processing techniques with **agent-based modeling (via MESA)** to detect and manage:
- Duplicate images
- Blurry (low-quality) images
- Outdated images
- Faces via webcam

Includes a **modern GUI** with optional **MESA simulation** interface for advanced analysis and visualization.

---

## 🚀 Features

### 🧠 Core Functionalities
- **Duplicate Image Removal**: Detects and deletes duplicate images using perceptual hashing.
- **Blurry Image Removal**: Removes low-quality images based on Laplacian variance.
- **Outdated Image Removal**: Deletes images older than a user-specified datetime.
- **Face Management**: Captures face via webcam and compares it against faces found in images.
- **MESA Simulation**: Agent-based modeling of image statuses with a visual simulation GUI.

### 🎨 User Interface Highlights
- One-time **“Select Folder”** button to set working directory.
- **Listbox** displays filenames of processed images.
- **Dark Mode toggle** and animated title.
- Buttons remain **disabled until a folder is selected**, enhancing user experience.

### 🧪 MESA Simulation GUI
- Visualizes each image as a **colored oval**:
  - Blue = Active  
  - Red = Duplicate  
  - Yellow = Blurred  
  - Gray = Outdated
- Displays results in a **table** format: Path, Duplicate, Blurred, Outdated.
- Allows **deletion of flagged images** with confirmation dialog.

---

## 🛠️ Prerequisites

- **Python:** 3.8 or higher  
- **OS:** Windows (macOS/Linux support with minor tweaks)

### 📦 Dependencies
Install via:

pip install opencv-python imagehash Pillow mesa customtkinter


**python GUI.py**

| File/Folder        | Purpose                                    |
| ------------------ | ------------------------------------------ |
| `GUI.py`           | Main GUI for image cleanup                 |
| `Duplicates.py`    | Handles duplicate image detection          |
| `lowQuality.py`    | Removes blurry/low-quality images          |
| `captureFace.py`   | Captures face via webcam                   |
| `compare_face.py`  | Face recognition and comparison            |
| `OldImages.py`     | Detects and removes outdated images        |
| `Mesa/`            | Contains agent-based simulation components |
| └ `gui.py`         | MESA simulation GUI                        |
| └ `agent.py`       | MESA agent logic                           |
| └ `model.py`       | MESA simulation model                      |
| `requirements.txt` | List of required Python packages           |

### 🔮 Future Plans

- Integrate MESA results into the main GUI Listbox.

- Add image preview thumbnails.

- Allow adjusting blur threshold and date cutoff.

- Export results to a CSV file.

- Make MESA deletion sync with GUI cleanup (optional).

**Email:** leekhithnunna1269@gmail.com
