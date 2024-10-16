from tkinter.constants import CASCADE

from django.db import models

fr= 'freshman'
so= 'sophmore'
jr= 'junior'
sn= 'senior'

class team (models.Model):
    team_name = models.CharField(max_length=20)
    wins = models.PositiveIntegerField()
    losses = models.PositiveIntegerField()

    def _str_(self):
        return (self.team_name + " " + self.wins + " " + self.losses)

class player (models.Model):
    player = models.ForeignKey(team, on_delete=models.CASCADE)
    player_name = models.CharField(max_length=50)
    player_age = models.PositiveIntegerField()
    player_year = models.Choices(fr, so, jr, sn)

    def _str_(self):
        return (self.player_name + " " + self.player_age + " " + self.player_year)
class coach (models.Model):
    coach = models.ForeignKey(team, on_delete=models.CASCADE)
    coach_name = models.CharField(max_length = 50)
    coach_year = models.PositiveIntegerField()

    def _str_(self):
        return (self.coach_name + " " + self.coach_year)
