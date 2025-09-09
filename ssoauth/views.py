from django.http import HttpResponse
from django.shortcuts import redirect
from django.conf import settings

# Create your views here.
from authlib.integrations.django_client import OAuth
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.models import Group
from django.urls import reverse
import requests

oauth = OAuth()
oauth.register(
    name='keycloak',
    server_metadata_url=settings.SSO_ENDPOINT,
    client_kwargs={
        'scope': 'openid email profile'
    }
)

def sso_login(request):
    redirect_uri = request.build_absolute_uri(reverse('auth'))
    return oauth.keycloak.authorize_redirect(request, redirect_uri)


def auth(request):
    token = oauth.keycloak.authorize_access_token(request)
    request.session["openid_token_resp"] = token
    userinfo = token['userinfo']
    User = get_user_model()
    user, created = User.objects.get_or_create(
        username=userinfo['preferred_username'],
        defaults={
            'email': userinfo.get('email', ''),
            'first_name': userinfo.get('given_name', ''),
            'last_name': userinfo.get('family_name', ''),
        }
    )
    default_group = Group.objects.get(name=settings.SSO_DEFAULT_GROUP) 
    default_group.user_set.add(user)
    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    return redirect('/')


def sso_logout(request):
    if not "openid_token_resp" in request.session:
        return HttpResponse('Unauthorized', status=401)
    request.session.pop('user', None)
    openid_token = request.session.pop('openid_token_resp', None)
    metadata = oauth.keycloak.load_server_metadata()
    requests.post(
        metadata["end_session_endpoint"],
        data={
                "client_id": oauth.keycloak.client_id,
                "client_secret": oauth.keycloak.client_secret,
                "refresh_token": openid_token.get("refresh_token", ""),
            },
    )
    logout(request)
    return redirect('/')