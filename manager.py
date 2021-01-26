import json
import time
import multiprocessing
import threading
from utils.HttpUtil import HttpUtil as httputil
from utils.ImgMetaUtil import *
from logger.Logger import Logger as Logger

API_SERVER_URL = 'http://127.0.0.1:8002/'
Log = Logger(__name__).getlog()

class Task(object):

    def __init__(self, imginfo):
        self.imginfo = imginfo

    def __call__(self):
        result = {}
        result["token"] = self.imginfo.get('token')

        metainfos = []
        for img in self.imginfo.get('imglist'):
            path = img.get('path')
            estimated_list = []
            try:
                Log.info("[TASK_INO] token: %s, img: %s", self.imginfo.get('token'), img)
                estimated_list = age_gender_emotion(path)
            except NoneDetectException as e:
                Log.error("[ERROR_TYPE]: %s [ERROR_INFO]: %s IMG: %s ", 'NoneDetectException', e, img)
            except Exception as e:
                Log.error("[ERROR_TYPE]: %s, IMG: %s ERROR_INFO: %s", 'RuntimeException',  e, img)
            metainfo = {}
            metainfo['img'] = img
            metainfo['estimated_list'] = estimated_list
            metainfos.append(metainfo)

        result["metainfos"] = metainfos
        return result

    def __str__(self):
        return 'token: %s  imginfos: %s' % (self.imginfo.get('token'), json.dumps(self.imginfo))

class TaskProducer(threading.Thread):

    def __init__(self, taskqueue, name=None):
        threading.Thread.__init__(self, target=None, name=name, daemon=True)
        self.taskqueue = taskqueue

    def run(self):
        while True:
            try:
                time.sleep(0.5)
                self.taskqueue.join() #Task가 다 처리될때 까지 대기
                task_list = self.request_tasks(20) #Api서버를 요청하여 이미지 정보를 가져온다
                for taskInfo in task_list:
                    self.taskqueue.put(Task(taskInfo), block=True, timeout=None) #Task queue가 꽉차 있으면 기다린다
            except Exception as e:
                Log.error("task_producer ERROR_INFO: %s", e)

    def request_tasks(self, limit):
        task_list = []
        try:
            limit = str(limit)
            task_result = json.loads(httputil.urlGet(API_SERVER_URL + 'ftp/tasks?limit={0}'.format(limit)))
            code = task_result.get('code')
            if code == 200:
                task_list = task_result.get('data')
        except Exception as e:
            Log.error("request_tasks ERROR_INFO: %s", e)
        return task_list

class TaskConsumer():

    def __init__(self, task_queue, result_queue):
        self.task_queue = task_queue
        self.result_queue = result_queue

    def run(self):
        while True:
            next_task = self.task_queue.get(block=True, timeout=None)
            if next_task is not None:
                try:
                    result = next_task()
                    self.result_queue.put(result)
                except Exception as e:
                    Log.error("TaskConsumer taskinfo: %s, ERROR_INFO: %s", json.dumps(next_task.imginfo), e)
                finally:
                    self.task_queue.task_done() # queue size -1; queue size가 0일따 join이 풀린다..
        return

class ResultProcessor(threading.Thread):

    def __init__(self, resultqueue, name=None):
        threading.Thread.__init__(self, target=None, name=name, daemon=True)
        self.resultqueue = resultqueue

    def run(self):
        while True:
            try:
                result = self.resultqueue.get(block=True, timeout=None)
                metainfos = []
                for metainfo in result.get('metainfos'):
                    detail_info = {}
                    detail_info['imgid'] = metainfo.get('img').get('id')
                    detail_info['imgpath'] = metainfo.get('img').get('path')
                    detail_info['estimated_list'] = metainfo.get('estimated_list')
                    metainfos.append(detail_info)

                json_obj = httputil.urlPost(API_SERVER_URL + 'metainfo/', {
                    'token': result.get('token'),
                    'metainfos': metainfos
                })
                code = json_obj.get('code')
                msg = json_obj.get('msg')
                data = json_obj.get('data')
                Log.info("[RESULT_INO] token: %s, code: %s, msg: %s", result.get('token'), code, msg)
            except Exception as e:
                Log.error("result_hanlder, ERROR_INFO: %s", e)

def start():
    task_queue = multiprocessing.JoinableQueue(100)
    result_queue = multiprocessing.Queue()

    # 1. 할일을 가져오는 일꾼을 생성(Api를 요청하여 미처리된 Task정보들 얽어온 후 Queue에다 둔다)
    taskProducer = TaskProducer(task_queue)
    taskProducer.start()

    # 2. 결과 값을 처리하는 일꾼을 생성
    result_thread_cout = 3
    for i in range(result_thread_cout):
        result_handler = ResultProcessor(result_queue)
        result_handler.start()

    # 3 이미지를 처리하는 Consumer생성
    imgHandler = TaskConsumer(task_queue, result_queue)
    imgHandler.run()

if __name__ == '__main__':
    start()
