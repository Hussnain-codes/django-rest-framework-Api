from rest_framework.response import Response as res
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import AuthenticationFailed
from .UserAuth import authPermission  # Custom authentication permission
from .serializers import UserSerializer, PostSerializer
from base.models import User, Post
import jwt
import datetime

# user's register view


@api_view(['POST'])
def registerUser(req):
    serializer = UserSerializer(data=req.data)
    if serializer.is_valid():
        serializer.save()
    return res(serializer.data)

# user's login view


@api_view(['POST'])
def loginUser(req):
    email = req.data['email']
    password = req.data['password']

    user = User.objects.filter(email=email).first()

    if user is None:
        raise AuthenticationFailed("Please enter correct email")

    if not user.check_password(password):
        raise AuthenticationFailed("Password is incorrect")

    payload = {
        "id": user.id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1),
        "iat": datetime.datetime.utcnow()
    }

    jwt_token = jwt.encode(
        payload, 'secrets', algorithm="HS256").decode('utf-8')

    response = res()
    response.set_cookie(key="jwt", value=jwt_token, httponly=True)
    response.data = {
        "message": "User logged in successfully",
        "jwt": jwt_token
    }

    return response

# user's home if it is authenticated


@api_view(['GET'])
def userView(req):
    jwt_token = req.COOKIES.get('jwt')

    if not jwt_token:
        raise AuthenticationFailed('Unauthenticated')

    try:
        jwt_payload = jwt.decode(jwt_token, 'secrets', algorithms="HS256")
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated')

    user = User.objects.filter(id=jwt_payload['id']).first()
    serializer = UserSerializer(user)

    return res(serializer.data)

# user logout here


@api_view(['POST'])
def logoutUser(req):
    response = res()
    response.delete_cookie('jwt')
    response.data = {
        'message': 'User Logged out'
    }
    return response

# if user is Authenticated


@api_view(['POST'])
@permission_classes([authPermission])
def createPost(req):
    serializer = PostSerializer(data=req.data)
    if serializer.is_valid():
        serializer.save()
    return res(serializer.data)


@api_view(['GET'])
@permission_classes([authPermission])
def getPosts(req):
    allPosts = Post.objects.all()
    serializer = PostSerializer(allPosts, many=True)
    return res(serializer.data)
