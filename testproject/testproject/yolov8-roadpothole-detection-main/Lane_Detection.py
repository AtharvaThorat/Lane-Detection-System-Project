import subprocess
import os


def open_with_default_player(file_path):
    try:
        os.startfile(file_path)
    except AttributeError:
        try:
            subprocess.Popen(['xdg-open', file_path])
        except:
            print("Unable to open file with the default player.")


# Example usage
file_path_1 = r"C:\Users\ATHARVA\Desktop\testproject\testproject\testproject\yolov8-roadpothole-detection-main\Lane_Detect_Output\Output_video_1.mp4"


file_path_2 = r"C:\Users\ATHARVA\Desktop\testproject\testproject\testproject\yolov8-roadpothole-detection-main\Lane_Detect_Output\Output_video_2.mp4"



file_path_3 = r"C:\Users\ATHARVA\Desktop\testproject\testproject\testproject\yolov8-roadpothole-detection-main\Lane_Detect_Output\Output_video_3.mp4"



# Command to run in Command Prompt
command1 = r"cd C:\Users\ATHARVA\Desktop\testproject\testproject\testproject\yolov8-roadpothole-detection-main\Lane_Detect_Vid1\project"
command2 = "python main.py"

command3 = r"cd C:\Users\ATHARVA\Desktop\testproject\testproject\testproject\yolov8-roadpothole-detection-main\Lane_Detect_Vid2\project"
command4 = "python main.py"

command5 = r"cd C:\Users\ATHARVA\Desktop\testproject\testproject\testproject\yolov8-roadpothole-detection-main\Lane_Detect_Vid3\project"
command6 = "python main.py"

# Open Command Prompt and execute the command
subprocess.run(["cmd", "/c", f"{command1} & {command2}"])
#open_with_default_player(file_path_1)
subprocess.run(["cmd", "/c", f"{command3} & {command4}"])
#open_with_default_player(file_path_2)
subprocess.run(["cmd", "/c", f"{command5} & {command6}"])
#open_with_default_player(file_path_3)
