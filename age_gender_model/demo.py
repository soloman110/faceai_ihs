from pathlib import Path
import cv2
import dlib
import numpy as np
import argparse
from contextlib import contextmanager
from age_gender_model.wide_resnet import WideResNet
from keras.utils.data_utils import get_file
import age_gender_model.ImageMetaExtractor as extractor

pretrained_model = "https://github.com/yu4u/age-gender-estimation/releases/download/v0.5/weights.28-3.73.hdf5"
modhash = 'fbe63257a054c1c5466cfd7bf14646d6'

def get_args():
    parser = argparse.ArgumentParser(description="This script detects faces from web cam input, "
                                                 "and estimates age and gender for the detected faces.",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--weight_file", type=str, default=None,
                        help="path to weight file (e.g. weights.28-3.73.hdf5)")
    parser.add_argument("--depth", type=int, default=16,
                        help="depth of network")
    parser.add_argument("--width", type=int, default=8,
                        help="width of network")
    parser.add_argument("--margin", type=float, default=0.4,
                        help="margin around detected face for age-gender estimation")
    parser.add_argument("--image_dir", type=str, default=None,
                        help="target image directory; if set, images in image_dir are used instead of webcam")
    parser.add_argument("--image_path", type=str, default=None,
                        help="target image path")
    args = parser.parse_args()
    return args


def draw_label(image, point, label, font=cv2.FONT_HERSHEY_SIMPLEX,
               font_scale=0.8, thickness=1):
    size = cv2.getTextSize(label, font, font_scale, thickness)[0]
    x, y = point
    cv2.rectangle(image, (x, y - size[1]), (x + size[0], y), (255, 0, 0), cv2.FILLED)
    cv2.putText(image, label, point, font, font_scale, (255, 255, 255), thickness, lineType=cv2.LINE_AA)
    return image

def main():
    args = get_args()
    weight_file = args.weight_file

    if not weight_file:
        weight_file = get_file("weights.28-3.73.hdf5", pretrained_model, cache_subdir="pretrained_models",
                               file_hash=modhash, cache_dir=str(Path(__file__).resolve().parent))

    metaExtractor = extractor.ImageMetaExtractor(weight_file, 64, args.depth, args.width)
    img = metaExtractor.load_img("/Users/sikongming/Downloads/test_image/1.jpg")
    detected, predicted_genders, predicted_ages = metaExtractor.age_gender(img)
    #결과를 가지고 처리한다
    for i, d in enumerate(detected):
        label = "{}, {}".format(int(predicted_ages[i]),
                                "M" if predicted_genders[i][0] < 0.5 else "F")
        draw_label(img, (d.left(), d.top()), label)
        print(label)
        cv2.imwrite('/tmp/1.jpg', img)
if __name__ == '__main__':
    main()
