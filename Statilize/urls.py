"""
URL configuration for Statilize project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from statalize_app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', display_home, name = 'home'),
    path('<uuid:id>/', display_team, name = 'teams'),
    path('players/', display_players, name = 'players'),
    path('logout/', logout_page, name='logout'),
    path('login/', login_page, name='login'),
]
