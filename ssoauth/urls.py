from django.urls import path

from ssoauth import views

urlpatterns = [
    path('login/', views.sso_login, name='login'),
    path('logout/', views.sso_logout, name='logout'),
    path('auth/', views.auth, name='auth'),
]