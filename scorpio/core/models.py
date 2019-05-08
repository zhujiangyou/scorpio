from django.db import models

# Create your models here.

USER_STATUS = [
    (0, 'consumer'),
    (1, 'provider'),
    (2, 'host'),
]


class User(models.Model):
    name = models.CharField(max_length=100, verbose_name='name')
    username = models.CharField(max_length=100, verbose_name='username', default='')
    password = models.CharField(max_length=100, verbose_name='password', default='')
    union_id = models.CharField(max_length=200)
    nickname = models.CharField(max_length=200)
    head_img = models.CharField(max_length=500)
    credit = models.IntegerField(default=0)
    event = models.ForeignKey('Event', null=True, on_delete=models.CASCADE, blank=True)
    status = models.IntegerField(choices=USER_STATUS)

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


class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now=True)
    credit = models.CharField(max_length=10)


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)


class LastFood(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    food_img = models.ImageField(upload_to='food')
    name = models.CharField(max_length=100)
