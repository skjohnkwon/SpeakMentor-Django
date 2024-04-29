from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import render
from rest_framework import status
from django.contrib.auth import logout as auth_logout

from rest_framework.decorators import api_view, authentication_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework import status
import stripe
import os
from .models import ChatHistory

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .serializers import ChatHistorySerializer
from rest_framework.authtoken.models import Token
from .models import Questionnaire
from .utility import generate_list

from dotenv import load_dotenv
load_dotenv()

from .serializers import UserSerializer

@api_view(['POST'])
def signup(request):
    print(request.data)
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        #return response in json format
        return Response({'token': token.key, 'user': serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    try:
        print(request.data)
        user = get_object_or_404(User, email=request.data['email'])
        if not user.check_password(request.data['password']):
            return Response("Invalid credentials", status=status.HTTP_404_NOT_FOUND)
        
        token, created = Token.objects.get_or_create(user=user)
        user_serializer = UserSerializer(user)

        return Response({
            'token': token.key, 
            'user': user_serializer.data
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def logout(request):
    try:
        # Properly logout the user using Django's logout function
        auth_logout(request)
        return Response("Logged out successfully", status=status.HTTP_200_OK)
    except Exception as e:
        # Return the error message and a 400 status code
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
def get_practice_list(request):
    print(request.user)
    if not request.user.is_authenticated:
        return Response("User not authenticated", status=status.HTTP_401_UNAUTHORIZED)

    try:
        practice_list = generate_list()
        
        return Response(practice_list, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
def save_chatbot_conversations(request):
    if not request.user.is_authenticated:
        print("User not authenticated")
        return Response("User not authenticated", status=status.HTTP_401_UNAUTHORIZED)
    try:
        title = request.data.get('title')
        conversation = request.data.get('messages')
        ChatHistory.objects.create(user=request.user, title=title, chat=conversation)
        return Response("Chatbot conversation saved", status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
def get_chatbot_conversations(request):
    print(request.user)
    if not request.user.is_authenticated:
        print("User not authenticated")
        return Response("User not authenticated", status=status.HTTP_401_UNAUTHORIZED)
    try:
        user = request.user
        chat_history = ChatHistory.objects.filter(user=user)
        print(chat_history)
        serializer = ChatHistorySerializer(chat_history, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
def test_token(request):
    if not request.user.is_authenticated:
        return Response("User not authenticated", status=status.HTTP_401_UNAUTHORIZED)
    return Response("User authenticated", status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
def subscriptionStatus(request):
    #Do logic here for accoutn subscription using the stripe account
    return Response("no SubscriptinStatus yet")

@api_view(['GET'])
def create_payment_intent(request):
    
    print("STRIPE_SECRET_KEY", os.getenv('STRIPE_SECRET_KEY'))
    print(request)

    try:
        stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

        payment_intent = stripe.PaymentIntent.create(
            amount=1999,
            currency='eur',
            automatic_payment_methods={'enabled': True},
        )
        return Response(data={'clientSecret': payment_intent.client_secret}, status=status.HTTP_200_OK)
    except stripe.error.StripeError as e:
        return Response(data={'error': {'message': str(e)}}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
def questionnaire(request):
    print(request.user, request.data)
    data = request.data.get('answers')
    user = request.user
    native_language = data.get('native_language')
    birth_year = data.get('birth_year')
    years_speaking_english = data.get('years_speaking_english')
    print(native_language, birth_year, years_speaking_english)
    try:
        Questionnaire.objects.create(user=user, native_language=native_language, birth_year=birth_year, years_speaking_english=years_speaking_english)
        return Response("Questionnaire saved", status=status.HTTP_200_OK)
    except Exception as e:
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)