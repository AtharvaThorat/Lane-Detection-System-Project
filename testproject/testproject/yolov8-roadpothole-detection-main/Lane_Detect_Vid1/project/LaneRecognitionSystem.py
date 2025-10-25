import cv2
import numpy as np
import matplotlib.image as mpimg

def hist(image):
    bottom_half = image[image.shape[0]//2:,:]
    return np.sum(bottom_half, axis=0)

class LaneRecognitionSystem:
   
    def __init__(self):
       
        self.left_fit = None
        self.right_fit = None
        self.binary = None
        self.nonzero = None
        self.nonzero_x = None
        self.nonzero_y = None
        self.clear_visibility = True
        self.dir = []
        self.left_curve_img = mpimg.imread('left_turn.png')
        self.right_curve_img = mpimg.imread('right_turn.png')
        self.keep_straight_img = mpimg.imread('straight.png')
        self.left_curve_img = cv2.normalize(src=self.left_curve_img, dst=None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        self.right_curve_img = cv2.normalize(src=self.right_curve_img, dst=None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        self.keep_straight_img = cv2.normalize(src=self.keep_straight_img, dst=None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        self.n_windows = 9
        self.margin = 100
        self.min_pix = 50

    def forward(self, image):

        self.extract_features(image)
        return self.fit_poly(image)

    def pixels_in_window(self, center, margin, height):

        top_left = (center[0]-margin, center[1]-height//2)
        bottom_right = (center[0]+margin, center[1]+height//2)

        condition_x = (top_left[0] <= self.nonzero_x) & (self.nonzero_x <= bottom_right[0])
        condition_y = (top_left[1] <= self.nonzero_y) & (self.nonzero_y <= bottom_right[1])
        return self.nonzero_x[condition_x & condition_y], self.nonzero_y[condition_x & condition_y]

    def extract_features(self, image):

        self.image = image
        self.window_height = int(image.shape[0]//self.n_windows)
        self.nonzero = image.nonzero()
        self.nonzero_x = np.array(self.nonzero[1])
        self.nonzero_y = np.array(self.nonzero[0])

    def find_lane_pixels(self, image):

        assert(len(image.shape) == 2)

        out_image = np.dstack((image, image, image))

        histogram = hist(image)
        midpoint = histogram.shape[0]//2
        left_x_base = np.argmax(histogram[:midpoint])
        right_x_base = np.argmax(histogram[midpoint:]) + midpoint

        left_x_current = left_x_base
        right_x_current = right_x_base
        y_current = image.shape[0] + self.window_height//2

        left_x, left_y, right_x, right_y = [], [], [], []

        for _ in range(self.n_windows):
            y_current -= self.window_height
            center_left = (left_x_current, y_current)
            center_right = (right_x_current, y_current)

            good_left_x, good_left_y = self.pixels_in_window(center_left, self.margin, self.window_height)
            good_right_x, good_right_y = self.pixels_in_window(center_right, self.margin, self.window_height)

            left_x.extend(good_left_x)
            left_y.extend(good_left_y)
            right_x.extend(good_right_x)
            right_y.extend(good_right_y)

            if len(good_left_x) > self.min_pix:
                left_x_current = np.int32(np.mean(good_left_x))
            if len(good_right_x) > self.min_pix:
                right_x_current = np.int32(np.mean(good_right_x))

        return left_x, left_y, right_x, right_y, out_image

    def fit_poly(self, image):

        left_x, left_y, right_x, right_y, out_image = self.find_lane_pixels(image)

        if len(left_y) > 1500:
            self.left_fit = np.polyfit(left_y, left_x, 2)
        if len(right_y) > 1500:
            self.right_fit = np.polyfit(right_y, right_x, 2)

        max_y = image.shape[0] - 1
        min_y = image.shape[0] // 3
        if len(left_y):
            max_y = max(max_y, np.max(left_y))
            min_y = min(min_y, np.min(left_y))

        if len(right_y):
            max_y = max(max_y, np.max(right_y))
            min_y = min(min_y, np.min(right_y))

        plot_y = np.linspace(min_y, max_y, image.shape[0])

        left_fit_x = self.left_fit[0] * plot_y**2 + self.left_fit[1] * plot_y + self.left_fit[2]
        right_fit_x = self.right_fit[0] * plot_y**2 + self.right_fit[1] * plot_y + self.right_fit[2]

        for i, y in enumerate(plot_y):
            l = int(left_fit_x[i])
            r = int(right_fit_x[i])
            y = int(y)
            cv2.line(out_image, (l, y), (r, y), (0, 255, 0))

        l_radius, r_radius, position = self.measure_curvature()

        return out_image
    
    def plot(self, out_img):
        np.set_printoptions(precision=6, suppress=True)
        lR, rR, pos = self.measure_curvature()

        value = None
        if abs(self.left_fit[0]) > abs(self.right_fit[0]):
            value = self.left_fit[0]
        else:
            value = self.right_fit[0]

        if abs(value) <= 0.00015:
            self.dir.append('F')
        elif value < 0:
            self.dir.append('L')
        else:
            self.dir.append('R')
        
        if len(self.dir) > 10:
            self.dir.pop(0)

        W = 400
        H = 500
        widget = np.copy(out_img[:H, :W])
        widget //= 2
        widget[0,:] = [0, 0, 255]
        widget[-1,:] = [0, 0, 255]
        widget[:,0] = [0, 0, 255]
        widget[:,-1] = [0, 0, 255]
        out_img[:H, :W] = widget

        direction = max(set(self.dir), key = self.dir.count)
        msg = "Keep Straight Ahead"
        curvature_msg = "Curvature = {:.0f} m".format(min(lR, rR))
        if direction == 'L':
            y, x = self.left_curve_img[:,:,3].nonzero()
            out_img[y, x-100+W//2] = self.left_curve_img[y, x, :3]
            msg = "Left Curve Ahead"
        if direction == 'R':
            y, x = self.right_curve_img[:,:,3].nonzero()
            out_img[y, x-100+W//2] = self.right_curve_img[y, x, :3]
            msg = "Right Curve Ahead"
        if direction == 'F':
            y, x = self.keep_straight_img[:,:,3].nonzero()
            out_img[y, x-100+W//2] = self.keep_straight_img[y, x, :3]

        cv2.putText(out_img, msg, org=(10, 240), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(255, 255, 255), thickness=2)
        '''if direction in 'LR':
            cv2.putText(out_img, curvature_msg, org=(10, 280), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(255, 255, 255), thickness=2)'''
        
        cv2.putText(
            out_img,
            "Good Lane Keeping",
            org=(10, 400),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=1.2,
            color=(0, 255, 0),
            thickness=2)



        return out_img

    def measure_curvature(self):
        y_m = 30/720
        x_m = 3.7/700

        left_fit = self.left_fit.copy()
        right_fit = self.right_fit.copy()
        y_eval = 700 * y_m

        # Compute R_curve (radius of curvature)
        left_curve_radius =  ((1 + (2*left_fit[0] *y_eval + left_fit[1])**2)**1.5)  / np.absolute(2*left_fit[0])
        right_curve_radius = ((1 + (2*right_fit[0]*y_eval + right_fit[1])**2)**1.5) / np.absolute(2*right_fit[0])

        x_left = np.dot(self.left_fit, [700**2, 700, 1])
        x_right = np.dot(self.right_fit, [700**2, 700, 1])
        position = (1280//2 - (x_left + x_right)//2) * x_m
        return left_curve_radius, right_curve_radius, position 
