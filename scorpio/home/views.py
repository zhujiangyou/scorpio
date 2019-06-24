from django.shortcuts import render

# Create your views here.
import qrcode
from django.utils.six import BytesIO
from django.shortcuts import render, redirect, HttpResponse
from django.core.files.uploadedfile import InMemoryUploadedFile
from team.decorators import user_required
from core.models import *
from django.core import serializers
from django.core.paginator import Paginator
import json

@user_required
def home(request, me):
    if me:
        if me.status == 1:
            ctx = {
                'me': me,
                'menu': 'home',
                'breadcrumb': [
                    ('Dashboard',
                     'home')],
                'title': 'Dashboard',
                'subtitle': 'food provider'}
        else:
            ctx = {
                'me': me,
                'menu': 'home',
                'breadcrumb': [
                    ('Dashboard',
                     'home')],
                'title': 'Dashboard',
                'subtitle': 'host'}

        return render(request, 'home.html', ctx)

    return redirect('login')


@user_required
def events(request, me):
    page = request.GET.get('page')
    ctx = {
        'me': me,
        'menu': 'event', 'submenu': 'events',
        'breadcrumb': [('Events', 'events')],
        'title': 'Events', 'subtitle': 'all events',
    }
    ctx['messages'] = messages = []
    ctx['errors'] = errors = []
    ctx['events'] = Event.objects.all()

    paginator = Paginator(ctx['events'], 5)
    if not page:
        page = 1
    ctx['pager'] = paginator.page(page)

    return render(request, 'team/events.html', ctx)


@user_required
def last_foods(request, me):
    # eid = me.event.id
    eid = request.GET.get('eid')
    page = request.GET.get('page')
    ctx = {
        'me': me,
        'menu': 'last_foods', 'submenu': 'last_foods',
        'breadcrumb': [('LastFoods', 'last_foods')],
        'title': 'LastFoods', 'subtitle': 'all last_foods',
    }
    ctx['messages'] = messages = []
    ctx['errors'] = errors = []
    ctx['last_food'] = LastFood.objects.filter(event_id=eid)

    paginator = Paginator(ctx['last_food'], 5)
    if not page:
        page = 1
    ctx['pager'] = paginator.page(page)
    ctx['eid'] = eid

    return render(request, 'team/last_foods.html', ctx)


@user_required
def foods(request, me):
    eid = request.GET.get('eid')
    event = Event.objects.filter(id=eid).first()
    page = request.GET.get('page', 1)
    ctx = {
        'me': me,
        'menu': 'food', 'submenu': 'foods',
        'breadcrumb': [('Food', 'foods')],
        'title': 'Foods', 'subtitle': 'all foods',
    }
    ctx['messages'] = messages = []
    ctx['errors'] = errors = []

    if me.status == 1:
        ctx['foods'] = foods = Food.objects.filter(provider=me)
    elif me.status == 2:
        ctx['foods'] = foods = Food.objects.filter(event=event)
    else:
        ctx['foods'] = foods = []

    ctx['eid'] = eid
    paginator = Paginator(ctx['foods'], 5)

    ctx['pager'] = pager = paginator.get_page(page)
    ctx['foods'] = foods[pager.start_index() - 1 if pager.start_index() else 0:pager.end_index()]

    return render(request, 'team/foods.html', ctx)


@user_required
def customers(request, me):
    page = request.GET.get('page')
    eid = request.GET.get('eid')
    ctx = {
        'me': me,
        'menu': 'customer', 'submenu': 'customers',
        'breadcrumb': [('Customer', 'customers')],
        'title': 'Customers', 'subtitle': 'all customers',
    }
    ctx['messages'] = messages = []
    ctx['errors'] = errors = []

    if me.status == 1:
        ctx['customers'] = User.objects.filter(event_id=eid)
    if me.status == 2:
        ctx['customers'] = User.objects.all()

    ctx['eid'] = eid
    paginator = Paginator(ctx['customers'], 5)

    ctx['pager'] = paginator.page(page)

    return render(request, 'team/customers.html', ctx)


