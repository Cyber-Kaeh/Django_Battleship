from django.urls import path
from .views import signup_view, matchmaking_view

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('matchmaking/', matchmaking_view, name='matchmaking'),
]