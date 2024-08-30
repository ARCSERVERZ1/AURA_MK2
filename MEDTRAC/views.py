from rest_framework.response import Response
from MEDTRAC.models import *
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Sum
import pytz
from datetime import datetime
from django.contrib.auth.decorators import login_required

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
        updated_by=requests.user.username
    )
    log_data.save()

    return render(requests, 'medtrac_dashboard.html')

@login_required()
def food_logger(request):
    if request.method == 'POST':
        food_qty = request.POST['food-qty']
        junk_rating = request.POST['junk-rating']
        satisfaction_level = request.POST['satisfaction-level']
        food_type = request.POST['food-type']
        time_stamp = request.POST['time']
        food_desc = ''
        user = request.user.username
        print(f'{food_qty}-{junk_rating}-{satisfaction_level}-{food_type}-{time_stamp}')

        if time_stamp == '':
            date = str(datetime.now().date())
            time_stamp = datetime.now()
        else:
            date = time_stamp.split('T')[0]

        def clean_data(data):
            return str(data).split(':')[1].strip()



        data = food_log(
            user = user,
            food_type = food_type,
            food_qty = clean_data(food_qty),
            junk_rating = clean_data(junk_rating),
            satisfaction_level = clean_data(satisfaction_level),
            food_description = food_desc,
            date = date,
            time_stamp = time_stamp,
            updated_by  = ''
        )

        data.save()
    return render(request, 'food_log_dashboard.html')
