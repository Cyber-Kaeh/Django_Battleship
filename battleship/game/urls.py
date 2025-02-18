from django.urls import path
from .views import signup_view, matchmaking_view, game_room_view

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('matchmaking/', matchmaking_view, name='matchmaking'),
    path("game/<int:game_id>/", game_room_view, name="game_room"),
]