@user_required
def delete_food(request, me):
    page = request.GET.get('page')
    eid = request.GET.get('eid')
    fid = request.GET.get('fid')
    ctx = {
        'me': me,
        'menu': 'food', 'submenu': 'foods',
        'breadcrumb': [('Food', 'foods')],
        'title': 'Foods', 'subtitle': 'all foods',
    }
    ctx['messages'] = messages = []
    ctx['errors'] = errors = []

    ctx['foods'] = []
    Food.objects.filter(id=fid).delete()

    return redirect('/foods/?eid={eid}&page={page}'.format(eid=eid, page=page))


@user_required
def delete_last_food(request, me):
    page = request.GET.get('page')
    eid = request.GET.get('eid')
    lfid = request.GET.get('lfid')
    ctx = {
        'me': me,
        'menu': 'last_food', 'submenu': 'last_food',
        'breadcrumb': [('LastFood', 'last_food')],
        'title': 'last_food', 'subtitle': 'all last_food',
    }
    ctx['messages'] = messages = []
    ctx['errors'] = errors = []

    LastFood.objects.filter(id=lfid).delete()

    return redirect('/last_foods/?eid={eid}&page={page}'.format(eid=eid, page=page))

@user_required
def data_report(request, me):
    ctx = {
        'me': me,
        'menu': 'report', 'submenu': 'report',
        'breadcrumb': [('DATA REPORT', 'report')],
        'title': 'DATA REPORT', 'subtitle': 'report',
    }

    ctx['all_users'] = User.objects.filter(status=0)
    users = User.objects.filter(status=0).order_by('credit')
    if users.count() < 20:
        ctx['top_user_names'] = json.dumps(list(users.values_list('name', flat=True))[::-1])
        ctx['top_user_credits'] = json.dumps(list(users.values_list('credit', flat=True))[::-1])
    else:
        ctx['top_user_names'] = json.dumps(list(users[0:20].values_list('name', flat=True))[::-1])
        ctx['top_user_credits'] = json.dumps(list(users[0:20].values_list('credit', flat=True))[::-1])


    foods = Food.objects.all()

    ctx['food_names'] = []
    ctx['counts'] = []
    ctx['foods'] = []
    for _ in foods:
        count = UserFood.objects.filter(food=_).count()
        if count >= 1:
            ctx['food_names'].append(_.name)
            ctx['counts'].append(count)
            ctx['foods'].append(_)

    return render(request, 'team/dashboard.html', ctx)

@user_required
def countdown(request, me):
    ctx = {
        'me': me,
        'menu': 'report', 'submenu': 'report',
        'breadcrumb': [('DATA REPORT', 'report')],
        'title': 'DATA REPORT', 'subtitle': 'report',
    }


    users = User.objects.filter(status=0).order_by('-credit')
    ctx['all_users'] = User.objects.filter(status=0)
    if users.count() < 20:
        ctx['top_user_names'] = json.dumps(list(users.values_list('name', flat=True))[::-1])
        ctx['top_user_credits'] = json.dumps(list(users.values_list('credit', flat=True))[::-1])
    else:
        ctx['top_user_names'] = json.dumps(list(users[0:20].values_list('name', flat=True))[::-1])
        ctx['top_user_credits'] = json.dumps(list(users[0:20].values_list('credit', flat=True))[::-1])
        # ctx['countdown'] = users[0:20]


    foods = Food.objects.all()

    ctx['food_names'] = []
    ctx['counts'] = []
    ctx['foods'] = []

    for _ in foods:
        count = UserFood.objects.filter(food=_).count()
        if count >= 1:
            ctx['food_names'].append(_.name)
            ctx['counts'].append(count)
            ctx['foods'].append(_)

    # ctx['foods'] = foods


    return render(request, 'team/dashboard.html', ctx)


