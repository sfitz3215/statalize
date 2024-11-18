"""
URL configuration for Statilize project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from statalize_app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', display_home, name = 'home'),
    path('teams/<uuid:id>/', display_team, name = 'teams'),
    path('standings/', display_standings, name = 'standings'),
    path('schedule/', display_schedule, name = 'schedule'),
    path('players/', display_players, name = 'players'),
    path('logout/', logout_page, name='logout'),
    path('login/', login_page, name='login'),
    path('new_coach/', create_new_coach, name='new_coach'),
    path('new_team/', create_new_team, name='new_team'),
    path('teams/<uuid:team_id>/edit_team/', edit_team, name='edit_team'),
    path('teams/<uuid:team_id>/add_player/<int:is_pitcher>/', add_player, name='add_player'),
    path('schedule/new_game/', new_game, name='new_game'),
    path('<uuid:team_id>/edit_team/', edit_team, name='edit_team'),
    path('game/<game_id>/', game_edit, name ='edit_game'),
    path('game/<uuid:game_id>/edit_player_game/<uuid:player_id>', edit_player_game, name='edit_player_game'),
    path('game/<uuid:game_id>/edit_pitcher_game/<uuid:pitcher_id>', edit_pitcher_game, name='edit_pitcher_game'),
]
