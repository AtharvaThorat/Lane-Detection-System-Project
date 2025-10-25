import cv2
import numpy as np

def threshold_rel(image, low, high):
    min_val = np.min(image)
    max_val = np.max(image)
    
    low_value = min_val + (max_val - min_val) * low
    high_value = min_val + (max_val - min_val) * high
    return np.uint8((image >= low_value) & (image <= high_value)) * 255

def threshold_abs(image, low, high):
    return np.uint8((image >= low) & (image <= high)) * 255

class ThresholdingLaneIdentifier:
    
    def __init__(self):
        """ Initializes Thresholding."""
        pass

    def forward(self, image):

        hls = cv2.cvtColor(image, cv2.COLOR_RGB2HLS)
        hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
        hue_channel = hls[:,:,0]
        lightness_channel = hls[:,:,1]
        saturation_channel = hls[:,:,2]
        value_channel = hsv[:,:,2]
        

        right_lane = threshold_rel(lightness_channel, 0.8, 1.0)
        right_lane[:,:750] = 0

        left_lane = threshold_abs(hue_channel, 20, 30)
        left_lane &= threshold_rel(value_channel, 0.7, 1.0)
        left_lane[:,550:] = 0

        final_image = left_lane | right_lane

        return final_image
