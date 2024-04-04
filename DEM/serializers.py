# serializers.py
from rest_framework import serializers
from .models import *


class transactions_data_Serializer(serializers.ModelSerializer):
    class Meta:
        model = transactions_data
        fields = '__all__'  # You can also specify specific fields instead of '__all__'
