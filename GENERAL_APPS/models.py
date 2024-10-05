from django.db import models
from django.utils import timezone
# Create your models here.


class locations_data(models.Model):
    id = models.AutoField(primary_key=True)
    location_name = models.CharField(max_length=255, null=False)
    latitude = models.CharField(max_length=255, null=False)
    longitude = models.CharField(max_length=255, null=False)
    remarks = models.CharField(max_length=255, null = True)
    group = models.CharField(max_length=255, null = True)
    temp_location = models.CharField(max_length=255, default='False')
    Active = models.CharField(max_length=255, default='True')
    user_permission = models.CharField(max_length=255, default='all')
    time_stamp = models.DateTimeField(default=timezone.now)
    user = models.CharField(max_length=255, default='')

    def __str__(self):
        return f"{self.location_name} | {self.temp_location}"


'''
Fresh red: #A41F13

White fog: #FAF5F1

Light gray: #E0DBD8

Carbon gray: #292F36

Soft Brown: #8F7A6E

'''