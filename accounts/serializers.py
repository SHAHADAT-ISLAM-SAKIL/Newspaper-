from rest_framework import serializers
from  .models import CustomUser
from django.contrib.auth.models import User


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','username','first_name', 'last_name', 'email', 'is_superuser','role']



class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required=True)
    
    class Meta:
        model = CustomUser  # Change here to use CustomUser model
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password']
        
    def save(self):
        username = self.validated_data['username']
        first_name = self.validated_data['first_name']
        last_name = self.validated_data['last_name']
        email = self.validated_data['email']
        password = self.validated_data['password']
        password2 = self.validated_data['confirm_password']
    
        if password != password2:
            raise serializers.ValidationError({'error': "Password doesn't match"})
        if CustomUser.objects.filter(email=email).exists():  # Use CustomUser here as well
            raise serializers.ValidationError({'error': "Email already exists"})
        
        account = CustomUser(username=username, email=email, first_name=first_name, last_name=last_name)
        account.set_password(password)
        account.is_active = False
        account.save()
        
        return account


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required = True)
    password = serializers.CharField(required = True)       
    
