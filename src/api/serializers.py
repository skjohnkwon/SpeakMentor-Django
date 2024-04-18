# from rest_framework import serializers
# from products.models import Product

# class ProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = '__all__'

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import PracticeList
from .models import ChatHistory
from .models import Questionnaire

class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User 
        fields = ['id', 'username', 'password', 'email']

class PracticeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PracticeList
        fields = '__all__'

class ChatHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatHistory
        fields = '__all__'

class QuestionnaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questionnaire
        fields = '__all__'
