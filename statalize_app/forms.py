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
    players = forms.ModelMultipleChoiceField(
        queryset=player.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    pitchers = forms.ModelMultipleChoiceField(
        queryset=pitcher.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    def __init__(self, team_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        set_team = team.objects.get(id=team_id)
        print(set_team)
        print(set_team.coach)
        self.fields['players'].queryset = player.objects.filter(plays_for=set_team)
        for Player in self.fields['players'].queryset:
            print(Player.player_name)
        self.fields['pitchers'].queryset = pitcher.objects.filter(pitches_for=set_team)


class NewPlayer(forms.Form):
    player_name = forms.CharField(max_length=50)
    player_age = forms.IntegerField(min_value=1)
    player_year = forms.ChoiceField(choices=[('FR', 'Freshman'), ('SO', 'Sophomore'), ('JR', 'Junior'), ('SR', 'Senior')], widget=forms.Select)
    player_position = forms.ChoiceField(choices=[('1B', 'Firstbase'), ('2B', 'Secondbase'),('3B', 'Thirdbase'),('SS', 'Shortstop'), ('C', 'Catcher'), ('OF', 'Outfield'), ('N/A', 'NoPosition')])
    player_height = forms.CharField(max_length=4, help_text='Feet\'Inches\" e.g. 5\'11\"',)
    player_weight = forms.CharField(max_length=3, help_text='Only the number (in pounds) e.g. 125')


class NewPitcher(forms.Form):
    player_name = forms.CharField(max_length=50)
    player_age = forms.IntegerField(min_value=1)
    player_year = forms.ChoiceField(choices=[('FR', 'Freshman'), ('SO', 'Sophomore'), ('JR', 'Junior'), ('SR', 'Senior')], widget=forms.Select)
    player_position = forms.ChoiceField(choices=[('SP', 'Starter'), ('RP', 'Relief'), ('N/A', 'NoPitcher')])
    player_height = forms.CharField(max_length=4, help_text='Feet\'Inches\" e.g. 5\'11\"',)
    player_weight = forms.CharField(max_length=3, help_text='Only the number (in pounds) e.g. 125')


class NewGame(forms.Form):
    date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    home_team = forms.ModelChoiceField(queryset=team.objects.all())
    away_team = forms.ModelChoiceField(queryset=team.objects.all())