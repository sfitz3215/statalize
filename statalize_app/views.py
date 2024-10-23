from django.shortcuts import render, get_object_or_404, redirect, HttpResponse, Http404
from django.db.models import Count
from statalize_app.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from .models import team, player, coach
# Create your views here.

def display_home(request):
    data = team.objects.all()
    context = {"Teams": data}
    return render(request, 'statalize/home.html', context)

def display_team(request, id):
    set_team = get_object_or_404(team, id=id)
    teams_players = player.objects.all().filter(plays_for=set_team.id)
    context = {"Team": set_team, "Players": teams_players}
    return render(request, 'statalize/teams.html', context)
