from django.shortcuts import render, get_object_or_404, redirect, HttpResponse, Http404
from statalize_app.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from .models import team, player, coach, pitcher, Game, GamePlayerStats, GamePitcherStats
from .util import calculate_slg, calculate_ops, calculate_avg, calculate_obp, calculate_ERA, calculate_WHIP
from django.db.models import Sum, Count

# Create your views here.

def display_home(request):
    data = team.objects.all()
    context = {"Teams": data}
    return render(request, 'statalize/home.html', context)

def display_players(request):
    players = player.objects.all()
    pitchers = pitcher.objects.all()
    player_stats = []
    pitcher_stats = []
    for Player in players:
        avg = calculate_avg(Player.player_hits, Player.player_AB)
        obp = calculate_obp(Player.player_hits, Player.player_BB, Player.player_AB)
        slg = calculate_slg(Player.player_Singles, Player.player_Doubles, Player.player_Triples, Player.player_HR, Player.player_AB)
        ops = calculate_ops(obp, slg)

        player_stats.append({
            'name': Player.player_name,
            'team': Player.plays_for,
            'age': Player.player_age,
            'year': Player.player_year,
            'height': Player.player_height,
            'weight': Player.player_weight,
            'position':Player.player_position,
            'games': Player.player_games,
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
            'avg': avg,
            'obp': obp,
            'slg': slg,
            'ops': ops,
            'stats': Player,
        })
    for Pitcher in pitchers:
        era = calculate_ERA(Pitcher.pitcher_ER, Pitcher.pitcher_IP)
        avg = calculate_avg(Pitcher.pitcher_hits, Pitcher.pitcher_AB)
        whip = calculate_WHIP(Pitcher.pitcher_walks, Pitcher.pitcher_hits, Pitcher.pitcher_IP)

        pitcher_stats.append({
            'name': Pitcher.pitcher_name,
            'team': Pitcher.pitches_for,
            'age': Pitcher.pitcher_age,
            'year': Pitcher.pitcher_year,
            'height': Pitcher.pitcher_height,
            'weight': Pitcher.pitcher_weight,
            'position':Pitcher.pitcher_position,
            'games': Pitcher.pitcher_games,
            'GS': Pitcher.pitcher_GS,
            'IP': Pitcher.pitcher_IP,
            'hits': Pitcher.pitcher_hits,
            'AB': Pitcher.pitcher_AB,
            'walks': Pitcher.pitcher_walks,
            'SO': Pitcher.pitcher_SO,
            'HR': Pitcher.pitcher_HR,
            'Runs': Pitcher.pitcher_runs,
            'ER':Pitcher.pitcher_ER,
            'era': round(era, 2),
            'avg': avg,
            'whip': round(whip, 2),
            'stats': Pitcher,
        })

    context = {"Pitcher": pitchers, "Players": players, 'player_stats': player_stats, 'pitcher_stats': pitcher_stats}
    return render(request, 'statalize/players.html', context)

def display_team(request, id):
    set_team = get_object_or_404(team, id=id)
    teams_players = player.objects.all().filter(plays_for=set_team.id)
    teams_pitchers = pitcher.objects.all().filter(pitches_for=set_team.id)
    player_stats = []
    pitcher_stats = []
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
            'position':Player.player_position,
            'games': Player.player_games,
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
            'avg': avg,
            'obp': obp,
            'slg': slg,
            'ops': ops,
            'stats': Player,
        })
    for Pitcher in teams_pitchers:
        era = calculate_ERA(Pitcher.pitcher_ER, Pitcher.pitcher_IP)
        avg = calculate_avg(Pitcher.pitcher_hits, Pitcher.pitcher_AB)
        whip = calculate_WHIP(Pitcher.pitcher_walks, Pitcher.pitcher_hits, Pitcher.pitcher_IP)

        pitcher_stats.append({
            'name': Pitcher.pitcher_name,
            'age': Pitcher.pitcher_age,
            'year': Pitcher.pitcher_year,
            'height': Pitcher.pitcher_height,
            'weight': Pitcher.pitcher_weight,
            'position':Pitcher.pitcher_position,
            'games': Pitcher.pitcher_games,
            'GS': Pitcher.pitcher_GS,
            'IP': Pitcher.pitcher_IP,
            'hits': Pitcher.pitcher_hits,
            'AB': Pitcher.pitcher_AB,
            'walks': Pitcher.pitcher_walks,
            'SO': Pitcher.pitcher_SO,
            'HR': Pitcher.pitcher_HR,
            'Runs': Pitcher.pitcher_runs,
            'ER':Pitcher.pitcher_ER,
            'era': round(era, 2),
            'avg': avg,
            'whip': round(whip, 2),
            'stats': Pitcher,
        })

    context = {"Team": set_team, "Players": teams_players, 'player_stats': player_stats, 'pitcher_stats': pitcher_stats}
    return render(request, 'statalize/teams.html', context)

def display_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)

    return render(request)