import logging
import os
from logging import handlers

MONITOR = False
BACKCNT = 7
ALL_LOG_FOLD = "/svc/ihs_log"
ERROR_LOG_FOLD = "/svc/ihs_log"
ROOT_LEVEL = "info"
FORMAT_STR = "%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s"

class Logger(object):
    level_relations = {
        'debug':logging.DEBUG,
        'info':logging.INFO,
        'warning':logging.WARNING,
        'error':logging.ERROR,
        'crit':logging.CRITICAL
    }

    def __init__(self, logger=None, backCount=7):
        self.init_log_file()
        self.logger = logging.getLogger(logger)
        format = logging.Formatter(FORMAT_STR)#Logger 포맷
        self.logger.setLevel(self.level_relations.get(ROOT_LEVEL))#Logger Level 설정

        '''
          #file에 출력 시 지정된 시간간격으로 자동으로 파일 생성 및 삭제
          backCount: 백업 파일 개수, 개수를 초과하면 자공 삭제됨
          when: 시간 간격:
              # S 초
              # M 분
              # H 한시간
              # D 하루
              # W 1주（interval==0 는 월요일）
              # midnight 매일 새벽 0시
          '''
        #모든 메시지를 처리하는 Handler
        all_file_handler = handlers.TimedRotatingFileHandler(filename=ALL_LOG_FOLD + '/all.log', when='midnight',backupCount=BACKCNT, encoding='utf-8')
        all_file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

        #Error 메시지를 처리하는 Handler
        error_file_handler = handlers.TimedRotatingFileHandler(filename=ERROR_LOG_FOLD + '/error.log', when='midnight',backupCount=BACKCNT, encoding='utf-8')
        error_file_handler.setLevel(logging.ERROR)
        error_file_handler.setFormatter(format)

        #모니터로 출력하는 Handler
        #monitor_handler = logging.StreamHandler()  # Monitor에 출력
        #monitor_handler.setFormatter(format)  # Monitor에 출련하는 포맷

        #Handler 추가
        #if MONITOR:
        #    self.logger.addHandler(monitor_handler)
        self.logger.addHandler(all_file_handler)
        self.logger.addHandler(error_file_handler)

    def init_log_file(self):
        if not os.path.exists(ERROR_LOG_FOLD):
            os.mkdir(ERROR_LOG_FOLD)
        if not os.path.exists(ALL_LOG_FOLD):
            os.mkdir(ALL_LOG_FOLD)

    def getlog(self):
        return self.logger