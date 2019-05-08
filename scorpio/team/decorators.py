from django.shortcuts import redirect

from core.models import User


def user_required(view_func):

    def wrapper(request, *args, **kwargs):
        if 'uid' not in request.session:
            return redirect('login')

        user = User.objects.filter(id=request.session['uid']).first()
        return view_func(request, me=user, *args, **kwargs)

    return wrapper

