from django.contrib import admin
from .models import *

admin.site.register(team),
admin.site.register(player)
admin.site.register(pitcher)
admin.site.register(Game)
admin.site.register(GamePlayerStats)
admin.site.register(GamePitcherStats)
