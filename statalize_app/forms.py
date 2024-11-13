from django import forms
from .models import *


class AuthenticationForm(forms.Form):
    username = forms.CharField(max_length=25)
    password = forms.CharField(max_length=25, widget=forms.PasswordInput)


class NewCoachForm(forms.Form):
    username = forms.CharField(max_length=25)
    password = forms.CharField(max_length=25, widget=forms.PasswordInput)
    password_check = forms.CharField(max_length=25, widget=forms.PasswordInput)
    first_name = forms.CharField(max_length=25)
    last_name = forms.CharField(max_length=25)


class NewTeamForm(forms.Form):
    coach = forms.ModelChoiceField(queryset=User.objects.all())
    team_name = forms.CharField(max_length=20)


class EditTeam(forms.Form):
    def __init__(self, team_id, *args, **kwargs):
        super().__init__(*args, **kwargs)

        set_team = team.objects.get(id=team_id)

        self.fields['players'] = forms.ModelMultipleChoiceField(
            queryset=player.objects.filter(plays_for=set_team),
            widget=forms.CheckboxSelectMultiple,
            required=False
        )

class GameForm(forms.Form):
    away_score = forms.IntegerField(min_value=0, max_value=99)
    home_score = forms.IntegerField(min_value=0, max_value=99)

    def __init__(self, game_id, *args, **kwargs):
        super().__init__(*args, **kwargs)

        set_game = Game.objects.get(id=game_id)

        self.fields['home_score'].initial = set_game.home_score
        self.fields['away_score'].initial = set_game.away_score


class AwayTeamPlayerForm(forms.Form):
    AB = forms.IntegerField(min_value=0, max_value=0)
    BB = forms.IntegerField(min_value=0, max_value=0)
    SO = forms.IntegerField(min_value=0, max_value=0)
    Singles = forms.IntegerField(min_value=0, max_value=0)
    Doubles = forms.IntegerField(min_value=0, max_value=0)
    Triples = forms.IntegerField(min_value=0, max_value=0)
    HR = forms.IntegerField(min_value=0, max_value=0)
    Runs = forms.IntegerField(min_value=0, max_value=0)
    RBI = forms.IntegerField(min_value=0, max_value=0)
    SB = forms.IntegerField(min_value=0, max_value=0)
    SAC = forms.IntegerField(min_value=0, max_value=0)
    def __init__(self, game, *args, **kwargs):
        super().__init__(*args, **kwargs)

        set_player = player.objects.get(team=game.away_team)

        self.fields['AB'].initial = set_player.AB
        self.fields['BB'].initial = set_player.BB
        self.fields['SO'].initial = set_player.SO
        self.fields['Singles'].initial = set_player.Singles
        self.fields['Doubles'].initial = set_player.Doubles
        self.fields['Triples'].initial = set_player.Triples
        self.fields['HR'].initial = set_player.HR
        self.fields['Runs'].initial = set_player.Runs
        self.fields['RBI'].initial = set_player.RBI
        self.fields['SB'].initial = set_player.SB
        self.fields['SAC'].initial = set_player.SAC




    def __init__(self, *args, **kwargs):
        game = kwargs.pop('game', None)
        super().__init__(*args, **kwargs)
        if game:
            self.fields['player'].queryset = player.objects.filter(plays_for=game.away_team)

class HomeTeamPlayerForm(forms.ModelForm):
    class Meta:
        model = GamePlayerStats
        fields = ['player', 'AB', 'BB', 'SO', 'Singles', 'Doubles', 'Triples', 'HR', 'Runs', 'RBI', 'SB', 'SAC']

    def __init__(self, *args, **kwargs):
        game = kwargs.pop('game', None)
        super().__init__(*args, **kwargs)
        if game:
            self.fields['player'].queryset = player.objects.filter(plays_for=game.home_team)

class AwayTeamPitcherForm(forms.ModelForm):
    class Meta:
        model = GamePitcherStats
        fields = ['pitcher', 'SO', 'hits', 'walks', 'HR', 'IP', 'runs', 'ER', 'games', 'GS', 'AB']

    def __init__(self, *args, **kwargs):
        game = kwargs.pop('game', None)
        super().__init__(*args, **kwargs)
        if game:
            self.fields['pitcher'].queryset = pitcher.objects.filter(plays_for=game.away_team)

class HomeTeamPitcherForm(forms.ModelForm):
    class Meta:
        model = GamePitcherStats
        fields = ['pitcher', 'SO', 'hits', 'walks', 'HR', 'IP', 'runs', 'ER', 'games', 'GS', 'AB']

    def __init__(self, *args, **kwargs):
        game = kwargs.pop('game', None)
        super().__init__(*args, **kwargs)
        if game:
            self.fields['pitcher'].queryset = pitcher.objects.filter(plays_for=game.home_team)