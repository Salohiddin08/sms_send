from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from users.serializers import UserSerializer
from rest_framework import status
from django.contrib.auth import authenticate
from .models import User, UserConfirmation
from rest_framework.permissions import AllowAny
from rest_framework import permissions



class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = RefreshToken.for_user(user)
            return Response({
                'message': 'User created successfully!',
                'access_token': str(token.access_token),
                'refresh_token': str(token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny] 

    def post(self, request):
    
        username = request.data.get('username', None)
        email = request.data.get('email', None)
        phone = request.data.get('phone', None)
        password = request.data.get('password', None)
        if not (username or email or phone):
            return Response({'error': 'Username, email, or phone is required.'}, status=status.HTTP_400_BAD_REQUEST)
        user = None
        if username:
            user = authenticate(username=username, password=password)
        elif email:
            try:
                user = authenticate(username=User.objects.get(email=email).username, password=password)
            except User.DoesNotExist:
                return Response({'error': 'No user found with this email.'}, status=status.HTTP_400_BAD_REQUEST)
        elif phone:
            try:
                user = authenticate(username=User.objects.get(phone=phone).username, password=password)
            except User.DoesNotExist:
                return Response({'error': 'No user found with this phone number.'}, status=status.HTTP_400_BAD_REQUEST)


class TokenRefreshView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.data.get('refresh_token', None)
        if refresh_token is None:
            return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            new_access_token = str(token.access_token)
            return Response({'access_token': new_access_token})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserConfirmationCodeView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        user = request.user
        code = request.data.get('code')
        user_confirm = UserConfirmation.objects.filter(user=user, code=code, is_confirmed=False).first()
        if user_confirm:
            user_confirm.is_confirmed = True
            user_confirm.save()
            return Response({'message': 'User confirmed successfully!'}, status=status.HTTP_200_OK)
        return Response(data={'message': 'User unconfirmed successfully!'}, status=status.HTTP_400_BAD_REQUEST)