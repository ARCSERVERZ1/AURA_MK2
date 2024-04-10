
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from DEM import views as dem_views
import os


def login(request):

    superusers = User.objects.filter(is_superuser=True)
    for user in superusers:
        print(user.username)

    if request.method == 'POST':
        name = request.POST['UserName']
        password = request.POST['password']
        user = auth.authenticate(username=name, password=password)

        if user is not None:
            auth.login(request, user)
            print("Logged in as ", user)
            # dem_views.speilspalz(request)
            # return render(request, 'dem_dashboard.html')
            return redirect('/home')
        else:

            print("login failed")
            messages.info(request, "Check User name or password")
            return render(request, "Login.html")
    else:
        pass

    return render(request, 'Login.html')

def home_page(request):
    return render(request, "home.html")
