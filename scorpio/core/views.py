import qrcode
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.six import BytesIO
from team.decorators import user_required
from django.views.decorators.csrf import csrf_exempt
from .models import *

import requests
import json
import hashlib
import urllib.parse
import string
import random
import time

def get_foods(request, pid):
    ctx = {}
    provider = User.objects.filter(id=pid).first()
    foods = Food.objects.filter(provider=provider)
    ctx['foods'] = foods
    ctx['provider_id'] = pid
    return render(request, 'foods.html', ctx)


def get_provider_info(request, pid):
    ctx = {}
    provider = User.objects.filter(id=pid).first()
    credits_list = History.objects.filter(user=provider)
    sum = 0
    for item in credits_list:
        sum = sum + int(item.credit)
    provider.credits_total = sum

    ctx['provider'] = provider
    return render(request, 'provider-profile.html', ctx)


def get_credit_list(request, pid):
    ctx = {}
    provider = User.objects.filter(id=pid).first()
    credits_list = History.objects.filter(user=provider)
    sum = 0
    for item in credits_list:
        sum = sum + int(item.credit)
    ctx['credits_list'] = credits_list
    ctx['total_credit'] = sum
    return render(request, 'provider-credits.html', ctx)


def customer_profile(request, user_id):
    """
    顾客首页
    """
    ctx = {}
    user = User.objects.filter(pk=user_id).first()
    ctx['user'] = user
    return render(request, 'customer-profile.html', ctx)

@user_required
def add_favorite(request, me):
    """
    添加喜欢food
    """
    user_id = request.GET['user_id']
    food_id = request.GET['food_id']
    favorite = Favorite()
    favorite.user_id = user_id
    favorite.food_id = food_id
    favorite.save()
    return redirect('/foods/')


@user_required
def last_supper(request, me):
    last_food = LastFood.objects.filter(event_id=me.event_id)
    ctx = {'last_foods': last_food}
    return render(request, 'last-supper.html', ctx)

@user_required
def credit_history(request, me):
    histories = History.objects.filter(user_id=me.id).order_by('-create_time')
    ctx = {
        'histories': histories,
        'me': me
    }
    return render(request, 'customer-credits.html', ctx)

@user_required
def pay_success(request, me):
    ctx = {
        'me':me
    }

    return render(request, 'pay-success.html', ctx)

@user_required
def pay_failed(request, me):
    ctx = {
        'me':me
    }

    return render(request, 'pay-failed.html', ctx)



def wechat_login(request):
    full_path = request.get_full_path()

    if 'code' in full_path:

        code = request.GET.get('code')
        user_data = wechat_api(code)

        nickname = user_data['nickname']
        union_id = user_data['union_id']
        head_img = user_data['head_img']

        user = User.objects.filter(union_id=union_id).first()

        status = request.GET.get('status')

        if user:
            request.session['uid'] = user.id
            if user.status == 1:
                if 'purchase' in full_path:
                    return HttpResponse("Food providers cannot buy food")

                return redirect('/get_provider_info/{0}/'.format(user.id))
            elif user.status == 0:
                if 'purchase' in full_path:
                    food_id = status.split('_')[2]
                    food = Food.objects.filter(id=food_id).first()
                    if user.credit >= food.credit:
                        user.credit -= food.credit
                        user.save()
                        provider = food.provider
                        provider.credit += food.credit
                        provider.save()

                        History.objects.create(user=user, credit='-{0}'.format(str(food.credit)), desc='Buying Food')
                        History.objects.create(user=provider, credit='+{0}'.format(str(food.credit)), desc='Selling Food')

                        return redirect('/pay_success')
                    else:
                        return redirect('/pay_failed')

                try:
                    credit = status.split('_')[2]
                except:
                    return HttpResponse('Customers cannot log in as food providers')

                user.credit += int(credit)
                user.save()
                History.objects.create(user=user, credit='+{0}'.format(str(credit)), desc='Scanning QRCode')

                return redirect('/customer_profile/{0}/'.format(user.id))
        else:
            event_id = status.split('_')[1]
            event = Event.objects.filter(id=int(event_id)).first()

            if 'provider' in full_path:
                user = User.objects.create(name=nickname, nickname=nickname, username=nickname, password='123456', union_id=union_id, head_img=head_img,
                                           status=1, event=event)
                request.session['uid'] = user.id
                return redirect('/get_provider_info/{0}/'.format(user.id))

            elif 'customer' in full_path:
                credit = status.split('_')[2]
                user = User.objects.create(
                    name=nickname, union_id=union_id,
                    head_img=head_img, status=0,
                    event=event, credit=int(credit))
                History.objects.create(user=user, credit='+{0}'.format(str(credit)), desc='Scanning QRCode')
                request.session['uid'] = user.id
                return redirect('/customer_profile/{0}/'.format(user.id))
            elif 'purchase' in full_path:
                return HttpResponse("Please get the credits before you buy them")
    else:

        redirect_uri = 'http://pinkslash.metatype.cn' + full_path
        get_code_url = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=wxc7594d7d49e0235f&redirect_uri=" + redirect_uri + "&response_type=code&scope=snsapi_userinfo";
        return redirect(get_code_url)

    return HttpResponse("xixi")


