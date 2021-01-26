
import http.client as httplib
import urllib
import urllib.request as urllib2
import requests
import json
#https://blog.csdn.net/shuhui018125/article/details/95978190
class HttpUtil:
    #使用 httplib
    @staticmethod
    def get(ip,url):
        conn = httplib.HTTPConnection(ip)
        conn.request('GET',url)
        result = conn.getresponse()
        resultContent = result.read()
        conn.close()
        return resultContent

    # urllib2를 사용
    @staticmethod
    def urlGet(url):
        req = urllib2.Request(url)
        res_data = urllib2.urlopen(req)
        res = res_data.read()
        return res

    @staticmethod
    def requestGet(url,params):
        res = requests.get(url, params)
        return res.text

    @staticmethod
    def post(ip,url,params):
        headers = {'Content-type': 'application/x-www-form-urlencoded', 'Accept': 'text/plain'}
        conn = httplib.HTTPConnection(ip)
        test_data_urlencode = urllib.parse.urlencode(params)
        conn.request('POST', url, test_data_urlencode,headers)
        result = conn.getresponse()
        resultContent = result.read()
        conn.close()
        return resultContent

    @staticmethod
    def urlPost(url,params):
        from urllib import request, parse
        data = parse.urlencode(params).encode()
        req = request.Request(url, data = data)  # this will make the method "POST"
        resp = request.urlopen(req)

        string = resp.read().decode('utf-8')
        json_obj = json.loads(string)
        return json_obj

    @staticmethod
    def requestPost(url,params):
        res = requests.get(url, params)
        return res.text