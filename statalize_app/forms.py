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