@user_required
def user_detail(request, me, user_id):
    ctx = {
        'me': me,
        'menu': 'report', 'submenu': 'report',
        'breadcrumb': [('DATA REPORT', 'report')],
        'title': 'DATA REPORT', 'subtitle': 'report',
    }

    user = User.objects.filter(id=user_id).first()
    userfoods = UserFood.objects.filter(user=user) #扫了食物生成的记录 desc:扫了食物二维码

    usercredits = UserCredit.objects.filter(user=user) #该用户扫了积分二维码生成的记录

    usersans = UserScan.objects.filter(user=user) #该用户扫了一次只能扫一次的二维码的记录

    # ctx['user_report'] = []

    # for _ in userfoods:
    #     ctx['user_report'].append(_.create_time)
    #     ctx['user_report'].append('扫了积分二维码')
    #     ctx['user_report'].append(-(_.food.credit))

    ctx['user_report'] = []

    for _ in userfoods:
        user_dict = {'create_time':_.create_time,'user_desc':'扫了食物二维码','user_credits':-(_.food.credit)}
        ctx['user_report'].append(user_dict)

    for _ in usercredits:
        user_dict = {'create_time':_.create_time,'user_desc':'扫了积分二维码','user_credits':+int(float(_.credit))}
        ctx['user_report'].append(user_dict)

    for _ in usersans:
        user_dict = {'create_time':_.create_time,'user_desc':'扫了一次性积分二维码','user_credits':+(_.credit.credit)}
        ctx['user_report'].append(user_dict)


    return render(request, 'team/user_detail.html',ctx)


@user_required
def food_detail(request, me, food_id):
    ctx = {
        'me': me,
        'menu': 'report', 'submenu': 'report',
        'breadcrumb': [('DATA REPORT', 'report')],
        'title': 'DATA REPORT', 'subtitle': 'report',
    }


    food = Food.objects.filter(id=food_id).first()
    userfoods = UserFood.objects.filter(food=food)

    ctx['food_report'] = []
    for userfood in userfoods:
        ctx['food_report'].append({'food_name':food.name,"buyer":userfood.user.name})

    return render(request, 'team/food_detail.html', ctx)

@user_required
def delete_event(request, me):
    eid = request.GET.get('eid')
    ctx = {
        'me': me,
        'menu': 'event', 'submenu': 'events',
        'breadcrumb': [('Events', 'events')],
        'title': 'Events', 'subtitle': 'all events',
    }
    ctx['messages'] = messages = []
    ctx['errors'] = errors = []

    ctx['events'] = []
    Event.objects.filter(id=eid).delete()

    return redirect('/events/')


@user_required
def delete_customer(request, me):
    eid = request.GET.get('eid')
    page = request.GET.get('page')
    uid = request.GET.get('uid')
    ctx = {
        'me': me,
        'menu': 'customer', 'submenu': 'customers',
        'breadcrumb': [('Customer', 'customers')],
        'title': 'Customers', 'subtitle': 'all customers',
    }
    ctx['messages'] = messages = []
    ctx['errors'] = errors = []

    ctx['customers'] = None
    User.objects.filter(id=uid).delete()

    return redirect('/customers/?eid={eid}&page={page}'.format(eid=eid, page=page))


@user_required
def event_detail(request, me):
    eid = request.GET.get('eid')
    ctx = {
        'me': me,
        'menu': 'Event', 'submenu': 'events',
        'breadcrumb': [('Events', 'events')],
        'title': 'Events', 'subtitle': 'all events',
    }
    ctx['messages'] = messages = []
    ctx['errors'] = errors = []
    ctx['eid'] = eid
    # 查询活动详情

    event = Event.objects.filter(pk=eid).first()
    ctx['event'] = event
    # 查询活动积分列表

    ctx['last_foods'] = last_foods = LastFood.objects.filter(event_id=eid)
    last_foods_page = request.GET.get('last_foods_page', 1)
    paginator = Paginator(last_foods, 5)
    ctx['last_foods_pager'] = last_foods_pager = paginator.get_page(last_foods_page)
    ctx['last_foods'] = last_foods[
                        last_foods_pager.start_index() - 1 if last_foods_pager.start_index() else 0:last_foods_pager.end_index()]

    e_credits = Credit.objects.filter(event_id=eid)
    page = request.GET.get('page', 1)
    paginator = Paginator(e_credits, 5)
    ctx['pager'] = pager = paginator.get_page(page)
    ctx['credits'] = e_credits[pager.start_index() - 1 if pager.start_index() else 0:pager.end_index()]

    once_credits = OnlyOnceCredit.objects.filter(event_id=eid)
    once_credit_page = request.GET.get('once_credit_page', 1)
    paginator = Paginator(once_credits, 5)
    ctx['once_credit_pager'] = once_credit_pager = paginator.get_page(once_credit_page)
    ctx['once_credits'] = once_credits[
                          once_credit_pager.start_index() - 1 if once_credit_pager.start_index() else 0:once_credit_pager.end_index()]

    return render(request, 'team/event_detail.html', ctx)


