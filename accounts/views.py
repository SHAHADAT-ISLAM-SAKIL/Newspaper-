from django.shortcuts import render
from rest_framework import viewsets
from . import models
from . import serializers
from rest_framework.views import APIView
from rest_framework.response import Response

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes

#for acitvate: 
from django.contrib.auth.models import User

from django.shortcuts import redirect

# for sending email:
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.conf import settings  # Add this if you are using settings in your email link

from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login,logout
from accounts.models import CustomUser

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = serializers.CustomUserSerializer


class UserRegistrationApiView(APIView):
    serializer_class = serializers.RegistrationSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            user.is_active = False  # Deactivate account until it is confirmed
            user.save()
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            confirm_link = f"http://127.0.0.1:8000/accounts/active/{uid}/{token}"  # Replace with your actual frontend URL
            email_subject = "Confirm Your Email"
            email_body = render_to_string('confirm_email.html', {'confirm_link': confirm_link})
            email = EmailMultiAlternatives(email_subject, '', to=[user.email])
            email.attach_alternative(email_body, 'text/html')
            email.send()

            # Generate and save token for the user
            token, created = Token.objects.get_or_create(user=user)

            return Response({"detail": "Check your email for confirmation."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def activate(request, uid64, token):
    
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = CustomUser._default_manager.get(pk=uid)
      
    except(User.DoesNotExist):
        user = None 
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login')
    else:
        return redirect('register')

class UserLoginApiView(APIView):
    def post(self, request):
        serializer = serializers.UserLoginSerializer(data = self.request.data)
        
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            
            user = authenticate(username = username, password = password)
            print('\nour  :', {user},'\n')
            if user:
                token, created = Token.objects.get_or_create(user = user)
                login(request, user)
                return Response({'token': token.key, 'user_id' : user.id})
            else:
                return Response({'error' : "Invalid Credential"})
        return Response(serializer.errors)
        
class UserLogoutView(APIView):
    def get(self, request):
        try:
            token = request.user.auth_token
            token.delete()
            logout(request)
            return Response({'success': "Logout successful"})
        except AttributeError:
            return Response({'error': "No token found for this user"}, status=400)