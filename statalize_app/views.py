from django.shortcuts import render, get_object_or_404, redirect, HttpResponse, Http404
from django.db.models import Count
from statalize_app.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from .models import team, player, coach
from .util import calculate_slg, calculate_ops, calculate_avg, calculate_obp
from django.db.models import Sum, Count

# Create your views here.

def display_home(request):
    data = team.objects.all()
    context = {"Teams": data}
    return render(request, 'statalize/home.html', context)

def display_team(request, id):
    set_team = get_object_or_404(team, id=id)
    teams_players = player.objects.all().filter(plays_for=set_team.id)
    player_stats = []
    for Player in teams_players:
        avg = calculate_avg(Player.player_hits, Player.player_AB)
        obp = calculate_obp(Player.player_hits, Player.player_BB, Player.player_AB)
        slg = calculate_slg(Player.player_Singles, Player.player_Doubles, Player.player_Triples, Player.player_HR, Player.player_AB)
        ops = calculate_ops(obp, slg)

        player_stats.append({
            'name': Player.player_name,
            'age': Player.player_age,
            'year': Player.player_year,
            'height': Player.player_height,
            'weight': Player.player_weight,
            'hits': Player.player_hits,
            'AB': Player.player_AB,
            'BB': Player.player_BB,
            'SO': Player.player_SO,
            'Singles': Player.player_Singles,
            'Doubles': Player.player_Doubles,
            'Triples': Player.player_Triples,
            'HR': Player.player_HR,
            'Runs': Player.player_Runs,
            'RBI': Player.player_RBI,
            'SB': Player.player_SB,
            'SAC': Player.player_SAC,
            'avg': round(avg, 3),
            'obp': round(obp, 3),
            'slg': round(slg, 3),
            'ops': round(ops, 3),
            'stats': Player,
        })
    context = {"Team": set_team, "Players": teams_players, 'player_stats': player_stats}
    return render(request, 'statalize/teams.html', context)
