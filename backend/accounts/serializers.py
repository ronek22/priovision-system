from rest_framework import serializers
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = UserModel
        fields = ['id', 'username', 'password', 'email', 
                    'first_name', 'last_name', 'is_active']
        write_only_fields = ['password']
        read_only_fields = ['id', 'is_active']


    def create(self, validated_data):

        user = UserModel.objects.create(
            username=validated_data['username'],
        )

        if validated_data.get('email', None):
            user.email = validated_data['email']
        if validated_data.get('first_name', None):
            user.first_name = validated_data['first_name']
        if validated_data.get('last_name', None):
            user.last_name = validated_data['last_name']

        user.set_password(validated_data['password'])
        user.is_active = True
        user.save()

        return user
    
