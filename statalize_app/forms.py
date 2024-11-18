from django import forms
from .models import *
from django.urls import reverse_lazy
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class AuthenticationForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_action = reverse_lazy('home')
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Login'))

    username = forms.CharField(max_length=25)
    password = forms.CharField(max_length=25, widget=forms.PasswordInput)


class NewCoachForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_action = reverse_lazy('login')
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Create Account'))

    username = forms.CharField(max_length=25)
    password = forms.CharField(max_length=25, widget=forms.PasswordInput)
    password_check = forms.CharField(max_length=25, widget=forms.PasswordInput)
    first_name = forms.CharField(max_length=25)
    last_name = forms.CharField(max_length=25)


class NewTeamForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_action = reverse_lazy('login')
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Create Team'))

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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_action = reverse_lazy('home')
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Add Player'))

    YEAR_CHOICES = (
        ('FR', 'Freshman'),
        ('SO', 'Sophomore'),
        ('JR', 'Junior'),
        ('SR', 'Senior')
    )

    POSITION_CHOICES = (
        ('1B', 'Firstbase'),
        ('2B', 'Secondbase'),
        ('3B', 'Thirdbase'),
        ('SS', 'Shortstop'),
        ('C', 'Catcher'),
        ('OF', 'Outfield'),
        ('N/A', 'NoPosition')
    )

    player_name = forms.CharField(max_length=50)
    player_age = forms.IntegerField(min_value=1)
    player_year = forms.ChoiceField(
        choices=YEAR_CHOICES,
        #[('FR', 'Freshman'), ('SO', 'Sophomore'), ('JR', 'Junior'), ('SR', 'Senior')],
        widget=forms.RadioSelect())
    player_position = forms.ChoiceField(
        choices=POSITION_CHOICES,
        #[('1B', 'Firstbase'), ('2B', 'Secondbase'),('3B', 'Thirdbase'),('SS', 'Shortstop'), ('C', 'Catcher'), ('OF', 'Outfield'), ('N/A', 'NoPosition')])
        widget = forms.RadioSelect())
    player_height = forms.CharField(max_length=5, help_text='Feet\'Inches\" e.g. 5\'11\"',)
    player_weight = forms.CharField(max_length=3, help_text='Only the number (in pounds) e.g. 125')


class NewPitcher(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_action = reverse_lazy('home')
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Add Player'))

    YEAR_CHOICES = (
        ('FR', 'Freshman'),
        ('SO', 'Sophomore'),
        ('JR', 'Junior'),
        ('SR', 'Senior')
    )

    POSITION_CHOICES = (
        ('SP', 'Starter'),
        ('RP', 'Relief'),
        ('N/A', 'NoPitcher')
    )

    player_name = forms.CharField(max_length=50)
    player_age = forms.IntegerField(min_value=1)
    player_year = forms.ChoiceField(
        choices= YEAR_CHOICES,
        #[('FR', 'Freshman'), ('SO', 'Sophomore'), ('JR', 'Junior'), ('SR', 'Senior')],
        widget= forms.RadioSelect())
    player_position = forms.ChoiceField(
        choices= POSITION_CHOICES,
        #[('SP', 'Starter'), ('RP', 'Relief'), ('N/A', 'NoPitcher')]
        widget= forms.RadioSelect())
    player_height = forms.CharField(max_length=4, help_text='Feet\'Inches\" e.g. 5\'11\"',)
    player_weight = forms.CharField(max_length=3, help_text='Only the number (in pounds) e.g. 125')



class NewGame(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_action = reverse_lazy('login')
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Add Game'))

    date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    home_team = forms.ModelChoiceField(queryset=team.objects.all())
    away_team = forms.ModelChoiceField(queryset=team.objects.all())

class GameForm(forms.Form):
    away_score = forms.IntegerField(min_value=0, max_value=99)
    home_score = forms.IntegerField(min_value=0, max_value=99)

    def __init__(self, game_id, *args, **kwargs):
        super().__init__(*args, **kwargs)

        set_game = Game.objects.get(id=game_id)

        self.fields['home_score'].initial = set_game.home_score
        self.fields['away_score'].initial = set_game.away_score


class GamePlayerForm(forms.Form):
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

        self.fields['AB'].initial = self.AB
        self.fields['BB'].initial = self.BB
        self.fields['SO'].initial = self.SO
        self.fields['Singles'].initial = self.Singles
        self.fields['Doubles'].initial = self.Doubles
        self.fields['Triples'].initial = self.Triples
        self.fields['HR'].initial = self.HR
        self.fields['Runs'].initial = self.Runs
        self.fields['RBI'].initial = self.RBI
        self.fields['SB'].initial = self.SB
        self.fields['SAC'].initial = self.SAC

class GamePitcherForm(forms.ModelForm):
        SO = forms.IntegerField(min_value=0, max_value=0)
        hits = forms.IntegerField(min_value=0, max_value=0)
        walks = forms.IntegerField(min_value=0, max_value=0)
        HR = forms.IntegerField(min_value=0, max_value=0)
        IP = forms.FloatField(min_value=0, max_value=0)
        runs = forms.IntegerField(min_value=0, max_value=0)
        ER = forms.IntegerField(min_value=0, max_value=0)
        games = forms.IntegerField(min_value=0, max_value=0)
        GS = forms.IntegerField(min_value=0, max_value=0)
        AB = forms.IntegerField(min_value=0, max_value=0)

        def __init__(self, game, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.fields['SO'].initial = self.SO
            self.fields['hits'].initial = self.hits
            self.fields['walks'].initial = self.walks
            self.fields['HR'].initial = self.HR
            self.fields['IP'].initial = self.IP
            self.fields['runs'].initial = self.runs
            self.fields['ER'].initial = self.ER
            self.fields['games'].initial = self.games
            self.fields['AB'].initial = self.AB