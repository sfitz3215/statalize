from django.shortcuts import render, get_object_or_404, redirect, HttpResponse, Http404
from django.db.models import Count
from statalize_app.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from .models import team, player, coach
from .forms import TeamForm
# Create your views here.

def display_home(request):
    data = team.objects.all()
    context = {"Teams": data}
    return render(request, 'statalize/home.html', context)
def add_team(request):
    if request.method == 'POST':
        form= TeamForm(request.POST)
        if form.is_valid():
            form.save()
            return
    else:
        form = TeamForm()
    return render(request, 'statalize/add_team.html', {'form': form})

