"""scorpio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from core import views as core_views
from team import views as team_views
from home import views as home_views

import restapi
urlpatterns = [

    path('admin/', admin.site.urls),
    path('', home_views.home, name='home'),
    path('login/', team_views.login, name='login'),
    path('logout/', team_views.logout, name='logout'),

    path('events/', home_views.events, name='events'),
    path('foods/', home_views.foods, name='foods'),
    path('add_food/', home_views.add_food, name='add_food'),
    path('customers/', home_views.customers, name='customers'),

    path('delete_food/', home_views.delete_food, name='delete_food'),
    path('delete_customer/', home_views.delete_customer, name='delete_customer'),
    path('delete_event/', home_views.delete_event, name='delete_event'),
    path('delete_last_food/', home_views.delete_last_food, name='delete_last_food'),

    path('last_foods/', home_views.last_foods, name='last_foods'),
    path('event/', home_views.event_detail),

    path('add_event/', home_views.add_event),
    path('add_credit/', home_views.add_credit),
    # 2019.5.20 by jiangyuwei
    path('add_only_once_credit/', home_views.add_only_once_credit),

    path('add_last_food/', home_views.add_last_food),
    path('add_favorite/<int:food_id>', core_views.add_favorite),

    path('get_foods/<int:pid>/', core_views.get_foods),
    path('get_provider_info/<int:pid>/', core_views.get_provider_info),
    path('get_credit_list/<int:pid>/', core_views.get_credit_list),

    path('customer_profile/<int:user_id>/', core_views.customer_profile),

    path('last_supper/', core_views.last_supper),
    path('credit_history', core_views.credit_history),
    path('reservation_list', core_views.reservation_list),

    path('pay_success', core_views.pay_success),
    path('pay_failed', core_views.pay_failed),

    path('wechat_login/', core_views.wechat_login),
    path('getticket', core_views.getticket),

    path('room_amenity/', core_views.room_amenity),
    path('lunch/', core_views.lunch),

    path('room_amenity/detail/<int:room_amenity_id>', core_views.room_amenity_detail),
    path('lunch/detail/<str:lunch_id>', core_views.lunch_detail),

    path('lunch/reserve/<int:lunch_id>', core_views.lunch_reserve),
    path('room_amenity/reserve/<int:room_amenity_id>/<str:flag1>/<str:flag2>/', core_views.room_amenity_reserve),

    path('reserve_success', core_views.reserve_success),
    path('reserve_failed', core_views.reserve_failed),

    path('user_reservation', core_views.user_reservation),

    path('customer/save_message/', core_views.customer_save_message),

    path('mini_customer/save_message/<str:user_id>/', core_views.mini_customer_save_message),

    path('provider/save_message/', core_views.provider_save_message),

    path('tea_break/', core_views.tea_break),

    path('send_credits/', core_views.send_credits),

    path('api/', restapi.urls),

    path('dashborad/', home_views.data_report, name='report'),
    path('dashborad/user_detail/<int:user_id>/', home_views.user_detail, name='user_detail'),
    path('dashborad/food_detail/<int:food_id>/', home_views.food_detail, name='food_detail'),
    path('countdown/', home_views.countdown),

    path('agenda/', core_views.agenda),
    path('agenda/detail/<str:agenda>/<str:agendatime>/', core_views.agenda_detail),

    path('lunch/packages/<str:lunch_type>/', core_views.lunch_packages),

    path('food_purchase/<int:food_id>/', core_views.food_purchase),
    path('purchase_food/<int:food_id>/', core_views.purchase_food),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
