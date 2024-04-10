# Generated by Django 5.0.4 on 2024-04-08 06:42

import DOCMA.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DOCMA', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='docma',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('holder', models.CharField(max_length=200)),
                ('refnumber', models.CharField(max_length=200)),
                ('document', models.FileField(upload_to=DOCMA.models.upload_setup)),
                ('type', models.CharField(max_length=200)),
                ('cat1', models.CharField(default='NA', max_length=200)),
                ('fnumber', models.CharField(default='NA', max_length=200)),
                ('value', models.IntegerField(default=0)),
                ('date', models.DateField()),
                ('end_date', models.DateField()),
                ('time_stamp', models.DateTimeField()),
                ('remarks', models.CharField(max_length=200)),
                ('updated_by', models.CharField(max_length=200)),
            ],
        ),
    ]
