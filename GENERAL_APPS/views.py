from django.shortcuts import render
from django.http import JsonResponse
from requests import request
from .models import *
from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
import json
from rest_framework.decorators import api_view, permission_classes

# Create your views here.


def form_save_loc(requests):
    loc_data = locations_data.objects.all()

    context = {
        "locations": loc_data
    }

    return render(requests, 'location_dashboard.html', context)


def save_loc(requests):
    if requests.method == 'POST':

        print("{}{}{", requests.POST)

        if requests.POST['Transaction'] == 'New':
            new_loc_data = locations_data(
                location_name=requests.POST['locationName'],
                latitude=str(requests.POST['co_ordinates']).split('|')[0],
                longitude=str(requests.POST['co_ordinates']).split('|')[1],
                remarks=requests.POST['remarks'],
                group=requests.POST['group'],
                temp_location=requests.POST.get('tempLocation'),
                Active=requests.POST.get('active'),
                user_permission=requests.POST['userPermission'],
                time_stamp=datetime.now(),
                user=requests.user.username
            )
            new_loc_data.save()

        elif requests.POST['Transaction'] == 'Update':
            record_instance = locations_data.objects.filter(id=requests.POST['id'])
            record_instance.update(
                location_name=requests.POST['locationName'],
                remarks=requests.POST['remarks'],
                group=requests.POST['group'],
                temp_location=requests.POST.get('tempLocation'),
                Active=requests.POST.get('active'),
                user_permission=requests.POST['userPermission'],
                time_stamp=datetime.now(),
                user=requests.user.username
            )

        return redirect('location_home')


def get_data_by_id(requests):
    print(requests.body)
    request_data = json.loads(requests.body)
    data = locations_data.objects.filter(id=request_data['id'])
    print(list(data.values())[0])
    return JsonResponse(list(data.values())[0], safe=False)


def delete_by_id(requests):
    request_data = json.loads(requests.body)
    data = locations_data.objects.filter(id=request_data['id']).delete()
    return JsonResponse({"status":"true"}, safe=False)

    # return JsonResponse({"Res": requests.POST.get('TempLocation')} , safe=False)


def test_run(requests):
    return render( requests ,'Test_Voice.html')


@api_view(['POST'])
def home_query(request):
    print(request.data)
    val = { 'response':request.data}
    print('final')
    return JsonResponse(val, safe=False)