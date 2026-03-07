"""
Lane Lines Detection pipeline

Usage:
    main.py [--video] INPUT_PATH OUTPUT_PATH 

Options:

-h --help                               show this screen
--video                                 process video file instead of image
"""

import numpy as np
import matplotlib.image as mpimg
import cv2
import webbrowser
from docopt import docopt
from IPython.display import HTML, Video
from moviepy import VideoFileClip
from CameraCalibrationTool import CameraCalibrationTool
from ThresholdingLaneIdentifier import *
from ImagePerspectiveTransformer import *
from LaneRecognitionSystem import *

class FindLaneLines:

    def __init__(self):
        """ Init Application"""
        self.calibration = CameraCalibrationTool('cam_cal', 9, 6)
        self.thresholding = ThresholdingLaneIdentifier()
        self.transform = ImagePerspectiveTransformer()
        self.lanelines = LaneRecognitionSystem()

    def forward(self, img):
        out_img = np.copy(img)
        img = self.calibration.undistort_image(img)
        img = self.transform.forward_transform(img)
        img = self.thresholding.forward(img)
        img = self.lanelines.forward(img)
        img = self.transform.backward_transform(img)

        out_img = cv2.addWeighted(out_img, 1, img, 0.6, 0)
        out_img = self.lanelines.plot(out_img)
        return out_img

    def process_image(self, input_path, output_path):
        img = mpimg.imread(input_path)
        out_img = self.forward(img)
        mpimg.imsave(output_path, out_img)

    def process_video(self, input_path, output_path):
        clip = VideoFileClip(input_path)
        out_clip = clip.image_transform(self.forward)
        out_clip.write_videofile(output_path, audio=False)

def main():
    base_path = "/Users/atharvathorat/Desktop/6th March/Final_Lane_Detection_Project/yolov8-roadpothole-detection-main"
    
    input = f"{base_path}/Lane_Detect_Output/Input_video_2.mp4"
    output = f"{base_path}/Lane_Detect_Output/Output_video_2.mp4"
    html_path = f"{base_path}/Lane_Detect_Output/UI_Name.html"
    
    findLaneLines = FindLaneLines()
    findLaneLines.process_video(input, output)
    webbrowser.open(html_path)
    
    '''
    args = docopt(__doc__)
    input = args['INPUT_PATH']
    output = args['OUTPUT_PATH']


    findLaneLines = FindLaneLines()
    if args['--video']:
        findLaneLines.process_video(input, output)
    else:
        findLaneLines.process_image(input, output)

    '''


if __name__ == "__main__":
    main()
