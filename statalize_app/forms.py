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

class GameEditForm(forms.Form):
    home_score = forms.IntegerField(min_value=0, max_value=99)
    away_score = forms.IntegerField(min_value=0, max_value=99)

class PlayerGameStats(forms.Form):
    AB = forms.IntegerField(min_value=0, max_value=99)
    BB = forms.IntegerField(min_value=0, max_value=99)
    SO = forms.IntegerField(min_value=0, max_value=99)
    Singles = forms.IntegerField(min_value=0, max_value=99)
    Doubles = forms.IntegerField(min_value=0, max_value=99)
    Triples = forms.IntegerField(min_value=0, max_value=99)
    HR = forms.IntegerField(min_value=0, max_value=99)
    Runs = forms.IntegerField(min_value=0, max_value=99)
    RBI = forms.IntegerField(min_value=0, max_value=99)
    SB = forms.IntegerField(min_value=0, max_value=99)
    SAC = forms.IntegerField(min_value=0, max_value=99)

class PitcherGameStats(forms.Form):
    SO = forms.IntegerField(min_value=0, max_value=99)
    hits = forms.IntegerField(min_value=0, max_value=99)
    walks = forms.IntegerField(min_value=0, max_value=99)
    HR = forms.IntegerField(min_value=0, max_value=99)
    IP = forms.FloatField(min_value=0, max_value=99)
    runs = forms.IntegerField(min_value=0, max_value=99)
    ER = forms.IntegerField(min_value=0, max_value=99)
    games = forms.IntegerField(min_value=0, max_value=99)
    GS = forms.IntegerField(min_value=0, max_value=99)
    AB = forms.IntegerField(min_value=0, max_value=99)