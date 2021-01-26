import cv2
import numpy as np

from age_gender_model.wide_resnet import WideResNet
from meta_extractors.ImageMetaExtractorBase import ImageMetaExtractorBase

class AgeGenderExtractor(ImageMetaExtractorBase):
    def __init__(self, weight_file, img_size, depth, width):
        super().__init__()
        self.weight_file = weight_file
        self.img_size = img_size
        self.depth = depth
        self.width = width
        self.model = self.load_model()
        self.model._make_predict_function()

    def load_model(self):
        model = WideResNet(self.img_size, depth=self.depth, k=self.width)()
        model.load_weights(self.weight_file)
        return model

    def extract(self, img_color, detected):
        img_rgb = cv2.cvtColor(img_color, cv2.COLOR_BGR2RGB)
        faces = np.empty((len(detected), self.img_size, self.img_size, 3))
        img_h, img_w, _ = self.img_shape(img_rgb)

        if len(detected) > 0:
            for i, d in enumerate(detected):
                x1, y1, x2, y2, w, h = d.left(), d.top(), d.right() + 1, d.bottom() + 1, d.width(), d.height()
                yw1, yw2, xw1, xw2 = self.process_margin(d, img_h, img_w)
                cv2.rectangle(img_color, (x1, y1), (x2, y2), (255, 0, 0), 2)
                faces[i, :, :, :] = cv2.resize(img_color[yw1:yw2 + 1, xw1:xw2 + 1, :], (self.img_size, self.img_size))

            # predict ages and genders of the detected faces
            results = self.model.predict(faces)
            predicted_genders = results[0]
            ages = np.arange(0, 101).reshape(101, 1)
            predicted_ages = results[1].dot(ages).flatten()

            return (predicted_genders, predicted_ages)

    def process_margin(self, d, img_h, img_w, margin=0.4):
        x1, y1, x2, y2, w, h = d.left(), d.top(), d.right() + 1, d.bottom() + 1, d.width(), d.height()
        xw1 = max(int(x1 - margin * w), 0)
        yw1 = max(int(y1 - margin * h), 0)
        xw2 = min(int(x2 + margin * w), img_w - 1)
        yw2 = min(int(y2 + margin * h), img_h - 1)
        return (yw1, yw2, xw1, xw2)

