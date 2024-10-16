from django.shortcuts import render, get_object_or_404, redirect, HttpResponse, Http404
from django.db.models import Count
from statalize_app.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from .models import team, player, coach

# Create your views here.

def display_home(request):
    data = team.objects.all()
    context = {"Teams": data}
    return render(request, '/home.html', context)