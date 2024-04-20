from django.db import models


# Create your models here.


class transactions_data(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.CharField(max_length=255, null=False)
    date = models.DateField()
    transaction_type = models.CharField(max_length=255, null=False)
    amount = models.IntegerField(null=False)
    sender_bank = models.CharField(max_length=255, null=False)
    receiver_bank = models.CharField(max_length=255, null=False)
    message = models.CharField(max_length=255, null=False)
    category = models.CharField(max_length=255, null=False)
    sub_category = models.CharField(max_length=255, null=False)
    group = models.CharField(max_length=255, null=False)
    payment_method = models.CharField(max_length=255, null=False)
    data_ts = models.DateTimeField()
    xtra = models.CharField(max_length=255, default='NA')

    def __str__(self):
        return f"{self.date}-{self.user} - {self.amount} - {self.category}"


class groupdata(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.CharField(max_length=255)
    Time_stamp = models.DateTimeField()
    grp_start = models.DateField()
    grp_end = models.DateField()
    grp_name = models.CharField(max_length=255)
    remarks = models.CharField(max_length=255)
    entry_type = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user}-{self.grp_name} - {self.grp_end} - {self.remarks}"


class category(models.Model):
    category = models.CharField(max_length=200, default='NA')
    sub_category = models.CharField(max_length=200, default='NA')

    def __str__(self):
        return self.category
