from django.shortcuts import render, redirect
from django.http import Http404
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator

from core.models import User
from .decorators import user_required

from hashlib import sha1

# make_password = lambda _: sha1(_.encode('utf-8')).hexdigest()

def login(request):
    ctx = { 'menu': 'team', 'submenu': 'user' }

    if request.method != 'POST':
        return render(request, 'login.html', ctx)

    ctx['name'] = name = request.POST.get('name', '')
    ctx['password'] = password = request.POST.get('password', '')

    ctx['errors'] = errors = []
    if not name:
        errors.append('Name is empty')

    if not password:
        errors.append('Password is empty')

    user = User.objects.filter(username=name, password=password).first()

    if not user:
        errors.append('Password wrong')
    else:
        if user.status == 0:
            errors.append('Password wrong')

    if not errors:
        request.session['uid'] = user.id
        return redirect('home')

    return render(request, 'login.html', ctx)


@user_required
def logout(request, me):
    del request.session['uid']
    return redirect(login)



