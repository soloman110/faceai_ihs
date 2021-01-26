import cv2
import numpy as np
from keras.models import load_model
from emotion_model.utils.preprocessor import preprocess_input
from emotion_model.utils.datasets import get_labels
from meta_extractors.ImageMetaExtractorBase import ImageMetaExtractorBase

class EmotionExtractor(ImageMetaExtractorBase):

    def __init__(self, emotion_model_path):
        super().__init__()
        self.emotion_labels = get_labels('fer2013')
        self.emotion_classifier = load_model(emotion_model_path, compile=False)

    def extract(self, img_color, detected):
        emotion_target_size = self.emotion_classifier.input_shape[1:3]
        estimated_list = []
        for i, d in enumerate(detected):
            x1, y1, x2, y2, w, h = d.left(), d.top(), d.right() + 1, d.bottom() + 1, d.width(), d.height()
            try:
                gray_image = cv2.cvtColor(img_color, cv2.COLOR_RGBA2GRAY) #이미지를 회색으로 변경
                gray_face = gray_image[y1:y2, x1:x2]    #얼굴 부분 추출
                gray_face = cv2.resize(gray_face, (emotion_target_size)) #이미지를 리사아즈
            except Exception as e:
                print(e)
                estimated_list.append("UNKNOWN")
                continue
            gray_face = preprocess_input(gray_face, True)
            gray_face = np.expand_dims(gray_face, 0)
            gray_face = np.expand_dims(gray_face, -1)
            emotion_label_arg = np.argmax(self.emotion_classifier.predict(gray_face))
            emotion_text = self.emotion_labels[emotion_label_arg]
            estimated_list.append(emotion_text)

        return estimated_list