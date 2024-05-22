# serializers.py
from rest_framework import serializers
from .models import Nurse, Record
from django.contrib.auth.hashers import make_password

class NurseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nurse
        fields = ['id', 'email', 'name', 'age', 'password']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super(NurseSerializer, self).create(validated_data)

class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = ['id', 'nurse','patient', 'context', 'date']