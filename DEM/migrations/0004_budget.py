# Generated by Django 4.2.7 on 2024-05-04 03:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DEM', '0003_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='budget',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=200)),
                ('date', models.DateField()),
                ('budget', models.IntegerField()),
                ('updated_time_stamp', models.DateTimeField()),
            ],
        ),
    ]
