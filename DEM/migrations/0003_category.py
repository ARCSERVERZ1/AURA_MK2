# Generated by Django 4.2.7 on 2024-04-20 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DEM', '0002_groupdata'),
    ]

    operations = [
        migrations.CreateModel(
            name='category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(default='NA', max_length=200)),
                ('sub_category', models.CharField(default='NA', max_length=200)),
            ],
        ),
    ]
