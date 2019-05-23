from django.db import models

# Create your models here.

USER_STATUS = [
    (0, 'consumer'),
    (1, 'provider'),
    (2, 'host'),
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


class Credit(models.Model):
    credit = models.IntegerField(default=0)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    qrcode = models.ImageField(upload_to='credit/qrcode')

# 2019.5.20 by jiangyuwei
class OnlyOnceCredit(models.Model):
    credit = models.IntegerField(default=0)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    qrcode = models.ImageField(upload_to='credit/qrcode')

# 2019.5.20 by jiangyuwei
class UserScan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    credit = models.ForeignKey(OnlyOnceCredit, on_delete=models.CASCADE)


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


class RoomAmenity(models.Model):
    name = models.CharField(max_length=100, default='')
    img = models.ImageField(upload_to='roomAmenity')
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    credit = models.IntegerField(default=0)


class RoomAmenityReservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    roomAmenity = models.ForeignKey(RoomAmenity, on_delete=models.CASCADE)


class LunchReservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lunch = models.ForeignKey(Lunch, on_delete=models.CASCADE)


class TeaBreak(models.Model):
    img = models.ImageField(upload_to='teaBreak')
    text = models.CharField(default='', max_length=5000)