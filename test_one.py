import json
import time
from utils.ImgMetaUtil import *
from utils.Logger import *
import os

logger = init_logger("result.log")

if __name__ == '__main__':
    test_minutes = 2 #테스트할 시간(분)
    count = 0   #테스트 한 이미지의 총 개수
    duration = 0 #테스트한 기간

    g = os.walk("/tmp/img_test1")

    for path, dir_list, file_list in g:
        for file_name in file_list:
            #print(os.path.join(path, file_name))
            try:
                estimated_list = age_gender_emotion(os.path.join(path, file_name))
                print(file_name, json.dumps(estimated_list))
            except Exception as e:
                print(file_name, e, "EEEEE")

    path = "/tmp/640-480.jpg" #이미지 경로
    #path = "/tmp/img_test/obama_52_M_neutral.png"  # 이미지 경로

    #estimated_list = age_gender_emotion(path)
    #print(json.dumps(estimated_list))

