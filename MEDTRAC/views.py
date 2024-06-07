from rest_framework.response import Response
from MEDTRAC.models import *
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Sum
import pytz
from datetime import datetime

def medtrac_dashboard(requests):
    return render(requests, 'medtrac_dashboard.html')


def log_medtrac(requests):
    print(f"medtrac data save request")
    ist_time_stamp = datetime.now(pytz.timezone('Asia/Kolkata'))
    print(ist_time_stamp)

    if requests.method == 'POST':
        print(requests.POST['date'])

    log_data = medtrac_log(
        participant=requests.POST['Participant'],
        recorder=requests.POST['recorder'],
        test_parameter=requests.POST['Parameter'],
        v1=requests.POST['Value1'],
        v2=requests.POST['Value2'],
        v3=requests.POST['Value3'],
        date=requests.POST['date'],
        time_stamp=ist_time_stamp,
        remarks=requests.POST['remarks'],
        updated_by= requests.user.username
    )
    log_data.save()

    return render(requests, 'medtrac_dashboard.html')
