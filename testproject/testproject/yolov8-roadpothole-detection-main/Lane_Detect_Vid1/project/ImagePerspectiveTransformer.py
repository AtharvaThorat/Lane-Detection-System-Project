import cv2
import numpy as np

class ImagePerspectiveTransformer:

    def __init__(self):
        """Init PerspectiveTransformation."""
        self.source_points = np.float32([(550, 460),     # top-left
                                         (150, 720),     # bottom-left
                                         (1200, 720),    # bottom-right
                                         (770, 460)])    # top-right
        self.destination_points = np.float32([(100, 0),
                                              (100, 720),
                                              (1100, 720),
                                              (1100, 0)])
        self.transformation_matrix = cv2.getPerspectiveTransform(self.source_points, self.destination_points)
        self.inverse_transformation_matrix = cv2.getPerspectiveTransform(self.destination_points, self.source_points)

    def forward_transform(self, img, img_size=(1280, 720), flags=cv2.INTER_LINEAR):
      
        return cv2.warpPerspective(img, self.transformation_matrix, img_size, flags=flags)

    def backward_transform(self, img, img_size=(1280, 720), flags=cv2.INTER_LINEAR):
     
        return cv2.warpPerspective(img, self.inverse_transformation_matrix, img_size, flags=flags)