def wechat_api(code):
    appid = 'wxc7594d7d49e0235f'
    secret = 'ebbda5cbab00241032bc936fe3839393'
    # 获取access_token、openid
    access_token_params = {
        'appid': appid,
        'secret': secret,
        'code': code,
        'grant_type': 'authorization_code'
    }
    get_access_token_url = 'https://api.weixin.qq.com/sns/oauth2/access_token'
    response = requests.get(url=get_access_token_url, params=access_token_params)
    response.encoding = 'utf-8'

    response = json.loads(response.text)

    access_token = response['access_token']
    openid = response['openid']
    # 获取用户信息
    get_user_info_url = 'https://api.weixin.qq.com/sns/userinfo'
    user_info_params = {
        'access_token': access_token,
        'openid': openid
    }
    res = json.loads(requests.get(url=get_user_info_url, params=user_info_params).text)
    print(res)
    openid = res['openid']
    nickname = res['nickname'].encode('raw_unicode_escape').decode()
    headimgurl = res['headimgurl']
    user_data = {
        'nickname': nickname,
        'union_id': openid,
        'head_img': headimgurl,
    }

    return user_data

@user_required
def add_favorite(request, me, food_id):
    user_id = me.id
    favo_food = Favorite.objects.filter(food_id=food_id).first()
    if favo_food is None:
        Favorite.objects.create(
            food_id=food_id,
            user_id=user_id
        )
    else:
        Favorite.objects.filter(food_id=food_id).delete()
    return redirect('/reservation_list')


@user_required
def reservation_list(request, me):

    eid = me.event_id
    foods = Food.objects.filter(event_id=eid)
    favo_foods = Favorite.objects.filter(user_id=me.id)
    favo_ids = []
    for favo_food in favo_foods:
        favo_ids.append(favo_food.food_id)
    ctx = {
        'foods': foods,
        'favo_ids': favo_ids
    }
    return render(request, 'reservation.html', ctx)


@user_required
def room_amenity(request, me):

    packages = RoomAmenity.objects.filter(event=me.event)
    ctx = {
        'packages': packages
    }

    return render(request, 'packages.html', ctx)


@user_required
def lunch(request, me):

    packages = Lunch.objects.filter(event=me.event)
    ctx = {
        'packages': packages
    }
    return render(request, 'packages.html', ctx)



@user_required
def room_amenity_detail(request, me, room_amenity_id):

    room_amenity = RoomAmenity.objects.filter(id=room_amenity_id).first()
    roomAmenityReserve = RoomAmenityReservation.objects.filter(user=me, roomAmenity=room_amenity).first()
    ctx = {
        'room_amenity':room_amenity
    }
    if roomAmenityReserve:
        ctx['status'] = 1
    else:
        ctx['status'] = 0

    return render(request, 'room-amenity-detail.html', ctx)

@user_required
def lunch_detail(request, me, lunch_id):
    lunch = Lunch.objects.filter(id=lunch_id).first()
    ctx = {
        'lunch':lunch
    }
    lunchReservation = LunchReservation.objects.filter(user=me, lunch=lunch).first()
    if lunchReservation:
        ctx['status'] = 1
    else:
        ctx['status'] = 0

    return render(request, 'lunch-detail.html', ctx)

@user_required
def lunch_reserve(request, me, lunch_id):

    lunch = Lunch.objects.filter(id=lunch_id).first()
    lunchReservation = LunchReservation.objects.filter(user=me, lunch=lunch).first()
    if not lunchReservation:
        LunchReservation.objects.create(user=me, lunch=lunch)

    ctx = {
        'lunch':lunch,
        'status':1
    }
    return render(request, 'lunch-detail.html', ctx)

@user_required
def room_amenity_reserve(request, me, room_amenity_id):
    room_amenity = RoomAmenity.objects.filter(id=room_amenity_id).first()
    roomAmenityReserve = RoomAmenityReservation.objects.filter(user=me, roomAmenity=room_amenity).first()
    if not roomAmenityReserve:
        RoomAmenityReservation.objects.create(user=me, roomAmenity=room_amenity)

    ctx = {
        'room_amenity':room_amenity,
        'status':1
    }

    return render(request, 'lunch-detail.html', ctx)

def getticket(request):

    current_url =  request.POST.get('current_url', '')

    appid = 'wxc7594d7d49e0235f'
    secret = 'ebbda5cbab00241032bc936fe3839393'
    access_token_params = {
        'appid': appid,
        'secret': secret,
        'grant_type': 'client_credential'
    }
    get_access_token_url = 'https://api.weixin.qq.com/cgi-bin/token'

    response = requests.get(url=get_access_token_url, params=access_token_params)
    response.encoding = 'utf-8'
    response = json.loads(response.text)
    print('response', response)
    access_token = response['access_token']
    get_jsapi_ticket_url = 'https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token={0}&type=jsapi'.format(access_token)

    jsapi_response = requests.get(url=get_jsapi_ticket_url)
    jsapi_response.encoding = 'utf-8'
    jsapi_response = json.loads(jsapi_response.text)
    jsapi_ticket = jsapi_response['ticket']

    noncestr = ''.join(random.sample(string.ascii_letters + string.digits, 8))

    timestamp = int(time.time())

    string1 = 'jsapi_ticket={0}&noncestr={1}&timestamp={2}&url={3}'.format(jsapi_ticket, noncestr, timestamp, current_url)
    signature = hashlib.sha1(string1.encode('utf-8')).hexdigest()

    params = {
        'appId': appid,
        'timestamp': timestamp,
        'nonceStr': noncestr,
        'signature': signature,
    }

    return HttpResponse(json.dumps(params), content_type='application/json')
