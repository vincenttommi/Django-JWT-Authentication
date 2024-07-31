from django.shortcuts import render
from rest_framework.decorators import api_view
from .serializers import UserSerializer
from  rest_framework.response import Response
from  .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from  rest_framework import status
from  django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from  rest_framework_simplejwt.exceptions import TokenError


import logging

logger  = logging.getLogger(__name__)

@api_view(['POST'])
def login(request):
    try:
        data = request.data
        logger.debug(f"Login request data: {data}")
        
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            logger.debug("Username or password not provided")
            return Response({'detail': 'Username and password are required'}, status=400)
        
        user = authenticate(username=username, password=password)

        if user is not None:
            serializer = UserSerializer(user)
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            response_data = {
                'user': serializer.data,
                'access_token': access_token,
                'refresh_token': str(refresh),
            }
            logger.debug(f"Login successful for user: {username}")
            return Response(response_data)
        else:
            logger.debug("Invalid credentials")
            return Response({'detail': 'Invalid credentials'}, status=400)
    except Exception as e:
        logger.error(f"Login view error: {str(e)}", exc_info=True)
        return Response({'detail': 'Internal server error'}, status=500)


@api_view(['POST'])
def Register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)




@api_view(['POST'])
def logout(request):
    try:
        refresh_token = request.data.get('refresh_token')
        if refresh_token:
            token  = RefreshToken(refresh_token)
            token.blacklist()
        return Response("Logout Successful", status=status.HTTP_200_OK)  

    except TokenError:
        raise AuthenticationFailed('Invalid Token')  
   


    


    