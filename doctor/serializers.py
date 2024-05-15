from rest_framework import serializers
from .models import Doctor
from django.contrib.auth.hashers import make_password

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['id', 'email', 'name', 'age', 'password']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super(DoctorSerializer, self).create(validated_data)
