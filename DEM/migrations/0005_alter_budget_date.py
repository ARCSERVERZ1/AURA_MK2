# Generated by Django 4.2.7 on 2024-05-04 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DEM', '0004_budget'),
    ]

    operations = [
        migrations.AlterField(
            model_name='budget',
            name='date',
            field=models.CharField(default='NA', max_length=200),
        ),
    ]
