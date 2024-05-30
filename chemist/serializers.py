from rest_framework import serializers
from .models import Chemist
from django.contrib.auth.hashers import make_password

class ChemistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chemist
        fields = ['id', 'email', 'name', 'age', 'password']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super(ChemistSerializer, self).create(validated_data)
