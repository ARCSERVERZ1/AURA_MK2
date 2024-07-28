class home_menu(models.Model):
    app_id = models.AutoField(primary_key=True)
    app_name = models.CharField(max_length=255, null=False)
    app_link = models.CharField(max_length=255, null=False)
    app_priority = models.IntegerField(null=False)
    app_icon = models.FileField(upload_to=upload_setup)

    def __str__(self):
        return f"{self.app_id}-{self.app_name} - {self.app_link} - {self.app_priority}"

