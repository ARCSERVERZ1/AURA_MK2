from django.db import models
# Create your models here.


class stock_list(models.Model):
    stock_ticker = models.CharField(max_length=255, null=False , primary_key=True)
    stock_name = models.CharField(max_length=255, null=False)
    state = models.BooleanField()
    stock_parameters = models.CharField(max_length=255, null=False)

    def __str__(self):
        return f"{self.stock_name} | {self.state}"

