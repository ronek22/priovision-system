from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Client

UserModel = get_user_model()

class ClientSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Client
        exclude = ['created_by',]

    def create(self, validated_data):

        validated_data['created_by'] = self.context["request"].user
        return super().create(validated_data)    
