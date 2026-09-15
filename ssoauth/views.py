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
    if request.GET.get('prompt') == 'login':
        return oauth.keycloak.authorize_redirect(request, redirect_uri, prompt='login')
    return oauth.keycloak.authorize_redirect(request, redirect_uri)


def auth(request):
    try:
        token = oauth.keycloak.authorize_access_token(request)
        request.session["openid_token_resp"] = token
        userinfo = token['userinfo']
        print(f"DEBUG: userinfo = {userinfo}")
        
        User = get_user_model()
        user, created = User.objects.get_or_create(
            username=userinfo['preferred_username'],
            defaults={
                'email': userinfo.get('email', ''),
                'first_name': userinfo.get('given_name', ''),
                'last_name': userinfo.get('family_name', ''),
            }
        )
        print(f"DEBUG: user = {user}, is_authenticated = {request.user.is_authenticated}")
        
        default_group, _ = Group.objects.get_or_create(name=settings.SSO_DEFAULT_GROUP) 
        default_group.user_set.add(user)
        
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        request.session.modified = True

        print(f"DEBUG: after login, is_authenticated = {request.user.is_authenticated}")
        
        return redirect('/')
    except Exception as e:
        print(f"ERROR in auth: {e}")
        import traceback
        traceback.print_exc()
        raise



def sso_logout(request):
    if not "openid_token_resp" in request.session:
        return HttpResponse('Unauthorized', status=401)
    logout(request)
    return redirect(f'{reverse("login")}?prompt=login')