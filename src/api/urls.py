from django.urls import path
from . import views

urlpatterns = [
    path('signup', views.signup),
    path('login', views.login),
    path('logout', views.logout),
    path('get_suggested_list', views.get_practice_list),
    path('get_chatbot_history', views.get_chat_history),
    path('test_token', views.test_token),
    path('create-payment-intent', views.create_payment_intent, name='create_payment_intent')
]