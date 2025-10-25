import numpy as np
import cv2
import glob
import matplotlib.image as mpimg
import matplotlib.pyplot as plt

class CameraCalibrationTool():

    def __init__(self, img_folder_path, nx_corners, ny_corners, debug=False):

        image_paths = glob.glob("{}/*".format(img_folder_path))
        object_points = []
        image_points = []

        object_point = np.zeros((nx_corners * ny_corners, 3), np.float32)
        object_point[:,:2] = np.mgrid[0:nx_corners, 0:ny_corners].T.reshape(-1, 2)
        

        for img_path in image_paths:
            img = mpimg.imread(img_path)
      
            gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

            ret, corners = cv2.findChessboardCorners(img, (nx_corners, ny_corners))
            if ret:
                image_points.append(corners)
                object_points.append(object_point)

        image_shape = (img.shape[1], img.shape[0])
        ret, self.intrinsic_mtx, self.distortion_coeffs, _, _ = cv2.calibrateCamera(object_points, image_points, image_shape, None, None)

        if not ret:
            raise Exception("Unable to calibrate camera")

    def undistort_image(self, input_img):

        gray_img = cv2.cvtColor(input_img, cv2.COLOR_RGB2GRAY)

        return cv2.undistort(input_img, self.intrinsic_mtx, self.distortion_coeffs, None, self.intrinsic_mtx)
