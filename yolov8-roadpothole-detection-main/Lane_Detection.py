import subprocess
import os
import sys

def open_with_default_player(file_path):
    try:
        if sys.platform == "darwin":  # macOS
            subprocess.Popen(['open', file_path])
        elif sys.platform == "win32":  # Windows
            os.startfile(file_path)
        else:  # Linux
            subprocess.Popen(['xdg-open', file_path])
    except Exception as e:
        print(f"Unable to open file with the default player: {e}")

# Update paths for Mac (use forward slashes and Mac-style paths)
base_path = "/Users/atharvathorat/Desktop/6th March/Final_Lane_Detection_Project/yolov8-roadpothole-detection-main"

file_path_1 = f"{base_path}/Lane_Detect_Output/Output_video_1.mp4"
file_path_2 = f"{base_path}/Lane_Detect_Output/Output_video_2.mp4"
file_path_3 = f"{base_path}/Lane_Detect_Output/Output_video_3.mp4"

# Directories for each project
dir1 = f"{base_path}/Lane_Detect_Vid1/project"
dir2 = f"{base_path}/Lane_Detect_Vid2/project"
dir3 = f"{base_path}/Lane_Detect_Vid3/project"

# Run each project using bash (Mac/Linux compatible)
subprocess.run(["bash", "-c", f"cd '{dir1}' && python main.py"])
# open_with_default_player(file_path_1)

subprocess.run(["bash", "-c", f"cd '{dir2}' && python main.py"])
# open_with_default_player(file_path_2)

subprocess.run(["bash", "-c", f"cd '{dir3}' && python main.py"])
# open_with_default_player(file_path_3)