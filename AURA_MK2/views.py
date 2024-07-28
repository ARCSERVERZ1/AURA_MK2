
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from DEM import views as dem_views
from DOCMA import views as docma_views
import os

def diagnostics():
    print(os.getcwd())
    folder_path = os.path.dirname(os.getcwd())
    folder_name = os.path.basename(folder_path)
    folder_size = sum(os.path.getsize(os.path.join(folder_path, file)) for file in os.listdir(folder_path) if
                      os.path.isfile(os.path.join(folder_path, file)))
    creation_time = os.path.getctime(folder_path)
    modification_time = os.path.getmtime(folder_path)

    # Print folder properties
    print("Folder Name:", folder_name)
    print("Folder Size (in bytes):", folder_size/ (1024 ** 2))
    print("Creation Time:", creation_time)
    print("Modification Time:", modification_time)


def login(request):

    superusers = User.objects.filter(is_superuser=True)
    for user in superusers:
        if user == 'Admin':
            pass
            # return redirect('/home')
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

    diagnostics()
    menu_bar = docma_views.home_menu_req()
    context = {
        'menu_bar' : menu_bar

    }
    # for i in menu_bar:
    #     print(i.app_name)
    return render(request, "home.html" , context)




