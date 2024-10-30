from django.db import models
import uuid
from django.contrib.auth.models import User
from django.db.models import Sum, Count


FRESHMAN = "FR"
SOPHOMORE = "SO"
JUNIOR = "JR"
SENIOR = "SR"
GRADUATE = "GR"
NoPosition = "N/A"
Firstbase = "1B"
Secondbase = "2B"
Shortstop = "SS"
Thirdbase = "3B"
Catcher = "C"
Outfield = "OF"
Starter = "SP"
Relief = "RP"
NoPitcher = "N/A"
YEAR_IN_SCHOOL_CHOICES = {
    FRESHMAN: "Freshman",
    SOPHOMORE: "Sophomore",
    JUNIOR: "Junior",
    SENIOR: "Senior",
    GRADUATE: "Graduate",
}

Position_Choices = {
    Firstbase: "Firstbase",
    Secondbase:"Secondbase",
    Shortstop: "Shortstop",
    Thirdbase: "Thirdbase",
    Catcher: "Catcher",
    Outfield: "Outfield",
    NoPosition: "N/A"
}

Pitcher_Choices = {
    Starter: "Starter",
    Relief: "Reliever",
    NoPitcher: "N/A",

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
    player_position = models.CharField(max_length=10, choices=Position_Choices, default=NoPosition)
    player_height = models.CharField(max_length= 4)
    player_weight = models.CharField(max_length= 3)
    player_games = models.PositiveIntegerField(default=0)
    player_hits = models.PositiveIntegerField(default=0)
    player_AB = models.PositiveIntegerField(default=0)
    player_BB = models.PositiveIntegerField(default=0)
    player_SO = models.PositiveIntegerField(default=0)
    player_Singles = models.PositiveIntegerField(default=0)
    player_Doubles = models.PositiveIntegerField(default=0)
    player_Triples = models.PositiveIntegerField(default=0)
    player_HR = models.PositiveIntegerField(default=0)
    player_Runs = models.PositiveIntegerField(default=0)
    player_RBI = models.PositiveIntegerField(default=0)
    player_SB = models.PositiveIntegerField(default=0)
    player_SAC = models.PositiveIntegerField(default=0)
    def _str_(self):
            return (self.player_name + " " + self.player_age + " " + self.player_year)

class pitcher (models.Model):
        id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
        pitches_for = models.ForeignKey(team, on_delete=models.CASCADE)
        pitcher_name = models.CharField(max_length=50)
        pitcher_age = models.PositiveIntegerField()
        pitcher_year = models.CharField(max_length=2, choices=YEAR_IN_SCHOOL_CHOICES)
        pitcher_position = models.CharField(max_length=10, choices=Pitcher_Choices, default=NoPitcher)
        pitcher_height = models.CharField(max_length=4)
        pitcher_weight = models.CharField(max_length=3)
        pitcher_SO = models.PositiveIntegerField(default=0)
        pitcher_hits = models.PositiveIntegerField(default=0)
        pitcher_walks = models.PositiveIntegerField(default=0)
        pitcher_HR = models.PositiveIntegerField(default=0)
        pitcher_IP = models.FloatField(default=0)
        pitcher_runs = models.PositiveIntegerField(default=0)
        pitcher_ER = models.PositiveIntegerField(default=0)
        pitcher_games = models.PositiveIntegerField(default=0)
        pitcher_GS = models.PositiveIntegerField(default=0)
        pitcher_AB = models.PositiveIntegerField(default=0)

        def _str_(self):
            return (self.player_name + " " + self.player_age + " " + self.player_year)

class coach (models.Model):
    coach = models.ForeignKey(team, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    coach_name = models.CharField(max_length = 50)
    coach_year = models.PositiveIntegerField()

    def _str_(self):
        return (self.coach_name + " " + self.coach_year)
