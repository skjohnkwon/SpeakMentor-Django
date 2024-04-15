from django.urls import path
from . import views

urlpatterns = [
    path('get_data',views.get_data),
    path('signup', views.signup),
    path('login', views.login),
    path('logout', views.logout),
    path('test_token', views.test_token),
    path('create-payment-intent', views.create_payment_intent, name='create_payment_intent')
]