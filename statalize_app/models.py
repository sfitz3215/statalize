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
    coach = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    team_name = models.CharField(max_length=20)
    wins = models.PositiveIntegerField()
    losses = models.PositiveIntegerField()

    def __str__(self):
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

    def __str__(self):
        return self.player_name

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


        def __str__(self):
            return self.pitcher_name
    

class Game(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateTimeField()
    home_team = models.ForeignKey(team, related_name="home_games", on_delete=models.CASCADE)
    away_team = models.ForeignKey(team, related_name="away_games", on_delete=models.CASCADE)
    home_score = models.PositiveIntegerField(default=0)
    away_score = models.PositiveIntegerField(default=0)
    winner = models.ForeignKey(team, on_delete=models.CASCADE)

class GamePlayerStats(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(player, on_delete=models.CASCADE)
    hits = models.PositiveIntegerField(default=0)
    AB = models.PositiveIntegerField(default=0)
    BB = models.PositiveIntegerField(default=0)
    SO = models.PositiveIntegerField(default=0)
    Singles = models.PositiveIntegerField(default=0)
    Doubles = models.PositiveIntegerField(default=0)
    Triples = models.PositiveIntegerField(default=0)
    HR = models.PositiveIntegerField(default=0)
    Runs = models.PositiveIntegerField(default=0)
    RBI = models.PositiveIntegerField(default=0)
    SB = models.PositiveIntegerField(default=0)
    SAC = models.PositiveIntegerField(default=0)

class GamePitcherStats(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    pitcher = models.ForeignKey(pitcher, on_delete=models.CASCADE)
    SO = models.PositiveIntegerField(default=0)
    hits = models.PositiveIntegerField(default=0)
    walks = models.PositiveIntegerField(default=0)
    HR = models.PositiveIntegerField(default=0)
    IP = models.FloatField(default=0)
    runs = models.PositiveIntegerField(default=0)
    ER = models.PositiveIntegerField(default=0)
    games = models.PositiveIntegerField(default=0)
    GS = models.PositiveIntegerField(default=0)
    AB = models.PositiveIntegerField(default=0)