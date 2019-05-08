from django.core.management import BaseCommand

from team.models import User

from hashlib import sha1


make_password = lambda _: sha1(_.encode('utf-8')).hexdigest()

class Command(BaseCommand):

    def handle(self, **kwargs):
        name = input('name: ')
        password = input('password: ')
        confirm_password = input('confirm password: ')

        if password != confirm_password:
            print ('password not same.')
            return

        if User.objects.filter(name=name, status=0).exists():
            print ('user exists.')
            return

        User.objects.create(name=name, password=make_password(password), user_admin=True, team_admin=True)
        print ('done.')
