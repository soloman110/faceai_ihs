import cv2
import dlib
import numpy as np
from keras.models import load_model

class ImageMetaExtractorBase():
    def __init__(self):
        self.detector = dlib.get_frontal_face_detector()
        self.img_size = 64

    #deprecated. 현재 사용하지 않음
    def load_img(self, image_path):
        img = cv2.imread(str(image_path), 1)
        if img is not None:
            h, w, _ = img.shape
            r = 640 / max(w, h)
            return cv2.resize(img, (int(w * r), int(h * r)))

    def img_shape(self, img):
        #input_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return np.shape(img)
