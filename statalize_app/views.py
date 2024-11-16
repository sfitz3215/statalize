from django.shortcuts import render, get_object_or_404, redirect, HttpResponse, Http404
from statalize_app.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from .models import *
from statalize_app.forms import *
from .util import calculate_slg, calculate_ops, calculate_avg, calculate_obp, calculate_ERA, calculate_WHIP
from django.db.models import Sum, Count

# Create your views here.

def login_page(request):
    form = AuthenticationForm(request.POST)
    first = True
    if form.is_valid():
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            first = False

    return render(request, 'login.html', {'form': form, 'first': first})


def create_new_coach(request):
    form = NewCoachForm(request.POST)
    new = True
    match = True

    if form.is_valid():
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        password_check = form.cleaned_data["password_check"]
        first = form.cleaned_data["first_name"]
        last = form.cleaned_data["last_name"]
        if password == password_check:
            if User.objects.filter(username=username).exists():
                new = False
            else:
                User.objects.create_user(username=username, password=password, first_name=first, last_name=last)
                return redirect('home')
        else:
            match = False

    return render(request, 'new_coach.html', {'form': form, 'match': match, 'new': new})


def create_new_team(request):
    form = NewTeamForm(request.POST)
    new = True

    if form.is_valid():
        coach = form.cleaned_data["coach"]
        team_name = form.cleaned_data["team_name"]
        if team.objects.filter(team_name=team_name).exists():
            new = False
        else:
            new_team = team(coach=coach, team_name=team_name, wins=0, losses=0)
            new_team.save()
            return redirect('teams', id=new_team.id)

    return render(request, 'new_team.html', {'form': form, 'new': new})


def edit_team(request, team_id):
    set_team = get_object_or_404(team, id=team_id)

    form = EditTeam(team_id=set_team.id, data=request.POST)

    team_players = form.fields['players'].queryset
    team_pitchers = form.fields['pitchers'].queryset

    if form.is_valid():
        selected_players = form.cleaned_data["players"]
        selected_pitchers = form.cleaned_data["pitchers"]
        # TODO: delete based on selected

    return render(request, 'edit_team.html', {'form': form, 'team': set_team, 'players': team_players, 'pitchers': team_pitchers})


def add_player(request, team_id, is_pitcher):
    if is_pitcher == 1:
        form = NewPitcher(request.POST)
    else:
        form = NewPlayer(request.POST)
    set_team = get_object_or_404(team, id=team_id)
    print(set_team)

    if form.is_valid():
        name = form.cleaned_data["player_name"]
        age = form.cleaned_data["player_age"]
        year = form.cleaned_data["player_year"]
        position = form.cleaned_data["player_position"]
        height = form.cleaned_data["player_height"]
        weight = form.cleaned_data["player_weight"]

        if is_pitcher == 1:
            new_pitcher = pitcher(pitches_for=set_team, pitcher_name=name, pitcher_age=age, pitcher_year=year, pitcher_position=position, pitcher_height=height, pitcher_weight=weight)
            new_pitcher.save()
            return redirect('teams', id=new_pitcher.pitches_for.id)
        else:
            new_player = player(plays_for=set_team, player_name=name, player_age=age, player_year=year, player_position=position, player_height=height, player_weight=weight)
            new_player.save()
            return redirect('teams', id=new_player.plays_for.id)

    return render(request, 'new_player.html', {'form': form})


def logout_page(request):
    logout(request)
    return redirect('home')

def display_home(request):
    data = team.objects.all()
    game_data = Game.objects.all()
    context = {"Teams": data, "games": game_data}
    return render(request, 'statalize/home.html', context)

def display_standings(request):
    data = team.objects.all()
    context = {"Teams": data}
    return render(request, 'statalize/standings.html', context)

def display_schedule(request):
    data = Game.objects.all()
    context = {"games": data}
    return render(request, 'statalize/schedule.html', context)

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

  

