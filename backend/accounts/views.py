from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView
from .serializers import UserSerializer
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from .utils import generate_access_token, generate_refresh_token
from django.conf import settings
import jwt


class CreateUserView(CreateAPIView):
    model = get_user_model()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

@api_view(['GET'])
def profile(request):
    user = request.user
    serialized_user = UserSerializer(user).data
    return Response({"user": serialized_user})


@api_view(['POST'])
@permission_classes([AllowAny])
@ensure_csrf_cookie
def login_view(request):
    # get data from form
    User = get_user_model()
    username = request.data.get('username')
    password = request.data.get('password')
    
    response = Response() # create response object
    print(f"Username: {username}")

    # validation form
    if (username is None) or (password is None):
        raise exceptions.AuthenticationFailed('username and password are required')

    # try to find user
    user = User.objects.filter(username=username).first()
    if (user is None):
        raise exceptions.AuthenticationFailed('user not found')
    if (not user.check_password(password)):
        raise exceptions.AuthenticationFailed('wrong password')

    # prepare json response with serializer
    serialized_user = UserSerializer(user).data
    
    access_token = generate_access_token(user)
    refresh_token = generate_refresh_token(user)

    # refresh token as http cookie, rest data as json
    response.set_cookie(key='refreshtoken', value=refresh_token, httponly=True)
    response.data = {
        'access_token': access_token,
        'user': serialized_user,
    }

    return response


@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_protect
def refresh_token_view(request):
    '''
    To obtain a new access_token this view expects 2 important things:
        1. a cookie that contains a valid refresh_token
        2. a header 'X-CSRFTOKEN' with a valid csrf token, client app can get it from cookies "csrftoken"
    '''

    User = get_user_model()
    refresh_token = request.COOKIES.get('refreshtoken')
    if refresh_token is None:
        raise exceptions.AuthenticationFailed('Authentication credentials were not provided')
    
    try:
        payload = jwt.decode(refresh_token, settings.REFRESH_TOKEN_SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise exceptions.AuthenticationFailed('expired refresh token, please login again.')

    user = User.objects.filter(id=payload.get('user_id')).first()
    if user is None:
        raise exceptions.AuthenticationFailed('User not found')

    if not user.is_active:
        raise exceptions.AuthenticationFailed('user is inactive')

    access_token = generate_access_token(user)
    return Response({'access_token': access_token})