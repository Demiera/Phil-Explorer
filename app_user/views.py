from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, LoginSerializer
from .models import AdminUser
from django.contrib.auth import authenticate
from rest_framework.response import Response


class RegisterAPIView(generics.CreateAPIView):
    queryset = AdminUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = self.serializer_class(response.data).data
        refresh = RefreshToken.for_user(AdminUser.objects.get(email=user['email']))
        data = {
            'email': user['email'],
            'first_name': user['first_name'],
            'last_name': user['last_name'],
            'access': str(refresh.access_token),
        }
        response.data = data
        return response


class LoginAPIView(generics.CreateAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            data = {
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'access': str(refresh.access_token),
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)
