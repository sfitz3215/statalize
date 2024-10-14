from django.shortcuts import render, get_object_or_404, redirect, HttpResponse, Http404
from django.db.models import Count
from statalize_app.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout


# Create your views here.

def display_home(request):
    return render(request, '/home.html')
