# Generated by Django 4.2.7 on 2024-08-25 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MEDTRAC', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='food_log',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('user', models.CharField(max_length=200)),
                ('food_type', models.CharField(max_length=200)),
                ('food_qty', models.CharField(max_length=200)),
                ('satisfaction_level', models.CharField(max_length=200)),
                ('junk_rating', models.CharField(max_length=200)),
                ('date', models.DateField()),
                ('time_stamp', models.DateTimeField()),
                ('food_description', models.CharField(max_length=200)),
                ('updated_by', models.CharField(max_length=200)),
            ],
        ),
    ]
