from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from apps.users import views

urlpatterns = [
    path(
        'register/',
        views.register_view,
        name='register'
    ),
    path(
        'login/',
        views.login_view,
        name='login'

    ),
    path(
        'logout/',
        views.logout_view,
        name='logout'
    ),
    
    path(
        'profile/',
        views.profile_view,
        name='profile'
    ),
    path(
        'profile/update/',
        views.update_profile_view,
        name='update-profile'
    ),
    path(
        'profile/change-password/',
        views.change_password_view,
        name='change-password'
    ),
    
]