@user_required
def add_food(request, me):
    if request.method == 'POST':
        # 获取表单提交数据
        name = request.POST['name']
        credit = request.POST['credit']
        # event_id = request.POST['event_id']

        food_img = request.FILES['food_img']

        event = me.event

        # 保存表单数据
        food = Food.objects.create(name=name,
                                   provider=me,
                                   credit=credit,
                                   event=event,
                                   food_img=food_img)
        # 生成二维码

        qr = qrcode.make('https://pinkslash.metatype.cn/wechat_login/?status=purchase_{0}_{1}'.format(event.id, food.id))
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
        food.qrcode = qr_img
        food.save()
        buf.close()

    return redirect('/foods?eid={0}'.format(event.id))


@user_required
def add_event(request, me):
    """
    创建活动
    """
    if request.method == 'POST':
        # 获取表单提交数据
        name = request.POST['name']
        time = request.POST['time']
        address = request.POST['address']
        introduce = request.POST['introduce']
        event_img = request.FILES['event_img']
        # 生成二维码

        # 保存表单数据
        event = Event.objects.create(name=name,
                                     time=time,
                                     address=address,
                                     introduce=introduce,
                                     event_img=event_img)
        qr = qrcode.make('https://pinkslash.metatype.cn/wechat_login/?status=provider_{0}'.format(event.id))
        buf = BytesIO()
        qr.save(buf)
        qr_data = buf.getvalue()
        buf.write(qr_data)
        qr_img = InMemoryUploadedFile(file=buf,
                                      field_name=None,
                                      name='event.png',
                                      content_type='image/png',
                                      size=len(qr_data),
                                      charset=None)
        # 保存表单数据
        event.qrcode = qr_img
        event.save()
        buf.close()

    return redirect('/events/')


@user_required
def add_credit(request, me):
    """
    添加活动积分
    """
    credit = request.POST['credit']
    event_id = request.POST['eid']
    # 创建二维码
    qr = qrcode.QRCode(
        version=1,
        box_size=1,
        border=4
    )
    qr.add_data('https://pinkslash.metatype.cn/wechat_login/?status=customer_{0}_{1}'.format(event_id, credit))
    img = qr.make_image()
    buf = BytesIO()
    img.save(buf)
    qr_data = buf.getvalue()
    qr_img = InMemoryUploadedFile(file=buf,
                                  field_name=None,
                                  name='credit.png',
                                  content_type='image/png',
                                  size=len(qr_data),
                                  charset=None)
    # 保存到数据库
    Credit.objects.create(
        credit=credit,
        event_id=event_id,
        qrcode=qr_img
    )
    return redirect('/event?eid={0}'.format(event_id))


@user_required
def add_last_food(request, me):
    """
    最后的晚餐食物添加
    """
    name = request.POST['name']
    eid = request.POST['eid']
    img = request.FILES['img']
    LastFood.objects.create(
        event_id=eid,
        food_img=img,
        name=name
    )
    return redirect('/event?eid={0}'.format(eid))


# 2019.5.20 by jiangyuwei
@user_required
def add_only_once_credit(request, me):
    """
    添加活动积分(每个用户只能扫一次)
    """
    credit = request.POST['credit']
    event_id = request.POST['eid']
    # 创建二维码
    qr = qrcode.QRCode(
        version=1,
        box_size=1,
        border=4
    )
    # 这里先创建一行数据，好将id传过去
    s = OnlyOnceCredit.objects.create(
        credit=credit,
        event_id=event_id,
        qrcode='a'
    )

    qr.add_data(
        'https://pinkslash.metatype.cn/wechat_login/?status=customeronce_{0}_{1}_{2}'.format(event_id, credit, s.id))
    img = qr.make_image()
    buf = BytesIO()
    img.save(buf)
    qr_data = buf.getvalue()
    qr_img = InMemoryUploadedFile(file=buf,
                                  field_name=None,
                                  name='oncecredit.png',
                                  content_type='image/png',
                                  size=len(qr_data),
                                  charset=None)
    # 保存到数据库
    # OnlyOnceCredit.objects.create(
    #     credit=credit,
    #     event_id=event_id,
    #     qrcode=qr_img
    # )
    s.qrcode = qr_img
    s.save()

    return redirect('/event?eid={0}'.format(event_id))
