from django.shortcuts import render
from django.http import JsonResponse
from requests import request
from .models import *
from datetime import datetime
# Create your views here.




def form_save_loc(requests):

    loc_data = locations_data.objects.all()

    for i in loc_data:
        print(i)

    context = {
        "locations" : loc_data
    }

    return  render(requests , 'location_dashboard.html',context)



def save_loc(requests):

    if requests.method == 'POST':

        new_loc_data = locations_data(
        location_name =  requests.POST['locationName'],
        latitude = str(requests.POST['co_ordinates']).split('|')[0] ,
        longitude = str(requests.POST['co_ordinates']).split('|')[0] ,
        remarks = requests.POST['remarks'],
        group = requests.POST['group'],
        temp_location = requests.POST.get('tempLocation'),
        Active = requests.POST.get('active'),
        user_permission = requests.POST['userPermission'],
        time_stamp=datetime.now(),
        user=requests.user.username
        )
        new_loc_data.save()

        loc_data = locations_data.objects.all()

        for i in loc_data:
            print(i)

        context = {
            "locations": loc_data
        }

        return render(requests, 'location_dashboard.html', context)







    #return JsonResponse({"Res": requests.POST.get('TempLocation')} , safe=False)