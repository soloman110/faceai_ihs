from Exception.CustomException import CustomException

class NoneDetectException(CustomException):
    def __init__(self):
        super().__init__(self) #初始化父类
        self.errorinfo="Face info is not Detected by dlib"

    def __str__(self):
        return self.errorinfo