from rest_framework.response import Response
from MEDTRAC.models import *
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Sum


def medtrac_dashboard(requests):
    return render(requests, 'medtrac_dashboard.html')


def medtrac_log(requests):
    return
