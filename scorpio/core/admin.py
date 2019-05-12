from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(User)
admin.site.register(Event)
admin.site.register(Food)
admin.site.register(Credit)
admin.site.register(History)

admin.site.register(Favorite)
admin.site.register(LastFood)
admin.site.register(Lunch)
admin.site.register(RoomAmenity)
admin.site.register(RoomAmenityReservation)
admin.site.register(LunchReservation)

