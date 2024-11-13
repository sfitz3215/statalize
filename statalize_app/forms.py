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

class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ('date', 'away_team', 'home_team', 'away_score', 'home_score', 'winner')


class AwayTeamPlayerForm(forms.ModelForm):
    class Meta:
        model = GamePlayerStats
        fields = ['player', 'AB', 'BB', 'SO', 'Singles', 'Doubles', 'Triples', 'HR', 'Runs', 'RBI', 'SB', 'SAC']

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