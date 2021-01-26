import os
import cv2
import dlib
import meta_extractors.AgeGenderExtractor as ageGenderExtractor
import meta_extractors.EmotionExtractor as emotionExtractor
import utils.CommonUtils as commutil
from Exception.NoneDetectException import NoneDetectException

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
emotion_model_path = os.path.join(BASE_DIR, 'emotion_model', 'trained_models/fer2013_big_XCEPTION.54-0.66.hdf5')
agegender_model_path = os.path.join(BASE_DIR, '', "pretrained_models/weights.28-3.73.hdf5")

ageGenderMetaExtractor = ageGenderExtractor.AgeGenderExtractor(agegender_model_path, 64, 16, 8)
emotionMetaExtractor = emotionExtractor.EmotionExtractor(emotion_model_path)

detector = dlib.get_frontal_face_detector()

def age_gender_emotion(img_path):
    if not commutil.isImage(img_path):
        return []
    img_color = load_img_color(img_path)
    detected = detect(img_color)
    if len(detected) == 0:
        raise NoneDetectException()


    predicted_genders, predicted_ages = ageGenderMetaExtractor.extract(img_color, detected)
    predicted_emotions = emotionMetaExtractor.extract(img_color, detected)
    # 결과를 가지고 처리한다
    estimated_list = []
    for i, d in enumerate(detected):
        gender = "M" if predicted_genders[i][0] < 0.5 else "F"
        age = int(predicted_ages[i])
        emotion = predicted_emotions[i]
        estimated_list.append({'age': age, 'gender': gender, 'emotion': emotion})
    return estimated_list


def load_img_color(image_path):
    img = cv2.imread(str(image_path), 1)
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img;

# dlib의 face_detector를 이용하여 얼굴을 detect한다
def detect(img):
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    detected = detector(img_rgb, 1)
    return detected

