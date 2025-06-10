import cv2
from mesa import Agent, Model
from mesa.time import RandomActivation

# Agent to capture a frame from video stream
class FaceCaptureAgent(Agent):
    def __init__(self, unique_id, model, save_path="captured_frame.jpg"):
        super().__init__(unique_id, model)
        self.save_path = save_path
        self.cap = None
        self.is_capturing = False
        self.is_exiting = False

    def start_video_capture(self):
        """ Initialize video capture and check if it opens successfully """
        self.cap = cv2.VideoCapture(0)  # 0 is the default camera
        if not self.cap.isOpened():
            print("Error: Could not open video stream.")
            return False
        return True

    def step(self):
        """ Capture frame when 'C' is pressed, exit when 'Q' is pressed """
        if self.cap is None:
            if not self.start_video_capture():
                return

        ret, frame = self.cap.read()
        if not ret:
            print("Failed to grab frame")
            return

        # Display the frame
        cv2.imshow('Video Frame', frame)

        # Check if key is pressed for actions
        key = cv2.waitKey(1) & 0xFF
        
        # Save frame when 'C' is pressed
        if key == ord('c') and not self.is_capturing:
            cv2.imwrite(self.save_path, frame)
            print(f"Frame captured and saved at {self.save_path}")
            self.is_capturing = True

        # Stop the capture and close on pressing 'Q'
        if key == ord('q'):
            self.is_exiting = True

    def stop_video_capture(self):
        """ Release the capture and destroy windows """
        if self.cap is not None:
            self.cap.release()
            cv2.destroyAllWindows()

# Model to manage face capture agents
class FaceCaptureModel(Model):
    def __init__(self, num_agents=1, save_path="captured_frame.jpg"):
        self.num_agents = num_agents
        self.schedule = RandomActivation(self)
        
        # Create the agents
        for i in range(self.num_agents):
            a = FaceCaptureAgent(i, self, save_path)
            self.schedule.add(a)

    def step(self):
        """ Run a step for all agents """
        self.schedule.step()

# Function to initiate the video capture and capture a frame using Mesa
def capture_face_with_mesa(save_path="captured_frame.jpg"):
    model = FaceCaptureModel(num_agents=1, save_path=save_path)

    while True:
        model.step()

        # Exit if any agent has triggered the exit condition
        if any(agent.is_exiting for agent in model.schedule.agents):
            break

    # Stop the video capture
    for agent in model.schedule.agents:
        agent.stop_video_capture()

# Example usage
if __name__ == "__main__":
     capture_face_with_mesa(save_path="captured_frame.jpg")
