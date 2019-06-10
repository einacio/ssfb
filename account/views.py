from django.shortcuts import render
from django.http import HttpRequest
from .models import User, UserHistory


def index(request: HttpRequest):
    request.session['is_logged_in'] = not request.session.get('is_logged_in')
    return render(request, 'account/index.html')
