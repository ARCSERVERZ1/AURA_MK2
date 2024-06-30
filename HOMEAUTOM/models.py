from django.db import models

# Create your models here.

class button_params(models.Model):
    id = models.AutoField(primary_key=True)
    button_name = models.CharField(max_length=200)
    button_type = models.CharField(max_length=200)
    button_icon = models.CharField(max_length=200 , default='NA')
    button_url_on = models.CharField(max_length=400)
    button_url_off = models.CharField(max_length=400 , default='NA')
    button_groupname = models.CharField(max_length=200 )
    button_parameters = models.CharField(max_length=200 ,default='NA')
    button_remarks = models.CharField(max_length=200 , default='NA')
    def __str__(self):
        return str(self.id)+'-'+str(self.button_name)+'-'+str(self.button_type)