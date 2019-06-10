from django.shortcuts import render, redirect
from django.http import HttpRequest
from .models import User, UserHistory
from .FBService import FBService


def index(request: HttpRequest):
    context = {}
    if not request.session['is_logged_in']:
        context['login_url'] = FBService.login()
    else:
        user = User.objects.get(pk=request.session['user'])
        context['user'] = user
        user_data = FBService.get_user_data(user.fb_token)
        context['avatar'] = user_data['picture']['data']['url']
    return render(request, 'account/index.html', context)


def login(request):
    ret = FBService.check_login(request.GET)
    if ret:
        request.session['is_logged_in'] = True
        request.session['user'] = ret.id
    else:
        request.session['is_logged_in'] = False
        del (request.session['user'])
    return redirect('/account')


def logout(request):
    request.session['is_logged_in'] = False
    del (request.session['user'])
    return redirect('/account')


def deauth(request):
    pass
