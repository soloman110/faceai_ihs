from utils.HttpUtil import HttpUtil as httputil
import json

API_SERVER_URL = 'http://0.0.0.0:8000/'

def imgpost():
    detail_info = {}
    #detail_info['imgid'] = metainfo.get('img').get('id')
    data = {
        'ftpid': '1'
    }
    imglist = []
    imginfo = {}
    imginfo['path'] = '2'
    imglist.append(imginfo)

    data['imglist'] = json.dumps(imglist)

    json_obj = httputil.urlPost(API_SERVER_URL + 'ftp/imginfo/', data)
    code = json_obj.get('code')
    msg = json_obj.get('msg')
    data = json_obj.get('data')
    print(code, msg, data)

if __name__ == '__main__':
    imgpost()