def new_game(request):
    form = NewGame(request.POST)
    if form.is_valid():
        date = form.cleaned_data["date"]
        home_team = form.cleaned_data["home_team"]
        away_team = form.cleaned_data["away_team"]

        set_game = Game(date=date, home_team=home_team, away_team=away_team)
        set_game.save()

        away_team_players = player.objects.filter(plays_for=away_team)
        away_team_pitchers = pitcher.objects.filter(pitches_for=away_team)
        home_team_players = player.objects.filter(plays_for=home_team)
        home_team_pitchers = pitcher.objects.filter(pitches_for=home_team)

        for away_player in away_team_players:
            away = GamePlayerStats(game=set_game, player=away_player)
            away.save()

        for home_player in home_team_players:
            home = GamePlayerStats(game=set_game, player=home_player)
            home.save()
        for away_pitcher in away_team_pitchers:
            awayp = GamePitcherStats(game=set_game, pitcher=away_pitcher)
            awayp.save()
        for home_pitcher in home_team_pitchers:
            homep = GamePitcherStats(game=set_game, pitcher=home_pitcher)
            homep.save()
        return redirect('home')

    return render(request, 'new_game.html', {'form': form})

def game_edit(request, game_id):
    set_game = get_object_or_404(Game, id=game_id)
    form = GameForm(data=request.POST or None, game_id=game_id)
    away_team = player.objects.filter(plays_for=set_game.away_team)
    away_teamp = pitcher.objects.filter(pitches_for=set_game.away_team)
    home_team = player.objects.filter(plays_for=set_game.home_team)
    home_teamp = pitcher.objects.filter(pitches_for=set_game.home_team)
    away_team_player = []
    away_team_pitcher = []
    home_team_player = []
    home_team_pitcher = []

    for person in away_team:
        game_player = get_object_or_404(GamePlayerStats, player=person)
        away_team_player.append(game_player)

    for person in away_teamp:
        game_player = get_object_or_404(GamePitcherStats, pitcher=person)
        away_team_pitcher.append(game_player)

    for person in home_team:
        game_player = get_object_or_404(GamePlayerStats, player=person)
        home_team_player.append(game_player)

    for person in home_teamp:
        game_player = get_object_or_404(GamePitcherStats, pitcher=person)
        home_team_pitcher.append(game_player)

    if form.is_valid():
        home_score=form.cleaned_data['home_score']
        away_score=form.cleaned_data['away_score']

        if home_score > away_score:
            winner = set_game.home_team
        else:
            winner = set_game.away_team

        set_game(home_score=home_score, away_score=away_score, winner=winner)
        set_game.save()
        return redirect('add_away_team', game_id=set_game.id)  # Redirect to add player stats after creation
    return render(request, 'game.html', {'form': form, 'home_team_pitcher': home_team_pitcher, 'home_team_player': home_team_player, 'away_team_pitcher': away_team_pitcher, 'away_team_player': away_team_player, 'set_game': set_game})

def add_away_team(request, game_id, is_pitcher):
    set_game = get_object_or_404(Game, id=game_id)
    if is_pitcher:
        form = AwayTeamPitcherForm(data=request.POST or None, game_id=game_id)
        if form.is_valid():
            pitcher_stats = form.save(commit=False)
            pitcher_stats.game = set_game
            pitcher_stats.pitcher = form.cleaned_data['pitcher']
            pitcher_stats.save()
            return redirect('edit_game', game_id=set_game.id)
    else:
        form = AwayTeamPlayerForm(data=request.POST or None, game_id=game_id)
        if form.is_valid():
            player_stats = form.save(commit=False)
            player_stats.game = set_game
            player_stats.player = form.cleaned_data['player']
            player_stats.save()
            return redirect('edit_game', game_id=set_game.id)
    return render(request, 'game.html',{'form': form})
  

def add_home_team(request, game_id, is_pitcher):
    set_game = get_object_or_404(Game, id=game_id)
    if is_pitcher:
        form = HomeTeamPitcherForm(data=request.POST or None, game_id=game_id)
        if form.is_valid():
            pitcher_stats = form.save(commit=False)
            pitcher_stats.game = set_game
            pitcher_stats.pitcher = form.cleaned_data['pitcher']
            pitcher_stats.save()
            return redirect('edit_game', game_id=set_game.id)
    else:
        form = HomeTeamPlayerForm(data=request.POST or None, game_id=game_id)
        if form.is_valid():
            player_stats = form.save(commit=False)
            player_stats.game = set_game
            player_stats.player = form.cleaned_data['player']
            player_stats.save()
            return redirect('edit_game', game_id=set_game.id)
    return render(request, 'game.html',{'form': form})