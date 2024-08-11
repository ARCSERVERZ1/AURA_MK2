# Generated by Django 5.0.4 on 2024-07-28 08:49

import DOCMA.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DOCMA', '0002_docma'),
    ]

    operations = [
        migrations.CreateModel(
            name='home_menu',
            fields=[
                ('app_id', models.AutoField(primary_key=True, serialize=False)),
                ('app_name', models.CharField(max_length=255)),
                ('app_link', models.CharField(max_length=255)),
                ('app_priority', models.IntegerField()),
                ('app_icon', models.FileField(upload_to=DOCMA.models.upload_setup)),
            ],
        ),
    ]