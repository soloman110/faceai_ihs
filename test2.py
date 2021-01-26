import json
import time
from utils.ImgMetaUtil import *
from utils.Logger import *

logger = init_logger("result.log")

if __name__ == '__main__':
    test_minutes = 10 #테스트할 시간(분)
    count = 0   #테스트 한 이미지의 총 개수
    duration = 0 #테스트한 기간
    time_start = time.time() #시작 시간
    time_end = test_minutes * 60 #종료 시간

    path = "/home/uftp/tps_test/640-480.jpg" #이미지 경로
    path = "/tmp/640-480.jpg" #이미지 경로
    path = "/tmp/img_test/27_M_neutral.jpg" #이미지 경로

    cnt_segment = {} #분 당 처리된 개수 기록
    segment = 1 #테스트 기간 단위 (분)
    prew_segment_cnt = 0
    while duration <= time_end:
        duration = time.time() - time_start
        estimated_list = age_gender_emotion(path)
        print(json.dumps(estimated_list))
        count = count + 1

        if duration > 60 * segment:
            cnt_segment[segment] = count - prew_segment_cnt
            prew_segment_cnt = count
            segment = segment +1

    print(cnt_segment)

