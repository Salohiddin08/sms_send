from rest_framework import serializers
from .models import User
from  .send_phone_code import send_phone_code
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        code = user.create_verify_code()
        send_phone_code(code=code
        return user