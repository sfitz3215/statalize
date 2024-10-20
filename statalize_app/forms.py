from django import forms
from .models import team, player, coach

class TeamForm(forms.ModelForm):
    class Meta:
        model = team
        fields = ['team_name', 'wins', 'losses']
