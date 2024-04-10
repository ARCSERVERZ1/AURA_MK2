from django.db import models
import os


# Create your models here.

def upload_setup(instances, filename):
    print(filename)
    ext = os.path.splitext(filename)[1]
    type = instances.type
    holder = instances.holder
    number = instances.number
    path = 'static/Docma/' + type + '/' + holder + '_' + number + '_front' + ext
    return path


class docma(models.Model):
    id = models.IntegerField(primary_key=True)
    holder = models.CharField(max_length=200)
    refnumber = models.CharField(max_length=200)
    document = models.FileField(upload_to=upload_setup)
    type = models.CharField(max_length=200)
    cat1 = models.CharField(max_length=200, default='NA')
    fnumber = models.CharField(max_length=200, default='NA')
    value = models.IntegerField(default=0)
    date = models.DateField()
    end_date = models.DateField()
    time_stamp = models.DateTimeField()
    remarks = models.CharField(max_length=200)
    updated_by = models.CharField(max_length=200)

    def __str__(self):
        return self.type


class doc_type(models.Model):
    type = models.CharField(max_length=200)
    subtype = models.CharField(max_length=200, default='NA')
    cat2 = models.CharField(max_length=200, default='NA')

    def __str__(self):
        return self.type


class doc_holder(models.Model):
    Holder = models.CharField(max_length=200, default='NA')
    full_name = models.CharField(max_length=200, default='NA')

    def __str__(self):
        return self.Holder
