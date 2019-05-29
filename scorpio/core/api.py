from restapi import api, APIError
from .models import *
import requests
import json

@api
def mini_login(code):
    print(code)
    appid = 'wx8c822d6f747d1e6a'
    secret = '2419917cec1c48a0e421a9e3513f754e'

    url = 'https://api.weixin.qq.com/sns/jscode2session?appid={0}&secret={1}&js_code={2}&grant_type=authorization_code'.format(appid, secret, code)
    res = requests.get(url)
    res = json.loads(res.text)

    print(res)
    # return code