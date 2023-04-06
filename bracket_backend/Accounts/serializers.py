from rest_framework import serializers
from .models import User, SEX_CHOICES


class UserListSerializer(serializers.ModelSerializer):
    sex = serializers.ChoiceField(choices=SEX_CHOICES, default='male')
    

    class Meta:
        model = User
        fields = "__all__"

    

    