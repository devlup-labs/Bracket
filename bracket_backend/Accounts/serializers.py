from rest_framework import serializers
from .models import User, SEX_CHOICES
from rest_framework.validators import UniqueValidator
from django.contrib.auth import password_validation

class UserListSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])
    username = serializers.CharField(validators=[UniqueValidator(queryset=User.objects.all())])
    class Meta:
        model = User
        fields = ('first_name','last_name','email','password','username','sex','age','bio')
        extra_kwargs={
            'password':{'write_only':True}
        }
    
    #Intermediate function between serializer and views.Helps in hashing of password 
    def create(self,validated_data):
        password=validated_data.pop('password','None')
        instance=self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    
    def validate_password(self, value):
        password_validation.validate_password(value)
        return value
    

