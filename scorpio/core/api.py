from restapi import api, APIError
from .models import *
from django.utils.six import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import requests
import json
import qrcode


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
            if user.name and user.hotel_name:
                return {'url':'https://pinkslash.metatype.cn/customer_profile/{0}/'.format(user.id)}
            else:
                return {'url':'https://pinkslash.metatype.cn/mini_customer/save_message/{0}/'.format(user.id)}
        else:
            head_img = userInfo['userInfo']['avatarUrl']
            user = User.objects.create(union_id=unionid, head_img=head_img, event=event,status=0)

            print('user',user)
            qr = qrcode.make('http://pinkslash.metatype.cn/wechat_login/?status=sendcredits_{0}_{1}'.format(user.id, event.id))
            buf = BytesIO()
            qr.save(buf)
            qr_data = buf.getvalue()
            buf.write(qr_data)
            qr_img = InMemoryUploadedFile(file=buf,
                                          field_name=None,
                                          name='food.png',
                                          content_type='image/png',
                                          size=len(qr_data),
                                          charset=None)
            _user = User.objects.get(id=user.id)
            _user.qrcode = qr_img
            _user.save()

            print('_user',_user)

            return {'url':'https://pinkslash.metatype.cn/mini_customer/save_message/{0}/'.format(user.id)}

    else:
        return {'url':'https://pinkslash.metatype.cn/customer_profile/{0}/'.format(user.id)}



