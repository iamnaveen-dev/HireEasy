from django.urls import path
from apps.companies import views

urlpatterns = [
    path(
        'create/',
        views.create_company_view,
        name='create_company'
    ),
    path(
        'me/',
        views.get_company_view,
        name='get_company'
    ),
    path(
        'me/update/',
        views.update_company_view,
        name='update_company'
    ),
    path(
        'me/members/',
        views.list_members_view,
        name='list_members'
    ),
    path(
        'me/invite/',
        views.invite_member_view,
        name='invite_member'
    ),
]