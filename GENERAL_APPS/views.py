from django.shortcuts import render
from django.http import JsonResponse
from requests import request


# Create your views here.




def form_save_loc(requests):
    return  render(requests , 'location_dashboard.html')



def save_loc(requests):

    if requests.method == 'POST':
        requests.POST['locationName']
        requests.POST['TempLocation']
        requests.POST['userPermission']
        requests.POST['remarks']
        requests.POST['laititide']
        requests.POST['longitiude']


    return JsonResponse({"Res":"True"} , safe=False)