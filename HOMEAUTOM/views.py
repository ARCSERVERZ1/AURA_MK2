from django.shortcuts import render
from HOMEAUTOM.models import *

# Create your views here.



def dashboard(request):


    all_groups = button_params.objects.values_list('button_groupname', flat=True).distinct()
    all_data= {}
    for group in all_groups:
        all_data[group] = button_params.objects.filter(button_groupname = group )

    # for group , groupdata in all_data.items() :
    #     print(group)
    #     for record in groupdata :
    #         print(record.button_name)
    #
    #
    # print(all_groups)
    context = {
        'all_data' : all_data
    }
    return render(request, "homeautom_main.html" , context)
