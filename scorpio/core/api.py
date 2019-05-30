from restapi import api, APIError
from .models import *
import requests
import json

@api
def mini_login(status, code, userInfo):
    appid = 'wx8c822d6f747d1e6a'
    secret = '2419917cec1c48a0e421a9e3513f754e'
    url = 'https://api.weixin.qq.com/sns/jscode2session?appid={0}&secret={1}&js_code={2}&grant_type=authorization_code'.format(appid, secret, code)
    res = requests.get(url)
    res = json.loads(res.text)
    unionid = res['unionid']
    user = User.objects.filter(union_id=unionid).first()


    print('code',code)
    print('userInfo',userInfo)
    print('res',res)
    print('status',status)

    event = Event.objects.all().first()
    if status == 'firstLogin':
        if user:
            return {'url':'https://pinkslash.metatype.cn/customer_profile/{0}/'.format(user.id)}
        else:
            head_img = userInfo['avatarUrl']
            user = User.objects.create(union_id=unionid, head_img=head_img, event=event)
            return {'url':'https://pinkslash.metatype.cn/mini_customer/save_message/{0}/'.format(user.id)}

    else:
        return {'url':'https://pinkslash.metatype.cn/customer_profile/{0}/'.format(user.id)}



