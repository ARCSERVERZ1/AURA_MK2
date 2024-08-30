from django.db import models


# Create your models here.

class medtrac_log(models.Model):
    id = models.IntegerField(primary_key=True)
    participant = models.CharField(max_length=200)
    recorder = models.CharField(max_length=200)
    test_parameter = models.CharField(max_length=200)
    v1 = models.CharField(max_length=200)
    v2 = models.CharField(max_length=200)
    v3 = models.CharField(max_length=200)
    date = models.DateField()
    time_stamp = models.DateTimeField()
    remarks = models.CharField(max_length=200)
    updated_by = models.CharField(max_length=200)

    def __str__(self):
        return str(self.id) + '-' + str(self.test_parameter) + '-' + str(self.date)


class food_log(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.CharField(max_length=200)
    food_type = models.CharField(max_length=200)
    food_qty = models.CharField(max_length=200)
    satisfaction_level = models.CharField(max_length=200)
    junk_rating = models.CharField(max_length=200)
    date = models.DateField()
    time_stamp = models.DateTimeField()
    food_description = models.CharField(max_length=200)
    updated_by = models.CharField(max_length=200)

    def __str__(self):
        return str(self.id) + '-' + str(self.food_type) + '-' + str(self.date)
