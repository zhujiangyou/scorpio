from django.db import models

# Create your models here.

USER_STATUS = [
    (0, 'consumer'),
    (1, 'provider'),
    (2, 'host'),
]

LUNCH_STATUS = [
    (0, 'Basic'),
    (1, 'Premium'),
]

class User(models.Model):

    username = models.CharField(max_length=100, verbose_name='username', default='')
    password = models.CharField(max_length=100, verbose_name='password', default='')
    union_id = models.CharField(max_length=200)
    nickname = models.CharField(max_length=200)
    head_img = models.CharField(max_length=500)
    credit = models.IntegerField(default=0)
    event = models.ForeignKey('Event', null=True, on_delete=models.CASCADE, blank=True)
    status = models.IntegerField(choices=USER_STATUS)
    qrcode = models.ImageField(upload_to='user/qrcode', default='')
    name = models.CharField(max_length=100, verbose_name='name', default='')
    hotel_name = models.CharField(max_length=100, verbose_name='hotel_name', default='')
    email = models.CharField(max_length=100, verbose_name='email', default='')

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=100)
    time = models.DateTimeField(auto_now=True)
    address = models.CharField(max_length=200)
    introduce = models.CharField(max_length=1000)
    event_img = models.ImageField(upload_to='event')
    qrcode = models.ImageField(upload_to='event/qrcode')

    def __str__(self):
        return self.name


class Food(models.Model):
    provider = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    food_img = models.ImageField(upload_to='food')
    name = models.CharField(max_length=100)
    credit = models.IntegerField(default=0)
    qrcode = models.ImageField(upload_to='food/qrcode')

    def __str__(self):
        return self.name

#用户扫过的食物二维码
class UserFood(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.name + '---' + self.food.name

class Credit(models.Model):
    credit = models.IntegerField(default=0)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    qrcode = models.ImageField(upload_to='credit/qrcode')

#用户扫过的积分二维码
class UserCredit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    credit = models.CharField(max_length=100, default='')
    create_time = models.DateTimeField(auto_now=True)

# 2019.5.20 by jiangyuwei
class OnlyOnceCredit(models.Model):
    credit = models.IntegerField(default=0)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    qrcode = models.ImageField(upload_to='credit/qrcode')

# 2019.5.20 by jiangyuwei
#用户扫过的一次性二维码
class UserScan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    credit = models.ForeignKey(OnlyOnceCredit, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now=True)

class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now=True)
    credit = models.CharField(max_length=10)
    desc = models.CharField(max_length=100, default='')

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)


class LastFood(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    food_img = models.ImageField(upload_to='food')
    name = models.CharField(max_length=100)


class Lunch(models.Model):
    name = models.CharField(max_length=100, default='')
    img = models.ImageField(upload_to='lunch')
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    credit = models.IntegerField(default=0)
    status = models.IntegerField(choices=LUNCH_STATUS, default=0)


class RoomAmenity(models.Model):
    name = models.CharField(max_length=100, default='')
    img = models.ImageField(upload_to='roomAmenity')
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    credit = models.IntegerField(default=0)
    text = models.CharField(max_length=5000, default='')


class RoomAmenityReservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    roomAmenity = models.ForeignKey(RoomAmenity, on_delete=models.CASCADE)


class LunchReservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lunch = models.ForeignKey(Lunch, on_delete=models.CASCADE)


class TeaBreak(models.Model):
    img = models.ImageField(upload_to='teaBreak')
    text = models.CharField(default='', max_length=5000)


class Agenda(models.Model):
    name = models.CharField(default='', max_length=100)
    img = models.ImageField(upload_to='agenda', null=True)
    text = models.CharField(default='', max_length=5000)

#选择完的附加选项
class Attach(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(default='', max_length=100)
    roomAmenity = models.ForeignKey(RoomAmenity, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.name + '预订了' + self.roomAmenity.name + ',额外添加了' + self.name