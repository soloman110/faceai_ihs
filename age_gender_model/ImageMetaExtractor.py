import cv2
import dlib
import numpy as np
from age_gender_model.wide_resnet import WideResNet

class ImageMetaExtractor():
    def __init__(self, weight_file, img_size, depth, width):
        self.weight_file = weight_file
        self.detector = dlib.get_frontal_face_detector()
        self.img_size = img_size
        self.depth = depth
        self.width = width
        self.model = self.load_model()
        self.model._make_predict_function()

    def load_img(self, image_path):
        img = cv2.imread(str(image_path), 1)
        if img is not None:
            h, w, _ = img.shape
            r = 640 / max(w, h)
            return cv2.resize(img, (int(w * r), int(h * r)))

    def load_img_original(self, image_path):
        img = cv2.imread(str(image_path), 1)
        return img;

    def load_model(self):
        model = WideResNet(self.img_size, depth=self.depth, k=self.width)()
        model.load_weights(self.weight_file)
        return model

    # dlib의 face_detector를 이용하여 얼굴을 detect한다
    def detect(self, img):
        input_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_h, img_w, _ = np.shape(input_img)

        # detect faces using dlib detector
        detected = self.detector(input_img, 1)
        faces = np.empty((len(detected), self.img_size, self.img_size, 3))
        return (detected, faces)

    def img_shape(self, img):
        input_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return np.shape(input_img)
    # img = self.load_img(image_path)
    def age_gender(self, img, margin=0.4):
        detected, faces = self.detect(img)
        img_h, img_w, _ = self.img_shape(img)
        if len(detected) > 0:
            for i, d in enumerate(detected):
                x1, y1, x2, y2, w, h = d.left(), d.top(), d.right() + 1, d.bottom() + 1, d.width(), d.height()
                xw1 = max(int(x1 - margin * w), 0)
                yw1 = max(int(y1 - margin * h), 0)
                xw2 = min(int(x2 + margin * w), img_w - 1)
                yw2 = min(int(y2 + margin * h), img_h - 1)
                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
                # cv2.rectangle(img, (xw1, yw1), (xw2, yw2), (255, 0, 0), 2)
                faces[i, :, :, :] = cv2.resize(img[yw1:yw2 + 1, xw1:xw2 + 1, :], (self.img_size, self.img_size))

            # predict ages and genders of the detected faces
            results = self.model.predict(faces)
            predicted_genders = results[0]
            ages = np.arange(0, 101).reshape(101, 1)
            predicted_ages = results[1].dot(ages).flatten()

            return (detected, predicted_genders, predicted_ages)
