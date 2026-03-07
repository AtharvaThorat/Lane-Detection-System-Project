import tkinter as tk
from tkinter import messagebox, ttk
import subprocess
from PIL import Image, ImageTk
import threading
import time  # Added for time.sleep()
import webbrowser

# Global variable to keep track of the process ID and progress bar
process = None
progress_bar = None
lane_detection_completed = False  # Flag to track if lane detection completed normally

def run_pothole_detection():
    global process
    try:
        # Start the pothole detection process
        process = subprocess.Popen(["python", "test.py"])

        messagebox.showinfo("Success", "Pothole detection process started!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def run_zebra_detection():
    global process
    try:
        # Start the zebra crossing detection process
        process = subprocess.Popen(["python", "zebra.py"])

        messagebox.showinfo("Success", "Zebra crossing detection process started!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def run_lane_detection():
    global process, progress_bar, lane_detection_completed
    try:
        # Start the lane line detection process in a separate thread
        thread = threading.Thread(target=start_lane_detection)
        thread.start()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def start_lane_detection():
    global process, progress_bar, lane_detection_completed
    try:
        # Start the lane line detection process
        process = subprocess.Popen(["python", "Lane_Detection.py"])

        messagebox.showinfo("Success", "Lane line detection process started!")


        # Mark lane detection as completed
        lane_detection_completed = True
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


def view_screenshots():
    try:
        subprocess.run(["python", "view_ss.py"])
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


def stop_detection():
    global process, progress_bar, lane_detection_completed
    if process:
        process.terminate()
        
        if not lane_detection_completed:
            messagebox.showinfo("Stopped", "Detection process stopped.")
    else:
        messagebox.showinfo("Info", "No process is running.")




def View_Result():
    try:
        base_path = "/Users/atharvathorat/Desktop/6th March/Final_Lane_Detection_Project/yolov8-roadpothole-detection-main"
        webbrowser.open(f"file://{base_path}/Lane_Detect_Output/UI_Name.html")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

        

# Create the main window
root = tk.Tk()
root.title("Road Detection System")

# Set the window size to 1400x900
root.geometry("1400x900")

# Load the background image
try:
    background_image = Image.open(
    "/Users/atharvathorat/Desktop/6th March/Final_Lane_Detection_Project/yolov8-roadpothole-detection-main/bgimages/bgo3.jpg")
    background_image = background_image.resize((1400, 900))
    background_photo = ImageTk.PhotoImage(background_image)

    # Create a label to hold the background image
    background_label = tk.Label(root, image=background_photo)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Raise the stacking order of the background label
    background_label.lift()

    # To prevent garbage collection
    root.background_photo = background_photo
except Exception as e:
    messagebox.showerror("Error", f"Failed to load background image: {str(e)}")

# Title text
title_text = "Enhanced Road Detection System"
title_label = tk.Label(root, text=title_text, font=("Arial", 27, "bold"), fg="#800080", bg="white")
title_label.pack(pady=20)

# Create a frame for buttons
button_frame = tk.Frame(root, bg="white", highlightbackground="gray", highlightcolor="gray", highlightthickness=5, bd=0)
button_frame.pack(pady=(50, 10))

# Create left section
left_frame = tk.Frame(button_frame, bg="white")
left_frame.pack(side="left", padx=20, pady=20)

# Button for running pothole detection
pothole_button = tk.Button(left_frame, text="Pothole Detection", command=run_pothole_detection, width=20, height=2,
                           bg="#0055cc", fg="black", font=("Arial", 12, "bold"),
                           cursor="hand2", relief=tk.RAISED, bd=3)
pothole_button.pack(pady=10)

# Button for stopping detection
stop_button = tk.Button(left_frame, text="Stop Detection", command=stop_detection, width=20, height=2,
                        bg="#cc0000", fg="black", font=("Arial", 12, "bold"),
                        cursor="hand2", relief=tk.RAISED, bd=3)
stop_button.pack(pady=10)

# Button for viewing screenshots
view_ss_button = tk.Button(left_frame, text="View Screenshots", command=view_screenshots, width=20, height=2,
                           bg="#0055cc", fg="black", font=("Arial", 12, "bold"),
                           cursor="hand2", relief=tk.RAISED, bd=3)
view_ss_button.pack(pady=10)

# Create middle section
middle_frame = tk.Frame(button_frame, bg="white")
middle_frame.pack(side="left", padx=20, pady=20)

# Button for running lane detection
lane_button = tk.Button(middle_frame, text="Lane Detection", command=run_lane_detection, width=20, height=2,
                        bg="#0055cc", fg="black", font=("Arial", 12, "bold"),
                        cursor="hand2", relief=tk.RAISED, bd=3)
lane_button.pack(pady=10)

# Button for View detection result
View_Result_button = tk.Button(middle_frame, text="View Detection", command=View_Result, width=20, height=2,
                               bg="#0055cc", fg="black", font=("Arial", 12, "bold"),
                               cursor="hand2", relief=tk.RAISED, bd=3)
View_Result_button.pack(pady=10)

# Create right section
right_frame = tk.Frame(button_frame, bg="white")
right_frame.pack(side="left", padx=20, pady=20)

# Button for running zebra detection
zebra_button = tk.Button(right_frame, text="Zebra Detection", command=run_zebra_detection, width=20, height=2,
                         bg="#0055cc", fg="black", font=("Arial", 12, "bold"),
                         cursor="hand2", relief=tk.RAISED, bd=3)
zebra_button.pack(pady=10)

# Button for stopping detection
stop_button = tk.Button(right_frame, text="Stop Detection", command=stop_detection, width=20, height=2,
                        bg="#cc0000", fg="black", font=("Arial", 12, "bold"),
                        relief=tk.RAISED, bd=3)
stop_button.pack(pady=10)






# Run the main loop
root.mainloop()
