from restapi import api, APIError
from .models import *
@api
def mini_login(code):

    print(1111)
    print(code)

    return code