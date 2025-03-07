from django.urls import path
from . import views

urlpatterns = [
    path('signup', views.signup),
    path('login', views.login),
    path('logout', views.logout),
    path('get-practice-list', views.get_practice_list),
    path('get-chatbot-conversations', views.get_chatbot_conversations),
    path('update-chatbot-conversations', views.update_chatbot_conversations),
    path('delete-chatbot-conversations', views.delete_chatbot_conversations),
    path('save-chatbot-conversations', views.save_chatbot_conversations),
    path('test-token', views.test_token),
    path('create-payment-intent', views.create_payment_intent, name='create_payment_intent'),
    path('questionnaire', views.questionnaire, name='questionnaire')
]