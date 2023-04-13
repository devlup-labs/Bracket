from django.db import IntegrityError
from django.forms import ValidationError
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import UserListSerializer
from .models import User
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
import  io
from rest_framework.parsers import JSONParser
import jwt,datetime



# Requires Deserialization ------  JSON Data — Parse data →Python native data — De-serialization →Complex Data
@api_view(['POST'])
@permission_classes((AllowAny,))
def SignUp(request): # Create a new user
  
  try:
        data = {}
        json_data=request.body
        stream= io.BytesIO(json_data)
        pythondata= JSONParser().parse(stream) # It parses the incoming request JSON content into python content type dict. It is used if "Content-Type" is set to "application/json".
        serializer = UserListSerializer(data=pythondata) # Converts python data to complex data type :- De-serialization
        if serializer.is_valid():
            if(User.objects.filter(username=serializer.validated_data['username']).exists() ):
                data['status'] = 'failed'
                data['message'] = 'Username already exists'
                return Response(data, status=HTTP_400_BAD_REQUEST, headers={'Access-Control-Allow-Origin': '*'})
            elif(User.objects.filter(email=serializer.validated_data['email']).exists() ):
                data['status'] = 'failed'
                data['message'] = 'Email already exists'
                return Response(data, status=HTTP_400_BAD_REQUEST, headers={'Access-Control-Allow-Origin': '*'})
            elif(User.objects.filter(email=serializer.validated_data['email']).exists() and User.objects.filter(email=serializer.validated_data['email']).exists() ):
                data['status'] = 'failed'
                data['message'] = 'Both Username and Email already exists'
                return Response(data, status=HTTP_400_BAD_REQUEST, headers={'Access-Control-Allow-Origin': '*'})
            
            account = serializer.save()
            account.save()
            token = Token.objects.get_or_create(user=account)[0].key
            data["message"] = "User registered successfully"
            data["email"] = account.email
            data["username"] = account.username
            data["sex"]=account.sex
            data["age"]=account.age
            data["bio"]=account.bio
            data["token"] = token
            # Save the user and return the above info as response
            return Response(data, status=HTTP_200_OK, headers={'Access-Control-Allow-Origin': '*'})
        else:
            data = serializer.errors
            return Response(data, status=HTTP_400_BAD_REQUEST, headers={'Access-Control-Allow-Origin': '*'})
  except IntegrityError as e:
        account=User.objects.get(username='')
        account.delete()
        raise ValidationError({"400": f'{str(e)}'})
  

@api_view(["GET"])
@permission_classes((AllowAny,))
def Login(request):

  email = request.headers.get('Email')
  password = request.headers.get('Password')
  try:
    Account = User.objects.get(email=email) # get the account with the given email
  except BaseException as e:
      return Response({"message": "No Such Email Registered!!  "}, status=HTTP_400_BAD_REQUEST, headers={'Access-Control-Allow-Origin': '*'})

  if not Account.check_password(password): # We cannot directly compare passwords so we have to use django inbuilt method 
      return Response({"message": "Incorrect Login Credentials"}, status=HTTP_400_BAD_REQUEST, headers={'Access-Control-Allow-Origin': '*'})

  # If the credentials are correct, return the token
  if Account:
    
    payload={
        'email': Account.email,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        'iat': datetime.datetime.utcnow()   # Date on which token is created
    }

    token= jwt.encode(payload,'secret',algorithm='HS256')

    # Now we have to send token as cookies
    response=Response()
    response.set_cookie(key='jwt',value=token,httponly=True)  # Use of httponly=True is that we want frontend to use only cookies not token , token is only for backend
    
    response.data = {"jwt": token}

    # response.content_type='application/json'
    # response.status=HTTP_200_OK, headers={'Access-Control-Allow-Origin': '*'}

    return response

  else:
      return Response({"message": "Incorrect Login credentials"}, status=HTTP_400_BAD_REQUEST, headers={'Access-Control-Allow-Origin': '*'})



@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def UserApi(request):
    token=request.COOKIES.get("jwt")
                                                                                     
    if not token:
        return Response({"message": "Token Invalid"}, status=HTTP_400_BAD_REQUEST, headers={'Access-Control-Allow-Origin': '*'})

    try:
        payload=jwt.decode(token,'secret',algorithms=['HS256'])
    except:
        return Response({"message": "User Not Authenticated"}, status=HTTP_400_BAD_REQUEST, headers={'Access-Control-Allow-Origin': '*'})

    Account=User.objects.filter(email=[payload['email']]).first()
    serializer=UserListSerializer(Account)
    return Response(serializer.data)






@api_view(["POST"])
# @permission_classes([IsAuthenticated])
def LogOut(request):
    response=Response()
    response.delete_cookie("jwt")
    response.data={
        "message":"Logged Out"
    }
    return response



        


    