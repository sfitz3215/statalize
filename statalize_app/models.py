from django.db import models
import uuid
from django.contrib.auth.models import User


FRESHMAN = "FR"
SOPHOMORE = "SO"
JUNIOR = "JR"
SENIOR = "SR"
GRADUATE = "GR"
YEAR_IN_SCHOOL_CHOICES = {
    FRESHMAN: "Freshman",
    SOPHOMORE: "Sophomore",
    JUNIOR: "Junior",
    SENIOR: "Senior",
    GRADUATE: "Graduate",
}


class team (models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    #coach = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    team_name = models.CharField(max_length=20)
    wins = models.PositiveIntegerField()
    losses = models.PositiveIntegerField()

    def _str_(self):
        return self.team_name

class player (models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    plays_for = models.ForeignKey(team, on_delete=models.CASCADE)
    player_name = models.CharField(max_length=50)
    player_age = models.PositiveIntegerField()
    player_year = models.CharField(max_length=2, choices=YEAR_IN_SCHOOL_CHOICES)
    player_height = models.CharField(max_length= 4)
    player_weight = models.CharField(max_length= 3)


    def _str_(self):
        return (self.player_name + " " + self.player_age + " " + self.player_year)

class coach (models.Model):
    coach = models.ForeignKey(team, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    coach_name = models.CharField(max_length = 50)
    coach_year = models.PositiveIntegerField()

    def _str_(self):
        return (self.coach_name + " " + self.coach_year)
