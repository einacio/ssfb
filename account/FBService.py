import hashlib
import hmac
import json

from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from django.utils.http import urlsafe_base64_decode

from .models import User, UserHistory
from urllib import request


class FBService:

    @staticmethod
    def login():
        return 'https://www.facebook.com/v3.3/dialog/oauth?client_id={app_id}&redirect_uri={redirect_uri}&state={state_param}'.format(
            app_id=settings.FB_APP_ID,
            redirect_uri=settings.BASE_URL + reverse('login'),
            state_param=1234
        )

    @classmethod
    def check_login(cls, get_params):
        if 'code' in get_params:
            token = cls.get_token(get_params['code'])
            if token:
                user_data = cls.get_user_data(token)
                try:
                    user = User.objects.get(fb_user_id=user_data['id'])
                except User.DoesNotExist:
                    user = User(fb_user_id=user_data['id'])
                user.fb_token = token
                user.name = user_data['name']
                user.save()
                user.activate()
                return user
        return False

    @staticmethod
    def get_token(code):
        req = request.Request(
            'https://graph.facebook.com/v3.3/oauth/access_token'
            '?client_id={app_id}'
            '&redirect_uri={redirect_uri}'
            '&client_secret={app_secret}'
            '&code={code_parameter}'.format(
                app_id=settings.FB_APP_ID,
                redirect_uri=settings.BASE_URL + reverse('login'),
                app_secret=settings.FB_APP_SECRET,
                code_parameter=code
            )
        )
        with request.urlopen(req) as a:
            resp = json.loads(a.read().decode('UTF-8'))
        if 'access_token' in resp:
            return resp['access_token']
        return False

    @staticmethod
    def get_user_data(access_token):
        req = request.Request(
            'https://graph.facebook.com/me'
            '?fields=id,name,picture'
            '&access_token={access_token}'.format(
                access_token=access_token
            ))
        with request.urlopen(req) as a:
            resp = json.loads(a.read().decode('UTF-8'))
        return resp

    @staticmethod
    def manage_deauth(post_data):
        if 'signed_request' in post_data:
            parts = post_data['signed_request'].split('.')
            signature = urlsafe_base64_decode(parts[0])

            expected_signature = hmac.new(bytes(settings.FB_APP_SECRET, 'UTF-8'), msg=bytes(parts[1], 'UTF-8'), digestmod=hashlib.sha256).digest()
            if hmac.compare_digest(expected_signature, signature):
                data = json.loads(urlsafe_base64_decode(parts[1]).decode('UTF-8'))
                return data['user_id']
        return False
