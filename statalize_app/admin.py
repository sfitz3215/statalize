from django.contrib import admin
from.models import team
from .models import player
from .models import pitcher
from .models import Game

admin.site.register(team),
admin.site.register(player)
admin.site.register(pitcher)
admin.site.register(Game)

